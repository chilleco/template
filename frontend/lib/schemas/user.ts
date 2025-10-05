import { z } from 'zod';

export const userSchema = z.object({
  id: z.number(),
  email: z.string().email().nullable().optional(),
  phone: z.string().nullable().optional(),
  username: z.string().nullable().optional(),
  role: z.string(),
  status: z.string(),
  is_email_verified: z.boolean(),
  is_phone_verified: z.boolean(),
  profile: z.record(z.any()),
  settings: z.record(z.any()),
  created_at: z.string(),
  updated_at: z.string()
});

export type User = z.infer<typeof userSchema>;
