# Design Tokens - Kodarkitektur Bokverkstad

## Overview

Design tokens are the foundational design decisions that drive the visual consistency of the Kodarkitektur Bokverkstad project. They serve as the single source of truth for all design values, ensuring that design guides development and that the appearance remains consistent across all platforms and formats.

## What Are Design Tokens?

Design tokens are named entities that store visual design attributes. They abstract design decisions into reusable, technology-agnostic values that can be applied across different platforms and technologies.

### Benefits of Design Tokens

1. **Single Source of Truth**: All design values are defined once and referenced everywhere
2. **Consistency**: Ensures visual consistency across web, PDF, presentations, and documentation
3. **Maintainability**: Changes to design values propagate automatically throughout the codebase
4. **Scalability**: Easy to extend with new tokens or update existing ones
5. **Design-Development Bridge**: Provides a common language between designers and developers
6. **Platform Agnostic**: Can be exported to CSS, JavaScript, mobile platforms, and design tools

## Token Categories

### 1. Color Tokens

Colors are the most critical design tokens in the Kvadrat brand system. All colors are defined in HSL format for maximum flexibility and consistency.

#### Primary Brand Colors

```css
/* Kvadrat Primary Blue - Main brand color for headers and important elements */
--primary: 221 67% 32%;                    /* #1e3a8a */
--primary-foreground: 0 0% 100%;           /* White text on primary */

/* Kvadrat Light Blue - For accents and interactive elements */
--accent: 217 91% 60%;                     /* #3b82f6 */
--accent-foreground: 0 0% 100%;            /* White text on accent */

/* Kvadrat Dark Blue - For text and high contrast */
--foreground: 214 32% 18%;                 /* #1e293b */
```

#### Semantic Colors

```css
/* Success - For positive states and confirmations */
--success: 160 84% 30%;                    /* #059669 */
--success-foreground: 0 0% 100%;

/* Warning - For caution and attention states */
--warning: 32 95% 44%;                     /* #d97706 */
--warning-foreground: 0 0% 100%;

/* Destructive - For errors and dangerous actions */
--destructive: 0 84% 51%;                  /* #dc2626 */
--destructive-foreground: 0 0% 100%;
```

#### Neutral Colors

```css
/* Backgrounds and surfaces */
--background: 0 0% 100%;                   /* Pure white */
--card: 0 0% 100%;                         /* Card backgrounds */
--muted: 214 32% 97%;                      /* Subtle backgrounds */

/* Text variations */
--foreground: 214 32% 18%;                 /* Primary text */
--muted-foreground: 215 20% 46%;           /* Secondary text */

/* Borders and separators */
--border: 214 20% 89%;                     /* Subtle borders */
--input: 214 20% 89%;                      /* Input borders */
```

### 2. Typography Tokens

Typography tokens ensure consistent text styling across all platforms.

#### Font Families

```css
/* Primary font for all text content */
font-family: 'Inter', system-ui, -apple-system, sans-serif;

/* Monospace font for code and technical content */
font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace;
```

#### Font Weights

- **Light**: 300 - Rarely used, for subtle text
- **Regular**: 400 - Body text, standard content
- **Medium**: 500 - Emphasis, subheadings
- **Semibold**: 600 - Section headers, important text
- **Bold**: 700 - Main headings
- **Extra Bold**: 800 - Hero text, primary headings

#### Type Scale

```css
/* Headings */
--font-size-h1: 2.25rem;     /* 36px - Page titles */
--font-size-h2: 1.875rem;    /* 30px - Section headers */
--font-size-h3: 1.5rem;      /* 24px - Subsection headers */
--font-size-h4: 1.25rem;     /* 20px - Minor headers */

/* Body text */
--font-size-base: 1rem;      /* 16px - Standard text */
--font-size-sm: 0.875rem;    /* 14px - Small text */

/* Line heights */
--line-height-tight: 1.2;    /* Headlines */
--line-height-snug: 1.4;     /* Subheadings */
--line-height-normal: 1.6;   /* Body text */
```

### 3. Spacing Tokens

Consistent spacing creates visual rhythm and hierarchy.

#### Spacing Scale

```css
/* Base spacing units (multiples of 4px) */
--space-xs: 4px;     /* 0.25rem - Tight spacing */
--space-sm: 8px;     /* 0.5rem - Small gaps */
--space-md: 16px;    /* 1rem - Standard spacing */
--space-lg: 24px;    /* 1.5rem - Section spacing */
--space-xl: 32px;    /* 2rem - Large spacing */
--space-2xl: 48px;   /* 3rem - Major sections */
--space-3xl: 64px;   /* 4rem - Hero spacing */

/* Custom spacing tokens */
--space-18: 72px;    /* 4.5rem - 18 units */
--space-88: 352px;   /* 22rem - 88 units */
```

