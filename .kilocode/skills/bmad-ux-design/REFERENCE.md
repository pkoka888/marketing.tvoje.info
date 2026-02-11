# UX Design Reference

## Core Concepts

### User-Centered Design
- Focus on user needs, goals, and pain points
- Design for the primary user journey first
- Consider edge cases and error states
- Ensure accessibility from the start

### Information Architecture
- Organize content logically and hierarchically
- Use clear, consistent navigation patterns
- Minimize cognitive load
- Support multiple user paths to the same goal

### Responsive Design
- Mobile-first approach
- Progressive enhancement
- Touch-friendly interactions
- Flexible layouts that adapt to content

## Design Patterns

### Navigation Patterns
- **Primary Navigation**: Top-level categories, always visible
- **Secondary Navigation**: Sub-categories, context-dependent
- **Breadcrumbs**: Show user's current location
- **Search**: Prominent when content is extensive
- **Footer Navigation**: Links to important pages and legal

### Layout Patterns
- **Single Column**: Simple content, mobile-first
- **Two Column**: Content + sidebar navigation
- **Three Column**: Navigation + content + sidebar
- **Grid**: Cards, galleries, product listings
- **Hero Section**: Value proposition, call-to-action

### Component Patterns
- **Cards**: Grouped content with consistent structure
- **Modals**: Focused interactions, overlay content
- **Tabs**: Organize related content without navigation
- **Accordions**: Expandable content, progressive disclosure
- **Carousels**: Multiple items, limited horizontal space

## Interaction Design

### User Flows
1. **Discovery**: User finds what they need
2. **Selection**: User chooses an option
3. **Action**: User performs the primary action
4. **Confirmation**: User receives feedback
5. **Return**: User can continue or go back

### State Management
- **Loading**: Show progress, set expectations
- **Success**: Clear confirmation, next steps
- **Error**: Explain what happened, how to fix
- **Empty**: Guide user to content or actions
- **Disabled**: Explain why, when it will be available

### Feedback Mechanisms
- **Immediate**: Button clicks, form submissions
- **Progressive**: Multi-step processes, file uploads
- **Persistent**: Notifications, status indicators
- **Contextual**: Related to the user's action

## Accessibility Standards

### WCAG 2.2 AA Requirements
- **Perceivable**: Content is visible and understandable
- **Operable**: Interface is usable with keyboard and assistive tech
- **Understandable**: Content is clear and predictable
- **Robust**: Works with current and future assistive technologies

### Color Contrast
- **Normal Text**: 4.5:1 minimum
- **Large Text (18pt+)**: 3:1 minimum
- **UI Components**: 3:1 minimum
- **Focus Indicators**: Visible on all backgrounds

### Keyboard Navigation
- **Tab Order**: Logical, follows visual layout
- **Focus Visible**: Clear indicator on all interactive elements
- **Skip Links**: Jump to main content, navigation
- **Shortcuts**: Common actions (search, submit)

### Screen Reader Support
- **Semantic HTML**: Proper use of headings, landmarks
- **ARIA Labels**: Descriptive labels for interactive elements
- **Live Regions**: Dynamic content announcements
- **Alt Text**: Descriptive text for images

## Design System Elements

### Typography
- **Scale**: Consistent hierarchy (H1-H6, body, small)
- **Line Height**: 1.5-1.8 for readability
- **Font Weight**: Regular, medium, bold for emphasis
- **Letter Spacing**: Adjusted for readability at small sizes

### Color Palette
- **Primary**: Main brand color, CTAs, links
- **Secondary**: Supporting elements, less emphasis
- **Neutral**: Backgrounds, borders, text
- **Semantic**: Success (green), error (red), warning (yellow)
- **Accessibility**: All combinations meet contrast ratios

### Spacing
- **Base Unit**: 4px or 8px grid
- **Consistent**: Use multiples of base unit
- **Breathing Room**: Generous whitespace between sections
- **Alignment**: Consistent margins and padding

### Components
- **Buttons**: Primary, secondary, tertiary variants
- **Forms**: Labels, placeholders, validation messages
- **Cards**: Image, title, description, actions
- **Modals**: Header, body, footer, close button
- **Navigation**: Links, dropdowns, breadcrumbs

## Responsive Breakpoints

### Common Breakpoints
- **Mobile**: < 640px (single column, stacked)
- **Tablet**: 640px - 1024px (two columns)
- **Desktop**: > 1024px (multi-column, full features)
- **Large Desktop**: > 1440px (max-width containers)

### Mobile Considerations
- **Touch Targets**: Minimum 44x44px
- **Thumb Zone**: Primary actions in bottom third
- **Simplified**: Hide non-essential content
- **Performance**: Optimize images, minimize scripts

## Validation Methods

### Usability Testing
- **Think Aloud**: Users verbalize thoughts while testing
- **Task Completion**: Measure success rate and time
- **Satisfaction**: Post-test surveys, interviews
- **Observation**: Note confusion, frustration, workarounds

### A/B Testing
- **Hypothesis**: Clear prediction of what will improve
- **Metrics**: Conversion, engagement, satisfaction
- **Sample Size**: Statistically significant results
- **Duration**: Run until confidence is achieved

### Analytics
- **Page Views**: Most and least visited pages
- **Bounce Rate**: Single-page sessions
- **Time on Page**: Engagement indicator
- **Conversion**: Goal completions, form submissions
- **User Flow**: Path analysis, drop-off points

## Common Pitfalls

### Design Issues
- **Too Many Options**: Decision paralysis
- **Hidden Actions**: Users can't find what they need
- **Inconsistent Patterns**: Different interactions for same task
- **Poor Feedback**: Users don't know if action succeeded
- **Accessibility Afterthought**: Retrofitting is expensive

### Technical Issues
- **Performance**: Slow load times, janky animations
- **Broken Layouts**: Elements overlap, content cut off
- **Missing States**: No loading, error, or empty states
- **Browser Incompatibility**: Features don't work everywhere
- **Mobile Issues**: Touch targets too small, content not responsive

## Best Practices

### Design Principles
- **Clarity Over Cleverness**: Obvious is better than clever
- **Consistency**: Same interaction = same result
- **Forgiveness**: Allow undo, easy recovery from errors
- **Efficiency**: Fewest steps to complete tasks
- **Learnability**: New users can use it immediately

### Documentation
- **Design Rationale**: Explain why decisions were made
- **Component Specs**: Detailed implementation guidance
- **User Stories**: Link to requirements and acceptance criteria
- **Handoff**: Clear instructions for developers

### Iteration
- **Start Rough**: Low-fidelity wireframes first
- **Test Early**: Validate assumptions before implementation
- **Iterate**: Improve based on feedback
- **Measure**: Use data to inform decisions
