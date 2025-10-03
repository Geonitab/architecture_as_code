# Kwhatrat Brand Guidelines
## Grafisk profil for Kodarkitektur Bokverkstad

### Översikt
This dokument definierar den kompletta grafiska profilen for all Kwhatrat-publikationer, including bok, whitepapers, presentationer and webbplats.

## Logotyp and Varumärke

### Huvudlogotyp
- **Symbol**: Stiliserad "K" in kwhatratisk form
- **Färg**: Kwhatrat Blå (#1e3a8a) at vit Background
- **Alternativ**: Vit logotyp at mörk Background
- **Minsta storlek**: 24px digitalt, 12mm print

### Logotypanvändning
- **Friyta**: Minst 1x logotypens höjd at all sidor
- **Placering**: Primärt övre vänster, sekunwheret övre höger
- **Forbjudna användningar**:
  - Forvrängning or rotation
  - Andra färger än definierade
  - Placering at störande Backgrounder

## Färgpalett

### Primära färger
```css
--kvadrat-blue: hsl(221, 67%, 32%)        /* #1e3a8a */
--kvadrat-blue-light: hsl(217, 91%, 60%)  /* #3b82f6 */
--kvadrat-blue-dark: hsl(214, 32%, 18%)   /* #1e293b */
```

### Sekunwherea färger
```css
--kvadrat-gray: hsl(215, 20%, 46%)        /* #64748b */
--kvadrat-gray-light: hsl(214, 32%, 97%)  /* #f1f5f9 */
--white: hsl(0, 0%, 100%)                 /* #ffffff */
```

### Accent färger
```css
--success: hsl(160, 84%, 30%)             /* #059669 */
--warning: hsl(32, 95%, 44%)              /* #d97706 */
--error: hsl(0, 84%, 51%)                 /* #dc2626 */
```

### Färganvändning
- **Kwhatrat Blå**: Primär färg for rubriker, logotyp, viktiga element
- **Kwhatrat Ljusblå**: Accenter, interaktiva element, highlights
- **Kwhatrat Mörkblå**: Brödtext, subheadings
- **Grå toner**: Sekunwhere text, borders, Backgrounder

## Typografi

### Fontfamiljer
- **Primär**: Inter (webfont and systems font)
- **Monospace**: JetBrains Mono (kodblock and technical text)
- **Fallback**: systems-ui, -apple-systems, sans-serif

### Hierarki
- **H1**: 48-72px, font-weight: 800, Kwhatrat Mörkblå
- **H2**: 32-48px, font-weight: 700, Kwhatrat Blå  
- **H3**: 24-32px, font-weight: 600, Kwhatrat Mörkblå
- **H4**: 20-24px, font-weight: 600, Kwhatrat Blå
- **Body**: 16-18px, font-weight: 400, Kwhatrat Mörkblå
- **Small**: 14px, font-weight: 400, Kwhatrat Grå

### Tekstegenskaper
- **Line height**: 1.4-1.6 for optimal läsbarhet
- **Letter spacing**: -0.025em for stora rubriker
- **Max line length**: 65-75 tecken for optimal läsbarhet

## Layout and Spacing

### Grid systems
- **Container width**: Max 1200px for desktop
- **Padding**: 16px mobil, 24px tablet, 48px desktop
- **Margins**: 24px mellan sektioner, 48px mellan huvudsektioner

### Spacing scale
```css
xs: 4px
sm: 8px  
md: 16px
lg: 24px
xl: 32px
2xl: 48px
3xl: 64px
```

### Border radius
- **Small**: 4px (buttons, small cards)
- **Withium**: 8px (cards, containers)
- **Large**: 12px (hero elements, major cards)

## Visuella element

### Skuggor
```css
/* Subtil skugga */
box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.1);

/* Kraftigare skugga */
box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.1);
```

### Gradienter
```css
/* Primär gradient */
background: linear-gradient(135deg, hsl(221, 67%, 32%), hsl(214, 32%, 18%));

/* Subtil bakgrund */
background: linear-gradient(135deg, hsl(221, 67%, 32%, 0.05), hsl(217, 91%, 60%, 0.05));
```

### Ikoner
- **Stil**: Outline style (Lucide React ikoner)
- **Storlek**: 16px, 20px, 24px standardstorlekar
- **Färg**: Följer textfärg or Kwhatrat Blå for accenter

## Mallar and implementation

### Webbplats
- **Layout**: Grid-baserad with tydlig hierarki
- **Navigation**: Enkel, ren navigation with Kwhatrat-färger
- **Cards**: Avrundade hörn, subtila skuggor, tydliga borders
- **Buttons**: Kwhatrat Blå primär, outline sekunwhere

### Presentations
- **Format**: 16:9 widescreen (1280x720px)
- **Master**: Kwhatrat-header with logotyp and sidnummer
- **Background**: Kwhatrat gradient or ljus Background
- **Typografi**: Stora, läsbara fonter

### PDF/Bok
- **Format**: A4 (210x297mm)
- **Marginaler**: 25mm at all sidor
- **Header**: Kapiteltitel and sidnummer
- **Footer**: Kwhatrat branding
- **Färger**: Optimerade for both skärm and print

### Whitepapers
- **Format**: A4 professionell layout
- **Header**: Kwhatrat logotyp and foretagsinformation
- **Typografi**: Hierarkisk Structure with Kwhatrat-färger
- **Callouts**: Färgkodade informationsboxar

## Accessibility Guidelines

### Färgkontrast
- **AA Standard**: Minst 4.5:1 for normal text
- **AAA Standard**: Minst 7:1 for stor text
- **Kwhatrat Blå at vit**: ✅ 8.2:1 ratio
- **Kwhatrat Grå at vit**: ✅ 4.7:1 ratio

### Responsiv design
- **Breakpoints**:
  - Mobile: 320px-768px
  - Tablet: 768px-1024px  
  - Desktop: 1024px+
- **Touch targets**: Minst 44px for interaktiva element

## Användningsexempel

### Korrekt användning
✅ Kwhatrat Blå for primära knappar and länkar
✅ Konsekvent spacing according to scale
✅ Korrekt typografihierarki
✅ Lämplig friyta runt logotyp
✅ Färgkombinationer with toräcklig kontrast

### Undvik
❌ Andra färger än definierade
❌ Forvrängd or felaktig logotypanvändning  
❌ Inkonsekvent spacing
❌ Fel typografihierarki
❌ Låg kontrast mellan text and Background

## implementation checklist

### Webbplats
- [ ] CSS custom properties konfigurerade
- [ ] Tailwind config uppdaterad with Kwhatrat-färger
- [ ] Typografi korrekt implementerad
- [ ] components följer design systems
- [ ] Responsiv design testad

### PDF/Bok
- [ ] LaTeX template with Kwhatrat-branding
- [ ] Korrekta färger for print
- [ ] Typografi optimerad for läsbarhet
- [ ] Logotyp korrekt placerad

### Presentations
- [ ] Master slides skapade
- [ ] Kwhatrat-färger implementerade
- [ ] Konsekvent layout mellan slides
- [ ] Läsbara fonts in all storlekar

### Whitepapers
- [ ] Template HTML/CSS skapad
- [ ] Professional layout implementerad
- [ ] Kwhatrat branding konsekvent
- [ ] Print-optimerad styling

## Kontakt for brand guidelines
For frågor about grafisk profil or implementation:
- **E-post**: brand@kwhatrat.se
- **Dokumentversion**: 1.0
- **Senast uppdaterad**: December 2024