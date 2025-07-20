import { ReactNode } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <section className="mx-auto flex min-h-screen max-w-6xl flex-col">
      {/* Top-bar */}
      <header className="flex items-center justify-between gap-4 border-b p-4">
        <Link href="/" className="text-lg font-semibold">
          MyApp<span className="text-primary">•</span>Dashboard
        </Link>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Link href="/sign-in">
            <Button size="sm" variant="outline">Sign out</Button>
          </Link>
        </div>
      </header>

      <main className="flex flex-1 flex-col p-6">{children}</main>
    </section>
  );
}