#### Layout Spacing

```css
/* Container padding */
--container-padding-mobile: 16px;
--container-padding-tablet: 24px;
--container-padding-desktop: 48px;

/* Section margins */
--section-margin-sm: 24px;
--section-margin-lg: 48px;
```

### 4. Border Radius Tokens

Rounded corners define the softness of the interface.

```css
/* Border radius scale */
--radius: 0.5rem;                          /* 8px - Base radius */
--radius-sm: calc(var(--radius) - 4px);    /* 4px - Small elements */
--radius-md: calc(var(--radius) - 2px);    /* 6px - Medium elements */
--radius-lg: var(--radius);                /* 8px - Large elements */

/* Custom radius values */
--radius-full: 9999px;                     /* Fully rounded (pills) */
--radius-none: 0px;                        /* No rounding */
```

### 5. Shadow Tokens

Shadows create depth and visual hierarchy.

```css
/* Kvadrat-branded shadows with blue tint */
--shadow-sm: 0 1px 2px 0 rgba(30, 58, 138, 0.05);
--shadow-md: 0 4px 6px -1px rgba(30, 58, 138, 0.1), 
             0 2px 4px -1px rgba(30, 58, 138, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(30, 58, 138, 0.1), 
             0 4px 6px -2px rgba(30, 58, 138, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(30, 58, 138, 0.1), 
             0 10px 10px -5px rgba(30, 58, 138, 0.04);
```

## How Design Guides Development

### 1. CSS Custom Properties (CSS Variables)

The design tokens are implemented as CSS custom properties in `src/index.css`, making them globally available:

```css
@layer base {
  :root {
    /* Color tokens */
    --primary: 221 67% 32%;
    --accent: 217 91% 60%;
    --background: 0 0% 100%;
    
    /* Spacing tokens */
    --radius: 0.5rem;
    
    /* Component-specific tokens */
    --sidebar-background: 214 32% 97%;
    --sidebar-primary: 221 67% 32%;
  }
}
```

**Usage in CSS:**
```css
.my-component {
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-radius: var(--radius);
  padding: var(--space-md);
}
```

### 2. Tailwind Configuration

Tokens are mapped to Tailwind utilities in `tailwind.config.ts`:

```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        kvadrat: {
          blue: "hsl(221 67% 32%)",
          "blue-light": "hsl(217 91% 60%)",
        },
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
      },
    },
  },
}
```

**Usage in JSX:**
```tsx
<div className="bg-primary text-primary-foreground rounded-lg p-md">
  Content
</div>
```

### 3. Component Integration

React components consume design tokens through Tailwind classes or CSS variables:

```tsx
// Button component using design tokens
export function Button({ children, variant = "primary" }) {
  return (
    <button 
      className={cn(
        "rounded-md px-4 py-2 font-medium transition-colors",
        variant === "primary" && "bg-primary text-primary-foreground hover:bg-primary/90",
        variant === "secondary" && "bg-secondary text-secondary-foreground"
      )}
    >
      {children}
    </button>
  );
}
```

### 4. Dark Mode Support

Design tokens enable seamless theme switching:

```css
.dark {
  /* Override tokens for dark theme */
  --background: 214 32% 9%;
  --foreground: 214 32% 97%;
  --primary: 217 91% 60%;      /* Lighter primary for dark backgrounds */
  --card: 214 32% 12%;
}
```

## Token Implementation Examples

### Example 1: Creating a Branded Card

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function BrandedCard({ title, children }) {
  return (
    <Card className="border-border shadow-kvadrat hover:shadow-kvadrat-lg transition-shadow">
      <CardHeader className="border-b border-border">
        <CardTitle className="text-primary">{title}</CardTitle>
      </CardHeader>
      <CardContent className="p-lg">
        {children}
      </CardContent>
    </Card>
  );
}
```

### Example 2: Status Badge with Semantic Colors

```tsx
export function StatusBadge({ status }) {
  const variants = {
    success: "bg-success text-success-foreground",
    warning: "bg-warning text-warning-foreground",
    error: "bg-destructive text-destructive-foreground",
  };
  
  return (
    <span className={cn("px-2 py-1 rounded-sm text-sm font-medium", variants[status])}>
      {status}
    </span>
  );
}
```

### Example 3: Consistent Typography

```tsx
export function ArticleContent({ content }) {
  return (
    <article className="space-y-lg max-w-prose">
      <h1 className="text-4xl font-bold text-foreground">
        {content.title}
      </h1>
      <h2 className="text-3xl font-semibold text-primary">
        {content.subtitle}
      </h2>
      <p className="text-base text-muted-foreground leading-normal">
        {content.body}
      </p>
    </article>
  );
}
```

### Example 4: Responsive Spacing

```tsx
export function Section({ children }) {
  return (
    <section className="
      py-lg md:py-xl lg:py-2xl
      px-md md:px-lg lg:px-xl
      space-y-md
    ">
      {children}
    </section>
  );
}
```

## Multi-Platform Token Export

Design tokens can be exported to multiple formats:

### CSS Variables
```css
:root {
  --primary: 221 67% 32%;
  --accent: 217 91% 60%;
}
```

### JavaScript/TypeScript
```typescript
export const tokens = {
  colors: {
    primary: 'hsl(221, 67%, 32%)',
    accent: 'hsl(217, 91%, 60%)',
  },
  spacing: {
    sm: '8px',
    md: '16px',
    lg: '24px',
  },
};
```

### Tailwind Utilities
```html
<div class="bg-primary text-primary-foreground p-lg rounded-md">
  Content
