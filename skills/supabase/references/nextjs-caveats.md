# Next.js Caveats Reference

Complete guide to Supabase integration with Next.js App Router, including SSR patterns, caveats, and best practices.

## Architecture Overview

Next.js App Router has distinct rendering environments:

| Environment | Package | Cookie Access | When to Use |
|-------------|---------|---------------|-------------|
| Server Components | `createServerClient` | `cookies()` | Data fetching |
| Client Components | `createBrowserClient` | Automatic | Interactivity |
| Route Handlers | `createServerClient` | `cookies()` | API endpoints |
| Server Actions | `createServerClient` | `cookies()` | Mutations |
| Proxy | `createServerClient` | `request.cookies` | Auth guards |

> **Important:** As of Next.js 16+, use `proxy.ts` instead of `middleware.ts`. See https://nextjs.org/docs/app/api-reference/file-conventions/proxy

## Critical Setup Requirements

### 1. Install Correct Package

```bash
npm install @supabase/ssr @supabase/supabase-js
```

**Do NOT use:**
```bash
# Deprecated - do not use
npm install @supabase/auth-helpers-nextjs
```

### 2. Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...

# Optional: For admin operations (server-side only)
SUPABASE_SECRET_KEY=sb_secret_...
```

> **Note:** Use the new publishable/secret keys (`sb_publishable_...`, `sb_secret_...`) instead of legacy `anon`/`service_role` keys. See https://supabase.com/docs/guides/api/api-keys

### 3. Create Client Utilities

**Browser Client:** `lib/supabase/client.ts`
```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
  )
}
```

**Server Client:** `lib/supabase/server.ts`
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
            // Ignore when called from Server Component
          }
        },
      },
    }
  )
}
```

## Server Components

### Fetching Data

```typescript
// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = await createClient()

  // Check auth
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  // Fetch data
  const { data: posts } = await supabase
    .from('posts')
    .select('*')
    .order('created_at', { ascending: false })

  return <PostList posts={posts} />
}
```

### Caveat: No Cookie Writes in Server Components

Server Components cannot set cookies. The `setAll` function will silently fail (caught by try-catch). This is expected behavior - cookies are only set during:
- Middleware execution
- Route Handler responses
- Server Action responses

## Client Components

### Using Supabase Client

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'

export function UserProfile() {
  const [user, setUser] = useState(null)
  const supabase = createClient()

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
    }
    getUser()
  }, [])

  return user ? <div>{user.email}</div> : <div>Loading...</div>
}
```

### Auth State Listener

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function AuthListener({ children }: { children: React.ReactNode }) {
  const supabase = createClient()
  const router = useRouter()

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        if (event === 'SIGNED_OUT') {
          router.push('/login')
        }
        // Refresh server components
        router.refresh()
      }
    )

    return () => subscription.unsubscribe()
  }, [router, supabase])

  return children
}
```

## Proxy (Replaces Middleware)

> **Important:** As of Next.js 16+, `middleware.ts` has been renamed to `proxy.ts`. The term "Proxy" better describes its function as a network proxy running before routes. See https://nextjs.org/docs/app/api-reference/file-conventions/proxy

### Critical: Session Refresh

The proxy MUST:
1. Call `getUser()` to refresh the session
2. Return `supabaseResponse` (not `NextResponse.next()`)

```typescript
// proxy.ts (at root or src/ directory)
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function proxy(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

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
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // CRITICAL: Refresh session
  const { data: { user } } = await supabase.auth.getUser()

  // Protect routes
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // CRITICAL: Return supabaseResponse
  return supabaseResponse
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)']
}
```

### Migration from middleware.ts

```bash
# Automatic migration
npx @next/codemod@canary middleware-to-proxy .
```

Or manually rename `middleware.ts` → `proxy.ts` and `middleware()` → `proxy()`.

### Common Proxy Mistakes

```typescript
// WRONG: Not calling getUser()
export async function proxy(request: NextRequest) {
  const supabase = createServerClient(...)
  // Missing: await supabase.auth.getUser()
  return NextResponse.next()
}

// WRONG: Returning NextResponse.next() instead of supabaseResponse
export async function proxy(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })
  const supabase = createServerClient(...)
  await supabase.auth.getUser()
  return NextResponse.next() // WRONG - cookies won't be set
}
```

## Server Actions

### Form Mutation

