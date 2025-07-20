import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

export default async function UsersPreview({ limit }: { limit: number }) {
  const res = await api.GET("/users", { params: { query: { limit } } });
  const users = res.data ?? [];

  return (
    <Card className="mb-10">
      <CardHeader>
        <CardTitle>Newest users</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-1">
          {users.map((u) => (
            <li key={u.id}>
              <Link
                href={`/dashboard/users/${u.id}`}
                className="text-sm hover:underline"
              >
                {u.name} <span className="text-muted-foreground">({u.email})</span>
              </Link>
            </li>
          ))}
        </ul>

        <Link
          className="mt-4 inline-block text-sm text-primary hover:underline"
          href="/dashboard/users"
        >
          View all →
        </Link>
      </CardContent>
    </Card>
  );
}