</div>
```

### Python (for PDF generation)
```python
KVADRAT_COLORS = {
    'primary': '#1e3a8a',
    'accent': '#3b82f6',
    'success': '#059669',
}
```

## Best Practices

### 1. Always Use Tokens

❌ **Don't hardcode values:**
```css
.button {
  background-color: #1e3a8a;  /* Hardcoded */
  padding: 16px;               /* Hardcoded */
}
```

✅ **Use design tokens:**
```css
.button {
  background-color: hsl(var(--primary));
  padding: var(--space-md);
}
```

### 2. Use Semantic Tokens

❌ **Don't use color names directly:**
```tsx
<Button className="bg-kvadrat-blue">Submit</Button>
```

✅ **Use semantic token names:**
```tsx
<Button className="bg-primary">Submit</Button>
```

### 3. Maintain Token Hierarchy

Organize tokens in logical groups:
- **Global tokens**: Base values (colors, spacing scale)
- **Semantic tokens**: Purpose-driven values (primary, success, warning)
- **Component tokens**: Component-specific values (button-padding, card-radius)

### 4. Document Token Usage

Always document what each token is for:

```css
/* Primary brand color - used for main headings, CTAs, and key UI elements */
--primary: 221 67% 32%;

/* Accent color - used for interactive elements, links, and highlights */
--accent: 217 91% 60%;
```

### 5. Version Control Tokens

Track changes to design tokens:
- Use semantic versioning for major design updates
- Document breaking changes
- Provide migration guides when tokens change

## Token Governance

### Adding New Tokens

1. **Justify the need**: Ensure the token serves a unique purpose
2. **Follow naming conventions**: Use clear, semantic names
3. **Document usage**: Explain when and how to use the token
4. **Update all platforms**: Ensure consistency across web, PDF, and documentation

### Modifying Existing Tokens

1. **Assess impact**: Check where the token is used
2. **Communicate changes**: Notify the team of upcoming changes
3. **Update documentation**: Keep examples and guides current
4. **Test thoroughly**: Verify changes across all use cases

### Deprecating Tokens

1. **Mark as deprecated**: Add deprecation notice
2. **Provide alternatives**: Suggest replacement tokens
3. **Set sunset date**: Give adequate time for migration
4. **Remove carefully**: Ensure no references remain

## Design Token Tools

### Recommended Tools

1. **Style Dictionary** - Transform tokens to multiple formats
2. **Figma Tokens Plugin** - Sync design tokens with Figma
3. **Theo** - Token transformation tool by Salesforce
4. **CSS Custom Properties** - Native browser support

### Current Implementation

This project uses:
- **CSS Custom Properties** for runtime token values
- **Tailwind Config** for build-time utilities
- **TypeScript** for type-safe token access

## Resources

### Internal Documentation
- `DESIGN_SYSTEM.md` - Complete design system overview
- `BRAND_GUIDELINES.md` - Brand usage guidelines
- `src/index.css` - Token definitions
- `tailwind.config.ts` - Tailwind token mapping

### External References
- [Design Tokens W3C Community Group](https://www.w3.org/community/design-tokens/)
- [Design Tokens Format Module](https://tr.designtokens.org/format/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [CSS Custom Properties Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

## Conclusion

Design tokens are the foundation of a scalable, maintainable design system. By abstracting design decisions into reusable tokens, we ensure that design truly guides development, creating a consistent visual experience across all platforms and touchpoints.

The Kodarkitektur Bokverkstad project demonstrates how design tokens bridge the gap between design and development, enabling rapid iteration while maintaining brand consistency.

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Maintained By**: Kvadrat Design Systems Team
