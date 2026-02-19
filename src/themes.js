// Theme definitions for the portfolio website
export const themes = {
  titan: {
    id: 'titan',
    name: { en: 'Titan', cs: 'Titan' },
    desc: { en: 'Direct, professional look', cs: 'Přímý, profesionální vzhled' },
    color: '#4285F4',
    gradient: 'linear-gradient(135deg, #4285F4, #0ea5e9)',
    cssVars: {
      '--theme-primary': '#4285F4',
      '--theme-secondary': '#0ea5e9',
      '--theme-accent': '#FBBC05',
      '--theme-bg': '#ffffff',
      '--theme-text': '#1f2937',
    },
  },
  nova: {
    id: 'nova',
    name: { en: 'Nova', cs: 'Nova' },
    desc: { en: 'Friendly and modern', cs: 'Přátelský a moderní' },
    color: '#6366F1',
    gradient: 'linear-gradient(135deg, #6366F1, #22D3EE)',
    cssVars: {
      '--theme-primary': '#6366F1',
      '--theme-secondary': '#22D3EE',
      '--theme-accent': '#F59E0B',
      '--theme-bg': '#ffffff',
      '--theme-text': '#1f2937',
    },
  },
  target: {
    id: 'target',
    name: { en: 'Target', cs: 'Cíl' },
    desc: { en: 'Focused and goal-oriented', cs: 'Zaměřený a cílevědomý' },
    color: '#EF4444',
    gradient: 'linear-gradient(135deg, #EF4444, #F97316)',
    cssVars: {
      '--theme-primary': '#EF4444',
      '--theme-secondary': '#F97316',
      '--theme-accent': '#10B981',
      '--theme-bg': '#ffffff',
      '--theme-text': '#1f2937',
    },
  },
  spark: {
    id: 'spark',
    name: { en: 'Spark', cs: 'Jiskra' },
    desc: { en: 'Energetic and creative', cs: 'Energetický a kreativní' },
    color: '#F59E0B',
    gradient: 'linear-gradient(135deg, #F59E0B, #EF4444)',
    cssVars: {
      '--theme-primary': '#F59E0B',
      '--theme-secondary': '#EF4444',
      '--theme-accent': '#8B5CF6',
      '--theme-bg': '#ffffff',
      '--theme-text': '#1f2937',
    },
  },
  lux: {
    id: 'lux',
    name: { en: 'Lux', cs: 'Lux' },
    desc: { en: 'Elegant and sophisticated', cs: 'Elegantní a sofistikovaný' },
    color: '#8B5CF6',
    gradient: 'linear-gradient(135deg, #8B5CF6, #EC4899)',
    cssVars: {
      '--theme-primary': '#8B5CF6',
      '--theme-secondary': '#EC4899',
      '--theme-accent': '#06B6D4',
      '--theme-bg': '#ffffff',
      '--theme-text': '#1f2937',
    },
  },
  obsidian: {
    id: 'obsidian',
    name: { en: 'Obsidian', cs: 'Obsidián' },
    desc: { en: 'Dark and mysterious', cs: 'Tmavý a záhadný' },
    color: '#1F2937',
    gradient: 'linear-gradient(135deg, #1F2937, #374151)',
    cssVars: {
      '--theme-primary': '#1F2937',
      '--theme-secondary': '#374151',
      '--theme-accent': '#F59E0B',
      '--theme-bg': '#1f2937',
      '--theme-text': '#f9fafb',
    },
  },
  playful: {
    id: 'playful',
    name: { en: 'Playful', cs: 'Hravý' },
    desc: { en: 'Fun and engaging', cs: 'Zábavný a poutavý' },
    color: '#EC4899',
    gradient: 'linear-gradient(135deg, #EC4899, #F97316)',
    cssVars: {
      '--theme-primary': '#EC4899',
      '--theme-secondary': '#F97316',
      '--theme-accent': '#10B981',
      '--theme-bg': '#ffffff',
      '--theme-text': '#1f2937',
    },
  },
  neon: {
    id: 'neon',
    name: { en: 'Neon', cs: 'Neon' },
    desc: { en: 'Cyberpunk glow effects', cs: 'Cyberpunkové efekty' },
    color: '#00f0ff',
    gradient: 'linear-gradient(135deg, #00f0ff, #ff00ff)',
    cssVars: {
      '--theme-primary': '#00f0ff',
      '--theme-secondary': '#ff00ff',
      '--theme-accent': '#00ff88',
      '--theme-bg': '#0a0a0f',
      '--theme-text': '#e0e0e0',
    },
  },
};

// Helper function to get theme by ID
export function getTheme(id) {
  return themes[id] || themes.titan; // fallback to titan
}

// Helper function to get all themes as array
export function getThemesArray(lang = 'en') {
  return Object.values(themes).map((theme) => ({
    id: theme.id,
    name: theme.name[lang] || theme.name.en,
    desc: theme.desc[lang] || theme.desc.en,
    color: theme.color,
    gradient: theme.gradient,
  }));
}
