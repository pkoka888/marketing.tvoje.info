import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date().optional(),
    tags: z.array(z.string()),
    category: z.string(),
    year: z.number(),
    image: z.string(),
    stats: z.array(
      z.object({
        value: z.string(),
        label: z.string(),
      })
    ),
    client: z.string().optional(),
    clientRole: z.string().optional(),
  }),
});

const services = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/services' }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    features: z.array(z.string()),
    icon: z.string(),
    price: z.string().optional(),
    popular: z.boolean().default(false),
  }),
});

const testimonials = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/testimonials' }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    company: z.string(),
    content: z.string(),
    avatar: z.string().optional(),
    lang: z.enum(['en', 'cs']).default('en'),
  }),
});

const faqs = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/faqs' }),
  schema: z.object({
    question: z.string(),
    answer: z.string(),
    category: z.string(),
    order: z.number().default(0),
  }),
});

export const collections = {
  projects,
  services,
  testimonials,
  faqs,
};
