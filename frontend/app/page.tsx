"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";
import { useLocale } from "@/lib/hooks";
import { translate, type SupportedLocale } from "@/lib/i18n";

export default function HomePage() {
  const locale = useLocale();
  const welcome = translate(locale as SupportedLocale, "welcome");
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-10 px-4 text-center">
      <section className="space-y-6">
        <p className="text-sm uppercase tracking-widest text-muted-foreground">{welcome}</p>
        <h1 className="text-balance text-4xl font-bold md:text-6xl">
          Build multi-platform products faster with aligned humans + AI
        </h1>
        <p className="mx-auto max-w-2xl text-muted-foreground">
          Opinionated architecture that keeps SEO, monetisation, realtime experiences, and compliance-friendly
          authentication in sync across web, bots, and mobile clients.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Button asChild size="lg">
            <Link href="/app">Launch App</Link>
          </Button>
          <Button asChild size="lg" variant="outline">
            <Link href="/docs/ai-flow">AI Dev Playbook</Link>
          </Button>
        </div>
      </section>
    </main>
  );
}
