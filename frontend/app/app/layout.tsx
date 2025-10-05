import Link from "next/link";
import type { ReactNode } from "react";

import { SidebarNav } from "@/components/sidebar-nav";

const navItems = [
  { href: "/app", label: "Dashboard" },
  { href: "/app/posts", label: "Posts" },
  { href: "/app/users", label: "Users" },
  { href: "/app/settings", label: "Settings" }
];

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col md:flex-row">
      <SidebarNav items={navItems} />
      <nav className="flex items-center justify-between border-b bg-background px-4 py-3 md:hidden">
        <span className="text-sm font-semibold">Operations Console</span>
        <div className="flex gap-3 text-sm">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="text-muted-foreground">
              {item.label}
            </Link>
          ))}
        </div>
      </nav>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
