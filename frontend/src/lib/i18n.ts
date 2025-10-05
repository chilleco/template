const translations = {
  en: { welcome: "Welcome" },
  ru: { welcome: "Добро пожаловать" },
  es: { welcome: "Bienvenido" },
  zh: { welcome: "欢迎" },
  ar: { welcome: "مرحبا" }
} as const;

export type SupportedLocale = keyof typeof translations;
export type TranslationKey = keyof (typeof translations)["en"];

export function translate(locale: SupportedLocale, key: TranslationKey): string {
  const dict = translations[locale] ?? translations.en;
  return dict[key] ?? key;
}
