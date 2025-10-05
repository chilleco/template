import Link from "next/link";

import { Button } from "@/components/ui/button";

const dashboardLinks = [
  { href: "/app/posts", label: "Posts" },
  { href: "/app/users", label: "Users" },
  { href: "/app/analytics", label: "Analytics" }
];

export default function AppDashboard() {
  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold">Operations Console</h1>
        <p className="text-muted-foreground">
          Manage content, review user activity, and monitor async workflows.
        </p>
      </header>
      <div className="grid gap-4 md:grid-cols-3">
        {dashboardLinks.map((link) => (
          <div key={link.href} className="rounded-lg border bg-card p-4 shadow-sm">
            <h2 className="text-lg font-medium">{link.label}</h2>
            <Button className="mt-4" asChild variant="outline">
              <Link href={link.href}>Open</Link>
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