```typescript
// app/posts/actions.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const title = formData.get('title') as string
  const content = formData.get('content') as string

  const { error } = await supabase
    .from('posts')
    .insert({ title, content, user_id: user.id })

  if (error) {
    return { error: error.message }
  }

  revalidatePath('/posts')
  redirect('/posts')
}
```

### Usage in Client Component

```typescript
'use client'

import { createPost } from './actions'

export function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Route Handlers

### API Endpoint

```typescript
// app/api/posts/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data, error } = await supabase
    .from('posts')
    .select('*')

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}

export async function POST(request: Request) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const body = await request.json()

  const { data, error } = await supabase
    .from('posts')
    .insert({ ...body, user_id: user.id })
    .select()
    .single()

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data, { status: 201 })
}
```

## OAuth Callback

### Callback Route Handler

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
    await supabase.auth.exchangeCodeForSession(code)
  }

  return NextResponse.redirect(new URL(next, request.url))
}
```

## Static vs Dynamic Rendering

### Force Dynamic Rendering

When using Supabase auth, pages are typically dynamic:

```typescript
// Force dynamic rendering
export const dynamic = 'force-dynamic'

export default async function Page() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  // ...
}
```

### Static Pages with Public Data

For public data that doesn't need auth:

```typescript
// Can be statically generated
export default async function PublicPage() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
  )

  const { data } = await supabase
    .from('public_posts')
    .select('*')

  return <PostList posts={data} />
}
```

## Caching Considerations

### Revalidation

```typescript
import { revalidatePath, revalidateTag } from 'next/cache'

// Revalidate specific path
revalidatePath('/posts')

// Revalidate with tag
revalidateTag('posts')
```

### Cache Tags with Supabase

```typescript
// Fetch with cache tag
async function getPosts() {
  const supabase = await createClient()

  const { data } = await supabase
    .from('posts')
    .select('*')

  return data
}

// In page
export default async function Page() {
  const posts = await getPosts()
  // ...
}

// Tag-based revalidation in action
export async function createPost(formData: FormData) {
  // ... create post
  revalidateTag('posts')
}
```

## Common Gotchas

### 1. Cookies Not Accessible in Server Components

```typescript
// WRONG: Will throw error
export default async function Page() {
  const { cookies } = await import('next/headers')
  const cookieStore = cookies() // Error: cookies() expects to be called in Server Component
}

// CORRECT: Await cookies()
export default async function Page() {
  const { cookies } = await import('next/headers')
  const cookieStore = await cookies()
}
```

### 2. Client Component Hydration

```typescript
// WRONG: SSR/Client mismatch
'use client'
export function UserDisplay() {
  const supabase = createClient()
  const { data: { user } } = supabase.auth.getUser() // Synchronous call fails

  return <div>{user?.email}</div>
}

// CORRECT: Use useEffect
'use client'
export function UserDisplay() {
  const [user, setUser] = useState(null)
  const supabase = createClient()

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => setUser(data.user))
  }, [])

  return <div>{user?.email}</div>
}
```

### 3. Proxy Not Running

Check `matcher` configuration:

```typescript
export const config = {
  matcher: [
    // Include all routes except static files
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### 4. Session Not Persisting

Ensure proxy returns `supabaseResponse`:

```typescript
// WRONG
return NextResponse.next()

// CORRECT
return supabaseResponse
```

## PKCE Flow for SSR

Supabase uses PKCE (Proof Key for Code Exchange) for SSR auth. This is handled automatically but requires:

1. **Callback route** to exchange code for session
2. **Proper redirects** after OAuth

```typescript
// Initiate OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${origin}/auth/callback?next=/dashboard`
  }
})

// Callback handles PKCE exchange automatically
// app/auth/callback/route.ts handles this
```

## Checklist

Before deploying:

- [ ] Using `@supabase/ssr` package
- [ ] Using `proxy.ts` (not `middleware.ts`) for Next.js 16+
- [ ] Proxy calls `getUser()` and returns `supabaseResponse`
- [ ] Server client uses `getAll()` and `setAll()` only
- [ ] OAuth callback route configured
- [ ] Environment variables set
- [ ] Protected routes redirect to login
- [ ] `router.refresh()` called after auth state changes
- [ ] Error boundaries handle auth errors

## References

- https://supabase.com/docs/guides/auth/server-side-rendering
- https://supabase.com/docs/guides/getting-started/tutorials/with-nextjs
- https://nextjs.org/docs/app/building-your-application/rendering
