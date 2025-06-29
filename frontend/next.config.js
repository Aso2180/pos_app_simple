/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker containers
  output: 'standalone',
  
  // Optimize for production
  swcMinify: true,
  
  // Compress images
  images: {
    domains: ['pos-backend.ashystone-fb341e56.japaneast.azurecontainerapps.io'],
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  
  // Disable x-powered-by header for security
  poweredByHeader: false,
  
  // Redirect HTTP to HTTPS in production
  async redirects() {
    return process.env.NODE_ENV === 'production' ? [
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'x-forwarded-proto',
            value: 'http',
          },
        ],
        destination: 'https://pos-frontend.ashystone-fb341e56.japaneast.azurecontainerapps.io/:path*',
        permanent: true,
      },
    ] : [];
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;