# Design Tokens Documentation

## Overview

Design tokens are the visual design atoms of the design system — specifically, they are named entities that store visual design attributes. They are used in place of hard-coded values in order to maintain a scalable and consistent visual system for UI development.

This documentation covers the design token system used in Kodarkitektur Bokverkstad, which is aligned with Kvadrat's brand identity.

## What are Design Tokens?

Design tokens are platform-agnostic variables that represent the smallest building blocks of a design system:
- **Colors**: Background colors, text colors, border colors
- **Typography**: Font families, font sizes, font weights, line heights
- **Spacing**: Margins, padding, gaps
- **Shadows**: Box shadows for depth and elevation
- **Border Radius**: Rounded corners
- **Animations**: Keyframes and timing functions

By using design tokens, we ensure:
- **Consistency**: Same values across the entire application
- **Maintainability**: Update once, apply everywhere
- **Scalability**: Easy to theme and customize
- **Accessibility**: Standardized color contrasts and spacing

## Token Structure

Our design token system uses CSS Custom Properties (CSS Variables) combined with Tailwind CSS configuration for maximum flexibility.

### File Organization

```
src/
├── index.css           # CSS Custom Properties definitions
tailwind.config.ts      # Tailwind theme extension with tokens
```

## Color Tokens

### Kvadrat Brand Colors

The primary brand colors are defined using HSL (Hue, Saturation, Lightness) format for better color manipulation and theming support.

#### Primary Colors

```css
/* Kvadrat Primary Blue */
--primary: 221 67% 32%;              /* hsl(221, 67%, 32%) - #1e3a8a */
--primary-foreground: 0 0% 100%;     /* White text on primary */

/* Kvadrat Light Blue for accents */
--accent: 217 91% 60%;               /* hsl(217, 91%, 60%) - #3b82f6 */
--accent-foreground: 0 0% 100%;      /* White text on accent */
```

**Usage in React/Tailwind:**
```tsx
// Using Tailwind classes
<div className="bg-primary text-primary-foreground">
  Primary Button
</div>

<div className="bg-accent text-accent-foreground">
  Accent Button
</div>

// Using Tailwind utility classes for Kvadrat colors
<div className="bg-kvadrat-blue">
  Direct brand color
</div>
```

**Usage in CSS:**
```css
.custom-element {
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}
```

#### Semantic Colors

```css
/* Success - Green */
--success: 160 84% 30%;              /* hsl(160, 84%, 30%) - #059669 */
--success-foreground: 0 0% 100%;

/* Warning - Amber */
--warning: 32 95% 44%;               /* hsl(32, 95%, 44%) - #d97706 */
--warning-foreground: 0 0% 100%;

/* Destructive - Red */
--destructive: 0 84% 51%;            /* hsl(0, 84%, 51%) - #dc2626 */
--destructive-foreground: 0 0% 100%;
```

**Usage Example:**
```tsx
import { Badge } from "@/components/ui/badge";

// Success state
<Badge variant="success">Completed</Badge>

// Warning state
<Badge variant="warning">Pending</Badge>

// Error state
<Badge variant="destructive">Failed</Badge>
```

#### Neutral Colors

```css
/* Background and foreground */
--background: 0 0% 100%;             /* White */
--foreground: 214 32% 18%;           /* Dark blue-gray */

/* Card backgrounds */
--card: 0 0% 100%;
--card-foreground: 214 32% 18%;

/* Muted backgrounds */
--muted: 214 32% 97%;                /* Light gray */
--muted-foreground: 215 20% 46%;     /* Medium gray */

/* Secondary backgrounds */
--secondary: 214 32% 97%;
--secondary-foreground: 214 32% 18%;

/* Borders and inputs */
--border: 214 20% 89%;
--input: 214 20% 89%;
--ring: 221 67% 32%;                 /* Focus ring (primary color) */
```

#### Kvadrat Utility Colors

These are hardcoded utility colors available as Tailwind classes:

```typescript
kvadrat: {
  blue: "hsl(221 67% 32%)",          // Main brand blue
  "blue-light": "hsl(217 91% 60%)",  // Light accent blue
  "blue-dark": "hsl(214 32% 18%)",   // Dark blue for text
  gray: "hsl(215 20% 46%)",          // Medium gray
  "gray-light": "hsl(214 32% 97%)",  // Light gray
}
```

**Usage:**
```tsx
<div className="bg-kvadrat-blue text-white">
  Direct Kvadrat brand color
</div>

<div className="bg-kvadrat-gray-light border-kvadrat-gray">
  Subtle background with gray border
</div>
```

### Dark Mode Support

All color tokens have dark mode variants:

```css
.dark {
  --background: 214 32% 9%;          /* Dark blue-gray */
  --foreground: 214 32% 97%;         /* Light gray */
  
  --primary: 217 91% 60%;            /* Lighter blue for dark theme */
  --primary-foreground: 214 32% 9%;
  
  /* ... other dark mode tokens */
}
```

