import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Home, Workflow, ClipboardList, MessageSquare, Target, Users, CalendarCheck, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

const roles = [
  {
    name: "Project Manager",
    focus: "Central agent",
    description:
      "Översätter projektägarens mål till konkreta sprintmål, prioriterar backloggen och koordinerar specialistrollerna.",
    responsibilities: [
      "Bryter ned mål till sprintplaner och uppgifter",
      "Koordinerar dagliga synkar och eskalerar blockerare",
      "Sammanställer status, risker och rekommendationer till projektägaren"
    ]
  },
  {
    name: "Architect",
    focus: "Systemstruktur",
    description:
      "Säkerställer skalbar och robust systemdesign genom arkitekturprinciper, riktlinjer och visualiseringar.",
    responsibilities: [
      "Definierar referensarkitekturer och tekniska riktlinjer",
      "Granskar tekniska förslag från Requirements Analyst och Developer",
      "Samarbetar med Graphic Designer för arkitekturdiagram"
    ]
  },
  {
    name: "Requirements Analyst",
    focus: "Kravhantering",
    description:
      "Fångar, prioriterar och spårar funktionella och icke-funktionella krav genom hela leveransflödet.",
    responsibilities: [
      "Dokumenterar user stories, acceptanskriterier och prioriteringar",
      "Säkerställer spårbarhet mellan krav, design, implementation och test",
      "Genomför gap-analyser och uppdaterar kravbasen vid förändringar"
    ]
  },
  {
    name: "Designer",
    focus: "UI/UX",
    description:
      "Tar fram användarupplevelser, wireframes och interaktionsflöden som harmoniserar med varumärkesriktlinjer.",
    responsibilities: [
      "Skapar wireframes och interaktionsflöden",
      "Synkar med Developer och Quality Control för att minimera iterationer",
      "Dokumenterar designbeslut och komponentbibliotek"
    ]
  },
  {
    name: "Developer",
    focus: "Implementation",
    description:
      "Implementerar funktionalitet enligt arkitektur, design och kodstandarder med fokus på kvalitet och automation.",
    responsibilities: [
      "Levererar kod och tester i små, granskbara leveranser",
      "Integrerar lösningar med CI/CD-pipelines",
      "Rapporterar tekniska risker och hinder"
    ]
  },
  {
    name: "Quality Control",
    focus: "Kvalitetssäkring",
    description:
      "Etablerar teststrategi, driver kvalitetsgranskningar och följer upp nyckeltal för leveranskvalitet.",
    responsibilities: [
      "Underhåller enhetstest, integrationstest och e2e-test",
      "Genomför granskningar av kod, dokumentation och leveranser",
      "Rapporterar testresultat, defekter och kvalitetsindikatorer"
    ]
  },
  {
    name: "Editor",
    focus: "Dokumentation",
    description:
      "Förvaltar dokumentationens struktur, språkstandard och versionering i hela projektet.",
    responsibilities: [
      "Uppdaterar README, API-specifikationer och release-noteringar",
      "Synkroniserar med krav- och designroller för att hålla artefakter aktuella",
      "Publicerar sprintanteckningar och kunskapsbasmaterial"
    ]
  },
  {
    name: "Graphic Designer",
    focus: "Visualisering",
    description:
      "Producerar diagram och grafiska element som stödjer arkitektur- och designkommunikation.",
    responsibilities: [
      "Skapar visuella diagram i Mermaid eller PlantUML",
      "Säkerställer korrekthet i samarbete med Architect och Editor",
      "Håller ett versionshanterat bibliotek av grafiska komponenter"
    ]
  }
];

const workflowSteps = [
  "Projektägaren definierar mål, prioriteringar och accepterar leveranser.",
  "Project Manager bryter ned mål till uppgifter och koordinerar teamet.",
  "Specialistroller producerar artefakter och rapporterar status.",
  "Project Manager konsoliderar status, kvalitet och rekommendationer till projektägaren."
];

const ceremonies = [
  {
    name: "Sprintplanering",
    participants: "Projektägare, Project Manager, alla specialistroller",
    frequency: "Varannan vecka",
    outcome: "Sprintmål, åtaganden och uppdaterad backlog"
  },
  {
    name: "Daglig synk",
    participants: "Project Manager och relevanta specialistroller",
    frequency: "Dagligen",
    outcome: "Status, hinder och nästa steg"
  },
  {
    name: "Demonstration",
    participants: "Project Manager, Developer, Designer, Quality Control",
    frequency: "Varannan vecka",
    outcome: "Leveransgenomgång och demo för projektägaren"
  },
  {
    name: "Retrospektiv",
    participants: "Project Manager och hela teamet",
    frequency: "Varannan vecka",
    outcome: "Förbättringslista och åtgärdsplan"
  }
];

const reporting = [
  {
    title: "Dagliga statuskort",
    description: "Kort sammanfattning (max 5 punkter) från varje roll till Project Manager."
  },
  {
    title: "Veckovisa kvalitetsrapporter",
    description: "Quality Control levererar testresultat, defekter och kvalitetsindikatorer."
  },
  {
    title: "Sprintrapport",
    description: "Project Manager sammanställer leveranser, KPI:er och rekommenderade beslut."
  },
  {
    title: "Dokumentationslogg",
    description: "Editor uppdaterar versionslogg i docs/README.md för kunskapsspårning."
  }
];

