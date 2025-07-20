"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import type { User } from "../model";

export function UserAvatar({ user }: { user: Pick<User, "name" | "email"> }) {
  // Если будет облачный провайдер аватаров — сюда src.
  const initials = user.name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <Avatar className="h-8 w-8">
      <AvatarFallback className="text-xs">{initials}</AvatarFallback>
    </Avatar>
  );
}
