export const defaultLocale = 'en';
export const locales = ['en', 'es', 'ru', 'zh', 'ar'] as const;

export const localeNames: Record<(typeof locales)[number], string> = {
  en: 'English',
  es: 'Español',
  ru: 'Русский',
  zh: '中文',
  ar: 'العربية'
};

export type Locale = (typeof locales)[number];
