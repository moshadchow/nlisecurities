# Role and Expertise

Act as a Senior UI/UX Designer, Frontend Architect, and Full-Stack Software Engineer specializing in production-grade financial websites, stock market platforms, and responsive web applications.

Your responsibility is to redesign the existing website with a professional visual theme, modern layout, improved readability, and an excellent user experience while preserving all existing backend functionality.

# 1. Objective

Transform the existing website's theme, design, and layout into a polished, production-grade financial market platform.

The redesigned website must provide:
- A professional and consistent visual identity.
- Clear typography and readable content.
- Well-organized page layouts.
- A logical visual hierarchy.
- Consistent spacing, alignment, and component sizing.
- Responsive layouts across desktop, laptop, tablet, and mobile.
- Clear and accessible market data tables, cards, forms, and navigation.
- Excellent usability without unnecessary visual complexity.

**Critical requirement:** All existing content must remain clearly visible and readable against the redesigned theme. No content should become hidden, clipped, overlapped, obscured, or difficult to read because of styling or layout changes.

# 2. Analyze the Existing Project

Before modifying any code, inspect the existing codebase.

Identify:
- Frontend framework and architecture.
- Existing page layouts and routing.
- Global CSS, theme configuration, and design tokens.
- Header, navigation, hero banner, and footer.
- Market data tables and indicators.
- Cards, forms, buttons, dialogs, and other UI components.
- Existing responsive breakpoints.
- API clients and data-fetching components.
- Existing loading, error, and empty states.
- Current component dependencies and reusable UI elements.

Understand how the existing frontend communicates with the backend before making any changes.

Prepare a focused implementation plan based on the actual codebase. Do not assume technologies or introduce a new architecture unnecessarily.

# 3. Production-Grade Design System

Create a consistent design system suitable for a professional securities company and financial market website.

## Color Palette

Choose a coordinated palette with:
- A professional primary brand color.
- Appropriate secondary and accent colors.
- Clear page and component backgrounds.
- Readable foreground and muted text colors.
- Consistent border and divider colors.
- Distinct positive, negative, warning, and informational states.

Use green for positive market movements and red for negative movements where appropriate. Use a neutral color for unchanged values.

Ensure sufficient contrast between text, backgrounds, borders, and interactive elements.

Do not apply colors arbitrarily or introduce inconsistent color combinations across different pages.

## Typography

Establish a consistent typography hierarchy for:
- Page titles.
- Section headings.
- Subheadings.
- Body text.
- Table headers and values.
- Labels and helper text.
- Buttons and navigation items.
- Financial figures and market indicators.

Use appropriate font sizes, weights, and line heights.

Avoid text that is too small, too faint, too tightly spaced, or difficult to read.

## Spacing and Alignment

Use a consistent spacing system throughout the application.

Ensure:
- Components align correctly.
- Content containers use available screen space efficiently.
- Cards have consistent padding.
- Sections have appropriate separation.
- Tables are not unnecessarily compressed.
- No excessive whitespace wastes valuable screen space.
- No content is crowded or visually cluttered.

# 4. Landing Page Layout

Redesign the landing page with a clear hierarchy that emphasizes the website's primary purpose: providing financial market information.

Maintain the following component order:

1. Header and navigation.
2. Existing hero banner.
3. DSE and CSE index tables.
4. Advance, Decline, and Unchanged market indicators.
5. Remaining market information and other existing landing page content.

The DSE/CSE index tables and market breadth indicators must appear immediately below the hero banner.

## First-Viewport Visibility

On standard desktop and laptop screens:
- Keep the header compact.
- Preserve the hero banner while optimizing its height where necessary.
- Display the DSE and CSE index tables prominently below the hero banner.
- Keep Advance, Decline, and Unchanged indicators visible alongside or directly adjacent to the index tables.
- Make primary market information accessible immediately without scrolling.

Do not insert unrelated promotional content between the hero banner and the market overview.

Optimize component dimensions and spacing to use the initial viewport efficiently without sacrificing readability.

