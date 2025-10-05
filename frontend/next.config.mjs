import { withSentryConfig } from "@sentry/nextjs";

const nextConfig = {
  experimental: {
    serverActions: true
  },
  reactStrictMode: true,
  i18n: {
    locales: ["en", "ru", "es", "zh", "ar"],
    defaultLocale: "en"
  }
};

export default withSentryConfig(nextConfig, { silent: true });
