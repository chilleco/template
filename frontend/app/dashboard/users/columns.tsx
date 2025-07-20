export const columns = [
  {
    accessorKey: "id",
    header: "ID",
  },
  {
    accessorKey: "name", 
    header: "Name",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "createdAt",
    header: "Created At",
    cell: ({ getValue }: any) => {
      const date = getValue();
      return date ? new Date(date).toLocaleDateString() : "";
    },
  },
]; 