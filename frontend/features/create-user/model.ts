import { z } from "zod";
import { userSchema } from "@/entities/user";

/* ===== Input DTO (frontend only) ===== */
export const createUserFormSchema = z
  .object({
    name: z.string().min(2),
    email: z.string().email(),
    password: z.string().min(8),
  })
  .required();

export type CreateUserForm = z.infer<typeof createUserFormSchema>;

/* ===== Result DTO (reuse entity schema) ===== */
export type CreatedUser = z.infer<typeof userSchema>;
