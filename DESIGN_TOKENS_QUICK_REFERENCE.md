# Design Tokens Quick Reference

Quick reference guide for using design tokens in the Kodarkitektur Bokverkstad project.

## 🎨 Color Classes

### Primary & Accent Colors
```tsx
bg-primary text-primary-foreground    // Kvadrat blue button
bg-accent text-accent-foreground      // Light blue accent
bg-kvadrat-blue text-white            // Direct brand color
bg-kvadrat-blue-light text-white      // Light variant
```

### Semantic Colors
```tsx
bg-success text-success-foreground    // Green - success states
bg-warning text-warning-foreground    // Amber - warnings
bg-destructive text-destructive-foreground  // Red - errors/delete
```

### Neutral Colors
```tsx
bg-background text-foreground         // Page background
bg-card text-card-foreground          // Card backgrounds
bg-muted text-muted-foreground        // Subtle backgrounds
bg-secondary text-secondary-foreground // Secondary backgrounds
```

### Borders & Inputs
```tsx
border-border       // Standard border color
border-input        // Input field borders
ring-ring           // Focus rings
```

## 📝 Typography

### Font Families
```tsx
font-sans    // Inter (headings & body)
font-mono    // JetBrains Mono (code)
```

### Text Sizes & Weights
```tsx
// Headings
text-4xl font-bold              // H1 - Main headings
text-3xl font-semibold          // H2 - Section headings
text-xl font-semibold           // H3 - Subsections
text-lg font-medium             // H4 - Small headings

// Body text
text-base                       // Regular body text
text-sm text-muted-foreground   // Secondary/helper text
```

## 📦 Spacing

### Custom Spacing
```tsx
w-18  h-18      // 4.5rem (72px)
w-88  h-88      // 22rem (352px)
```

### Standard Spacing (Tailwind defaults)
```tsx
p-4  m-4        // 1rem (16px)
p-6  m-6        // 1.5rem (24px)
p-8  m-8        // 2rem (32px)
```

## 🎭 Shadows

```tsx
shadow-kvadrat      // Subtle card shadow
shadow-kvadrat-lg   // Prominent shadow
```

## 🔲 Border Radius

```tsx
rounded-lg     // 8px - cards, buttons
rounded-md     // 6px - smaller elements
rounded-sm     // 4px - minimal rounding
```

## ✨ Animations

```tsx
animate-fade-in     // Fade in from bottom
animate-slide-in    // Slide in from left
```

## 🌈 Custom Gradients

```tsx
kvadrat-gradient          // Primary → Accent gradient
kvadrat-gradient-subtle   // Background → Muted gradient
```

## 🧩 Common Component Patterns

### Primary Button
```tsx
<Button className="bg-primary hover:bg-accent text-primary-foreground shadow-kvadrat">
  Click Me
</Button>
```

### Success Badge
```tsx
<Badge className="bg-success text-success-foreground">
  Active
</Badge>
```

### Card with Branded Shadow
```tsx
<Card className="shadow-kvadrat border-primary/20">
  <CardHeader>
    <CardTitle className="text-foreground">Title</CardTitle>
    <CardDescription className="text-muted-foreground">
      Description
    </CardDescription>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

### Gradient Header
```tsx
<header className="kvadrat-gradient p-8 text-white rounded-lg">
  <h1 className="text-4xl font-bold">Architecture as Code</h1>
  <p className="text-lg opacity-90">Subtitle text</p>
</header>
```

### Subtle Background Section
```tsx
<section className="kvadrat-gradient-subtle p-8 rounded-lg border border-border">
  <h2 className="text-3xl font-semibold text-foreground mb-4">Section Title</h2>
  <p className="text-muted-foreground">Section content</p>
</section>
```

## 🌙 Dark Mode

All components automatically adapt to dark mode. No additional classes needed:

```tsx
// This works in both light and dark mode
<div className="bg-background text-foreground">
  Content adapts automatically
</div>
```

## 💡 Pro Tips

### ✅ Do
- Use semantic color names (`bg-success`, `bg-destructive`)
- Pair colors with their foreground variants (`bg-primary text-primary-foreground`)
- Use `text-muted-foreground` for secondary text
- Apply `shadow-kvadrat` to cards for consistency
- Use opacity modifiers (`bg-primary/20` for 20% opacity)

### ❌ Don't
- Hard-code hex colors (`#1e3a8a`)
- Use inline styles for colors
- Mix HSL and RGB formats
- Create custom colors outside the token system
- Forget to test in dark mode

## 📚 Full Documentation

For complete documentation, see:
- [DESIGN_TOKENS.md](DESIGN_TOKENS.md) - Complete reference
- [/design-tokens](http://localhost:8081/design-tokens) - Live showcase (dev server)

## 🔍 Token Values Reference

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `primary` | `hsl(221 67% 32%)` | `hsl(217 91% 60%)` | Buttons, links, brand |
| `accent` | `hsl(217 91% 60%)` | `hsl(221 67% 55%)` | Highlights, hover states |
| `success` | `hsl(160 84% 30%)` | `hsl(160 84% 45%)` | Success messages, badges |
| `warning` | `hsl(32 95% 44%)` | `hsl(32 95% 55%)` | Warnings, alerts |
| `destructive` | `hsl(0 84% 51%)` | `hsl(0 84% 60%)` | Errors, delete actions |
| `muted` | `hsl(214 32% 97%)` | `hsl(214 32% 15%)` | Subtle backgrounds |

## 🛠️ CSS Custom Properties

Access tokens directly in CSS:

```css
.custom-element {
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-radius: var(--radius);
  box-shadow: var(--shadow-kvadrat);
}
```

## 📱 Responsive Design

Combine with Tailwind breakpoints:

```tsx
<div className="p-4 md:p-8 lg:p-12">
  Responsive padding
</div>

<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">
  Responsive heading
</h1>
```

---

**Last Updated:** 2025-10-04
