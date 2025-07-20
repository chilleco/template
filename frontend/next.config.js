/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    experimental: {
      serverActions: true,
      serverComponentsExternalPackages: ["openapi-typescript-fetch"],
    },
    images: {
      domains: [],          // добавите CDN-домены при нужде
    },
  };
  
  module.exports = nextConfig;
  