**Usage:**
```tsx
// Component automatically adapts to dark mode
<div className="bg-background text-foreground">
  Content that adapts to theme
</div>
```

## Typography Tokens

### Font Families

```typescript
fontFamily: {
  sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
  mono: ['JetBrains Mono', 'Consolas', 'Courier New', 'monospace'],
}
```

**Usage:**
```tsx
<h1 className="font-sans">Heading with Inter font</h1>
<code className="font-mono">const code = 'monospace';</code>
```

**CSS Usage:**
```css
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

code, pre {
  font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace;
}
```

### Font Sizes and Weights

Typography is configured through Tailwind's default system with custom overrides in CSS:

```css
h1 {
  @apply text-4xl font-bold leading-tight tracking-tight;
}

h2 {
  @apply text-3xl font-semibold leading-tight;
}

h3 {
  @apply text-xl font-semibold leading-snug;
}

h4 {
  @apply text-lg font-medium leading-snug;
}
```

## Spacing Tokens

Custom spacing values extend Tailwind's default spacing scale:

```typescript
spacing: {
  '18': '4.5rem',    // 72px
  '88': '22rem',     // 352px
}
```

**Usage:**
```tsx
<div className="mt-18 mb-88">
  Custom spacing
</div>
```

## Border Radius Tokens

```css
--radius: 0.5rem;  /* Base radius: 8px */
```

```typescript
borderRadius: {
  lg: "var(--radius)",                    // 8px
  md: "calc(var(--radius) - 2px)",       // 6px
  sm: "calc(var(--radius) - 4px)",       // 4px
}
```

**Usage:**
```tsx
<div className="rounded-lg">Large rounded corners</div>
<div className="rounded-md">Medium rounded corners</div>
<div className="rounded-sm">Small rounded corners</div>
```

## Shadow Tokens

Custom Kvadrat-branded shadows:

```typescript
boxShadow: {
  'kvadrat': '0 4px 6px -1px rgba(30, 58, 138, 0.1), 0 2px 4px -1px rgba(30, 58, 138, 0.06)',
  'kvadrat-lg': '0 10px 15px -3px rgba(30, 58, 138, 0.1), 0 4px 6px -2px rgba(30, 58, 138, 0.05)',
}
```

**Usage:**
```tsx
<Card className="shadow-kvadrat">
  Card with subtle Kvadrat shadow
</Card>

<div className="shadow-kvadrat-lg">
  Element with larger Kvadrat shadow
</div>
```

## Animation Tokens

### Keyframes

```typescript
keyframes: {
  "accordion-down": {
    from: { height: "0" },
    to: { height: "var(--radix-accordion-content-height)" },
  },
  "accordion-up": {
    from: { height: "var(--radix-accordion-content-height)" },
    to: { height: "0" },
  },
  "fade-in": {
    from: { opacity: "0", transform: "translateY(10px)" },
    to: { opacity: "1", transform: "translateY(0)" },
  },
  "slide-in": {
    from: { transform: "translateX(-100%)" },
    to: { transform: "translateX(0)" },
  },
}
```

### Animations

```typescript
animation: {
  "accordion-down": "accordion-down 0.2s ease-out",
  "accordion-up": "accordion-up 0.2s ease-out",
  "fade-in": "fade-in 0.3s ease-out",
  "slide-in": "slide-in 0.3s ease-out",
}
```

**Usage:**
```tsx
<div className="animate-fade-in">
  Fades in from bottom
</div>

<div className="animate-slide-in">
  Slides in from left
</div>
```

## Custom Utility Classes

### Kvadrat Gradients

```css
.kvadrat-gradient {
  background: linear-gradient(135deg, hsl(var(--primary)) 0%, hsl(var(--accent)) 100%);
}

.kvadrat-gradient-subtle {
  background: linear-gradient(135deg, hsl(var(--background)) 0%, hsl(var(--muted)) 100%);
}
```

**Usage:**
```tsx
<header className="kvadrat-gradient">
  Gradient header with brand colors
</header>

<section className="kvadrat-gradient-subtle">
  Subtle background gradient
</section>
```

## Practical Examples

### Example 1: Creating a Branded Button

```tsx
import { Button } from "@/components/ui/button";

export function BrandedButton() {
  return (
    <Button className="bg-primary hover:bg-accent text-primary-foreground shadow-kvadrat">
      Click Me
    </Button>
  );
}
```

