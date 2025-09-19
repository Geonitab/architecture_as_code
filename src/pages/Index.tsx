import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BookOpen, Code, Layers, GitBranch, CheckCircle, Clock, Download } from "lucide-react";

const Index = () => {
  const chapters = [
    { id: "01", title: "Inledning", area: "Grundläggande konceptens", status: "planned" },
    { id: "02", title: "Grundläggande principer för Infrastructure as Code", area: "Systemutveckling", status: "planned" },
    { id: "03", title: "Versionhantering och kodstruktur", area: "Systemutveckling", status: "planned" },
    { id: "04", title: "Automatisering och CI/CD-pipelines", area: "Systemutveckling", status: "planned" },
    { id: "05", title: "Molnarkitektur som kod", area: "Arkitektur", status: "planned" },
    { id: "06", title: "Säkerhet i Infrastructure as Code", area: "Säkerhet", status: "planned" },
    { id: "07", title: "Monitering och observabilitet", area: "Systemutveckling", status: "planned" },
    { id: "08", title: "Skalbarhet och prestanda", area: "Arkitektur", status: "planned" },
    { id: "09", title: "Digitalisering genom kodbaserad infrastruktur", area: "Digitalisering", status: "planned" },
    { id: "10", title: "Organisatorisk förändring och teamstrukturer", area: "Organisationsutveckling", status: "planned" },
    { id: "11", title: "Projektledning för IaC-initiativ", area: "Projektledning", status: "planned" },
    { id: "12", title: "Innovation genom infrastrukturtransformation", area: "Innovation", status: "planned" },
    { id: "13", title: "Produktutveckling med IaC-verktyg", area: "Produkt- och tjänstutveckling", status: "planned" },
    { id: "14", title: "Compliance och regelefterlevnad", area: "Säkerhet", status: "planned" },
    { id: "15", title: "Kostnadsoptimering och resurshantering", area: "Arkitektur", status: "planned" },
    { id: "16", title: "Teststrategier för infrastrukturkod", area: "Systemutveckling", status: "planned" },
    { id: "17", title: "Migration från traditionell infrastruktur", area: "Digitalisering", status: "planned" },
    { id: "18", title: "Framtida trender och teknologier", area: "Innovation", status: "planned" },
    { id: "19", title: "Best practices och lärda läxor", area: "Styrning", status: "planned" },
    { id: "20", title: "Fallstudier och praktiska exempel", area: "Systemutveckling", status: "planned" },
    { id: "21", title: "Slutsats", area: "Sammanfattning", status: "planned" },
    { id: "22", title: "Ordlista", area: "Referens", status: "planned" },
    { id: "23", title: "Om författarna", area: "Biografi", status: "planned" }
  ];

  const areas = [
    "Systemutveckling", "Digitalisering", "Produkt- och tjänstutveckling", 
    "Innovation", "Arkitektur", "Organisationsutveckling", "Säkerhet", "Projektledning"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3 mb-2">
            <BookOpen className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Arkitektur som kod
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            En omfattande bok om Infrastructure as Code - från grundläggande principer till avancerad implementation
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid gap-8">
          {/* Project Overview */}
          <Card className="border-primary/20">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Code className="h-5 w-5 text-primary" />
                <CardTitle>Projektöversikt</CardTitle>
              </div>
              <CardDescription>
                Iteration 1: Kapitelstruktur och planering
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-accent/10 p-4 rounded-lg">
                  <h3 className="font-semibold text-accent-foreground">Totalt kapitel</h3>
                  <p className="text-2xl font-bold text-primary">{chapters.length}</p>
                </div>
                <div className="bg-secondary/10 p-4 rounded-lg">
                  <h3 className="font-semibold text-secondary-foreground">Fokusområden</h3>
                  <p className="text-2xl font-bold text-primary">{areas.length}</p>
                </div>
                <div className="bg-muted/20 p-4 rounded-lg">
                  <h3 className="font-semibold text-muted-foreground">Status</h3>
                  <p className="text-2xl font-bold text-primary">Planering</p>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                {areas.map((area) => (
                  <Badge key={area} variant="secondary" className="text-xs">
                    {area}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Chapter Structure */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Layers className="h-5 w-5 text-primary" />
                <CardTitle>Kapitelstruktur</CardTitle>
              </div>
              <CardDescription>
                Alla planerade kapitel för boken om arkitektur som kod
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3">
                {chapters.map((chapter) => (
                  <div key={chapter.id} className="flex items-center justify-between p-3 bg-card border rounded-lg hover:bg-accent/5 transition-colors">
                    <div className="flex items-center gap-3">
                      <Badge variant="outline" className="font-mono text-xs">
                        {chapter.id}
                      </Badge>
                      <div>
                        <h3 className="font-medium">{chapter.title}</h3>
                        <p className="text-sm text-muted-foreground">{chapter.area}</p>
                      </div>
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {chapter.status === "planned" ? "Planerad" : "Klar"}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Technical Requirements */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <GitBranch className="h-5 w-5 text-primary" />
                <CardTitle>Tekniska krav</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Markdown-filer för varje kapitel
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Pandoc-kompatibla filer för PDF/EPUB konvertering
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Python-script för generering av allt innehåll
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Mermaid-diagram (max 5 element, horisontell orientering)
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Komplett termlista på svenska
                </li>
              </ul>
            </CardContent>
          </Card>

          {/* CI/CD Status */}
          <Card className="border-accent/20">
            <CardHeader>
              <div className="flex items-center gap-2">
                <GitBranch className="h-5 w-5 text-accent" />
                <CardTitle>GitHub CI/CD Status</CardTitle>
              </div>
              <CardDescription>
                Automatisk bokbygge via GitHub Actions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">Workflow konfiguration</h3>
                      <p className="text-sm text-muted-foreground">GitHub Actions YAML skapad</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">Klar</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">Markdown-filer</h3>
                      <p className="text-sm text-muted-foreground">Bokstruktur och innehåll</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">Klar</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Clock className="h-5 w-5 text-yellow-500" />
                    <div>
                      <h3 className="font-medium">GitHub repository</h3>
                      <p className="text-sm text-muted-foreground">Anslut till GitHub för CI/CD</p>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-yellow-600">Väntande</Badge>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-accent/10 rounded-lg">
                <h4 className="font-medium mb-2">Byggprocessen kommer att:</h4>
                <ul className="text-sm space-y-1 text-muted-foreground">
                  <li>• Konvertera Mermaid-diagram till PNG</li>
                  <li>• Bygga PDF med Pandoc och Eisvogel-template</li>
                  <li>• Skapa automatiska releases på main branch</li>
                  <li>• Spara PDF som downloadable artifacts</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button size="lg" className="gap-2" variant="default">
              <GitBranch className="h-4 w-4" />
              Anslut till GitHub
            </Button>
            <Button size="lg" className="gap-2" variant="outline">
              <Download className="h-4 w-4" />
              Ladda ner lokalt script
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;