import { NextIntlClientProvider } from 'next-intl';
import { ReactNode } from 'react';

import { Locale } from '@/config/i18n';

interface Props {
  locale: Locale;
  messages: Record<string, string>;
  children: ReactNode;
}

export function LocaleProvider({ locale, messages, children }: Props) {
  return (
    <NextIntlClientProvider locale={locale} messages={messages} timeZone="UTC">
      {children}
    </NextIntlClientProvider>
  );
}
