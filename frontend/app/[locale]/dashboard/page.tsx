import { Suspense } from 'react';

import { DashboardClient } from '@/components/dashboard/dashboard-client';

export default function DashboardPage() {
  return (
    <section className="mx-auto w-full max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold">Command center</h1>
      <p className="mt-2 text-foreground/70">Monitor AI tasks, queues, and experiments across projects.</p>
      <Suspense fallback={<p className="mt-6 text-foreground/60">Loading dashboard...</p>}>
        <DashboardClient />
      </Suspense>
    </section>
  );
}
