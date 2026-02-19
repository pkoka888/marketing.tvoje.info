# DevOps & AI Developer Portfolio

Modern, performant portfolio website showcasing DevOps and AI expertise. Built with **Astro 5.0**, **Tailwind CSS 3.4**, and **TypeScript**.

## Features

- 🚀 **Astro 5.0** - Zero-JS by default, island architecture
- 🎨 **Tailwind CSS 4.0** - Utility-first styling with dark mode
- 🌐 **Bilingual** - Full Czech and English support
- ♿ **Accessible** - WCAG 2.2 AA compliant
- 📊 **Performance** - 95+ Lighthouse scores
- 🔒 **Privacy** - GDPR compliant with Plausible analytics
- 🔄 **CI/CD** - Automated testing and deployment

## Tech Stack

| Category  | Technology                      |
| --------- | ------------------------------- |
| Framework | Astro 5.0                       |
| Styling   | Tailwind CSS 3.4                |
| Language  | TypeScript 5.7                  |
| Hosting   | VPS (s60/s61/s62 via Tailscale) |
| Forms     | Formspree                       |
| Analytics | Plausible (privacy-focused)     |
| CI/CD     | GitHub Actions                  |

## Deployment

**Target: VPS (NOT Vercel)**

This project deploys to VPS via GitHub Actions:

- **Build**: `npm run build` (outputs to `dist/`)
- **Deploy**: Push to VPS servers (s60/s61/s62) via Tailscale VPN
- See `docs/DEPLOYMENT.md` for details

- Node.js 20+
- npm or pnpm

### Installation

```bash
# Clone the repository
git clone https://github.com/pkoka888/marketing.tvoje.info.git
cd marketing.tvoje.info

# Install dependencies
npm install

# Start development server
npm run dev
```

## Available Scripts

| Command                | Description               |
| ---------------------- | ------------------------- |
| `npm run dev`          | Start development server  |
| `npm run build`        | Build for production      |
| `npm run preview`      | Preview production build  |
| `npm run lint`         | Run ESLint                |
| `npm run typecheck`    | Run TypeScript checks     |
| `npm run format`       | Format code with Prettier |
| `npm run format:check` | Check code formatting     |

## Project Structure

```
marketing.tvoje.info/
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── common/     # Common components (Header, Footer)
│   │   ├── sections/  # Section components (Hero, About, Projects)
│   │   └── ui/         # UI primitives (Button, Card, Badge)
│   ├── layouts/        # Page layouts
│   ├── pages/          # Astro pages (routing)
│   │   ├── cs/         # Czech language pages
│   │   └── projects/  # Project detail pages
│   ├── styles/         # Global styles
│   ├── i18n/           # Internationalization
│   ├── content/        # MDX content (projects)
│   └── layouts/        # Layout components
├── public/             # Static assets
├── tests/             # Test files
├── plans/             # Planning documents
└── .github/
    └── workflows/     # GitHub Actions
```

## Deployment

This project automatically deploys to Vercel:

- **Preview**: Deploys on every PR
- **Production**: Deploys on push to main branch

## Performance

Target metrics:

- Lighthouse Performance: ≥95
- Lighthouse Accessibility: ≥95
- LCP: <2.5s
- FID: <100ms
- CLS: <0.1

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a PR

## License

MIT License - see LICENSE file for details.
test
