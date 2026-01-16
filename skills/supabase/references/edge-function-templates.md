# Edge Function Templates Reference

Complete templates for Supabase Edge Functions with Deno runtime.

## Core Principles

### ✅ ALWAYS USE:
1. **Web APIs and Deno Core APIs**
   - `fetch` instead of Axios
   - WebSockets API instead of node-ws
   - `Deno.serve` instead of std@http/server

2. **Proper Import Specifiers**
   ```typescript
   // ✅ CORRECT
   import express from "npm:express@4.18.2"
   import { createClient } from "npm:@supabase/supabase-js@2"
   import process from "node:process"

   // ❌ WRONG
   import express from "express"  // No bare specifiers!
   ```

3. **Shared Utilities**
   - Place in `supabase/functions/_shared/`
   - Import with relative paths
   - NO cross-dependencies between functions

4. **Pre-populated Environment Variables**
   ```typescript
   // These are automatically available:
   Deno.env.get('SUPABASE_URL')
   Deno.env.get('SUPABASE_PUBLISHABLE_KEY')  // or SUPABASE_ANON_KEY (legacy)
   Deno.env.get('SUPABASE_SECRET_KEY')       // or SUPABASE_SERVICE_ROLE_KEY (legacy)
   Deno.env.get('SUPABASE_DB_URL')
   ```

> **Note:** Use the new key names (`SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SECRET_KEY`) for new projects. See https://supabase.com/docs/guides/api/api-keys

### ❌ NEVER USE:
- Bare specifiers without npm:/jsr:/node: prefix
- Imports without version numbers
- Cross-dependencies between Edge Functions
- File writes outside `/tmp` directory
- Old `serve` from deno.land/std

## Template 1: Basic Function Structure

**Use when:** Simple API endpoint with CORS support

**File:** `supabase/functions/hello-world/index.ts`

```typescript
interface RequestPayload {
  name?: string
  message?: string
}

console.info('Function hello-world started')

Deno.serve(async (req: Request) => {
  // CORS headers for browser requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
      }
    })
  }

  try {
    const payload: RequestPayload = await req.json()

    // Your logic here
    const result = {
      message: `Hello, ${payload.name || 'World'}!`,
      timestamp: new Date().toISOString(),
    }

    return new Response(
      JSON.stringify({ success: true, data: result }),
      {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  }
})
```

## Template 2: Function with Supabase Client

**Use when:** Need to query/modify Supabase database

**File:** `supabase/functions/get-students/index.ts`

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

interface RequestPayload {
  institution_id: string
  status?: string
}

console.info('Function get-students started')

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
      }
    })
  }

  try {
    // Get auth header
    const authHeader = req.headers.get('Authorization')

    if (!authHeader) {
      return new Response(
        JSON.stringify({ error: 'Missing authorization header' }),
        { status: 401 }
      )
    }

    // Create Supabase client with user's auth (respects RLS)
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_PUBLISHABLE_KEY')!,
      {
        global: {
          headers: { Authorization: authHeader }
        }
      }
    )

    // Verify user
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401 }
      )
    }

    // Parse request
    const payload: RequestPayload = await req.json()

    // Query database
    let query = supabase
      .from('students')
      .select('*')
      .eq('institution_id', payload.institution_id)

    if (payload.status) {
      query = query.eq('status', payload.status)
    }

    const { data, error } = await query

    if (error) {
      throw error
    }

    return new Response(
      JSON.stringify({ success: true, data }),
      {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      }
    )
  } catch (error) {
    console.error('Error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  }
})
```

## Template 3: Function with Service Role (Admin)

**Use when:** Need elevated permissions (bypass RLS)

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  try {
    // Verify admin user first
    const authHeader = req.headers.get('Authorization')
    const supabaseUser = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_PUBLISHABLE_KEY')!,
      {
        global: {
          headers: { Authorization: authHeader! }
        }
      }
    )

    const { data: { user }, error } = await supabaseUser.auth.getUser()

    if (error || !user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401 }
      )
    }

    // Check if user is admin
    if (user.user_metadata?.role !== 'admin') {
      return new Response(
        JSON.stringify({ error: 'Forbidden' }),
        { status: 403 }
      )
    }

    // Create admin client (bypasses RLS)
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SECRET_KEY')!
    )

    // Perform admin operation
    const { data, error: adminError } = await supabaseAdmin
      .from('students')
      .select('*')  // Access all data, bypassing RLS

    if (adminError) {
      throw adminError
    }

    return new Response(
      JSON.stringify({ success: true, data }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
})
```

## Template 4: Function with Express (Multiple Routes)

**Use when:** Need multiple endpoints in one function

**File:** `supabase/functions/api-handler/index.ts`

