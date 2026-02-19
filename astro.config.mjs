import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

import node from '@astrojs/node';

export default defineConfig({
  site: 'https://marketing.tvoje.info',
  output: 'static',
  integrations: [tailwind(), sitemap(), mdx()],

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'cs'],
    routing: {
      prefixDefaultLocale: false,
    },
  },

  prefetch: {
    prefetchAll: false,
  },

  build: {
    inlineStylesheets: 'auto',
    assets: 'assets',
  },

  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
    domains: [],
    remotePatterns: [],
  },

  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: true,
    },
  },

  adapter: node({
    mode: 'standalone',
  }),
});
