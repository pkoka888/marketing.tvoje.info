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
      devops: string;
      ai: string;
      web: string;
      infrastructure: string;
    };
  };
  services: {
    title: string;
    subtitle: string;
    devops: {
      title: string;
      description: string;
      items: string[];
    };
    ai: {
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
      title: 'DevOps & AI Developer',
      subtitle: 'Building scalable solutions with automation and artificial intelligence',
      cta: 'View Projects',
      secondaryCta: 'Get in Touch',
    },
    about: {
      title: 'About Me',
      bio: `I'm a passionate DevOps and AI Developer with over 5 years of experience in building scalable, automated infrastructure solutions. My expertise lies in bridging the gap between development and operations, implementing CI/CD pipelines, and integrating AI solutions into existing workflows.\n\nI believe in the power of automation to transform businesses and am dedicated to helping organizations achieve operational excellence through modern DevOps practices and AI-powered solutions.`,
      skills: 'Technical Skills',
      certifications: 'Certifications',
      downloadCV: 'Download CV',
    },
    projects: {
      title: 'Featured Projects',
      description: 'A selection of projects demonstrating expertise in DevOps, AI, and cloud infrastructure',
      viewDetails: 'View Details',
      categories: {
        all: 'All Projects',
        devops: 'DevOps',
        ai: 'AI & ML',
        web: 'Web Development',
        infrastructure: 'Infrastructure',
      },
    },
    services: {
      title: 'Services',
      subtitle: 'How I can help your business grow',
      devops: {
        title: 'DevOps & Automation',
        description: 'Transform your development workflow with modern DevOps practices',
        items: [
          'CI/CD Pipeline Implementation',
          'Infrastructure as Code',
          'Container orchestration with Kubernetes',
          'Cloud architecture design',
          'Monitoring & observability',
        ],
      },
      ai: {
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
    contact: {
      title: 'Get in Touch',
      subtitle: 'Ready to start your next project? Let\'s talk!',
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
      description: 'DevOps & AI Developer portfolio showcasing expertise in automation, cloud infrastructure, and artificial intelligence solutions',
      keywords: 'DevOps, AI, Machine Learning, Cloud Architecture, Automation, CI/CD, Kubernetes, Portfolio',
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
      title: 'DevOps & AI Vývojář',
      subtitle: 'Vytvářím škálovatelná řešení s automatizací a umělou inteligencí',
      cta: 'Zobrazit projekty',
      secondaryCta: 'Kontaktovat',
    },
    about: {
      title: 'O mně',
      bio: `Jsem nadšený DevOps a AI vývojář s více než 5 lety zkušeností v budování škálovatelných, automatizovaných infrastrukturních řešení. Moje specializace spočívá v překlenutí propasti mezi vývojem a provozem, implementaci CI/CD pipeline a integraci AI řešení do stávajících pracovních postupů.\n\nVěřím v sílu automatizace, která dokáže transformovat podniky, a jsem odhodlan pomáhat organizacím dosáhnout provozní dokonalosti pomocí moderních DevOps postupů a AI řešení.`,
      skills: 'Technické dovednosti',
      certifications: 'Certifikace',
      downloadCV: 'Stáhnout životopis',
    },
    projects: {
      title: 'Vybrané projekty',
      description: 'Výběr projektů demonstrujících odbornost v DevOps, AI a cloud infrastruktuře',
      viewDetails: 'Zobrazit detaily',
      categories: {
        all: 'Všechny projekty',
        devops: 'DevOps',
        ai: 'AI & ML',
        web: 'Webový vývoj',
        infrastructure: 'Infrastruktura',
      },
    },
    services: {
      title: 'Služby',
      subtitle: 'Jak mohu pomoci vašemu podnikání růst',
      devops: {
        title: 'DevOps & Automatizace',
        description: 'Transformujte svůj vývojový workflow pomocí moderních DevOps postupů',
        items: [
          'Implementace CI/CD pipeline',
          'Infrastructure as Code',
          'Orchestrace kontejnerů s Kubernetes',
          'Návrh cloud architektury',
          'Monitoring a pozorovatelnost',
        ],
      },
      ai: {
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
      description: 'DevOps & AI vývojářské portfolio ukazující odbornost v automatizaci, cloud infrastruktuře a řešeních umělé inteligence',
      keywords: 'DevOps, AI, Strojové učení, Cloud architektura, Automatizace, CI/CD, Kubernetes, Portfolio',
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
