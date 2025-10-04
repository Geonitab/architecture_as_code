# Kodarkitektur Bokverkstad - Grafisk profil

## Overview
a comprehensive grafisk profil as is anpassad for Kvadrat.se:s visuella identitet and designspråk.

## Färgpalett

### Primära färger
- **Kvadrat Blå**: `#1e3a8a` (HSL: 221 67% 32%) - Huvudfärg for rubriker and viktiga element
- **Kvadrat Mörkblå**: `#1e293b` (HSL: 214 32% 18%) - For text and kontrast
- **Kvadrat Ljusblå**: `#3b82f6` (HSL: 217 91% 60%) - For accenter and interaktiva element

### Sekunwherea färger
- **Neutral Grå**: `#64748b` (HSL: 215 20% 46%) - For sekunwhere text
- **Ljus Grå**: `#f1f5f9` (HSL: 214 32% 97%) - For Backgrounder
- **Vit**: `#ffffff` (HSL: 0 0% 100%) - For kort and huvudsaklig Background

### Accent and specialfärger
- **success Grön**: `#059669` (HSL: 160 84% 30%) - For statusindikationer
- **Varning Amber**: `#d97706` (HSL: 32 95% 44%) - For uppmärksamhet
- **Fel Röd**: `#dc2626` (HSL: 0 84% 51%) - For felwithdelanden

## Typografi

### Fonthierarki
- **H1**: 2.25rem (36px), font-weight: 700, line-height: 1.2
- **H2**: 1.875rem (30px), font-weight: 600, line-height: 1.3
- **H3**: 1.5rem (24px), font-weight: 600, line-height: 1.4
- **H4**: 1.25rem (20px), font-weight: 500, line-height: 1.4
- **Body**: 1rem (16px), font-weight: 400, line-height: 1.6
- **Small**: 0.875rem (14px), font-weight: 400, line-height: 1.5

### Fontfamiljer
- **Primär**: Inter, systems-ui, sans-serif
- **Monospace**: 'JetBrains Mono', Consolas, monospace

## Logotyp and visuella element

### Logotypriktlinjer
- Minsta storlek: 120px bredd
- Friytor: Minst 1x logotypens höjd at all sidor
- Färgvarianter: Mörk, ljus, and monokrom

### Visuella element
- **Rundade hörn**: 8px for kort, 4px for mindre element
- **Skuggor**: Subtila, mjuka skuggor for deep
- **Gradients**: Subtila gradienter from primär to accent

## Mallar

### Bokens framsida
- Logotyp: Övre vänster hörn
- Title: Centrerad, stor typografi
- Undertitel: Under Title, Medium storlek
- Forfattare: Längst ner
- Background: Gradient from Kvadrat Blå to Mörkblå

### Whitepapers
- Standardformat: A4
- Marginaler: 2.5cm at all sidor
- Typsnitt: Inter for rubriker, systems for text
- Färgschema: Primära färger with sparsam accent

### Presentationsmallar
- Format: 16:9 widescreen
- Masterlayout with logotyp and sidnummer
- Konsistent use of färger and typografi
- Bullet points with Kvadrat Blå accenter

### Webbplatslayout
- Responsiv design
- Enhetlig navigering
- Tydlig informationshierarki
- Optimerad for togänglighet

## Användningsriktlinjer

### Gör
- Använd konsekventa marginaler and utfyllnad
- Följ färgpaletten strikt
- Använd toräcklig kontrast for togänglighet
- Håll designen ren and professionell

### Gör not
- Blanda olika fonter utanfor systemet
- Använd färger utanfor paletten
- Överanvänd accent färger
- Glöm responsiv design

## Technical implementation

### Design Tokens
For en djupgående översikt över designtokens och hur de säkerställer att designen guidar utvecklingen, se [DESIGN_TOKENS.md](DESIGN_TOKENS.md).

### CSS Custom Properties
all färger and mått definieras that CSS custom properties for enkel underhåll.

### Tailwind Configuration
Anpassad konfiguration as matchar designsystemet.

### Komponentbibliotek
Konsistenta React-components as följer designsystemet.