<task name="Implement Portfolio Section">

<task_objective>
Implement a new section for the Marketing Portfolio website following project conventions.
</task_objective>

<detailed_sequence_steps>
## Step 1: Analyze Requirements
1. read_file the task requirements to understand what section is being implemented
2. Review PRD.md for section specifications
3. Check existing similar sections in src/components/sections/
4. Review bilingual requirements in .clinerules/i18n-content.md
5. Check accessibility requirements in .clinerules/accessibility-rules.md

## Step 2: Prepare Component Structure
1. Create the Astro component file in src/components/sections/
2. Create the component following the structure:
   ```astro
   ---
   import type { Props } from '../types';
   interface Props {
     lang: 'cs' | 'en';
   }
   const { lang } = Astro.props;
   ---
   <section id="section-id" class="py-16 md:py-24">
     <!-- Content -->
   </section>
   ```
3. Add to src/components/index.ts exports

## Step 3: Add Translations
1. Add translation keys to src/i18n/translations.ts
2. Include both cs and en translations
3. Verify all text is in translation file, not hardcoded

## Step 4: Implement with Tailwind
1. Use semantic HTML structure
2. Apply Tailwind classes from .clinerules/tailwind-css.md
3. Ensure responsive design (mobile-first)
4. Add dark mode support with dark: classes

## Step 5: Accessibility Implementation
1. Add ARIA labels where needed
2. Include skip links if section is major
3. Ensure keyboard navigation works
4. Add proper heading hierarchy (h2, h3, etc.)
5. Add alt text for images
6. Test color contrast ratios

## Step 6: Add to Pages
1. Import and use component in src/pages/index.astro (EN)
2. Import and use component in src/pages/cs/index.astro (CS)
3. Pass lang prop correctly

## Step 7: Test
1. Verify component renders in both languages
2. Check responsive layout
3. Test keyboard navigation
4. Verify accessibility with axe DevTools
5. Check Lighthouse performance impact

## Step 8: Document
1. Add section description to Memory Bank context.md
2. Update relevant documentation if needed
</detailed_sequence_steps>

</task>
