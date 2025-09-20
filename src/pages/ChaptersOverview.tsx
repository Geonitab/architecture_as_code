import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookOpen, Home, Search, Eye, Filter } from "lucide-react";
import { Link } from "react-router-dom";

const ChaptersOverview = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedArea, setSelectedArea] = useState<string>("all");

  const chapters = [
    { 
      id: "01", 
      title: "Inledning till arkitektur som kod", 
      area: "Grundläggande koncept",
      summary: "En introduktion till Infrastructure as Code och dess fundamentala principer. Täcker bakgrund, motivation och definierar omfattningen för kodbaserad infrastruktur.",
      keyTopics: ["IaC definition", "Traditionella utmaningar", "Svenska drivkrafter", "Compliance krav"]
    },
    { 
      id: "02", 
      title: "Grundläggande principer för Infrastructure as Code", 
      area: "Grundläggande koncept",
      summary: "Fundamentala principer som säkerställer framgångsrik IaC-implementation. Fokus på deklarativ approach, versionskontroll och automatisering.",
      keyTopics: ["Deklarativ vs imperativ", "Versionskontroll", "Automatisering", "Reproducerbarhet"]
    },
    { 
      id: "03", 
      title: "Versionhantering och kodstruktur", 
      area: "Systemutveckling",
      summary: "Best practices för att strukturera och versionshantera infrastrukturkod. Inkluderar Git workflows och kodorganisation.",
      keyTopics: ["Git workflows", "Kodstruktur", "Branching strategies", "Collaboration"]
    },
    { 
      id: "04", 
      title: "Architecture Decision Records (ADR)", 
      area: "Grundläggande koncept",
      summary: "Strukturerad metod för att dokumentera viktiga arkitekturbeslut. Täcker ADR-format, verktyg och integration med Infrastructure as Code.",
      keyTopics: ["Decision documentation", "ADR structure", "Architectural governance", "Compliance tracking"]
    },
    { 
      id: "05", 
      title: "Automatisering och CI/CD-pipelines", 
      area: "Systemutveckling",
      summary: "Implementering av automatiserade CI/CD-pipelines för infrastrukturkod. Täcker testing, validation och deployment strategies.",
      keyTopics: ["CI/CD pipelines", "Automated testing", "Deployment strategies", "Quality gates"]
    },
    { 
      id: "06", 
      title: "Molnarkitektur som kod", 
      area: "Arkitektur",
      summary: "Designprinciper för molnbaserad infrastruktur som kod. Fokus på skalbarhet, resiliens och multi-cloud strategier.",
      keyTopics: ["Cloud design patterns", "Multi-cloud", "Skalbarhet", "Resiliens"]
    },
    { 
      id: "07", 
      title: "Säkerhet i Infrastructure as Code", 
      area: "Säkerhet",
      summary: "Säkerhetsaspekter och best practices för IaC. Inkluderar secrets management, compliance och security scanning.",
      keyTopics: ["Security by design", "Secrets management", "Compliance", "Vulnerability scanning"]
    },
    { 
      id: "08", 
      title: "Monitering och observabilitet", 
      area: "Systemutveckling",
      summary: "Implementering av omfattande monitoring och observabilitet för kodbaserad infrastruktur.",
      keyTopics: ["Monitoring strategies", "Observability", "Alerting", "Performance metrics"]
    },
    { 
      id: "09", 
      title: "Skalbarhet och prestanda", 
      area: "Arkitektur",
      summary: "Tekniker för att säkerställa skalbar och högpresterande infrastruktur genom kod.",
      keyTopics: ["Auto-scaling", "Performance optimization", "Load balancing", "Resource management"]
    },
    { 
      id: "10", 
      title: "Digitalisering genom kodbaserad infrastruktur", 
      area: "Digitalisering",
      summary: "Hur IaC möjliggör och accelererar digital transformation inom svenska organisationer.",
      keyTopics: ["Digital transformation", "Innovation", "Business agility", "Competitive advantage"]
    },
    { 
      id: "11", 
      title: "Organisatorisk förändring och teamstrukturer", 
      area: "Organisationsutveckling",
      summary: "Hantering av organisatoriska förändringar vid IaC-implementation. Fokus på team dynamics och cultural change.",
      keyTopics: ["Change management", "Team structures", "Cultural transformation", "Skills development"]
    },
    { 
      id: "12", 
      title: "Projektledning för IaC-initiativ", 
      area: "Projektledning",
      summary: "Projektledningsmetodiker och best practices för framgångsrika IaC-implementationer.",
      keyTopics: ["Project planning", "Risk management", "Stakeholder engagement", "Success metrics"]
    },
    { 
      id: "13", 
      title: "Innovation genom infrastrukturtransformation", 
      area: "Innovation",
      summary: "Hur IaC möjliggör innovation och snabbare time-to-market för nya produkter och tjänster.",
      keyTopics: ["Innovation frameworks", "Rapid prototyping", "Experimentation", "Technology adoption"]
    },
    { 
      id: "14", 
      title: "Produktutveckling med IaC-verktyg", 
      area: "Produkt- och tjänstutveckling",
      summary: "Integration av IaC i produktutvecklingsprocesser för snabbare och mer tillförlitliga releases.",
      keyTopics: ["Product development", "DevOps integration", "Release management", "Quality assurance"]
    },
    { 
      id: "15", 
      title: "Compliance och regelefterlevnad", 
      area: "Säkerhet",
      summary: "Säkerställande av compliance med svenska och europeiska regleringar genom kodbaserad infrastruktur.",
      keyTopics: ["GDPR compliance", "Regulatory requirements", "Audit trails", "Data sovereignty"]
    },
    { 
      id: "16", 
      title: "Kostnadsoptimering och resurshantering", 
      area: "Arkitektur",
      summary: "Strategier för kostnadsoptimering och effektiv resurshantering genom IaC.",
      keyTopics: ["Cost optimization", "Resource management", "Budget control", "ROI measurement"]
    },
    { 
      id: "17", 
      title: "Teststrategier för infrastrukturkod", 
      area: "Systemutveckling",
      summary: "Omfattande teststrategier för att säkerställa kvalitet och tillförlitlighet i infrastrukturkod.",
      keyTopics: ["Testing strategies", "Test automation", "Quality gates", "Validation frameworks"]
    },
    { 
      id: "18", 
      title: "Hybridmolnstrategier", 
      area: "Arkitektur",
      summary: "Design och implementation av hybridmolnlösningar med kodbaserad infrastruktur.",
      keyTopics: ["Hybrid cloud", "On-premises integration", "Data governance", "Connectivity"]
    },
    { 
      id: "19", 
      title: "Framtida trender och teknologier", 
      area: "Innovation",
      summary: "Emerging technologies och framtida trender inom Infrastructure as Code.",
      keyTopics: ["Emerging technologies", "Future trends", "Technology roadmaps", "Industry evolution"]
    },
    { 
      id: "20", 
      title: "Best practices och lärda läxor", 
      area: "Systemutveckling",
      summary: "Sammanställning av best practices och viktiga lärdomar från framgångsrika IaC-implementationer.",
      keyTopics: ["Best practices", "Lessons learned", "Success factors", "Common pitfalls"]
    },
    { 
      id: "21", 
      title: "Fallstudier och praktiska exempel", 
      area: "Praktisk tillämpning",
      summary: "Detaljerade fallstudier från svenska organisationer som framgångsrikt implementerat Infrastructure as Code.",
      keyTopics: ["Case studies", "Real-world examples", "Implementation journeys", "Results achieved"]
    },
    { 
      id: "22", 
      title: "Slutsats", 
      area: "Sammanfattning",
      summary: "Sammanfattning av bokens huvudbudskap och rekommendationer för framtida IaC-arbete.",
      keyTopics: ["Key takeaways", "Future recommendations", "Action items", "Next steps"]
    },
    { 
      id: "23", 
      title: "Ordlista", 
      area: "Referenser",
      summary: "Omfattande ordlista med definitioner av termer och begrepp inom Infrastructure as Code.",
      keyTopics: ["Terminology", "Definitions", "Glossary", "Technical terms"]
    },
    { 
      id: "24", 
      title: "Om författarna", 
      area: "Referenser",
      summary: "Information om bokens författare och deras bakgrund inom Infrastructure as Code.",
      keyTopics: ["Author bios", "Professional background", "Expertise", "Contributions"]
    }
  ];

  const areas = ["all", ...Array.from(new Set(chapters.map(chapter => chapter.area)))];

  const filteredChapters = chapters.filter(chapter => {
    const matchesSearch = chapter.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         chapter.summary.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesArea = selectedArea === "all" || chapter.area === selectedArea;
    return matchesSearch && matchesArea;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-card/50 to-muted/30">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Link to="/" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                <Home className="h-4 w-4" />
                Hem
              </Link>
              <div className="text-muted-foreground">/</div>
              <div className="flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-primary" />
                <h1 className="text-xl font-semibold">Bokens kapitel</h1>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          
          {/* Page Header */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold mb-4">Utforska alla kapitel</h2>
            <p className="text-lg text-muted-foreground mb-6">
              Bläddra genom bokens 23 kapitel och upptäck djupgående innehåll om Infrastructure as Code
            </p>
            
            {/* Search and Filter */}
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Sök i kapitel..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-muted-foreground" />
                <select
                  value={selectedArea}
                  onChange={(e) => setSelectedArea(e.target.value)}
                  className="px-3 py-2 border rounded-md bg-background"
                >
                  {areas.map(area => (
                    <option key={area} value={area}>
                      {area === "all" ? "Alla områden" : area}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Chapters Grid */}
          <div className="grid gap-6">
            {filteredChapters.map((chapter) => (
              <Card key={chapter.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <Badge variant="outline" className="font-mono text-sm">
                        {chapter.id}
                      </Badge>
                      <div>
                        <CardTitle className="text-xl">{chapter.title}</CardTitle>
                        <CardDescription className="mt-1">
                          <Badge variant="secondary" className="text-xs">
                            {chapter.area}
                          </Badge>
                        </CardDescription>
                      </div>
                    </div>
                    <Button variant="outline" size="sm" className="gap-2" asChild>
                      <Link to={`/chapter/${chapter.id}`}>
                        <Eye className="h-4 w-4" />
                        Läs kapitel
                      </Link>
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">{chapter.summary}</p>
                  
                  <div>
                    <h4 className="font-medium mb-2">Nyckelämnen:</h4>
                    <div className="flex flex-wrap gap-2">
                      {chapter.keyTopics.map((topic, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {topic}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {filteredChapters.length === 0 && (
            <Card>
              <CardContent className="text-center py-8">
                <p className="text-muted-foreground">Inga kapitel hittades som matchar dina sökkriterier.</p>
              </CardContent>
            </Card>
          )}

        </div>
      </main>
    </div>
  );
};

export default ChaptersOverview;