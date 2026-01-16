# Auth SSR Patterns Reference

Complete authentication SSR implementation patterns for Next.js 14+ with Supabase, including OAuth providers, phone auth, and anonymous sign-ins.

> **Important:** As of Next.js 16+, use `proxy.ts` instead of `middleware.ts`. See https://nextjs.org/docs/app/api-reference/file-conventions/proxy

## Critical Rules

### ⛔ NEVER USE (DEPRECATED - BREAKS APPLICATION)

```typescript
// ❌ DEPRECATED - Individual cookie methods
cookies: {
  get(name: string) { ... },      // ❌ BREAKS
  set(name: string, value: string) { ... },  // ❌ BREAKS
  remove(name: string) { ... }     // ❌ BREAKS
}

// ❌ DEPRECATED - Auth helpers package
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'
```

### ✅ ALWAYS USE

```typescript
// ✅ CORRECT - SSR package
import { createBrowserClient, createServerClient } from '@supabase/ssr'

// ✅ CORRECT - Cookie methods
cookies: {
  getAll() { ... },    // ✅ ONLY THIS
  setAll() { ... }     // ✅ ONLY THIS
}
```

## Browser Client Pattern

**File:** `lib/supabase/client.ts`

**Use for:** Client components, browser-side operations

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
  )
}
```

> **Note:** Use publishable keys (`sb_publishable_...`) for client code. See https://supabase.com/docs/guides/api/api-keys

**Usage in Client Components:**

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'

export default function ClientComponent() {
  const [user, setUser] = useState(null)
  const supabase = createClient()

  useEffect(() => {
    // Get initial user
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
    }
    getUser()

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setUser(session?.user ?? null)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  if (!user) {
    return <div>Please log in</div>
  }

  return <div>Hello, {user.email}</div>
}
```

## Server Client Pattern

**File:** `lib/supabase/server.ts`

**Use for:** Server Components, Server Actions, API Routes

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Ignore if called from Server Component
            // This can happen during static rendering
          }
        },
      },
    }
  )
}
```

**Usage in Server Components:**

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  // Fetch data
  const { data: students } = await supabase
    .from('students')
    .select('*')
    .eq('institution_id', user.user_metadata.institution_id)

  return (
    <div>
      <h1>Welcome, {user.email}</h1>
      <StudentList students={students} />
    </div>
  )
}
```

## Proxy Pattern (Replaces Middleware)

**File:** `proxy.ts` (at root or `src/` directory)

**Use for:** Authentication checks, session refresh, route protection

> **Important:** As of Next.js 16+, `middleware.ts` has been renamed to `proxy.ts`. The term "Proxy" better describes its function as a network proxy running before routes.

```typescript
// proxy.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function proxy(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({
            request,
          })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // CRITICAL: Must call getUser() to refresh session
  const { data: { user } } = await supabase.auth.getUser()

  // Redirect to login if not authenticated
  if (!user && !request.nextUrl.pathname.startsWith('/login')) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  // Redirect to dashboard if already logged in
  if (user && request.nextUrl.pathname === '/login') {
    const url = request.nextUrl.clone()
    url.pathname = '/dashboard'
    return NextResponse.redirect(url)
  }

  return supabaseResponse  // MUST return supabaseResponse
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### Migration from middleware.ts

```bash
# Automatic migration
npx @next/codemod@canary middleware-to-proxy .
```

Or manually rename `middleware.ts` → `proxy.ts` and `middleware()` → `proxy()`.

## Server Action Pattern

**File:** `app/(routes)/some-feature/actions.ts`

**Use for:** Form submissions, mutations, server-side operations

```typescript
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createStudent(formData: FormData) {
  const supabase = await createClient()

  // Check auth
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  // Extract form data
  const firstName = formData.get('firstName') as string
  const lastName = formData.get('lastName') as string

  // Insert data
  const { data, error } = await supabase
    .from('students')
    .insert({
      first_name: firstName,
      last_name: lastName,
      institution_id: user.user_metadata.institution_id,
      created_by: user.id,
    })
    .select()
    .single()

  if (error) {
    throw new Error(`Failed to create student: ${error.message}`)
  }

  // Revalidate and redirect
  revalidatePath('/students')
  redirect('/students')
}

