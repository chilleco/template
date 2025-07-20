import { api } from "@/lib/api";
import type { components } from "@/generated/api/schema";
import { createUserFormSchema, CreatedUser } from "./model";

/** Обёртка над POST /users */
export async function createUser(
  data: unknown,
): Promise<CreatedUser> {
  const payload = createUserFormSchema.parse(data);

  const res = await api.POST("/users", {
    body: payload as components["schemas"]["UserCreate"],
  });

  if (res.error || !res.data) {
    throw new Error(res.error?.message ?? "Failed to create user");
  }
  return res.data;
}
