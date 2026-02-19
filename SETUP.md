# Setup Guide

This guide will help you set up the marketing portfolio project for development.

## Prerequisites

Before you begin, ensure you have:

- **Node.js 20+** - [Download](https://nodejs.org/) (LTS version recommended)
- **npm** or **pnpm** - Comes with Node.js installation
- **Git** - [Download](https://git-scm.com/) for version control

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/pkoka888/marketing.tvoje.info.git
cd marketing.tvoje.info
```

## Step 2: Install Dependencies

```bash
# Install dependencies using npm
npm install

# OR using pnpm
pnpm install
```

## Step 3: Configure Environment Variables

1. Copy the environment template:

   ```bash
   copy .env.template .env
   ```

2. Edit the `.env` file and update the following variables:
   - `PROJECT_NAME`: Your project name (e.g., marketing-tvoje.info)
   - `PUBLIC_SITE_URL`: Your public site URL (e.g., https://portfolio.tvoje.info)
   - `FORMSPREE_ENDPOINT`: Your Formspree form endpoint (optional)
   - `PLAUSIBLE_API_KEY`: Your Plausible analytics API key (optional)

3. Save the `.env` file

## Step 4: Start Development Server

```bash
# Start the development server
npm run dev

# The site will be available at http://localhost:4321
```

## Available Commands

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
││      ├── common/     # Common components (Header, Footer)
││      ├── sections/  # Section components (Hero, About, Projects)
││      └── ui/         # UI primitives (Button, Card, Badge)
│   ├── layouts/        # Page layouts
│   ├── pages/          # Astro pages (routing)
││      ├── cs/         # Czech language pages
││      └── projects/  # Project detail pages
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

**NOTE: Vercel deployment is DISABLED. See docs/DEPLOYMENT.md for VPS deployment.**

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
│ ├── common/ # Common components (Header, Footer)
│ │ ├── sections/ # Section components (Hero, About, Projects)
│ │ └── ui/ # UI primitives (Button, Card, Badge)
│ ├── layouts/ # Page layouts
│ ├── pages/ # Astro pages (routing)
│ │ ├── cs/ # Czech language pages
│ │ └── projects/ # Project detail pages
│ ├── styles/ # Global styles
│ ├── i18n/ # Internationalization
│ ├── content/ # MDX content (projects)
│ └── layouts/ # Layout components
├── public/ # Static assets
├── tests/ # Test files
├── plans/ # Planning documents
└── .github/
└── workflows/ # GitHub Actions

```

## Deployment

This project automatically deploys to Vercel:

- **Preview**: Deploys on every PR
- **Production**: Deploys on push to main branch

**NOTE: Vercel deployment is DISABLED. See docs/DEPLOYMENT.md for VPS deployment.**

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
```