export async function updateStudent(id: string, formData: FormData) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    throw new Error('Unauthorized')
  }

  const { error } = await supabase
    .from('students')
    .update({
      first_name: formData.get('firstName') as string,
      last_name: formData.get('lastName') as string,
      updated_at: new Date().toISOString(),
    })
    .eq('id', id)

  if (error) {
    throw new Error(`Failed to update student: ${error.message}`)
  }

  revalidatePath('/students')
}

export async function deleteStudent(id: string) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    throw new Error('Unauthorized')
  }

  const { error } = await supabase
    .from('students')
    .delete()
    .eq('id', id)

  if (error) {
    throw new Error(`Failed to delete student: ${error.message}`)
  }

  revalidatePath('/students')
}
```

## API Route Pattern

**File:** `app/api/students/route.ts`

**Use for:** REST API endpoints

```typescript
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const supabase = await createClient()

  // Check auth
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  // Get query params
  const { searchParams } = new URL(request.url)
  const status = searchParams.get('status')

  // Query data
  let query = supabase
    .from('students')
    .select('*')
    .eq('institution_id', user.user_metadata.institution_id)

  if (status) {
    query = query.eq('status', status)
  }

  const { data, error } = await query

  if (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }

  return NextResponse.json({ data })
}

export async function POST(request: Request) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  const body = await request.json()

  const { data, error } = await supabase
    .from('students')
    .insert({
      ...body,
      institution_id: user.user_metadata.institution_id,
      created_by: user.id,
    })
    .select()
    .single()

  if (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }

  return NextResponse.json({ data }, { status: 201 })
}
```

## Login/Signup Patterns

**File:** `app/login/page.tsx`

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()
  const supabase = createClient()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) {
      console.error('Login error:', error.message)
      return
    }

    router.push('/dashboard')
    router.refresh()
  }

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    })

    if (error) {
      console.error('Signup error:', error.message)
      return
    }

    // Optionally redirect to email verification page
    router.push('/verify-email')
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/login')
    router.refresh()
  }

  return (
    <div>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Log In</button>
        <button type="button" onClick={handleSignup}>
          Sign Up
        </button>
      </form>
    </div>
  )
}
```

## OAuth Login Pattern

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export default function OAuthLogin() {
  const supabase = createClient()
  const router = useRouter()

  const handleGoogleLogin = async () => {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      console.error('OAuth error:', error.message)
    }
  }

  return (
    <button onClick={handleGoogleLogin}>
      Sign in with Google
    </button>
  )
}
```

**OAuth Callback Route:** `app/auth/callback/route.ts`

```typescript
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = await createClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  // Redirect to dashboard after OAuth login
  return NextResponse.redirect(`${requestUrl.origin}/dashboard`)
}
```

## Role-Based Access Pattern

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function AdminPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  // Check user role from JWT
  const role = user.user_metadata?.role || 'user'

  if (!['admin', 'super_admin'].includes(role)) {
    redirect('/unauthorized')
  }

  return <div>Admin Content</div>
}
```

## Session Management Patterns

### Check if User is Authenticated

```typescript
const supabase = await createClient()
const { data: { user } } = await supabase.auth.getUser()

if (user) {
  // User is authenticated
  console.log('Logged in as:', user.email)
} else {
  // User is not authenticated
  redirect('/login')
}
```

### Get User Metadata

```typescript
const { data: { user } } = await supabase.auth.getUser()

if (user) {
  const institutionId = user.user_metadata?.institution_id
  const role = user.user_metadata?.role
  const email = user.email
}
```

### Refresh Session

```typescript
// This happens automatically in middleware
// Manual refresh if needed:
const { data, error } = await supabase.auth.refreshSession()
```

## Common Patterns Checklist

- [ ] Using `@supabase/ssr` package (NOT auth-helpers)
- [ ] Using `proxy.ts` (NOT `middleware.ts`) for Next.js 16+
- [ ] Using ONLY `getAll()` and `setAll()` methods
- [ ] NEVER using `get()`, `set()`, or `remove()` methods
- [ ] Proxy calls `getUser()` to refresh session
- [ ] Proxy returns `supabaseResponse` object
- [ ] Server client has try-catch for `setAll`
- [ ] Client components use `createBrowserClient`
- [ ] Server components use `createServerClient`
- [ ] Auth state changes handled with `onAuthStateChange`

