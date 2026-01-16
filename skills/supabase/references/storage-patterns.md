# Storage Patterns Reference

Complete guide to Supabase Storage including bucket configuration, RLS policies, image transformations, and CDN delivery.

## Overview

Supabase Storage provides:
- S3-compatible object storage
- Global CDN (285+ cities)
- On-the-fly image transformations
- Row Level Security for fine-grained access
- Resumable uploads (TUS protocol)
- Direct URL access

## Bucket Configuration

### Create Bucket via SQL

```sql
-- Public bucket (files accessible without auth)
INSERT INTO storage.buckets (id, name, public)
VALUES ('public-assets', 'public-assets', true);

-- Private bucket (requires auth)
INSERT INTO storage.buckets (id, name, public)
VALUES ('user-files', 'user-files', false);

-- Bucket with file size limit (10MB)
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('avatars', 'avatars', false, 10485760);

-- Bucket with allowed MIME types
INSERT INTO storage.buckets (id, name, public, allowed_mime_types)
VALUES ('images', 'images', false, ARRAY['image/png', 'image/jpeg', 'image/webp']);
```

### Create Bucket via JavaScript

```typescript
const { data, error } = await supabase
  .storage
  .createBucket('avatars', {
    public: false,
    fileSizeLimit: 1024 * 1024 * 10, // 10MB
    allowedMimeTypes: ['image/png', 'image/jpeg']
  })
```

### List Buckets

```typescript
const { data: buckets } = await supabase.storage.listBuckets()
```

## Storage RLS Policies

Storage uses the `storage.objects` table for RLS.

### Policy for User Avatar Upload

```sql
-- Allow users to upload to their own folder
CREATE POLICY "Users upload own avatar"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'avatars' AND
  (SELECT auth.uid())::text = (storage.foldername(name))[1]
);

-- Allow users to update their own avatar
CREATE POLICY "Users update own avatar"
ON storage.objects
FOR UPDATE
TO authenticated
USING (
  bucket_id = 'avatars' AND
  (SELECT auth.uid())::text = (storage.foldername(name))[1]
);

-- Allow users to delete their own avatar
CREATE POLICY "Users delete own avatar"
ON storage.objects
FOR DELETE
TO authenticated
USING (
  bucket_id = 'avatars' AND
  (SELECT auth.uid())::text = (storage.foldername(name))[1]
);

-- Allow public read access to avatars
CREATE POLICY "Public read avatars"
ON storage.objects
FOR SELECT
TO public
USING (bucket_id = 'avatars');
```

### Policy for Team Files

```sql
-- Team members can upload to team folder
CREATE POLICY "Team members upload files"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'team-files' AND
  (storage.foldername(name))[1] IN (
    SELECT team_id::text
    FROM public.team_members
    WHERE user_id = (SELECT auth.uid())
  )
);

-- Team members can read team files
CREATE POLICY "Team members read files"
ON storage.objects
FOR SELECT
TO authenticated
USING (
  bucket_id = 'team-files' AND
  (storage.foldername(name))[1] IN (
    SELECT team_id::text
    FROM public.team_members
    WHERE user_id = (SELECT auth.uid())
  )
);
```

### Policy for Private User Files

```sql
-- Users can only access their own files
CREATE POLICY "Users manage own files"
ON storage.objects
FOR ALL
TO authenticated
USING (
  bucket_id = 'private-files' AND
  owner_id = (SELECT auth.uid())
)
WITH CHECK (
  bucket_id = 'private-files' AND
  owner_id = (SELECT auth.uid())
);
```

## File Operations

### Upload File

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true // Overwrite if exists
  })

// Upload with content type
const { data, error } = await supabase.storage
  .from('documents')
  .upload('report.pdf', file, {
    contentType: 'application/pdf'
  })
```

### Download File

```typescript
// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download(`${userId}/avatar.png`)

// Get public URL (public buckets only)
const { data } = supabase.storage
  .from('public-assets')
  .getPublicUrl('logo.png')