```typescript
import express from "npm:express@4.18.2"
import { Application } from "npm:express@4.18.2"

const app: Application = express()
app.use(express.json())

// IMPORTANT: Routes must be prefixed with function name
const FUNCTION_NAME = 'api-handler'

app.get(`/${FUNCTION_NAME}/health`, (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() })
})

app.get(`/${FUNCTION_NAME}/students`, async (req, res) => {
  try {
    // Your logic here
    res.json({ success: true, data: [] })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.post(`/${FUNCTION_NAME}/students`, async (req, res) => {
  try {
    const { name, email } = req.body

    // Validation
    if (!name || !email) {
      return res.status(400).json({ error: 'Missing required fields' })
    }

    // Your logic here
    res.status(201).json({ success: true, data: { name, email } })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.put(`/${FUNCTION_NAME}/students/:id`, async (req, res) => {
  try {
    const { id } = req.params
    const updates = req.body

    // Your logic here
    res.json({ success: true, data: { id, ...updates } })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.delete(`/${FUNCTION_NAME}/students/:id`, async (req, res) => {
  try {
    const { id } = req.params

    // Your logic here
    res.json({ success: true, message: 'Deleted' })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

app.listen(8000)
console.info('Express server listening on port 8000')
```

## Template 5: Function with Background Tasks

**Use when:** Need to respond immediately but process in background

```typescript
Deno.serve(async (req: Request) => {
  try {
    const { task, data } = await req.json()

    // Validate request
    if (!task) {
      return new Response(
        JSON.stringify({ error: 'Missing task parameter' }),
        { status: 400 }
      )
    }

    // Respond immediately
    const response = new Response(
      JSON.stringify({
        message: 'Task queued',
        task_id: crypto.randomUUID(),
      }),
      { status: 202 }
    )

    // Run long task in background
    EdgeRuntime.waitUntil(
      performLongRunningTask(task, data)
        .then(result => {
          console.log('Task completed:', result)
        })
        .catch(error => {
          console.error('Task failed:', error)
        })
    )

    return response
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
})

async function performLongRunningTask(task: string, data: any) {
  // Simulate long operation
  await new Promise(resolve => setTimeout(resolve, 5000))

  // Your actual long-running logic here
  console.log('Processing task:', task)

  return { completed: true, task, data }
}
```

## Template 6: Function with File Operations

**Use when:** Need to create/read temporary files

```typescript
import { writeFile, readFile } from "node:fs/promises"
import { join } from "node:path"

Deno.serve(async (req: Request) => {
  try {
    const { content, filename } = await req.json()

    if (!filename || !content) {
      return new Response(
        JSON.stringify({ error: 'Missing filename or content' }),
        { status: 400 }
      )
    }

    // ONLY /tmp is writable
    const filepath = join('/tmp', filename)

    // Write file
    await writeFile(filepath, content, 'utf-8')

    // Read file back
    const data = await readFile(filepath, 'utf-8')

    return new Response(
      JSON.stringify({
        success: true,
        saved: true,
        content: data,
        path: filepath,
      }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
})
```

## Template 7: Function with External API Call

**Use when:** Need to call external services

```typescript
interface WeatherResponse {
  temperature: number
  condition: string
  location: string
}

Deno.serve(async (req: Request) => {
  try {
    const { city } = await req.json()

    if (!city) {
      return new Response(
        JSON.stringify({ error: 'Missing city parameter' }),
        { status: 400 }
      )
    }

    // Call external API
    const apiKey = Deno.env.get('WEATHER_API_KEY')
    const response = await fetch(
      `https://api.weather.com/v1/current?city=${city}&key=${apiKey}`
    )

    if (!response.ok) {
      throw new Error(`Weather API error: ${response.statusText}`)
    }

    const weatherData: WeatherResponse = await response.json()

    return new Response(
      JSON.stringify({ success: true, data: weatherData }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    console.error('Error fetching weather:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
})
```

## Template 8: Function with AI Embeddings

**Use when:** Need to generate embeddings for vector search

```typescript
const model = new Supabase.ai.Session('gte-small')

Deno.serve(async (req: Request) => {
  try {
    const { text } = await req.json()

    if (!text) {
      return new Response(
        JSON.stringify({ error: 'Missing text parameter' }),
        { status: 400 }
      )
    }

    // Generate embeddings
    const embeddings = await model.run(text, {
      mean_pool: true,
      normalize: true
    })

    // Store in database
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SECRET_KEY')!
    )

    const { data, error } = await supabase
      .from('documents')
      .insert({
        content: text,
        embedding: embeddings
      })
      .select()
      .single()

    if (error) {
      throw error
    }

    return new Response(
      JSON.stringify({
        success: true,
        data,
        embedding_length: embeddings.length
      }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
})
```

## Template 9: Scheduled Function (Cron)

**Use when:** Need to run function on schedule

**File:** `supabase/functions/daily-report/index.ts`

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  try {
    // Verify this is a scheduled invocation
    const authHeader = req.headers.get('Authorization')
    const cronSecret = Deno.env.get('CRON_SECRET')

    if (authHeader !== `Bearer ${cronSecret}`) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401 }
      )
    }

    console.log('Running daily report...')

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SECRET_KEY')!
    )

    // Generate report
    const { data, error } = await supabase
      .rpc('generate_daily_report')

    if (error) {
      throw error
    }

    console.log('Report generated:', data)

    return new Response(
      JSON.stringify({ success: true, report: data }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    console.error('Cron job error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
})
```

## Shared Utilities Pattern

**File:** `supabase/functions/_shared/auth.ts`

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

export async function verifyUser(authHeader: string | null) {
  if (!authHeader) {
    throw new Error('Missing authorization header')
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_PUBLISHABLE_KEY')!,
    {
      global: {
        headers: { Authorization: authHeader }
      }
    }
  )

  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    throw new Error('Unauthorized')
  }

  return { user, supabase }
}

export function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  }
}
```

**Usage in function:**

```typescript
import { verifyUser, corsHeaders } from '../_shared/auth.ts'

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders() })
  }

  try {
    const authHeader = req.headers.get('Authorization')
    const { user, supabase } = await verifyUser(authHeader)

    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders(), 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 401 }
    )
  }
})
```

## Deployment Commands

```bash
# Deploy single function
supabase functions deploy function-name

