export type Language = 'en' | 'cs';

export interface Translations {
  nav: {
    home: string;
    projects: string;
    services: string;
    about: string;
    contact: string;
  };
  hero: {
    title: string;
    subtitle: string;
    cta: string;
    secondaryCta: string;
  };
  about: {
    title: string;
    bio: string;
    skills: string;
    certifications: string;
    downloadCV: string;
  };
  projects: {
    title: string;
    description: string;
    viewDetails: string;
    categories: {
      all: string;
      seo: string;
      ppc: string;
      web: string;
      infrastructure: string;
    };
  };
  services: {
    title: string;
    subtitle: string;
    strategy: {
      title: string;
      description: string;
      items: string[];
    };
    campaigns: {
      title: string;
      description: string;
      items: string[];
    };
    consulting: {
      title: string;
      description: string;
      items: string[];
    };
  };
  testimonials: {
    title: string;
  };
  clients: {
    title: string;
    subtitle: string;
  };
  team: {
    title: string;
    subtitle: string;
  };
  process: {
    title: string;
    subtitle: string;
  };
  blog: {
    title: string;
    subtitle: string;
    readMore: string;
    recentPosts: string;
  };
  certifications: {
    title: string;
  };
  contact: {
    title: string;
    subtitle: string;
    name: string;
    email: string;
    company: string;
    subject: string;
    message: string;
    budget: string;
    submit: string;
    success: string;
    error: string;
    required: string;
  };
  footer: {
    copyright: string;
    social: string;
    links: {
      privacy: string;
      terms: string;
    };
  };
  common: {
    learnMore: string;
    viewAll: string;
    loading: string;
    error: string;
    back: string;
    next: string;
    previous: string;
    search: string;
    filter: string;
  };
  meta: {
    description: string;
    keywords: string;
  };
}

