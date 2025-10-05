import Link from 'next/link';
import { getTranslations } from 'next-intl/server';

import { Button } from '@/components/ui/button';

export default async function LandingPage({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale, namespace: 'common' });

  return (
    <section className="mx-auto flex w-full max-w-5xl flex-col gap-12 px-6 py-16 md:flex-row md:items-center">
      <div className="flex-1 space-y-6">
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">{t('hero.headline')}</h1>
        <p className="text-lg text-foreground/75">{t('hero.copy')}</p>
        <div className="flex flex-col gap-4 sm:flex-row">
          <Button asChild>
            <Link href={`/${locale}/dashboard`}>{t('cta.getStarted')}</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/docs">{t('cta.viewDocs')}</Link>
          </Button>
        </div>
      </div>
      <div className="flex-1 rounded-xl border border-border bg-foreground/5 p-8 text-sm text-foreground/70">
        <p className="font-semibold">AI workflow checklist</p>
        <ol className="mt-4 space-y-2">
          <li>1. Plan with context-aware prompts</li>
          <li>2. Sync models and migrations</li>
          <li>3. Cover domain with tests</li>
          <li>4. Generate API + frontend surfaces</li>
          <li>5. Verify accessibility, locales, themes</li>
        </ol>
      </div>
    </section>
  );
}
