---
name: supabase-expert
description: >-
  This skill should be used when the user asks to "create a Supabase table",
  "write RLS policies", "set up Supabase Auth", "create Edge Functions",
  "configure Storage buckets", "use Supabase with Next.js", "migrate API keys",
  "implement row-level security", "create database functions", "set up SSR auth",
  or mentions 'Supabase', 'RLS', 'Edge Function', 'Storage bucket', 'anon key',
  'service role', 'publishable key', 'secret key'. Automatically triggers when
  user mentions 'database', 'table', 'SQL', 'migration', 'policy'.
---

# Supabase Expert

## Overview

Comprehensive guidance for working with Supabase including database operations, authentication, storage, edge functions, and Next.js integration. Enforces security patterns, performance optimizations, and modern best practices.

## Critical Rules

### API Keys (New System)

Supabase now offers two key types with improved security:

| Key Type | Prefix | Safety | Use Case |
|----------|--------|--------|----------|
| Publishable | `sb_publishable_...` | Safe for client | Browser, mobile, CLI |
| Secret | `sb_secret_...` | Backend only | Servers, Edge Functions |
| Legacy anon | JWT-based | Safe for client | Being deprecated |
| Legacy service_role | JWT-based | Backend only | Being deprecated |

**Key Rules:**
- Secret keys return HTTP 401 if used in browser
- New keys support independent rotation without downtime
- Migrate from legacy keys when possible

**See `references/api-keys.md` for migration guide and security practices.**

### Authentication SSR Rules

**NEVER USE (DEPRECATED):**
- Individual cookie methods: `get()`, `set()`, `remove()`
- Package: `@supabase/auth-helpers-nextjs`

**ALWAYS USE:**
- Package: `@supabase/ssr`
- Cookie methods: `getAll()` and `setAll()` ONLY
- Proxy (formerly Middleware) MUST call `getUser()` to refresh session
- Proxy MUST return `supabaseResponse` object

> **Important:** As of Next.js 16+, use `proxy.ts` instead of `middleware.ts`. See https://nextjs.org/docs/app/api-reference/file-conventions/proxy

**See `references/auth-ssr-patterns.md` for complete patterns.**

### RLS Policy Rules

- Always wrap functions in SELECT: `(SELECT auth.uid())` not `auth.uid()`
- **SELECT**: USING only (no WITH CHECK)
- **INSERT**: WITH CHECK only (no USING)
- **UPDATE**: Both USING and WITH CHECK
- **DELETE**: USING only (no WITH CHECK)
- Always specify `TO authenticated` or `TO anon`
- Create indexes on ALL columns used in policies
- NEVER use `FOR ALL` - create 4 separate policies

**See `references/rls-policy-patterns.md` for performance-optimized templates.**

### Database Function Rules

- **DEFAULT**: Use `SECURITY INVOKER` (safer than DEFINER)
- **ALWAYS**: Set `search_path = ''` for security
- **USE**: Fully qualified names (`public.table_name`)
- **SPECIFY**: Correct volatility (IMMUTABLE/STABLE/VOLATILE)
- **AVOID**: `SECURITY DEFINER` unless absolutely required

### Edge Function Rules

- **USE**: `Deno.serve` (not old serve import)
- **IMPORTS**: Always use `npm:/jsr:/node:` prefix with version numbers
- **SHARED**: Place shared code in `_shared/` folder
- **FILES**: Write only to `/tmp` directory
- **NEVER**: Use bare specifiers or cross-function dependencies

**See `references/edge-function-templates.md` for complete templates.**

### Storage Rules

- Enable RLS on storage buckets
- Use signed URLs for private content
- Apply image transformations via URL parameters
- Leverage CDN for public assets

**See `references/storage-patterns.md` for setup and patterns.**

## Workflow Decision Tree

```
User mentions database/Supabase work?
├─> Creating new tables?
│   └─> Use: Table Creation Workflow
├─> Creating RLS policies?
│   └─> Use: RLS Policy Workflow (references/rls-policy-patterns.md)
├─> Creating database function?
│   └─> Use: Database Function Workflow (references/sql-templates.md)
├─> Setting up Auth?
│   └─> Use: Auth SSR Workflow (references/auth-ssr-patterns.md)
├─> Creating Edge Function?
│   └─> Use: Edge Function Workflow (references/edge-function-templates.md)
├─> Setting up Storage?
│   └─> Use: Storage Workflow (references/storage-patterns.md)
├─> Next.js integration?
│   └─> Use: Next.js Patterns (references/nextjs-caveats.md)
└─> API key questions?
    └─> Use: API Keys Guide (references/api-keys.md)
```

## Table Creation Workflow

**When to use:** Creating new database tables.

1. **Design table structure:**
   - `id` (UUID PRIMARY KEY)
   - `created_at`, `updated_at` (TIMESTAMPTZ)
   - `created_by` (UUID reference to auth.users or profiles)
   - Use snake_case for all identifiers
   - Add comments on all tables