On smaller screens, prioritize access to the primary market information and use appropriate responsive layouts.

# 5. Improve All Existing UI Components

Apply the new design consistently across the entire website.

Review and improve the following components wherever they exist:

## Header and Navigation
- Logo sizing and alignment.
- Navigation spacing and hierarchy.
- Menu interactions.
- Active and hover states.
- Mobile navigation.
- Header height and responsiveness.

## Hero Banner
- Text readability.
- Image positioning and scaling.
- Appropriate height and spacing.
- Responsive behavior.
- Visual consistency with the overall theme.

Preserve existing hero content and functionality.

## Market Data Tables
- Clear column headings.
- Consistent alignment of financial values.
- Appropriate numeric formatting.
- Readable row spacing.
- Subtle borders and separators.
- Positive, negative, and unchanged indicators.
- Responsive horizontal scrolling where necessary.
- Clear loading, empty, and error states.

Do not introduce hardcoded market data or change existing calculations.

## Cards and Indicators
- Consistent card dimensions and padding.
- Clear labels and values.
- Appropriate visual emphasis.
- Consistent borders, backgrounds, and typography.
- Responsive stacking and alignment.

## Forms and Interactive Elements
- Readable labels and placeholders.
- Clear validation messages.
- Consistent button styling.
- Visible focus states.
- Appropriate disabled and loading states.
- Accessible interaction behavior.

## Remaining Content
Apply the same visual standards to every existing section, including informational content, promotional sections, service descriptions, notices, and the footer.

Preserve existing content unless a visual restructuring is necessary.

# 6. Content Visibility and Readability

This is a mandatory requirement across the entire website.

Ensure that:
- Text contrasts sufficiently with its background.
- No text is obscured by images or decorative elements.
- No components overlap.
- No headings or values are unintentionally clipped.
- No buttons or controls extend beyond their containers.
- No table columns become unreadable.
- No content is hidden behind fixed or sticky headers.
- No important information disappears at smaller viewport sizes.
- Long content wraps or scrolls appropriately.
- Images scale without distorting their aspect ratios.
- Dialogs and dropdown menus remain within the visible viewport.

Avoid fixed heights on content containers when they could clip text or dynamic data.

Use flexible layouts, appropriate minimum heights, and responsive sizing.

If a section contains more information than can reasonably fit in its available space, provide an appropriate scrolling or expansion mechanism rather than silently hiding the content.

**Do not interpret a clean design as permission to remove, truncate, or conceal existing content.**

# 7. Responsive Design

Ensure the redesigned website works across desktop monitors, laptops, tablets, and mobile phones.

### Desktop and Laptop
- Use screen space efficiently.
- Maintain consistent content widths.
- Prioritize visibility of market data.
- Keep tables readable without unnecessary compression.

### Tablet
- Adapt grids and column layouts.
- Adjust spacing and typography.
- Prevent component overlap.
- Preserve access to essential market information.

### Mobile
- Use a compact navigation layout.
- Stack cards and indicators where appropriate.
- Keep text readable.
- Use horizontal scrolling inside wide tables when necessary.
- Ensure controls have adequate touch targets.
- Prevent unintended horizontal scrolling of the entire page.
- Keep essential market information near the top.

Test representative viewport sizes rather than relying exclusively on CSS assumptions.

# 8. Backend and Functional Preservation

**This is a frontend redesign only. Do not modify backend functionality.**

The following requirements are mandatory:

1. Do not modify backend source code.
2. Do not modify API endpoints, HTTP methods, or request/response contracts.
3. Do not modify database schemas, models, or migrations.
4. Do not change authentication or authorization logic.
5. Do not change existing business rules or calculations.
6. Do not change market data processing logic.
7. Do not replace existing API responses with mock data.
8. Do not remove existing API integrations.
9. Do not change environment variables or deployment configuration unnecessarily.
10. Do not modify backend services merely to accommodate a frontend styling preference.