# Deploy all functions
supabase functions deploy

# Set secrets
supabase secrets set --env-file ./supabase/.env.local

# Test locally
supabase functions serve function-name --env-file ./supabase/.env.local

# Invoke function locally
curl -i --location --request POST \
  'http://localhost:54321/functions/v1/function-name' \
  --header 'Authorization: Bearer YOUR_PUBLISHABLE_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"key":"value"}'
```

## Edge Functions Checklist

- [ ] Using Deno.serve (not old serve import)
- [ ] All imports have npm:/jsr:/node: prefix
- [ ] All npm packages have version numbers
- [ ] Shared code in _shared folder
- [ ] No cross-function dependencies
- [ ] File operations only in /tmp
- [ ] CORS headers for browser requests
- [ ] Error handling with try-catch
- [ ] Using EdgeRuntime.waitUntil for background tasks
- [ ] Proper authentication checks
- [ ] Environment variables loaded correctly

## Troubleshooting

### Import Errors

```typescript
// ❌ WRONG
import { createClient } from '@supabase/supabase-js'

// ✅ CORRECT
import { createClient } from 'npm:@supabase/supabase-js@2'
```

### CORS Errors

```typescript
// Always include CORS headers
return new Response(data, {
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  }
})
```

### File Write Errors

```typescript
// ❌ WRONG - Not allowed
await writeFile('/home/file.txt', content)

// ✅ CORRECT - Only /tmp is writable
await writeFile('/tmp/file.txt', content)
```

## Template 10: Webhook Handler (Stripe)

**Use when:** Receiving webhooks from external services

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'
import Stripe from 'npm:stripe@14'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
})

const endpointSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET')!

Deno.serve(async (req: Request) => {
  const signature = req.headers.get('stripe-signature')

  if (!signature) {
    return new Response('Missing signature', { status: 400 })
  }

  try {
    const body = await req.text()
    const event = stripe.webhooks.constructEvent(body, signature, endpointSecret)

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SECRET_KEY')!
    )

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object
        await supabase
          .from('orders')
          .update({ status: 'paid' })
          .eq('stripe_session_id', session.id)
        break
      }
      case 'customer.subscription.updated': {
        const subscription = event.data.object
        await supabase
          .from('subscriptions')
          .update({
            status: subscription.status,
            current_period_end: new Date(subscription.current_period_end * 1000).toISOString()
          })
          .eq('stripe_subscription_id', subscription.id)
        break
      }
      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    return new Response(JSON.stringify({ received: true }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (err) {
    console.error('Webhook error:', err.message)
    return new Response(`Webhook Error: ${err.message}`, { status: 400 })
  }
})
```

## Template 11: GitHub Webhook Handler