2. **Follow template:**
   ```sql
   CREATE TABLE IF NOT EXISTS public.table_name (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       name TEXT NOT NULL,
       status TEXT DEFAULT 'active',
       created_by UUID REFERENCES auth.users(id),
       created_at TIMESTAMPTZ DEFAULT NOW(),
       updated_at TIMESTAMPTZ DEFAULT NOW()
   );

   COMMENT ON TABLE public.table_name IS 'Description';
   ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;

   CREATE INDEX idx_table_name_status ON public.table_name(status);
   ```

3. **Enable RLS and create policies**

4. **Create TypeScript types** for type safety

**See `references/sql-templates.md` for complete templates.**

## Auth SSR Quick Reference

**Browser Client:**
```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
  )
}
```

**Server Client:**
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
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch { /* Ignore in Server Components */ }
        },
      },
    }
  )
}
```

**Proxy (Critical) - replaces middleware.ts:**
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
        getAll() { return request.cookies.getAll() },
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

  // CRITICAL: Must call getUser() to refresh session
  await supabase.auth.getUser()

  return supabaseResponse  // MUST return supabaseResponse
}
```

## RLS Policy Quick Reference

| Operation | USING | WITH CHECK |
|-----------|-------|------------|
| SELECT | Required | Ignored |
| INSERT | Ignored | Required |
| UPDATE | Required | Required |
| DELETE | Required | Ignored |

**Example Policy:**
```sql
CREATE POLICY "Users view own records"
ON public.table_name
FOR SELECT
TO authenticated
USING ((SELECT auth.uid()) = user_id);
```

## Storage Quick Reference

**Create bucket:**
```sql
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', false);
```

**Storage policy:**
```sql
CREATE POLICY "Users upload own avatar"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'avatars' AND
  (SELECT auth.uid())::text = (storage.foldername(name))[1]
);
```

**Image transformation URL:**
```
/storage/v1/object/public/bucket/image.jpg?width=200&height=200&resize=cover
```

## Edge Function Quick Reference

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, content-type',
      }
    })
  }

  // User-scoped client (respects RLS)
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_PUBLISHABLE_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )

  // Admin client (bypasses RLS) - use SUPABASE_SECRET_KEY for admin operations
  // const adminClient = createClient(
  //   Deno.env.get('SUPABASE_URL')!,
  //   Deno.env.get('SUPABASE_SECRET_KEY')!
  // )

  // Your logic here

  return new Response(JSON.stringify({ success: true }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

## PostgreSQL Style Guide

- **lowercase** for SQL keywords
- **snake_case** for tables and columns
- **Plural** table names (users, orders)
- **Singular** column names (user_id, order_date)
- **Schema prefix** in queries (public.users)
- **Comments** on all tables
- **ISO 8601** dates

## Pre-Flight Checklist

Before ANY Supabase work:

- [ ] Using publishable key (`sb_publishable_...`) for client code
- [ ] Using secret key (`sb_secret_...`) only in secure backend
- [ ] Following table naming conventions
- [ ] Enabled RLS on tables
- [ ] Created indexes for policy columns
- [ ] Wrapped auth functions in SELECT
- [ ] Using @supabase/ssr with getAll/setAll
- [ ] Edge Functions using Deno.serve
- [ ] Imports have version numbers

## Resources

### Reference Files (Load as needed)

- **`references/api-keys.md`** - New API key system, migration guide
- **`references/storage-patterns.md`** - Storage setup, RLS, transformations
- **`references/nextjs-caveats.md`** - Next.js specific patterns and gotchas
- **`references/sql-templates.md`** - Complete SQL templates
- **`references/rls-policy-patterns.md`** - Performance-optimized RLS patterns
- **`references/auth-ssr-patterns.md`** - Complete Auth SSR implementation
- **`references/edge-function-templates.md`** - Edge function templates

## Common Mistakes to Avoid

1. Using auth.uid() without wrapping in SELECT
2. Forgetting to create indexes on policy columns
3. Using SECURITY DEFINER by default
4. Mixing individual cookie methods (get/set/remove)
5. Using bare import specifiers in Edge Functions
6. Using secret keys in browser code
7. Not calling getUser() in proxy
8. Not returning supabaseResponse from proxy
9. Using middleware.ts instead of proxy.ts (deprecated in Next.js 16+)

## Auth Providers Supported

Supabase Auth supports 20+ OAuth providers:
- Google, GitHub, GitLab, Bitbucket
- Apple, Microsoft, Facebook, Twitter
- Discord, Slack, Spotify, Twitch
- LinkedIn, Notion, Figma, Zoom
- Phone auth (Twilio, MessageBird, Vonage)
- Anonymous sign-ins
- Enterprise SSO (SAML)

**See `references/auth-ssr-patterns.md` for provider setup.**

---

**Skill Version:** 2.0.0
**Last Updated:** 2025-01-01
**Documentation:** https://supabase.com/docs
