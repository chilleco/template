import { getMessages } from 'next-intl/server';
import { ReactNode } from 'react';

import { SiteFooter } from '@/components/layout/site-footer';
import { SiteHeader } from '@/components/layout/site-header';
import { LocaleProvider } from '@/providers/locale-provider';
import { AppProvider } from '@/providers/app-provider';
import { Locale, locales } from '@/config/i18n';

export function generateStaticParams() {
  return locales.map(locale => ({ locale }));
}

export default async function LocaleLayout({ children, params }: { children: ReactNode; params: { locale: Locale } }) {
  const { locale } = params;
  if (!locales.includes(locale)) {
    throw new Error('Unsupported locale');
  }
  const messages = await getMessages();

  return (
    <html lang={locale} suppressHydrationWarning>
      <body>
        <LocaleProvider locale={locale} messages={messages as Record<string, string>}>
          <AppProvider>
            <div className="flex min-h-screen flex-col">
              <SiteHeader />
              <main className="flex-1 bg-background">{children}</main>
              <SiteFooter />
            </div>
          </AppProvider>
        </LocaleProvider>
      </body>
    </html>
  );
}