export const translations: Record<Language, Translations> = {
  en: {
    nav: {
      home: 'Home',
      projects: 'Projects',
      services: 'Services',
      about: 'About',
      contact: 'Contact',
    },
    hero: {
      title: 'Growth That Scales',
      subtitle:
        'AI-powered marketing strategies that turn visitors into customers. Data-driven campaigns with measurable ROI.',
      cta: 'View Projects',
      secondaryCta: 'Get in Touch',
    },
    about: {
      title: 'Marketing & AI Specialist',
      bio: `I'm a passionate Marketing and AI Specialist with over 5 years of experience in building scalable growth strategies and automated marketing ecosystems. My expertise lies in bridging the gap between creative design and data-driven automation, implementing high-converting funnels, and integrating AI solutions into modern marketing workflows.\n\nI believe in the power of automation to transform businesses and am dedicated to helping organizations achieve exponential growth through state-of-the-art marketing practices and AI-powered solutions.`,
      skills: 'Technical Skills',
      certifications: 'Certifications',
      downloadCV: 'Download CV',
    },
    projects: {
      title: 'Featured Projects',
      description:
        'A selection of projects demonstrating expertise in Growth Strategy, AI, and Marketing Automation',
      viewDetails: 'View Details',
      categories: {
        all: 'All Projects',
        seo: 'SEO',
        ppc: 'PPC/Ads',
        web: 'Content',
        infrastructure: 'Growth',
      },
    },
    services: {
      title: 'Services',
      subtitle: 'How I can help your business grow',
      aiCampaigns: {
        title: 'AI Campaign Optimization',
        description:
          'Precision targeting with AI that learns and improves. Smart bidding, automated A/B testing, and real-time optimization.',
        items: [
          'AI-powered bidding strategies',
          'Cross-platform campaign management',
          'Automated A/B testing at scale',
          'Real-time performance optimization',
        ],
        result: '+40% ROAS typical',
      },
      tiktokAds: {
        title: 'TikTok & Short-Form Ads',
        description:
          'Tap into the fastest-growing marketing channel. Spark Ads, creator partnerships, and viral content strategies.',
        items: [
          'Spark Ads campaigns',
          'Creator collaboration',
          'Viral content strategy',
          'Short-form video production',
        ],
        result: '3x reach vs traditional',
      },
      automation: {
        title: 'Marketing Automation',
        description:
          'Turn visitors into customers with automated funnels that work 24/7. Lead nurturing, behavior triggers, and CRM integration.',
        items: [
          'Lead scoring & nurturing',
          'Behavior-triggered campaigns',
          'CRM integration (HubSpot, Klaviyo)',
          'Multi-channel orchestration',
        ],
        result: '50% more qualified leads',
      },
      aiSearch: {
        title: 'AI Search Optimization',
        description:
          'Optimize for the new frontier of search. Rank in ChatGPT, Perplexity, and AI Answer Engines.',
        items: [
          'AI Overview optimization',
          'Structured data for AI',
          'Content for LLM training',
          'Answer Engine positioning',
        ],
        result: 'Top 3 AI results',
      },
    },
    testimonials: {
      title: 'What Clients Say',
    },
    clients: {
      title: 'Trusted By',
      subtitle: "Companies we've worked with",
    },
    team: {
      title: 'Our Team',
      subtitle: 'Meet the experts behind your success',
    },
    process: {
      title: 'How We Work',
      subtitle: 'A proven process for delivering results',
    },
    blog: {
      title: 'Latest Insights',
      subtitle: 'Tips and trends from the marketing world',
      readMore: 'Read More',
      recentPosts: 'Recent Posts',
    },
    certifications: {
      title: 'Certifications',
    },
    contact: {
      title: 'Get in Touch',
      subtitle: "Ready to start your next project? Let's talk!",
      name: 'Full Name',
      email: 'Email Address',
      company: 'Company',
      subject: 'Subject',
      message: 'Message',
      budget: 'Project Budget',
      submit: 'Send Message',
      success: 'Thank you! Your message has been sent successfully.',
      error: 'Something went wrong. Please try again.',
      required: 'Required',
    },
    footer: {
      copyright: '© {year} Portfolio. All rights reserved.',
      social: 'Social',
      links: {
        privacy: 'Privacy Policy',
        terms: 'Terms of Service',
      },
    },
    common: {
      learnMore: 'Learn More',
      viewAll: 'View All',
      loading: 'Loading...',
      error: 'An error occurred',
      back: 'Back',
      next: 'Next',
      previous: 'Previous',
      search: 'Search',
      filter: 'Filter',
    },
    meta: {
      description:
        'Marketing & AI Specialist portfolio showcasing expertise in growth strategy, creative design, and AI-powered automation solutions',
      keywords: 'Marketing, AI, Growth Strategy, Automation, Funnels, Lead Generation, Portfolio',
    },
  },
  cs: {
    nav: {
      home: 'Domů',
      projects: 'Projekty',
      services: 'Služby',
      about: 'O mně',
      contact: 'Kontakt',
    },
    hero: {
      title: 'Růst, který funguje',
      subtitle:
        'AI marketingové strategie, které proměňují návštěvníky v zákazníky. Datově řízené kampaně s měřitelným ROI.',
      cta: 'Zobrazit projekty',
      secondaryCta: 'Kontaktovat',
    },
    about: {
      title: 'Marketingový & AI specialista',
      bio: `Jsem nadšený marketingový a AI specialista s více než 5 lety zkušeností v budování škálovatelných růstových strategií a automatizovaných marketingových ekosystémů. Moje specializace spočívá v propojení kreativního designu a datově řízené automatizace, implementaci vysoce konverzních funnelů a integraci AI řešení do moderních marketingových procesů.\n\nVěřím v sílu automatizace, která dokáže transformovat podniky, a jsem odhodlán pomáhat organizacím dosáhnout exponenciálního růstu pomocí špičkových marketingových postupů a AI řešení.`,
      skills: 'Technické dovednosti',
      certifications: 'Certifikace',
      downloadCV: 'Stáhnout životopis',
    },
    projects: {
      title: 'Vybrané projekty',
      description:
        'Výběr projektů demonstrujících odbornost v růstových strategiích, AI a automatizaci marketingu',
      viewDetails: 'Zobrazit detaily',
      categories: {
        all: 'Všechny projekty',
        seo: 'SEO',
        ppc: 'PPC/Reklamy',
        web: 'Obsah',
        infrastructure: 'Růst',
      },
    },
    services: {
      title: 'Služby',
      subtitle: 'Jak mohu pomoci vašemu podnikání růst',
      aiCampaigns: {
        title: 'AI optimalizace kampaní',
        description:
          'Precizní cílení s AI, která se učí a zlepšuje. Chytrý bidding, automatizované testování a optimalizace v reálném čase.',
        items: [
          'AI strategie bidování',
          'Správa kampaní napříč platformami',
          'Automatizované A/B testování',
          'Optimalizace v reálném čase',
        ],
        result: '+40% ROAS typicky',
      },
      tiktokAds: {
        title: 'TikTok & krátká videa',
        description:
          'Využijte nejrychleji rostoucí marketingový kanál. Spark Ads, spolupráce s tvůrci a virální strategie.',
        items: [
          'Spark Ads kampaně',
          'Spolupráce s influencery',
          'Virální content strategie',
          'Produkce krátkých videí',
        ],
        result: '3x dosah vs tradiční',
      },
      automation: {
        title: 'Marketingová automatizace',
        description:
          'Proměňte návštěvníky v zákazníky s automatizovanými funnely, které fungují 24/7. Lead nurturing, behaviorální triggery a CRM integrace.',
        items: [
          'Scoring a nurturing leadů',
          'Kampaně na základě chování',
          'CRM integrace (HubSpot, Klaviyo)',
          'Orchestrace napříč kanály',
        ],
        result: '50% více kvalifikovaných leadů',
      },
      aiSearch: {
        title: 'AI vyhledávání SEO',
        description:
          'Optimalizujte pro novou éru vyhledávání. Pozice v ChatGPT, Perplexity a AI odpovědních enginech.',
        items: [
          'Optimalizace pro AI Overview',
          'Strukturovaná data pro AI',
          'Content pro LLM modely',
          'Pozicování v AI odpovědích',
        ],
        result: 'Top 3 v AI výsledcích',
      },
    },
    testimonials: {
      title: 'Co říkají klienti',
    },
    clients: {
      title: 'Spolupracujeme s',
      subtitle: 'Společnosti, se kterými jsme pracovali',
    },
    team: {
      title: 'Náš tým',
      subtitle: 'Poznejte experty za vaším úspěchem',
    },
    process: {
      title: 'Jak pracujeme',
      subtitle: 'Osvědčený proces pro dosažení výsledků',
    },
    blog: {
      title: 'Nejnovější insighty',
      subtitle: 'Tipy a trendy ze světa marketingu',
      readMore: 'Číst více',
      recentPosts: 'Nejnovější články',
    },
    certifications: {
      title: 'Certifikace',
    },
    contact: {
      title: 'Kontaktujte mě',
      subtitle: 'Připraveni začít váš další projekt? Pojďme mluvit!',
      name: 'Celé jméno',
      email: 'E-mailová adresa',
      company: 'Společnost',
      subject: 'Předmět',
      message: 'Zpráva',
      budget: 'Rozpočet projektu',
      submit: 'Odeslat zprávu',
      success: 'Děkuji! Vaše zpráva byla úspěšně odeslána.',
      error: 'Něco se pokazilo. Zkuste to prosím znovu.',
      required: 'Povinné pole',
    },
    footer: {
      copyright: '© {year} Portfolio. Všechna práva vyhrazena.',
      social: 'Sociální sítě',
      links: {
        privacy: 'Zásady ochrany osobních údajů',
        terms: 'Obchodní podmínky',
      },
    },
    common: {
      learnMore: 'Další informace',
      viewAll: 'Zobrazit vše',
      loading: 'Načítání...',
      error: 'Došlo k chybě',
      back: 'Zpět',
      next: 'Další',
      previous: 'Předchozí',
      search: 'Hledat',
      filter: 'Filtrovat',
    },
    meta: {
      description:
        'Portfolio marketingového a AI specialisty ukazující odbornost v růstových strategiích, kreativním designu a řešeních AI automatizace',
      keywords:
        'Marketing, AI, Růstová strategie, Automatizace, Funnely, Generování leadů, Portfolio',
    },
  },
};

export function getLangFromUrl(url: URL | string): Language {
  const pathname = typeof url === 'string' ? url : url.pathname;
  return pathname.startsWith('/cs') ? 'cs' : 'en';
}

export function getPathWithoutLocale(url: string): string {
  if (url.startsWith('/cs')) {
    return url.replace('/cs', '') || '/';
  }
  return url;
}

export function getAlternateLocaleUrl(currentPath: string, targetLang: Language): string {
  if (targetLang === 'cs') {
    return `/cs${currentPath}`;
  }
  return currentPath.replace('/cs', '') || '/';
}
