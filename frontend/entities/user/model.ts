import { z } from "zod";
import type { components } from "@/generated/api/schema";

/**
 * ↓ Схема JSON coming from backend (components.schemas.UserRead)
 *    — оставляем обязательные поля, расширяем при желании.
 */
export const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string(),
  is_active: z.boolean(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type User = z.infer<typeof userSchema>;

/**
 * Helper — нормализация raw-ответа (полезно при кешировании SWR/React-Query)
 */
export function parseUser(
  payload: components["schemas"]["UserRead"]
): User {
  return userSchema.parse(payload);
}