## Troubleshooting

### Session Not Persisting

**Problem:** User gets logged out on refresh

**Solution:**
```typescript
// Ensure proxy is returning supabaseResponse
return supabaseResponse  // NOT NextResponse.next()

// Ensure proxy calls getUser()
await supabase.auth.getUser()
```

### Cookies Not Setting

**Problem:** Auth cookies not being set

**Solution:**
```typescript
// Ensure using setAll, not set
cookies: {
  setAll(cookiesToSet) {  // ✅ CORRECT
    cookiesToSet.forEach(({ name, value, options }) =>
      cookieStore.set(name, value, options)
    )
  }
}
```

### Proxy Errors

**Problem:** Proxy throws errors

**Solution:**
```typescript
// Add try-catch in server client setAll
cookies: {
  setAll(cookiesToSet) {
    try {
      cookiesToSet.forEach(({ name, value, options }) =>
        cookieStore.set(name, value, options)
      )
    } catch {
      // Ignore if called from Server Component
    }
  }
}
```

## OAuth Providers

Supabase supports 20+ OAuth providers. Configure in Dashboard under Authentication > Providers.

### Supported Providers

| Provider | ID | Notes |
|----------|-----|-------|
| Google | `google` | Most common |
| GitHub | `github` | Developer apps |
| GitLab | `gitlab` | Self-hosted supported |
| Bitbucket | `bitbucket` | Atlassian |
| Apple | `apple` | Requires Apple Developer |
| Microsoft | `azure` | Azure AD |
| Facebook | `facebook` | Meta apps |
| Twitter | `twitter` | X/Twitter |
| Discord | `discord` | Gaming/community |
| Slack | `slack` | Workspace apps |
| Spotify | `spotify` | Music apps |
| Twitch | `twitch` | Streaming |
| LinkedIn | `linkedin_oidc` | Professional |
| Notion | `notion` | Productivity |
| Figma | `figma` | Design |
| Zoom | `zoom` | Video |
| Keycloak | `keycloak` | Self-hosted |
| WorkOS | `workos` | Enterprise SSO |

### OAuth Sign-In Pattern

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'

export function OAuthButtons() {
  const supabase = createClient()

  const handleOAuth = async (provider: 'google' | 'github' | 'discord') => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${window.location.origin}/auth/callback`
      }
    })

    if (error) console.error('OAuth error:', error)
  }

  return (
    <div>
      <button onClick={() => handleOAuth('google')}>
        Continue with Google
      </button>
      <button onClick={() => handleOAuth('github')}>
        Continue with GitHub
      </button>
      <button onClick={() => handleOAuth('discord')}>
        Continue with Discord
      </button>
    </div>
  )
}
```

### OAuth with Scopes

```typescript
const { error } = await supabase.auth.signInWithOAuth({
  provider: 'github',
  options: {
    redirectTo: `${origin}/auth/callback`,
    scopes: 'repo read:user'  // Request additional permissions
  }
})
```

### OAuth Callback Handler

```typescript
// app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')
  const next = requestUrl.searchParams.get('next') ?? '/dashboard'

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)

    if (!error) {
      return NextResponse.redirect(new URL(next, request.url))
    }
  }

  // OAuth error - redirect to error page
  return NextResponse.redirect(new URL('/auth/error', request.url))
}
```

## Phone Authentication

Supabase supports SMS authentication via third-party providers.

### Supported SMS Providers

| Provider | Setup |
|----------|-------|
| Twilio | Most popular, global coverage |
| MessageBird | European focus |
| Vonage | Enterprise grade |

### Phone Sign-In Flow

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useState } from 'react'

