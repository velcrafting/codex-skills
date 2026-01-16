# API Keys Reference

Complete guide to Supabase API keys, including the new key system and migration from legacy keys.

## Key Types Overview

Supabase provides four API key types:

### New Keys (Recommended)

| Key Type | Prefix | Privileges | Safe for Client |
|----------|--------|------------|-----------------|
| Publishable | `sb_publishable_...` | Low | Yes |
| Secret | `sb_secret_...` | Elevated (full data access) | No |

### Legacy Keys (Being Deprecated)

| Key Type | Format | Privileges | Safe for Client |
|----------|--------|------------|-----------------|
| `anon` | JWT-based | Low | Yes |
| `service_role` | JWT-based | Elevated | No |

## Publishable Keys

**Prefix:** `sb_publishable_...`

**Safe for:**
- Web pages (browser JavaScript)
- Mobile applications
- Desktop applications
- CLI tools
- GitHub Actions

**Protects against:**
- Basic denial-of-service attacks
- Bots and scrapers
- Automated vulnerability scanners

**Does NOT protect against:**
- Code analysis and reverse engineering
- Network inspection in browsers
- Cross-site attacks
- Man-in-the-middle attacks

**Usage:**
```typescript
import { createClient } from '@supabase/supabase-js'

// Safe to use in browser
const supabase = createClient(
  'https://your-project.supabase.co',
  'sb_publishable_...'  // Safe in client code
)
```

## Secret Keys

**Prefix:** `sb_secret_...`

**Use ONLY in:**
- Backend servers
- Edge Functions
- Microservices
- Secure environments

**Security:**
- Returns HTTP 401 if used in browser
- Full data access (bypasses RLS)
- Should never be exposed to clients

**Usage:**
```typescript
// Server-side only
import { createClient } from '@supabase/supabase-js'

const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY  // sb_secret_...
)

// Bypasses RLS - use carefully
const { data } = await supabaseAdmin
  .from('users')
  .select('*')
```

## Security Best Practices

### For Publishable Keys

1. **Data Protection:** Always use Row Level Security (RLS)
   ```sql
   ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

   CREATE POLICY "Users view own data"
   ON public.users
   FOR SELECT
   TO authenticated
   USING ((SELECT auth.uid()) = id);
   ```

2. **Rate Limiting:** Enable project rate limits in dashboard

3. **CORS:** Configure allowed origins

### For Secret Keys

1. **Never commit to source control**
   ```bash
   # .gitignore
   .env
   .env.local
   *.env
   ```

2. **Use environment variables**
   ```bash
   # .env.local
   SUPABASE_SECRET_KEY=sb_secret_...
   ```

3. **Use native secrets capability**
   ```bash
   # Supabase CLI
   supabase secrets set CUSTOM_SECRET=value
   ```

4. **Use separate keys per component**
   - One key for API server
   - One key for background jobs
   - One key for admin dashboard
   - Easier rotation if compromised

5. **Logging rules**
   - Log only first 6 characters: `sb_sec...`
   - Or store SHA256 hash for audit

6. **If compromised**
   - Rotate immediately in dashboard
   - Update all services
   - Review access logs

## Migration from Legacy Keys

### Benefits of New Keys

| Feature | Legacy Keys | New Keys |
|---------|-------------|----------|
| Independent rotation | No | Yes |
| Zero-downtime rotation | No | Yes |
| Shorter expiry | No | Yes |
| Reduced key size | No | Yes |
| Browser detection | No | Yes (401 for secret) |

### Migration Process

1. **Generate new keys** in Supabase Dashboard
   - Go to Project Settings > API
   - Generate new publishable/secret keys

2. **Update client code**
   ```typescript
   // Before (legacy)
   const supabase = createClient(url, process.env.SUPABASE_ANON_KEY)

   // After (new)
   const supabase = createClient(url, process.env.SUPABASE_PUBLISHABLE_KEY)
   ```

3. **Update server code**
   ```typescript
   // Before (legacy)
   const admin = createClient(url, process.env.SUPABASE_SERVICE_ROLE_KEY)

   // After (new)
   const admin = createClient(url, process.env.SUPABASE_SECRET_KEY)
   ```

4. **Run both keys in parallel** during transition

5. **Deprecate legacy keys** once migration complete

### Environment Variables

```bash
# Legacy (keep during migration)
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...

# New (recommended)
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...
SUPABASE_SECRET_KEY=sb_secret_...
```

## Access Control with RLS

API keys work with PostgreSQL's built-in roles:

### `anon` Role
- Used for unauthenticated requests
- Publishable/anon key requests default to this role
- Very limited permissions

```sql
-- Grant minimal access to anon
GRANT SELECT ON public.public_content TO anon;
```

### `authenticated` Role
- Used after user signs in
- JWT contains user info accessible via `auth.uid()`

```sql
-- Grant access to authenticated users
GRANT ALL ON public.user_data TO authenticated;

-- RLS policy using auth.uid()
CREATE POLICY "Users own data"
ON public.user_data
FOR ALL
TO authenticated
USING ((SELECT auth.uid()) = user_id);
```

### `service_role` Role
- Used with secret/service_role key
- Bypasses RLS completely
- Use with extreme caution

## Key Rotation

### New Keys (Zero-Downtime)

1. Generate new key in dashboard
2. Update environment variables
3. Deploy changes
4. Revoke old key

### Legacy Keys (Requires Planning)

1. Legacy keys are tied to JWT secret
2. Rotation affects all existing tokens
3. Plan for brief service interruption
4. Update all services simultaneously

## Common Patterns

### Browser Client (Publishable Key)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!  // or ANON_KEY
  )
}
```

### Server Client (Publishable Key + User Auth)

```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'

// Uses publishable key but with user's session
export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    { cookies: { /* ... */ } }
  )
}
```

### Admin Client (Secret Key)

```typescript
// lib/supabase/admin.ts
import { createClient } from '@supabase/supabase-js'

// Bypasses RLS - use for admin operations
export const supabaseAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SECRET_KEY!
)
```

### Edge Function

```typescript
// supabase/functions/admin-task/index.ts
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req) => {
  // For user-scoped operations (respects RLS)
  const userClient = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )

  // For admin operations (bypasses RLS)
  const adminClient = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // ...
})
```

## Troubleshooting

### HTTP 401 with Secret Key in Browser

**Problem:** Using secret key in client-side code

**Solution:** Use publishable key for browser code
```typescript
// Wrong
const supabase = createClient(url, 'sb_secret_...')

// Correct
const supabase = createClient(url, 'sb_publishable_...')
```

### RLS Blocking Requests

**Problem:** Data not returned despite valid key

**Solution:** Check RLS policies
```sql
-- Verify RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- Check policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';
```

### Key Rotation Issues

**Problem:** Services failing after rotation

**Solution:**
1. Ensure all services updated
2. Check for cached keys
3. Clear CDN cache if applicable
4. Verify environment variable names match

## Checklist

Before deploying:

- [ ] Using publishable key for browser/client code
- [ ] Using secret key only in secure server environments
- [ ] Secret key not committed to source control
- [ ] RLS enabled on all tables
- [ ] Environment variables properly configured
- [ ] Key rotation plan documented
- [ ] Separate keys for different services (optional but recommended)

## References

- https://supabase.com/docs/guides/api/api-keys
- https://supabase.com/docs/guides/database/postgres/row-level-security
