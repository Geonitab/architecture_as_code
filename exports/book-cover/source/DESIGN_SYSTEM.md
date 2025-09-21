# Kodarkitektur Bokverkstad - Grafisk profil

## Översikt
En omfattande grafisk profil som är anpassad för Kvadrat.se:s visuella identitet och designspråk.

## Färgpalett

### Primära färger
- **Kvadrat Blå**: `#1e3a8a` (HSL: 221 67% 32%) - Huvudfärg för rubriker och viktiga element
- **Kvadrat Mörkblå**: `#1e293b` (HSL: 214 32% 18%) - För text och kontrast
- **Kvadrat Ljusblå**: `#3b82f6` (HSL: 217 91% 60%) - För accenter och interaktiva element

### Sekundära färger
- **Neutral Grå**: `#64748b` (HSL: 215 20% 46%) - För sekundär text
- **Ljus Grå**: `#f1f5f9` (HSL: 214 32% 97%) - För bakgrunder
- **Vit**: `#ffffff` (HSL: 0 0% 100%) - För kort och huvudsaklig bakgrund

### Accent och specialfärger
- **Framgång Grön**: `#059669` (HSL: 160 84% 30%) - För statusindikationer
- **Varning Amber**: `#d97706` (HSL: 32 95% 44%) - För uppmärksamhet
- **Fel Röd**: `#dc2626` (HSL: 0 84% 51%) - För felmeddelanden

## Typografi

### Fonthierarki
- **H1**: 2.25rem (36px), font-weight: 700, line-height: 1.2
- **H2**: 1.875rem (30px), font-weight: 600, line-height: 1.3
- **H3**: 1.5rem (24px), font-weight: 600, line-height: 1.4
- **H4**: 1.25rem (20px), font-weight: 500, line-height: 1.4
- **Body**: 1rem (16px), font-weight: 400, line-height: 1.6
- **Small**: 0.875rem (14px), font-weight: 400, line-height: 1.5

### Fontfamiljer
- **Primär**: Inter, system-ui, sans-serif
- **Monospace**: 'JetBrains Mono', Consolas, monospace

## Logotyp och visuella element

### Logotypriktlinjer
- Minsta storlek: 120px bredd
- Friytor: Minst 1x logotypens höjd på alla sidor
- Färgvarianter: Mörk, ljus, och monokrom

### Visuella element
- **Rundade hörn**: 8px för kort, 4px för mindre element
- **Skuggor**: Subtila, mjuka skuggor för djup
- **Gradients**: Subtila gradienter från primär till accent

## Mallar

### Bokens framsida
- Logotyp: Övre vänster hörn
- Titel: Centrerad, stor typografi
- Undertitel: Under titel, medium storlek
- Författare: Längst ner
- Bakgrund: Gradient från Kvadrat Blå till Mörkblå

### Whitepapers
- Standardformat: A4
- Marginaler: 2.5cm på alla sidor
- Typsnitt: Inter för rubriker, system för text
- Färgschema: Primära färger med sparsam accent

### Presentationsmallar
- Format: 16:9 widescreen
- Masterlayout med logotyp och sidnummer
- Konsistent användning av färger och typografi
- Bullet points med Kvadrat Blå accenter

### Webbplatslayout
- Responsiv design
- Enhetlig navigering
- Tydlig informationshierarki
- Optimerad för tillgänglighet

## Användningsriktlinjer

### Gör
- Använd konsekventa marginaler och utfyllnad
- Följ färgpaletten strikt
- Använd tillräcklig kontrast för tillgänglighet
- Håll designen ren och professionell

### Gör inte
- Blanda olika fonter utanför systemet
- Använd färger utanför paletten
- Överanvänd accent färger
- Glöm responsiv design

## Teknisk implementation

### CSS Custom Properties
Alla färger och mått definieras som CSS custom properties för enkel underhåll.

### Tailwind Configuration
Anpassad konfiguration som matchar designsystemet.

### Komponentbibliotek
Konsistenta React-komponenter som följer designsystemet.