export function PhoneAuth() {
  const [phone, setPhone] = useState('')
  const [token, setToken] = useState('')
  const [step, setStep] = useState<'phone' | 'verify'>('phone')
  const supabase = createClient()

  // Step 1: Send OTP
  const sendOtp = async () => {
    const { error } = await supabase.auth.signInWithOtp({
      phone,
      options: {
        channel: 'sms'  // or 'whatsapp'
      }
    })

    if (!error) setStep('verify')
  }

  // Step 2: Verify OTP
  const verifyOtp = async () => {
    const { error } = await supabase.auth.verifyOtp({
      phone,
      token,
      type: 'sms'
    })

    if (!error) {
      window.location.href = '/dashboard'
    }
  }

  if (step === 'phone') {
    return (
      <div>
        <input
          type="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="+1234567890"
        />
        <button onClick={sendOtp}>Send Code</button>
      </div>
    )
  }

  return (
    <div>
      <input
        type="text"
        value={token}
        onChange={(e) => setToken(e.target.value)}
        placeholder="Enter 6-digit code"
        maxLength={6}
      />
      <button onClick={verifyOtp}>Verify</button>
    </div>
  )
}
```

## Anonymous Sign-Ins

Allow users to explore the app before creating an account.

### Enable in Dashboard

Authentication > Providers > Anonymous Sign-ins > Enable

### Anonymous Sign-In

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'

export function GuestMode() {
  const supabase = createClient()

  const signInAnonymously = async () => {
    const { data, error } = await supabase.auth.signInAnonymously()

    if (!error) {
      // User now has anonymous session
      console.log('Anonymous user:', data.user)
    }
  }

  return (
    <button onClick={signInAnonymously}>
      Continue as Guest
    </button>
  )
}
```

### Convert Anonymous to Permanent

```typescript
// Link email to anonymous account
const { error } = await supabase.auth.updateUser({
  email: 'user@example.com'
})

// Or link OAuth provider
const { error } = await supabase.auth.linkIdentity({
  provider: 'google'
})
```

### Check if User is Anonymous

```typescript
const { data: { user } } = await supabase.auth.getUser()

if (user?.is_anonymous) {
  // Show "Create Account" prompt
}
```

## Magic Link Authentication

Passwordless email authentication.

```typescript
// Send magic link
const { error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: `${origin}/auth/callback`
  }
})

// User clicks link in email, lands on callback
// Callback handler exchanges code for session
```

## Multi-Factor Authentication (MFA)

### Enroll TOTP

```typescript
// Start enrollment
const { data, error } = await supabase.auth.mfa.enroll({
  factorType: 'totp'
})

// Show QR code
const qrCode = data.totp.qr_code  // SVG string

// Verify enrollment
const { error: verifyError } = await supabase.auth.mfa.challengeAndVerify({
  factorId: data.id,
  code: userEnteredCode
})
```

### Verify MFA on Sign-In

```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email,
  password
})

// Check if MFA required
if (data.user && !data.session) {
  // User has MFA enabled, need to verify
  const { data: factors } = await supabase.auth.mfa.listFactors()

  const { data: challenge } = await supabase.auth.mfa.challenge({
    factorId: factors.totp[0].id
  })

  // Get TOTP code from user
  const { data: session, error } = await supabase.auth.mfa.verify({
    factorId: factors.totp[0].id,
    challengeId: challenge.id,
    code: userEnteredCode
  })
}
```

## Enterprise SSO (SAML)

For enterprise customers requiring SAML-based authentication.

### Sign In with SSO

```typescript
const { data, error } = await supabase.auth.signInWithSSO({
  domain: 'company.com'  // Enterprise domain
})

if (data?.url) {
  // Redirect to IdP
  window.location.href = data.url
}
```

## Password Reset Flow

```typescript
// Request password reset
const { error } = await supabase.auth.resetPasswordForEmail(email, {
  redirectTo: `${origin}/auth/reset-password`
})

// Handle reset (on reset-password page)
const { error } = await supabase.auth.updateUser({
  password: newPassword
})
```

## User Metadata

### Set User Metadata

```typescript
// During sign-up
const { error } = await supabase.auth.signUp({
  email,
  password,
  options: {
    data: {
      full_name: 'John Doe',
      avatar_url: 'https://...',
      role: 'user'
    }
  }
})

// Update existing user
const { error } = await supabase.auth.updateUser({
  data: {
    full_name: 'Jane Doe'
  }
})
```

### Access Metadata

```typescript
const { data: { user } } = await supabase.auth.getUser()

console.log(user.user_metadata.full_name)
console.log(user.app_metadata.role)  // Set by admin/server
```

## References

- https://supabase.com/docs/guides/auth
- https://supabase.com/docs/guides/auth/social-login
- https://supabase.com/docs/guides/auth/phone-login
- https://supabase.com/docs/guides/auth/auth-anonymous
- https://supabase.com/docs/guides/auth/auth-mfa
