import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./config/i18n.ts');

const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: true,
  },
  eslint: {
    dirs: ['app', 'components', 'features', 'lib', 'store', 'config']
  }
};

export default withNextIntl(nextConfig);
