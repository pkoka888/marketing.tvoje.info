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
      title: 'Marketing & Growth Specialist',
      subtitle: 'Building scalable growth strategies with automation and data-driven marketing',
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
      strategy: {
        title: 'Marketing Automation',
        description: 'Transform your customer journey with modern growth automation practices',
        items: [
          'Growth strategy development',
          'Marketing funnel optimization',
          'Lead generation campaigns',
          'Email marketing automation',
          'CRM integration',
        ],
      },
      campaigns: {
        title: 'AI & Machine Learning',
        description: 'Leverage the power of artificial intelligence for your business',
        items: [
          'AI solution integration',
          'Machine learning pipelines',
          'Natural language processing',
          'Computer vision applications',
          'AI-powered automation',
        ],
      },
      consulting: {
        title: 'Technical Consulting',
        description: 'Strategic guidance for your technical initiatives',
        items: [
          'Technology strategy',
          'Team augmentation',
          'Code review & optimization',
          'Best practices implementation',
          'Technical debt assessment',
        ],
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
      title: 'Marketingový a růstový specialista',
      subtitle: 'Buduji škálovatelné růstové strategie s automatizací a datově řízeným marketingem',
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
      strategy: {
        title: 'Marketingová automatizace',
        description:
          'Transformujte svou zákaznickou cestu pomocí moderních postupů růstové automatizace',
        items: [
          'Vývoj růstové strategie',
          'Optimalizace marketingových funnelů',
          'Kampaně na generování leadů',
          'Automatizace e-mailového marketingu',
          'Integrace CRM',
        ],
      },
      campaigns: {
        title: 'AI & Strojové učení',
        description: 'Využijte sílu umělé inteligence pro váš podnik',
        items: [
          'Integrace AI řešení',
          'Strojové učení pipeline',
          'Zpracování přirozeného jazyka',
          'Počítačové vidění aplikace',
          'AI poháněná automatizace',
        ],
      },
      consulting: {
        title: 'Technické konzultace',
        description: 'Strategické vedení pro vaše technické iniciativy',
        items: [
          'Technologická strategie',
          'Augmentace týmu',
          'Revize a optimalizace kódu',
          'Implementace best practices',
          'Hodnocení technického dluhu',
        ],
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
