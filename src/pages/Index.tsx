import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BookOpen, Code, Layers, GitBranch, CheckCircle, Clock, Download } from "lucide-react";
import { Link } from "react-router-dom";

const Index = () => {
  const chapters = [
    { id: "01", title: "Inledning", area: "Grundläggande konceptens", status: "completed" },
    { id: "02", title: "Grundläggande principer för Infrastructure as Code", area: "Systemutveckling", status: "completed" },
    { id: "03", title: "Versionhantering och kodstruktur", area: "Systemutveckling", status: "completed" },
    { id: "04", title: "Automatisering och CI/CD-pipelines", area: "Systemutveckling", status: "completed" },
    { id: "05", title: "Molnarkitektur som kod", area: "Arkitektur", status: "completed" },
    { id: "06", title: "Säkerhet i Infrastructure as Code", area: "Säkerhet", status: "completed" },
    { id: "07", title: "Monitering och observabilitet", area: "Systemutveckling", status: "completed" },
    { id: "08", title: "Skalbarhet och prestanda", area: "Arkitektur", status: "completed" },
    { id: "09", title: "Digitalisering genom kodbaserad infrastruktur", area: "Digitalisering", status: "completed" },
    { id: "10", title: "Organisatorisk förändring och teamstrukturer", area: "Organisationsutveckling", status: "completed" },
    { id: "11", title: "Projektledning för IaC-initiativ", area: "Projektledning", status: "completed" },
    { id: "12", title: "Innovation genom infrastrukturtransformation", area: "Innovation", status: "completed" },
    { id: "13", title: "Produktutveckling med IaC-verktyg", area: "Produkt- och tjänstutveckling", status: "completed" },
    { id: "14", title: "Compliance och regelefterlevnad", area: "Säkerhet", status: "completed" },
    { id: "15", title: "Kostnadsoptimering och resurshantering", area: "Arkitektur", status: "completed" },
    { id: "16", title: "Teststrategier för infrastrukturkod", area: "Systemutveckling", status: "completed" },
    { id: "17", title: "Migration från traditionell infrastruktur", area: "Digitalisering", status: "completed" },
    { id: "18", title: "Framtida trender och teknologier", area: "Innovation", status: "completed" },
    { id: "19", title: "Best practices och lärda läxor", area: "Styrning", status: "completed" },
    { id: "20", title: "Lovable för design och IT-arkitektur mockups", area: "Design och Prototyping", status: "completed" },
    { id: "21", title: "Fallstudier och praktiska exempel", area: "Systemutveckling", status: "completed" },
    { id: "22", title: "Slutsats", area: "Sammanfattning", status: "completed" },
    { id: "23", title: "Ordlista", area: "Referens", status: "completed" },
    { id: "24", title: "Om författarna", area: "Biografi", status: "completed" }
  ];

  const areas = [
    "Systemutveckling", "Digitalisering", "Produkt- och tjänstutveckling", 
    "Innovation", "Arkitektur", "Organisationsutveckling", "Säkerhet", "Projektledning"
  ];

  return (
    <div className="min-h-screen kvadrat-gradient-subtle">
      <header className="border-b bg-card/80 backdrop-blur-sm shadow-sm">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center gap-4 mb-3">
            <div className="flex items-center justify-center w-12 h-12 bg-primary rounded-lg shadow-kvadrat">
              <BookOpen className="h-7 w-7 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-foreground tracking-tight">
                Arkitektur som kod
              </h1>
              <div className="text-sm font-medium text-primary bg-primary/10 px-3 py-1 rounded-full inline-block mt-1">
                En professionell Kvadrat-publikation
              </div>
            </div>
          </div>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-4xl">
            En omfattande bok om Infrastructure as Code - från grundläggande principer till avancerad implementation.
            Utvecklad enligt Kvadrats professionella standarder för teknisk dokumentation.
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        <div className="grid gap-10">
          {/* Project Overview - Enhanced styling */}
          <Card className="shadow-kvadrat border-primary/20 bg-gradient-to-br from-card to-card/80">
            <CardHeader className="pb-6">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-12 h-12 bg-primary/10 rounded-xl border border-primary/20">
                  <Code className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <CardTitle className="text-2xl text-foreground">Projektöversikt</CardTitle>
                  <CardDescription className="text-base">
                    Iteration 2: AI-prompt utvecklad och GitHub CI/CD aktiverad
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gradient-to-br from-primary/5 to-primary/10 p-6 rounded-xl border border-primary/20">
                  <h3 className="font-semibold text-primary mb-2">Totalt kapitel</h3>
                  <p className="text-3xl font-bold text-primary">{chapters.length}</p>
                </div>
                <div className="bg-gradient-to-br from-accent/5 to-accent/10 p-6 rounded-xl border border-accent/20">
                  <h3 className="font-semibold text-accent mb-2">Fokusområden</h3>
                  <p className="text-3xl font-bold text-accent">{areas.length}</p>
                </div>
                <div className="bg-gradient-to-br from-success/5 to-success/10 p-6 rounded-xl border border-success/20">
                  <h3 className="font-semibold text-success mb-2">Status</h3>
                  <p className="text-2xl font-bold text-success">Utveckling</p>
                </div>
              </div>
              
              <div className="space-y-4">
                <h4 className="text-lg font-semibold text-foreground">Fokusområden</h4>
                <div className="flex flex-wrap gap-3">
                  {areas.map((area) => (
                    <Badge 
                      key={area} 
                      variant="secondary" 
                      className="bg-primary/10 text-primary hover:bg-primary/20 transition-all duration-200 px-3 py-1.5 text-sm font-medium"
                    >
                      {area}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Chapter Structure - Enhanced */}
          <Card className="shadow-kvadrat bg-gradient-to-br from-card to-card/80">
            <CardHeader className="pb-6">
              <div className="flex items-center gap-3">
                <div className="flex items-center justify-center w-12 h-12 bg-accent/10 rounded-xl border border-accent/20">
                  <Layers className="h-6 w-6 text-accent" />
                </div>
                <div>
                  <CardTitle className="text-2xl text-foreground">Kapitelstruktur</CardTitle>
                  <CardDescription className="text-base">
                    Alla planerade kapitel för boken om arkitektur som kod
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {chapters.map((chapter) => (
                  <div key={chapter.id} className="flex items-center justify-between p-4 bg-gradient-to-r from-card to-muted/20 border border-border rounded-xl hover:border-primary/30 hover:shadow-sm transition-all duration-200">
                    <div className="flex items-center gap-4">
                      <Badge variant="outline" className="font-mono text-sm bg-primary/5 text-primary border-primary/30 px-3 py-1">
                        {chapter.id}
                      </Badge>
                      <div>
                        <h3 className="font-semibold text-foreground text-base">{chapter.title}</h3>
                        <p className="text-sm text-muted-foreground">{chapter.area}</p>
                      </div>
                    </div>
                    <Badge variant="secondary" className="bg-success/10 text-success border-success/30 font-medium">
                      {chapter.status === "completed" ? "Klar" : "Planerad"}
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
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">GitHub repository</h3>
                      <p className="text-sm text-muted-foreground">CI/CD pipeline aktiverad</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">Aktiv</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">Senaste PR</h3>
                      <p className="text-sm text-muted-foreground">Bot.md uppdaterad med förbättrade instruktioner</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">✓ Merged</Badge>
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
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button size="lg" className="gap-2" variant="default" asChild>
              <Link to="/preview">
                <BookOpen className="h-4 w-4" />
                Förhandsgranska bok
              </Link>
            </Button>
            <Button size="lg" className="gap-2" variant="outline">
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