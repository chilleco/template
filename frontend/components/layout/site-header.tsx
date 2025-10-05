import Link from 'next/link';

import { ThemeToggle } from '@/components/navigation/theme-toggle';

export function SiteHeader() {
  return (
    <header className="flex items-center justify-between border-b border-border bg-background/80 px-6 py-4 backdrop-blur">
      <Link href="/" className="text-lg font-semibold">
        AI Native Template
      </Link>
      <div className="flex items-center gap-4">
        <nav className="hidden gap-4 text-sm font-medium md:flex">
          <Link href="/posts" className="hover:underline">
            Posts
          </Link>
          <Link href="/dashboard" className="hover:underline">
            Dashboard
          </Link>
        </nav>
        <ThemeToggle />
      </div>
    </header>
  );
}