```

### Signed URLs (Private Buckets)

```typescript
// Generate signed URL (valid for 1 hour)
const { data, error } = await supabase.storage
  .from('private-files')
  .createSignedUrl('document.pdf', 3600)

// Generate multiple signed URLs
const { data, error } = await supabase.storage
  .from('private-files')
  .createSignedUrls(['file1.pdf', 'file2.pdf'], 3600)
```

### Delete Files

```typescript
// Delete single file
const { error } = await supabase.storage
  .from('avatars')
  .remove([`${userId}/avatar.png`])

// Delete multiple files
const { error } = await supabase.storage
  .from('uploads')
  .remove(['file1.png', 'file2.png', 'folder/file3.png'])
```

### List Files

```typescript
// List files in bucket
const { data, error } = await supabase.storage
  .from('avatars')
  .list(userId, {
    limit: 100,
    offset: 0,
    sortBy: { column: 'created_at', order: 'desc' }
  })
```

### Move/Copy Files

```typescript
// Move file
const { error } = await supabase.storage
  .from('avatars')
  .move('old-path/file.png', 'new-path/file.png')

// Copy file
const { error } = await supabase.storage
  .from('avatars')
  .copy('source/file.png', 'destination/file.png')
```

## Image Transformations

Supabase provides on-the-fly image transformations via URL parameters.

### Transform Parameters

| Parameter | Description | Values |
|-----------|-------------|--------|
| `width` | Width in pixels | 1-2500 |
| `height` | Height in pixels | 1-2500 |
| `resize` | Resize mode | `cover`, `contain`, `fill` |
| `quality` | JPEG/WebP quality | 20-100 |
| `format` | Output format | `origin`, `avif` |

### Transform URL Pattern

```
https://[project].supabase.co/storage/v1/render/image/public/[bucket]/[path]?width=200&height=200
```

### Examples

```typescript
// Get transformed URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user/avatar.jpg', {
    transform: {
      width: 200,
      height: 200,
      resize: 'cover'
    }
  })

// Manual URL construction
const transformedUrl = `${supabaseUrl}/storage/v1/render/image/public/avatars/user/avatar.jpg?width=200&height=200&resize=cover`
```

### Common Transformations

```typescript
// Thumbnail (cover crop to square)
const thumbnail = supabase.storage
  .from('images')
  .getPublicUrl('photo.jpg', {
    transform: { width: 150, height: 150, resize: 'cover' }
  })

// Profile picture (maintain aspect ratio)
const profile = supabase.storage
  .from('avatars')
  .getPublicUrl('avatar.jpg', {
    transform: { width: 400, height: 400, resize: 'contain' }
  })

// Optimized for web (WebP, reduced quality)
const optimized = supabase.storage
  .from('photos')
  .getPublicUrl('large-photo.jpg', {
    transform: { width: 1200, quality: 80, format: 'origin' }
  })
```

## CDN and Caching

### Cache Control

```typescript
// Upload with cache headers
const { data, error } = await supabase.storage
  .from('assets')
  .upload('logo.png', file, {
    cacheControl: '31536000', // 1 year
    upsert: false
  })
```

### CDN Best Practices

1. **Static assets:** Use long cache times (1 year)
2. **User content:** Use shorter cache times or unique filenames
3. **Versioning:** Include version in filename for cache busting

```typescript
// Cache busting with timestamp
const filename = `avatar_${Date.now()}.png`
await supabase.storage.from('avatars').upload(`${userId}/${filename}`, file)
```

## Resumable Uploads (TUS)

For large files, use TUS protocol for resumable uploads.

```typescript
import { createClient } from '@supabase/supabase-js'
import * as tus from 'tus-js-client'

const supabase = createClient(url, key)

