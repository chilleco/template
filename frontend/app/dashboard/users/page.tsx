import { DataTable } from "@/components/ui/data-table";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { api } from "@/lib/api";
import { CreateUserFormCard } from "@/features/create-user";
import { Button } from "@/shared/ui/button";
import { columns } from "./columns";

export const metadata = { title: "Users – dashboard" };

export default async function UsersPage() {
  const res = await api.GET("/users");
  const data = res.data ?? [];
  return (
    <>
      <h1 className="mb-6 text-2xl font-semibold">Users</h1>
      <Dialog>
        <DialogTrigger asChild>
          <Button size="sm">+ New user</Button>
        </DialogTrigger>
        <DialogContent>
          <CreateUserFormCard />
        </DialogContent>
      </Dialog>
      <DataTable
        columns={columns}
        data={data}
        rowHref={(row) => `/dashboard/users/${row.id}`}
      />
    </>
  );
}