Preserve existing API clients, data-fetching logic, state management, event handlers, and application behavior.

Restrict changes to frontend presentation, layout, styling, and component structure wherever possible.

If an existing component combines presentation and business logic, refactor it only when necessary and preserve its behavior exactly.

Before changing a component, understand its responsibilities and dependencies.

# 9. Performance, Accessibility, and Maintainability

## Performance
- Avoid unnecessary dependencies.
- Avoid excessive animations and expensive visual effects.
- Reuse existing components and assets.
- Avoid unnecessary component re-renders.
- Keep primary market information responsive.
- Avoid introducing large libraries for simple styling requirements.

## Accessibility
- Use semantic HTML.
- Maintain sufficient contrast.
- Provide visible keyboard-focus indicators.
- Ensure keyboard navigation works correctly.
- Use accessible labels for interactive controls.
- Provide appropriate table headers.
- Do not communicate market movement through color alone.

## Maintainability
- Follow the existing project architecture.
- Reuse existing styling conventions.
- Centralize shared design tokens where appropriate.
- Avoid duplicate CSS and conflicting style rules.
- Remove obsolete frontend styles only after confirming they are no longer used.
- Keep the implementation easy to understand and maintain.

# 10. Implementation Workflow

Follow these steps in order.

### Phase 1: Inspect
Analyze the existing frontend and identify the files responsible for the theme, layout, and components.

### Phase 2: Plan
Determine the minimum set of changes required to achieve the redesign without affecting backend behavior.

### Phase 3: Implement
Update the theme, typography, spacing, page layout, tables, cards, and responsive behavior.

### Phase 4: Validate
Run the available frontend checks and inspect the rendered website.

Verify:
- The application builds successfully.
- Existing navigation continues to work.
- API requests and responses remain unchanged.
- Market data displays correctly.
- Forms and interactive elements remain functional.
- No content is clipped or obscured.
- The first-viewport layout meets the market visibility requirements.
- The website works at desktop, tablet, and mobile sizes.

### Phase 5: Refine
Inspect the actual rendered pages and correct any visual inconsistencies, readability problems, spacing issues, or responsive defects.

Do not stop after modifying CSS or successfully compiling the project. Verify the rendered result.

# 11. Definition of Done

The redesign is complete only when:

- [ ] The website has a consistent, professional, production-grade theme.
- [ ] All existing pages use a coherent visual design.
- [ ] All existing content remains present and readable.
- [ ] No content is unintentionally clipped, hidden, or overlapped.
- [ ] Typography, spacing, colors, and alignment are consistent.
- [ ] The DSE and CSE index tables appear immediately below the hero banner.
- [ ] Advance, Decline, and Unchanged indicators are clearly visible near the index tables.
- [ ] Primary market information is visible in the initial desktop/laptop viewport without scrolling.
- [ ] Responsive layouts work correctly.
- [ ] Existing frontend interactions continue to work.
- [ ] Backend source code remains unchanged.
- [ ] API contracts, database structures, and business logic remain unchanged.
- [ ] No unnecessary dependencies have been introduced.
- [ ] Available frontend builds and tests pass.
- [ ] The rendered website has been visually inspected.

# 12. Final Report

After completing the implementation, provide:

1. A summary of the design and layout improvements.
2. The main visual changes made across the website.
3. How content visibility and readability were improved.
4. The files modified or created.
5. Confirmation that backend source code was not changed.
6. Confirmation that existing API contracts and business logic were preserved.
7. Build, test, and visual verification results.
8. Any remaining issues or limitations.

# Final Instruction

Redesign the existing website into a polished, production-grade financial platform with a consistent theme, professional layout, clear typography, and excellent readability.

Preserve all existing content and functionality. Ensure the DSE/CSE index tables and Advance, Decline, and Unchanged indicators appear immediately below the hero banner and are visible in the initial desktop/laptop viewport.

**Make the necessary frontend changes directly in the existing project. Do not modify the backend, database, API contracts, or business logic. Verify the final rendered website before reporting completion.**