# Open Questions Deep-Dive Research

**Phase**: 7 (Deep-Dive Research)
**Status**: In Progress

This document contains the research and analysis for the "Open Questions" identified in the initial `research-log.md`. The questions are grouped by topic for clarity.

---

## Group 1: Technology Stack

This section addresses the technical questions related to the choice of static site generator, hosting, and internationalization (i18n).

### Tech Q1: Which static site generator offers the best balance of performance and ease of use?

**Analysis:**
The Static Site Generator (SSG) market in 2026 is mature, with clear leaders for different use cases.

- **For Raw Speed:** **Hugo** (Go-based) and **Zola** (Rust-based) are consistently ranked as the fastest, capable of building thousands of pages in seconds. They are ideal for massive, content-heavy sites where build time is a critical factor.
- **For Modern Features & Performance:** **Astro** stands out significantly. Its "islands architecture" ships minimal to zero JavaScript by default, resulting in exceptionally fast page loads and high Lighthouse scores. It is considered a top choice for content-focused sites like blogs, marketing pages, and portfolios.
- **For Ease of Use & Flexibility:** **Eleventy (11ty)** is highly praised for its simplicity and flexibility, allowing developers to use various templating languages. It has a minimal core and is easy to learn.
- **For Full-Stack Applications:** **Next.js** (React) and **SvelteKit** (Svelte) are powerful frameworks that offer static site generation but are more geared towards complex, dynamic web applications. They tend to ship more client-side JavaScript than Astro, making them less optimal for purely static, performance-focused sites.

**Conclusion:**
For this project (a marketing portfolio), **Astro is an optimal choice**. It provides an excellent balance of top-tier performance, a modern developer experience with component-based architecture, and a strong focus on content-driven websites. The project's current use of Astro is well-justified.

---

### Tech Q2: What hosting platform provides the best value for the Czech market?

**Analysis:**
The choice of hosting platform depends heavily on control requirements, DevOps expertise, and data residency needs. The user has clarified that they are deploying to their own **VPS server via GitHub Actions**.