### Example 2: Creating a Status Card

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function StatusCard() {
  return (
    <Card className="shadow-kvadrat-lg border-primary/20">
      <CardHeader>
        <CardTitle className="text-foreground">Project Status</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground">Build</span>
            <Badge variant="success">Passing</Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground">Tests</span>
            <Badge variant="warning">Running</Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Example 3: Dark Mode Aware Component

```tsx
export function ThemedCard() {
  return (
    <div className="bg-card text-card-foreground border-border rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Themed Content</h2>
      <p className="text-muted-foreground">
        This card automatically adapts to light and dark themes.
      </p>
    </div>
  );
}
```

### Example 4: Custom Gradient Section

```tsx
export function HeroSection() {
  return (
    <section className="kvadrat-gradient text-white py-16">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-4">
          Architecture as Code
        </h1>
        <p className="text-lg opacity-90">
          A comprehensive guide to modern architecture practices
        </p>
      </div>
    </section>
  );
}
```

### Example 5: Animated Component

```tsx
export function AnimatedNotification() {
  return (
    <div className="animate-fade-in bg-success text-success-foreground rounded-lg p-4 shadow-kvadrat">
      <p className="font-medium">Success! Your changes have been saved.</p>
    </div>
  );
}
```

## Best Practices

### Do's ✅

1. **Always use design tokens** instead of hard-coded values
   ```tsx
   // ✅ Good
   <div className="bg-primary text-primary-foreground">

   // ❌ Bad
   <div style={{ backgroundColor: '#1e3a8a', color: '#ffffff' }}>
   ```

2. **Use semantic color names** for better maintainability
   ```tsx
   // ✅ Good
   <Badge variant="success">Completed</Badge>

   // ❌ Bad
   <Badge className="bg-green-600">Completed</Badge>
   ```

3. **Leverage Tailwind classes** for consistency
   ```tsx
   // ✅ Good
   <div className="rounded-lg shadow-kvadrat p-4">

   // ❌ Bad
   <div style={{ borderRadius: '8px', padding: '16px' }}>
   ```

4. **Use HSL format** for color tokens to enable better theming
   ```css
   /* ✅ Good */
   --primary: 221 67% 32%;

   /* ❌ Bad */
   --primary: #1e3a8a;
   ```

### Don'ts ❌

1. **Don't hard-code colors** in components
2. **Don't bypass the design system** with inline styles
3. **Don't create new color variations** without adding them to the token system
4. **Don't mix HSL and RGB** formats in the same codebase
5. **Don't ignore dark mode** - always test components in both themes

## Updating Design Tokens

When you need to update or add new design tokens:

1. **Add CSS Custom Property** in `src/index.css`:
   ```css
   :root {
     --new-token: 200 50% 50%;
   }
   ```

2. **Add Tailwind Configuration** in `tailwind.config.ts`:
   ```typescript
   colors: {
     'new-color': "hsl(var(--new-token))",
   }
   ```

3. **Document the token** in this file

4. **Test in both light and dark modes**

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Design Tokens W3C Community Group](https://www.w3.org/community/design-tokens/)
- [shadcn/ui Theming](https://ui.shadcn.com/docs/theming)

## Token Reference Table

### Color Tokens Quick Reference

| Token Name | Light Mode | Dark Mode | Purpose |
|------------|------------|-----------|---------|
| `--primary` | `221 67% 32%` | `217 91% 60%` | Primary brand color |
| `--accent` | `217 91% 60%` | `221 67% 55%` | Accent highlights |
| `--background` | `0 0% 100%` | `214 32% 9%` | Page background |
| `--foreground` | `214 32% 18%` | `214 32% 97%` | Primary text |
| `--muted` | `214 32% 97%` | `214 32% 15%` | Muted backgrounds |
| `--success` | `160 84% 30%` | `160 84% 45%` | Success states |
| `--warning` | `32 95% 44%` | `32 95% 55%` | Warning states |
| `--destructive` | `0 84% 51%` | `0 84% 60%` | Error states |

### Spacing Tokens Quick Reference

| Token | Value | Usage |
|-------|-------|-------|
| `18` | `4.5rem` (72px) | Extra spacing |
| `88` | `22rem` (352px) | Large spacing |

### Shadow Tokens Quick Reference

| Token | Usage |
|-------|-------|
| `shadow-kvadrat` | Subtle card shadows |
| `shadow-kvadrat-lg` | Prominent element shadows |

## Migration Guide

If you're updating existing code to use design tokens:

1. **Find hard-coded colors:**
   ```bash
   # Search for hex colors
   grep -r "#[0-9a-f]\{6\}" src/
   
   # Search for rgb colors
   grep -r "rgb(" src/
   ```

2. **Replace with token classes:**
   ```tsx
   // Before
   <div style={{ color: '#1e3a8a' }}>

   // After
   <div className="text-primary">
   ```

3. **Test thoroughly** in both light and dark modes

4. **Update component documentation** to reflect token usage

---

**Last Updated:** 2025-10-04
**Maintained By:** Kodarkitektur Bokverkstad Team
