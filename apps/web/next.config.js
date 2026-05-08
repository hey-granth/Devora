/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  transpilePackages: ['@shadcn/ui'],
}

module.exports = nextConfig
