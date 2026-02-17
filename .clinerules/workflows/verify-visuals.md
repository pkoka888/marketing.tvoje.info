---
description: Verify the visual appearance of the site using Playwright.
---

1.  **Start the Dev Server**: Ensure the Astro dev server is running (e.g., `npm run dev` at port 4321).
    - _Note_: If `npm run dev` is already running, reuse the existing instance.
2.  **Navigate & Screenshot**:
    - Use `playwright_navigate` to go to `http://localhost:4321/`.
    - Use `playwright_screenshot` to save `evidence/homepage-light.png`.
    - Use `playwright_evaluate` to toggle theme: `window.setSiteTheme('target')`.
    - Use `playwright_screenshot` to save `evidence/homepage-target.png`.
3.  **Compare**: Check if the screenshots align with expectations.
