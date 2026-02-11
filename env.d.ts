/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly PUBLIC_FORMSPREE_ID: string;
  readonly PUBLIC_GA_ID?: string;
  readonly PUBLIC_SITE_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare namespace App {
  interface Locals {
    lang: 'en' | 'cs';
  }
}

declare module '*.md' {
  import type { MarkdownLayoutProps } from 'astro';
  
  export const frontmatter: Record<string, unknown>;
  export const file: string;
  export const url: string | undefined;
  
  export default function Layout({
    frontmatter,
    ...props
  }: MarkdownLayoutProps<Record<string, unknown>>): string;
}

declare module '*.mdx' {
  import type { MDXComponentProps } from 'astro/mdx';
  
  export const frontmatter: Record<string, unknown>;
  
  export default function Layout({
    components,
    ...props
  }: MDXComponentProps): string;
}
