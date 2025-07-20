import { Badge } from "@/components/ui/badge";
import type { User } from "../model";

export function UserStatusBadge({ user }: { user: Pick<User, "is_active"> }) {
  return user.is_active ? (
    <Badge variant="outline" className="text-green-600">
      Active
    </Badge>
  ) : (
    <Badge variant="destructive">Inactive</Badge>
  );
}