- **Self-Hosted VPS (User's Setup):**
  - **Pros:** Offers maximum control over the environment, allowing for highly customized configurations, fine-tuned performance optimizations, and strict adherence to data residency requirements (if the VPS is located in the Czech Republic). Leveraging GitHub Actions for CI/CD provides a robust and automated deployment pipeline, showcasing DevOps expertise. This setup can be very cost-effective for high-traffic sites if managed efficiently.
  - **Cons:** Requires significant DevOps expertise for setup, maintenance, security, and scaling. The user is responsible for managing the server, including updates, backups, and security patches. Initial setup time can be higher than with managed platforms.

- **Global Platforms (Vercel, Netlify):**
  - **Pros:** Superior developer experience with integrated Git-based CI/CD, global CDN for fast content delivery worldwide (crucial for a bilingual CS/EN site), automatic HTTPS, and preview deployments. Excellent for rapid iteration and minimal maintenance overhead.
  - **Cons:** Less control over the underlying infrastructure. Data is distributed globally, which may not meet strict EU/Czech data residency requirements. Pricing is usage-based, which can be less predictable.

- **Local Czech Hosting (e.g., Wedos, Forpsi, Coolhousing):**
  - **Pros:** Primary advantage is guaranteed **data residency** within the Czech Republic, compliant with local/EU regulations. Can offer competitive fixed pricing.
  - **Cons:** Generally lack the integrated CI/CD and global CDN capabilities of Vercel/Netlify. Requires more manual DevOps work. Global performance for the English-speaking audience might be slower without a separate CDN.

**Conclusion:**
The user's current setup of a **self-hosted VPS with GitHub Actions for deployment represents an excellent and highly capable solution.** This approach offers maximum control, can ensure data residency (if the VPS is located in the Czech Republic), and perfectly showcases advanced DevOps expertise. While managed platforms like Vercel offer convenience, the user's current setup provides superior flexibility and aligns with the project's technical depth. Therefore, continuing with the current VPS + GitHub Actions deployment is highly recommended.

---

### Tech Q3: How to implement bilingual support effectively?

**Analysis:**
While the specific search for Astro i18n failed, modern SSGs, including Astro, have robust support for internationalization (i18n). The standard approach is using file-based routing.

- **Directory Structure:** Content is organized into language-specific directories. For example:
  - `src/pages/cs/` for Czech pages.
  - `src/pages/en/` for English pages.
- **Routing:** Astro will automatically generate the routes based on this structure, leading to URLs like `example.com/cs/o-nas` and `example.com/en/about`.
- **UI Translations:** For shared components (like headers and footers), a "dictionary" or translation map is used. You would create JSON or JS objects for each language containing the translated strings.
  ```javascript
  // src/i18n/ui.js
  export const ui = {
    en: { 'nav.home': 'Home' },
    cs: { 'nav.home': 'Domů' },
  };
  ```
  A utility function would then retrieve the correct string based on the current page's language.

**Conclusion:**
Astro natively supports i18n through its routing and allows for flexible implementation of UI translation management. The official Astro documentation provides detailed guides on setting this up effectively.

---

## Group 2: SEO & Compliance

This section addresses GDPR, cookie consent, and search engine optimization for the Czech market.

### Tech Q4: What are the GDPR compliance requirements?

**Analysis:**
For a portfolio website, the key GDPR requirements are:

- **Lawful & Transparent Data Collection:** Only collect data you absolutely need (e.g., for a contact form). Clearly explain in a privacy policy what you collect, why, and for how long.
- **Data Minimization:** Do not ask for more information than is necessary. A contact form should not ask for a home address, for example.
- **Cookie Consent:** This is the most visible requirement. Before you load any non-essential cookies or trackers (like Google Analytics, Meta Pixel, etc.), you must get explicit, opt-in consent from the user.
- **Cookie Banner Requirements (Czech Republic):**
  - The consent must be an active "opt-in". Implied consent ("by using this site, you agree...") is not valid.
  - The "Reject All" option must be as easy to access as the "Accept All" option.
  - "Cookie walls" that block access to the site before consent is given are illegal.
  - Granular control must be provided, allowing users to consent to some cookie categories (e.g., Analytics) but not others (e.g., Marketing).
- **User Rights:** You must have a process to handle user requests to access, rectify, or delete their personal data.
- **Security:** The website must be secure (use HTTPS) to protect any data transmitted.

**Conclusion:**
A portfolio site must have a clear **Privacy Policy**, an **explicit opt-in Cookie Banner**, and a simple way for users to contact the owner to request data actions. The use of any analytics or marketing trackers requires prior consent.

---

### Tech Q5: How to optimize for both Google.cz and Seznam.cz?

**Analysis:**
While both search engines value high-quality content and user experience, they have different priorities.

- **Google:** Focuses on sophisticated signals like Core Web Vitals, user intent, semantic context, and the quality/relevance of backlinks. It has a global context but delivers localized results.
- **Seznam:** Is intensely focused on the Czech market. Its ranking factors are more traditional and place a heavy emphasis on:
  - **Czech Language & Domain:** It strongly favors `.cz` domains and high-quality, natural-sounding Czech content.
  - **Keywords:** Relies more on the presence of exact-match Czech keywords in titles, headings, and body text compared to Google's more semantic understanding.
  - **Local Ecosystem:** A major ranking signal is integration with Seznam's own services. Creating a profile on **`Firmy.cz`** (business directory) is considered essential for local SEO. If applicable, using `Mapy.cz` and `Zbozi.cz` also provides strong positive signals.
  - **Backlinks:** While quality is a factor, Seznam's algorithm appears to be more influenced by the _quantity_ of backlinks from other Czech domains than Google's.

**Conclusion:**
A dual SEO strategy is required:

1.  **For Google:** Focus on technical excellence (performance, mobile-friendliness), high-quality content that satisfies user intent, and earning quality backlinks.
2.  **For Seznam:**
    - Ensure the primary version of the site is in flawless Czech on a `.cz` domain if possible.
    - Create and fully optimize a **`Firmy.cz`** profile.
    - Perform specific keyword research for Czech phrases and ensure they are used naturally in titles, headings, and content.
    - Build a backlink profile with a focus on acquiring links from other relevant Czech websites.

---

## Group 3: Business & Market

This section addresses questions related to pricing, trust, and measuring success in the Czech market.

### Business Q1: What is the optimal pricing strategy for the Czech market?

**Analysis:**
The freelance developer market in the Czech Republic is competitive. An effective pricing strategy should blend market rates with value-provided.

- **Market Rates:** Average hourly rates are around **$50/hour**, typically falling within a **$35-$100/hour** range based on experience and specific tech skills.
- **Pricing Models:**
  - **Hourly:** Best for consulting or projects with undefined scopes.
  - **Project-Based:** Preferred by clients for well-defined deliverables like a standard portfolio website or e-shop.
  - **Value-Based:** Can yield higher income but requires demonstrating a clear, significant impact on the client's business goals.
- **Local Costs:** As a freelancer (OSVČ), you must account for a 15-23% income tax, social/health insurance contributions, and a 21% VAT if applicable.

**Conclusion:**
A hybrid strategy is recommended. Define **fixed-price packages** for common, well-scoped projects (e.g., "Basic Portfolio Site," "Small E-shop"). For custom development, consultations, or ongoing work, use an **hourly rate** benchmarked against your experience (e.g., starting at $50/hr and increasing with proven expertise).

---

### Business Q2: Which trust indicators are most valued by Czech businesses?

**Analysis:**
Trust is paramount, especially in e-commerce and B2B services. Key indicators for the Czech market include:

- **Transparency:** Complete and easily verifiable company information (IČO, business name, address, contact details) is a baseline expectation.
- **Legal Compliance:** Clear, accessible Terms and Conditions and a GDPR-compliant privacy policy are mandatory.
- **Security:** A secure connection (HTTPS/SSL) is non-negotiable.
- **Social Proof:** Customer reviews, testimonials, and case studies are highly influential. Displaying logos of well-known clients is very effective.
- **Professionalism:** A high-quality, modern website design that is free of errors and performs well builds significant credibility.
- **Certifications:** Official certifications (e.g., "Bezpečný nákup") or membership in business associations like APEK (Association for Electronic Commerce) are strong trust signals.

**Conclusion:**
For a portfolio site, this means having: a professional design, an SSL certificate, a dedicated page with clear contact and identification details (IČO), a link to a privacy policy, and prominently featuring testimonials and logos from past clients.

---

### Business Q3 & Q4: What is the expected conversion rate, and how can success be measured beyond traffic?

**Analysis:**
Measuring the success of a portfolio website requires looking past simple traffic metrics and focusing on tangible outcomes and user engagement.

- **Conversion Rate:** "Conversion" for a portfolio is typically a lead (e.g., a contact form submission). While the overall website average is ~3.3%, a well-optimized portfolio should aim for a **5-10% conversion rate** on its primary call-to-action (like the contact form).
- **Success Metrics Beyond Traffic:**
  - **Primary Metric: Lead Generation.** The number of qualified inquiries received through the website is the most important measure of success.
  - **Engagement Metrics:** These indicate the quality of the traffic. Key metrics include:
    - **Time on Site:** Higher duration suggests visitors are genuinely interested in your work.
    - **Pages per Visit:** Shows that visitors are exploring multiple projects.
    - **Low Bounce Rate:** Indicates the site meets visitor expectations.
  - **Goal Completions:** Use analytics to track specific, valuable actions, such as "Resume Downloads," clicks on your LinkedIn profile, or video plays on case studies.
  - **Qualitative Metric: Client Acquisition.** The ultimate success metric is the number of paying projects or job offers that originate from the website.

**Conclusion:**
Define clear goals in your analytics tool. The primary KPI should be **leads generated**. Support this with key engagement metrics (Time on Site, Pages per Visit) and specific goal completions (Resume Downloads) to get a holistic view of the portfolio's performance.
