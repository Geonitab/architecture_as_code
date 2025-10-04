/**
 * Design Tokens Example Component
 * 
 * This component demonstrates the practical usage of design tokens
 * from the Kodarkitektur Bokverkstad design system.
 * 
 * It showcases:
 * - Color tokens (primary, accent, semantic colors)
 * - Typography tokens (font families, sizes)
 * - Spacing tokens
 * - Shadow tokens
 * - Animation tokens
 * - Gradient utilities
 * - Dark mode support
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Palette, Type, Box, Sparkles } from "lucide-react";

export function DesignTokensExample() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header with gradient */}
        <header className="kvadrat-gradient rounded-lg p-8 text-white animate-fade-in">
          <h1 className="text-4xl font-bold mb-2">Design Tokens Showcase</h1>
          <p className="text-lg opacity-90">
            Demonstrating the Kodarkitektur Bokverkstad design system
          </p>
        </header>

        {/* Color Tokens Section */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground flex items-center gap-2">
            <Palette className="h-8 w-8 text-primary" />
            Color Tokens
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Primary Colors */}
            <Card className="shadow-kvadrat border-primary/20">
              <CardHeader>
                <CardTitle>Primary Colors</CardTitle>
                <CardDescription>Main brand colors</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="bg-primary text-primary-foreground p-4 rounded-md">
                  Primary
                </div>
                <div className="bg-accent text-accent-foreground p-4 rounded-md">
                  Accent
                </div>
                <div className="bg-kvadrat-blue text-white p-4 rounded-md">
                  Kvadrat Blue
                </div>
              </CardContent>
            </Card>

            {/* Semantic Colors */}
            <Card className="shadow-kvadrat border-primary/20">
              <CardHeader>
                <CardTitle>Semantic Colors</CardTitle>
                <CardDescription>Status and feedback colors</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="bg-success text-success-foreground p-4 rounded-md">
                  Success
                </div>
                <div className="bg-warning text-warning-foreground p-4 rounded-md">
                  Warning
                </div>
                <div className="bg-destructive text-destructive-foreground p-4 rounded-md">
                  Destructive
                </div>
              </CardContent>
            </Card>

            {/* Neutral Colors */}
            <Card className="shadow-kvadrat border-primary/20">
              <CardHeader>
                <CardTitle>Neutral Colors</CardTitle>
                <CardDescription>Backgrounds and text</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="bg-background text-foreground border border-border p-4 rounded-md">
                  Background
                </div>
                <div className="bg-muted text-muted-foreground p-4 rounded-md">
                  Muted
                </div>
                <div className="bg-secondary text-secondary-foreground p-4 rounded-md">
                  Secondary
                </div>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Badge Examples */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground flex items-center gap-2">
            <Sparkles className="h-8 w-8 text-accent" />
            Badges with Semantic Colors
          </h2>

          <Card className="shadow-kvadrat-lg">
            <CardContent className="pt-6">
              <div className="flex flex-wrap gap-2">
                <Badge variant="default">Default</Badge>
                <Badge variant="secondary">Secondary</Badge>
                <Badge variant="destructive">Destructive</Badge>
                <Badge variant="outline">Outline</Badge>
                <Badge className="bg-success text-success-foreground">Success</Badge>
                <Badge className="bg-warning text-warning-foreground">Warning</Badge>
                <Badge className="bg-kvadrat-blue text-white">Kvadrat Blue</Badge>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Typography Tokens */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground flex items-center gap-2">
            <Type className="h-8 w-8 text-primary" />
            Typography Tokens
          </h2>

          <Card className="shadow-kvadrat">
            <CardContent className="pt-6 space-y-4">
              <div>
                <h1 className="text-4xl font-bold text-foreground mb-2">
                  Heading 1 - Inter Bold
                </h1>
                <p className="text-sm text-muted-foreground font-mono">
                  className="text-4xl font-bold"
                </p>
              </div>

              <div>
                <h2 className="text-3xl font-semibold text-foreground mb-2">
                  Heading 2 - Inter Semibold
                </h2>
                <p className="text-sm text-muted-foreground font-mono">
                  className="text-3xl font-semibold"
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold text-foreground mb-2">
                  Heading 3 - Inter Semibold
                </h3>
                <p className="text-sm text-muted-foreground font-mono">
                  className="text-xl font-semibold"
                </p>
              </div>

              <div>
                <p className="text-base text-foreground mb-2">
                  Body text - Inter Regular
                </p>
                <p className="text-sm text-muted-foreground font-mono">
                  className="text-base"
                </p>
              </div>

              <div>
                <code className="font-mono bg-muted px-2 py-1 rounded text-sm">
                  Code text - JetBrains Mono
                </code>
                <p className="text-sm text-muted-foreground font-mono mt-2">
                  className="font-mono"
                </p>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Shadows and Spacing */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground flex items-center gap-2">
            <Box className="h-8 w-8 text-accent" />
            Shadows & Spacing
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="shadow-kvadrat">
              <CardHeader>
                <CardTitle>Shadow Kvadrat</CardTitle>
                <CardDescription>Subtle shadow for cards</CardDescription>
              </CardHeader>
              <CardContent>
                <code className="text-sm font-mono">className="shadow-kvadrat"</code>
              </CardContent>
            </Card>

            <Card className="shadow-kvadrat-lg">
              <CardHeader>
                <CardTitle>Shadow Kvadrat Large</CardTitle>
                <CardDescription>Prominent shadow for emphasis</CardDescription>
              </CardHeader>
              <CardContent>
                <code className="text-sm font-mono">className="shadow-kvadrat-lg"</code>
              </CardContent>
            </Card>
          </div>

          <Card className="shadow-kvadrat">
            <CardHeader>
              <CardTitle>Spacing Tokens</CardTitle>
              <CardDescription>Custom spacing values</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="bg-primary h-4 w-18 rounded mb-2"></div>
                <code className="text-sm font-mono">w-18 (4.5rem / 72px)</code>
              </div>
              <div>
                <div className="bg-accent h-4 w-88 rounded mb-2"></div>
                <code className="text-sm font-mono">w-88 (22rem / 352px)</code>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Animations */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground">Animations</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="shadow-kvadrat animate-fade-in">
              <CardHeader>
                <CardTitle>Fade In Animation</CardTitle>
                <CardDescription>Fades in from bottom</CardDescription>
              </CardHeader>
              <CardContent>
                <code className="text-sm font-mono">className="animate-fade-in"</code>
              </CardContent>
            </Card>

            <Card className="shadow-kvadrat animate-slide-in">
              <CardHeader>
                <CardTitle>Slide In Animation</CardTitle>
                <CardDescription>Slides in from left</CardDescription>
              </CardHeader>
              <CardContent>
                <code className="text-sm font-mono">className="animate-slide-in"</code>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Gradients */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground">Custom Gradients</h2>

          <div className="space-y-4">
            <div className="kvadrat-gradient rounded-lg p-8 text-white">
              <h3 className="text-2xl font-bold mb-2">Kvadrat Gradient</h3>
              <p className="opacity-90">Primary to accent color gradient</p>
              <code className="text-sm opacity-80 mt-2 block">
                className="kvadrat-gradient"
              </code>
            </div>

            <div className="kvadrat-gradient-subtle rounded-lg p-8 border border-border">
              <h3 className="text-2xl font-bold mb-2 text-foreground">Kvadrat Gradient Subtle</h3>
              <p className="text-muted-foreground">Subtle background gradient</p>
              <code className="text-sm text-muted-foreground mt-2 block">
                className="kvadrat-gradient-subtle"
              </code>
            </div>
          </div>
        </section>

        {/* Buttons */}
        <section className="space-y-4">
          <h2 className="text-3xl font-semibold text-foreground">Buttons with Tokens</h2>

          <Card className="shadow-kvadrat">
            <CardContent className="pt-6">
              <div className="flex flex-wrap gap-2">
                <Button>Default</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="destructive">Destructive</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="link">Link</Button>
                <Button className="bg-success hover:bg-success/90 text-success-foreground">
                  Success
                </Button>
                <Button className="bg-kvadrat-blue hover:bg-kvadrat-blue-light text-white">
                  Kvadrat Blue
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Dark Mode Note */}
        <Card className="shadow-kvadrat-lg border-primary/20">
          <CardHeader>
            <CardTitle>Dark Mode Support</CardTitle>
            <CardDescription>All components automatically adapt to dark mode</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              All design tokens include dark mode variants. Toggle dark mode in your browser or
              system settings to see the components adapt automatically.
            </p>
            <div className="bg-muted p-4 rounded-lg">
              <code className="text-sm font-mono block">
                {`// Dark mode is applied via the .dark class`}<br />
                {`.dark {`}<br />
                {`  --background: 214 32% 9%;`}<br />
                {`  --foreground: 214 32% 97%;`}<br />
                {`  /* ... other dark mode tokens */`}<br />
                {`}`}
              </code>
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  );
}

export default DesignTokensExample;
