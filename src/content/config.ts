import { defineCollection, z } from 'astro:content';

const projectsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    image: z.string(),
    tags: z.array(z.string()),
    category: z.enum(['seo', 'ppc', 'web', 'infrastructure']),
    client: z.string().optional(),
    year: z.number(),
    duration: z.string().optional(),
    stats: z
      .array(
        z.object({
          value: z.string(),
          label: z.string(),
        })
      )
      .optional(),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

const testimonialsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    role: z.string(),
    company: z.string(),
    content: z.string(),
    avatar: z.string().optional(),
    rating: z.number().min(1).max(5).default(5),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

const servicesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    icon: z.string(),
    tags: z.array(z.string()),
    category: z.enum(['strategy', 'campaigns', 'content', 'analytics', 'ecommerce']),
    features: z.array(z.string()),
    pricing: z
      .object({
        starting: z.string(),
        unit: z.enum(['hour', 'day', 'month', 'project']),
      })
      .optional(),
    featured: z.boolean().default(false),
    order: z.number().default(0),
  }),
});

export const collections = {
  projects: projectsCollection,
  testimonials: testimonialsCollection,
  services: servicesCollection,
};
