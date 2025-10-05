import { z } from 'zod';

export const postSchema = z.object({
  id: z.number(),
  slug: z.string(),
  title: z.string(),
  summary: z.string().nullable(),
  content: z.string(),
  visibility: z.string(),
  status: z.string(),
  locale: z.string(),
  seo: z.record(z.any()),
  extra: z.record(z.any()),
  is_featured: z.boolean(),
  author_id: z.number(),
  published_at: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string()
});

export type Post = z.infer<typeof postSchema>;
