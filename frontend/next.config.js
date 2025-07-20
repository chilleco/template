/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    typescript: {
      ignoreBuildErrors: true,  // Skip TypeScript checking to prevent hangs
    },
    eslint: {
      ignoreDuringBuilds: true,  // Skip ESLint checking
    },
    experimental: {
      serverActions: true,
      serverComponentsExternalPackages: ["openapi-typescript-fetch"],
    },
    images: {
      domains: [],          // добавите CDN-домены при нужде
    },
  };
  
  module.exports = nextConfig;
  