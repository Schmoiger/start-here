# Visual Design Standards

**Core Principle**: Design for clarity, accessibility, and user comprehension. Every visual element should serve a purpose.

## Visual Hierarchy

**Priority Order**: Size → Colour → Position → Contrast

| Element | Treatment |
|---------|-----------|
| Primary action | Largest, highest contrast, prominent position |
| Secondary info | Medium size, muted colour |
| Supporting details | Smallest, lowest visual weight |

**Gestalt Principles**:
- **Proximity**: Related elements close together
- **Similarity**: Consistent visual cues for related items
- **Continuity**: Guide eye along natural paths
- **Closure**: Use implied shapes to reduce clutter

## Colour & Accessibility

**WCAG 2.1 AA Requirements** (Mandatory):

| Element | Minimum Contrast |
|---------|-----------------|
| Normal text (<18px) | 4.5:1 |
| Large text (≥18px or 14px bold) | 3:1 |
| UI components (borders, icons) | 3:1 |
| Focus indicators | 3:1 |

**WCAG AAA Target** (Recommended):

| Element | Target Contrast |
|---------|----------------|
| Normal text | 7:1 |
| Large text | 4.5:1 |

**Colour Token Naming** (Semantic):

```
✓ action-primary, danger-01, text-muted
✗ blue-500, red-400, gray-300
```

**Colour-Blind Safe**:
- Don't rely on colour alone to convey information
- Use shapes, patterns, or labels alongside colour
- Test with colour blindness simulators

## Data Visualisation

### Chart Types

**Line Charts**: Time-series data, trends over time
- Single-colour for one dataset, multi-colour for comparison
- Clear data points at appropriate density
- Smooth lines for continuous data, stepped for discrete

**Bar Charts**: Comparing quantities across categories
- Consistent bar width and spacing
- Baseline at zero (unless justified otherwise)
- Horizontal bars for long category labels

**Scatter Plots**: Correlation between two variables
- Size/colour for third dimension
- Trend line when showing correlation
- Clear axis labels with units

**Heatmaps**: Dense data showing intensity/frequency
- Sequential colour scale (light to dark)
- Diverging scale for positive/negative values
- Clear legend showing scale

### Chart Best Practices

| Do | Don't |
|----|-------|
| Start Y-axis at appropriate scale | Truncate axes deceptively |
| Use consistent scales across related charts | Mix scales without clear labels |
| Add clear axis labels with units | Assume users know the scale |
| Use annotations sparingly | Clutter with excessive labels |
| Show data density appropriate to timeframe | Compress/expand data misleadingly |
| Use colour purposefully | Rainbow gradients without meaning |

**Chart Clarity**:
- One key insight per visualisation
- Title describes the takeaway, not just the data
- Legend positioned to not obscure data
- Gridlines subtle (10-20% opacity)
- Markers/indicators at points of interest, not spanning entire chart

## Tooltips

**Content Rules**:
- Maximum ~20 characters per line
- Show only relevant information for context
- Different tooltip content for different element types
- No critical information hidden in tooltips only

**Positioning**:
- Adjacent to target element (above, below, or side)
- Never obscure the element being described
- Use arrow/pointer to connect tooltip to target
- Flip position if near viewport edge

**Behaviour**:
- Appear on hover (desktop) or tap (mobile)
- 100-200ms delay before showing (prevent flicker)
- Smooth fade animation (150-200ms)
- Easy to dismiss (move away, click elsewhere)

**Accessibility**:
- Keyboard accessible (focus triggers tooltip)
- Screen reader compatible (aria-describedby)
- Sufficient contrast for tooltip text

## Interactive States

**Required States for Interactive Elements**:

| State | Visual Treatment |
|-------|-----------------|
| Default | Base styling |
| Hover | Subtle highlight (background, border, or shadow) |
| Focus | Visible outline (2px, high contrast) |
| Active/Pressed | Slightly depressed or colour shift |
| Disabled | 50% opacity, cursor: not-allowed |
| Loading | Spinner or skeleton, preserve dimensions |
| Error | Red border/text, error icon, message |
| Success | Green indicator, confirmation message |

**Focus Indicators**:
- Never remove focus outlines without alternative
- Use `outline-offset` for better aesthetics
- Ensure 3:1 contrast against background

## Responsive Design

**Breakpoints** (Mobile-first):

| Name | Width | Target |
|------|-------|--------|
| sm | ≥640px | Large phones |
| md | ≥768px | Tablets |
| lg | ≥1024px | Laptops |
| xl | ≥1280px | Desktops |
| 2xl | ≥1536px | Large monitors |

**Touch Targets**:
- Minimum 44×44px for touch devices
- 8px minimum spacing between targets
- Larger targets for primary actions

## Typography

**Scale** (Consistent rhythm):
```
xs: 12px    sm: 14px    base: 16px
lg: 18px    xl: 20px    2xl: 24px
3xl: 30px   4xl: 36px
```

**Line Height**:
- Body text: 1.5 (150%)
- Headings: 1.2-1.3 (120-130%)
- UI labels: 1.25 (125%)

**Readability**:
- 45-75 characters per line optimal
- Left-align body text (avoid justified)
- Sufficient paragraph spacing (1em minimum)

## Animation & Motion

**Principles**:
- Purposeful: Guides attention or provides feedback
- Quick: 150-300ms for UI, 300-500ms for page transitions
- Eased: Use ease-out for entering, ease-in for exiting
- Reducible: Respect `prefers-reduced-motion`

**When to Animate**:
- State changes (hover, focus, toggle)
- Loading/progress indication
- Drawing attention to important updates
- Smooth transitions between views

**When NOT to Animate**:
- Critical error messages (show immediately)
- High-frequency updates (avoid visual noise)
- User-initiated navigation (keep fast)

## Component Patterns

**Cards**:
- Consistent padding (16-24px)
- Subtle shadow or border for separation
- Clear visual hierarchy within card
- Interactive cards: hover state, cursor pointer

**Forms**:
- Label above input (not placeholder as label)
- Error messages below field, not in tooltip
- Group related fields visually
- Clear required field indicators

**Tables**:
- Zebra striping OR borders (not both)
- Sticky headers for long lists
- Sortable columns: clear indicator of sort state
- Responsive: horizontal scroll or card layout on mobile

## Anti-Patterns (Forbidden)

| Don't | Why |
|-------|-----|
| Text over busy images without overlay | Poor contrast, unreadable |
| Pure black (#000) on pure white (#FFF) | Too harsh, causes eye strain |
| Relying on colour alone | Accessibility failure |
| Hiding critical info in tooltips | May not be discovered |
| Disabled buttons without explanation | User doesn't know why |
| Infinite scroll without position indicator | User loses context |
| Auto-playing animations/videos | Disruptive, accessibility issue |
| Small touch targets on mobile | Frustrating, unusable |

## Tools & Validation

**Contrast Checkers**:
- WebAIM Contrast Checker
- Figma A11y plugins
- Chrome DevTools colour picker

**Colour Blindness Testing**:
- Sim Daltonism (macOS)
- Colorblindly (Chrome extension)

**Design Token Management**:
- Tokens Studio (Figma)
- Style Dictionary (code export)

## Sources

- [Laws of UX](https://lawsofux.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Nielsen Norman Group - Tooltip Guidelines](https://www.nngroup.com/articles/tooltip-guidelines/)
- [WebAIM - Contrast and Colour Accessibility](https://webaim.org/articles/contrast/)
- [Figma UI Design Principles](https://www.figma.com/resource-library/ui-design-principles/)