async function uploadLargeFile(file: File) {
  const { data: { session } } = await supabase.auth.getSession()

  return new Promise((resolve, reject) => {
    const upload = new tus.Upload(file, {
      endpoint: `${supabaseUrl}/storage/v1/upload/resumable`,
      retryDelays: [0, 3000, 5000, 10000, 20000],
      headers: {
        authorization: `Bearer ${session?.access_token}`,
        'x-upsert': 'true'
      },
      uploadDataDuringCreation: true,
      metadata: {
        bucketName: 'videos',
        objectName: `user/${file.name}`,
        contentType: file.type,
        cacheControl: '3600'
      },
      chunkSize: 6 * 1024 * 1024, // 6MB chunks
      onError: (error) => reject(error),
      onProgress: (bytesUploaded, bytesTotal) => {
        const percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2)
        console.log(`${percentage}%`)
      },
      onSuccess: () => resolve(upload)
    })

    upload.findPreviousUploads().then((previousUploads) => {
      if (previousUploads.length) {
        upload.resumeFromPreviousUpload(previousUploads[0])
      }
      upload.start()
    })
  })
}
```

## S3 Compatibility

Supabase Storage is S3-compatible. Use with AWS SDK:

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const s3Client = new S3Client({
  forcePathStyle: true,
  region: 'us-east-1', // Required but ignored
  endpoint: `${supabaseUrl}/storage/v1/s3`,
  credentials: {
    accessKeyId: 'your-project-ref',
    secretAccessKey: 'your-service-role-key'
  }
})

// Upload via S3 SDK
await s3Client.send(new PutObjectCommand({
  Bucket: 'avatars',
  Key: 'user/avatar.png',
  Body: fileBuffer,
  ContentType: 'image/png'
}))
```

## Common Patterns

### Avatar Upload Component

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useState } from 'react'

export function AvatarUpload({ userId }: { userId: string }) {
  const [uploading, setUploading] = useState(false)
  const supabase = createClient()

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)

    const fileExt = file.name.split('.').pop()
    const filePath = `${userId}/avatar.${fileExt}`

    const { error } = await supabase.storage
      .from('avatars')
      .upload(filePath, file, { upsert: true })

    if (error) {
      console.error('Upload error:', error)
    }

    setUploading(false)
  }

  return (
    <input
      type="file"
      accept="image/*"
      onChange={handleUpload}
      disabled={uploading}
    />
  )
}
```

### File Gallery with Pagination

```typescript
async function getFiles(bucket: string, folder: string, page = 0) {
  const limit = 20
  const offset = page * limit

  const { data, error } = await supabase.storage
    .from(bucket)
    .list(folder, { limit, offset })

  if (error) throw error

  // Get signed URLs for private bucket
  const filesWithUrls = await Promise.all(
    data.map(async (file) => {
      const { data: urlData } = await supabase.storage
        .from(bucket)
        .createSignedUrl(`${folder}/${file.name}`, 3600)

      return { ...file, url: urlData?.signedUrl }
    })
  )

  return filesWithUrls
}
```

## Troubleshooting

### Upload Fails with 403

**Cause:** RLS policy blocking upload

**Solution:** Check storage policies
```sql
SELECT * FROM pg_policies WHERE tablename = 'objects';
```

### File Not Found After Upload

**Cause:** Path mismatch or incorrect bucket

**Solution:** Verify bucket name and file path
```typescript
// Check file exists
const { data } = await supabase.storage.from('bucket').list('folder')
console.log(data)
```

### Transformation Not Working

**Cause:** Using wrong URL endpoint

**Solution:** Use `/render/image/` not `/object/`
```
// Wrong
/storage/v1/object/public/bucket/image.jpg?width=200

// Correct
/storage/v1/render/image/public/bucket/image.jpg?width=200
```

## Checklist

Before deploying storage:

- [ ] Bucket created with appropriate settings
- [ ] RLS policies configured for all operations
- [ ] File size limits set appropriately
- [ ] MIME type restrictions if needed
- [ ] Cache control headers configured
- [ ] Signed URLs used for private content
- [ ] Image transformations tested
- [ ] Upload error handling implemented

## References

- https://supabase.com/docs/guides/storage
- https://supabase.com/docs/guides/storage/uploads
- https://supabase.com/docs/guides/storage/serving
- https://supabase.com/docs/guides/storage/image-transformations