```typescript
import { createHmac } from 'node:crypto'
import { createClient } from 'npm:@supabase/supabase-js@2'

const GITHUB_WEBHOOK_SECRET = Deno.env.get('GITHUB_WEBHOOK_SECRET')!

function verifySignature(payload: string, signature: string): boolean {
  const hmac = createHmac('sha256', GITHUB_WEBHOOK_SECRET)
  const digest = 'sha256=' + hmac.update(payload).digest('hex')
  return signature === digest
}

Deno.serve(async (req: Request) => {
  const signature = req.headers.get('x-hub-signature-256')
  const event = req.headers.get('x-github-event')

  if (!signature) {
    return new Response('Missing signature', { status: 401 })
  }

  const body = await req.text()

  if (!verifySignature(body, signature)) {
    return new Response('Invalid signature', { status: 401 })
  }

  const payload = JSON.parse(body)

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SECRET_KEY')!
  )

  switch (event) {
    case 'push':
      await supabase.from('commits').insert({
        repo: payload.repository.full_name,
        sha: payload.after,
        message: payload.head_commit?.message,
        author: payload.head_commit?.author?.name,
        pushed_at: payload.head_commit?.timestamp
      })
      break

    case 'pull_request':
      await supabase.from('pull_requests').upsert({
        repo: payload.repository.full_name,
        number: payload.pull_request.number,
        title: payload.pull_request.title,
        state: payload.pull_request.state,
        action: payload.action
      })
      break
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

## Cold Start Best Practices

Edge Functions have cold starts when a new instance is created. Optimize for fast cold starts:

### 1. Minimize Top-Level Imports

```typescript
// ❌ Slow - imports at top level
import { createClient } from 'npm:@supabase/supabase-js@2'
import Stripe from 'npm:stripe@14'
import { PDFDocument } from 'npm:pdf-lib@1.17.1'

// ✅ Fast - lazy imports
Deno.serve(async (req) => {
  // Only import what you need for this request
  const { createClient } = await import('npm:@supabase/supabase-js@2')

  // Heavy libraries imported only when needed
  if (req.url.includes('/generate-pdf')) {
    const { PDFDocument } = await import('npm:pdf-lib@1.17.1')
  }
})
```

### 2. Initialize Clients Inside Handler

```typescript
Deno.serve(async (req) => {
  // Create client per request (Deno caches module)
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_PUBLISHABLE_KEY')!
  )

  // Your logic
})
```

### 3. Keep Functions Small

```typescript
// ❌ One large function doing everything
// supabase/functions/do-everything/index.ts

// ✅ Multiple focused functions
// supabase/functions/process-order/index.ts
// supabase/functions/send-email/index.ts
// supabase/functions/generate-report/index.ts
```

### 4. Use Shared Modules Wisely

```typescript
// _shared/constants.ts - Fast (no async)
export const ALLOWED_ORIGINS = ['https://example.com']
export const MAX_FILE_SIZE = 10 * 1024 * 1024

// _shared/heavy-utils.ts - Slow (complex logic)
// Only import when needed
```

## Idempotency Pattern

Design functions to handle duplicate requests safely:

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req: Request) => {
  const { order_id, action } = await req.json()

  // Use idempotency key from header or generate from payload
  const idempotencyKey = req.headers.get('idempotency-key')
    ?? `${order_id}-${action}`

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SECRET_KEY')!
  )

  // Check if already processed
  const { data: existing } = await supabase
    .from('processed_requests')
    .select('result')
    .eq('idempotency_key', idempotencyKey)
    .single()

  if (existing) {
    // Return cached result
    return new Response(JSON.stringify(existing.result), {
      headers: { 'Content-Type': 'application/json' }
    })
  }

  // Process the request
  const result = await processOrder(order_id, action)

  // Store result for future identical requests
  await supabase
    .from('processed_requests')
    .insert({
      idempotency_key: idempotencyKey,
      result,
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
    })

  return new Response(JSON.stringify(result), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

## Rate Limiting Pattern

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

const RATE_LIMIT = 100  // requests
const WINDOW_MS = 60 * 1000  // per minute

Deno.serve(async (req: Request) => {
  const clientIp = req.headers.get('x-forwarded-for')?.split(',')[0] ?? 'unknown'

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SECRET_KEY')!
  )

  const windowStart = new Date(Date.now() - WINDOW_MS).toISOString()

  // Count requests in window
  const { count } = await supabase
    .from('rate_limits')
    .select('*', { count: 'exact', head: true })
    .eq('client_ip', clientIp)
    .gte('created_at', windowStart)

  if ((count ?? 0) >= RATE_LIMIT) {
    return new Response('Rate limit exceeded', {
      status: 429,
      headers: {
        'Retry-After': '60'
      }
    })
  }

  // Record this request
  await supabase
    .from('rate_limits')
    .insert({ client_ip: clientIp })

  // Process request
  // ...
})
```

## MCP Deployment

Edge Functions can be deployed via Model Context Protocol (MCP):

```bash
# Using Supabase CLI
supabase functions deploy my-function

# Using MCP (if available)
# Check dashboard for MCP deployment options
```

## References

- https://supabase.com/docs/guides/functions
- https://supabase.com/docs/guides/functions/quickstart
- https://supabase.com/docs/guides/functions/deploy
- https://deno.land/manual
