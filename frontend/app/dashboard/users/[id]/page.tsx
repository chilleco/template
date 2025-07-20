import { notFound, redirect } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type Props = { params: { id: string } };

export default async function UserDetail({ params }: Props) {
  const userResp = await api.GET("/users/{user_id}", {
    params: { path: { user_id: params.id } },
  });

  if (!userResp.data) notFound();
  const user = userResp.data;

  async function deactivate() {
    "use server"; // server action
    await api.POST("/users/{user_id}/deactivate", {
      params: { path: { user_id: params.id } },
    });
    redirect("/dashboard/users");
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{user.name}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <p>Email: {user.email}</p>
        <p>Status: {user.is_active ? "Active" : "Inactive"}</p>

        {user.is_active && (
          <form action={deactivate}>
            <Button variant="destructive">Deactivate</Button>
          </form>
        )}
      </CardContent>
    </Card>
  );
}
