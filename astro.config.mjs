import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://portfolio.tvoje.info',
  integrations: [
    tailwind(),
    sitemap(),
    mdx()
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'cs'],
    routing: {
      prefixDefaultLocale: false
    }
  },
  // Performance optimizations
  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'viewport',
    prefetchPages: {
      '/': true,
      '/cs': true
    }
  },
  // Build optimizations
  build: {
    inlineStylesheets: 'auto',
    assets: 'assets'
  },
  // Image optimization
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp'
    },
    domains: [],
    remotePatterns: []
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: true
    }
  }
});