const channels = [
  {
    name: "Projektkanal",
    purpose: "Övergripande information, sprintmål och beslut",
    tools: "Slack eller Microsoft Teams"
  },
  {
    name: "Designforum",
    purpose: "UI/UX-iterationer och diagramfeedback",
    tools: "FigJam eller Miro"
  },
  {
    name: "Tekniksync",
    purpose: "Kod- och arkitekturfrågor",
    tools: "GitHub Projects eller Linear"
  },
  {
    name: "Kvalitetsrapportering",
    purpose: "Testresultat och releasegodkännanden",
    tools: "Notion eller Confluence"
  }
];

const kpis = [
  "Ledtid från krav till release under två sprintar",
  "Testtäckning för kritiska komponenter på minst 85%",
  "Dokumentationsuppdateringar inom 24 timmar efter beslut",
  "Färre än tre blockerare per sprint"
];

const onboarding = [
  "Project Manager introducerar mål, backlogg och verktyg.",
  "Editor delar dokumentationsstandarder och åtkomst till docs/.",
  "Quality Control beskriver teststrategi och kvalitetskriterier.",
  "Architect presenterar arkitekturplan och tekniska riktlinjer.",
  "Den nya agenten redovisar sin leveransplan för nästa sprint."
];

const AIAgentTeam = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-card/50 to-muted/30">
      <header className="border-b bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <Link to="/" className="flex items-center gap-2 hover:text-foreground transition-colors">
              <Home className="h-4 w-4" />
              Hem
            </Link>
            <span>/</span>
            <span className="text-foreground font-medium">AI-agentteam</span>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto space-y-10">
          <section className="text-center space-y-4">
            <Badge variant="secondary" className="px-3 py-1">Koordinerad AI-leverans</Badge>
            <h1 className="text-4xl font-bold tracking-tight">Virtuellt AI-agentteam</h1>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              En komplett teamstruktur som arbetar i tvåveckorscykler, säkerställer spårbarhet och levererar enligt
              riktlinjerna i Architecture as Code-initiativet. Projektägaren fungerar som slutlig beslutsfattare och
              mottar sprintrapporter från Project Manager.
            </p>
          </section>

          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Workflow className="h-5 w-5 text-primary" />
                Övergripande arbetsflöde
              </CardTitle>
              <CardDescription>Fyra steg som beskriver hur teamet levererar värde i varje sprint.</CardDescription>
            </CardHeader>
            <CardContent>
              <ol className="space-y-4 text-muted-foreground">
                {workflowSteps.map((step, index) => (
                  <li key={step} className="flex gap-4 text-left">
                    <span className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary font-semibold">
                      {index + 1}
                    </span>
                    <span className="text-base text-foreground">{step}</span>
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>

          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <Users className="h-5 w-5 text-primary" />
              <h2 className="text-2xl font-semibold">Roller och ansvar</h2>
            </div>
            <div className="grid gap-6 md:grid-cols-2">
              {roles.map((role) => (
                <Card key={role.name} className="h-full border-border/60">
                  <CardHeader className="space-y-1">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-xl">{role.name}</CardTitle>
                      <Badge variant="outline" className="text-xs uppercase tracking-wide">
                        {role.focus}
                      </Badge>
                    </div>
                    <CardDescription className="text-sm text-muted-foreground">
                      {role.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      {role.responsibilities.map((item) => (
                        <li key={item} className="flex items-start gap-2">
                          <span className="mt-1 h-2 w-2 rounded-full bg-primary"></span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CalendarCheck className="h-5 w-5 text-primary" />
                Sprintceremonier
              </CardTitle>
              <CardDescription>Återkommande forum som driver fokus, transparens och kontinuerlig förbättring.</CardDescription>
            </CardHeader>
            <CardContent className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ceremoni</TableHead>
                    <TableHead>Deltagare</TableHead>
                    <TableHead>Frekvens</TableHead>
                    <TableHead>Resultat</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {ceremonies.map((ceremony) => (
                    <TableRow key={ceremony.name}>
                      <TableCell className="font-medium text-foreground">{ceremony.name}</TableCell>
                      <TableCell>{ceremony.participants}</TableCell>
                      <TableCell>{ceremony.frequency}</TableCell>
                      <TableCell>{ceremony.outcome}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <section className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <ClipboardList className="h-5 w-5 text-primary" />
                  Rapporteringsstruktur
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {reporting.map((item) => (
                  <div key={item.title} className="p-4 rounded-lg border bg-accent/10">
                    <h3 className="font-semibold text-foreground">{item.title}</h3>
                    <p className="text-sm text-muted-foreground">{item.description}</p>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5 text-primary" />
                  Kommunikationskanaler
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {channels.map((channel) => (
                  <div key={channel.name} className="p-4 rounded-lg border">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-foreground">{channel.name}</h3>
                      <Badge variant="secondary">{channel.tools}</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mt-2">{channel.purpose}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </section>

          <Card className="border-success/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-success" />
                Kvalitetsmått och KPI:er
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="grid gap-3 md:grid-cols-2 text-sm text-muted-foreground">
                {kpis.map((metric) => (
                  <li key={metric} className="flex items-start gap-2">
                    <span className="mt-1 h-2 w-2 rounded-full bg-success"></span>
                    <span>{metric}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="border-accent/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-accent" />
                Onboarding av nya agentroller
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="space-y-3 text-sm text-muted-foreground">
                {onboarding.map((step, index) => (
                  <li key={step} className="flex gap-3">
                    <span className="font-semibold text-accent">{index + 1}.</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default AIAgentTeam;
