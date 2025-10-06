import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BookOpen, Download, Users, Target, CheckCircle, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

const BookOverview = () => {
  const themes = [
    "Grundläggande Architecture as Code-principer",
    "Infrastructure as Code som praktiskt exempel",
    "Molnarkitektur som kod", 
    "Säkerhet och compliance",
    "CI/CD och automatisering",
    "Organisatorisk transformation",
    "Praktiska fallstudier"
  ];

  const targetAudience = [
    "Systemarkitekter",
    "DevOps-ingenjörer",
    "Utvecklare", 
    "Projektledare",
    "IT-chefer"
  ];

  const authors = [
    {
      name: "Gunnar Nordqvist",
      title: "Certifierad Chefsarkitekt och IT-säkerhetsspecialist"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-accent/5">
      {/* Hero Section */}
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-12">
          <div className="max-w-4xl mx-auto text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <BookOpen className="h-12 w-12 text-primary" />
              <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Arkitektur som kod
              </h1>
            </div>
            <p className="text-xl md:text-2xl text-muted-foreground mb-6">
              En omfattande bok om Architecture as Code på svenska
            </p>
            <p className="text-lg text-muted-foreground mb-8 max-w-3xl mx-auto">
              Från grundläggande principer till avancerad implementation, med fokus på praktisk tillämpning inom svenska organisationer. 
              Lär dig hur Architecture as Code kan transformera din organisation, med Infrastructure as Code som viktigt praktiskt exempel.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="gap-2" asChild>
                <Link to="/chapters">
                  <BookOpen className="h-4 w-4" />
                  Utforska kapitel
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="gap-2" asChild>
                <Link to="/resources">
                  <Download className="h-4 w-4" />
                  Ladda ner resurser
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="gap-2" asChild>
                <Link to="/ai-agent-team">
                  <Users className="h-4 w-4" />
                  AI-agentteamet
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto space-y-12">
          
          {/* Book Description */}
          <Card className="border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-primary" />
                Om boken
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg mb-6">
                Denna bok täcker Architecture as Code från grundläggande principer till avancerad implementation, 
                med fokus på praktisk tillämpning inom svenska organisationer. Infrastructure as Code behandlas som 
                ett viktigt praktiskt exempel inom den bredare Architecture as Code-ramen, med omfattande praktiska exempel 
                från svenska företag som framgångsrikt implementerat kodbaserad arkitektur.
              </p>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <Users className="h-4 w-4" />
                    Målgrupp
                  </h3>
                  <div className="space-y-2">
                    {targetAudience.map((audience, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span>{audience}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold mb-4">Vad du kommer att lära dig</h3>
                  <ul className="space-y-2 text-muted-foreground">
                    <li>• Designa och implementera omfattande IaC-lösningar</li>
                    <li>• Etablera robusta workflows för infrastrukturutveckling</li>
                    <li>• Navigera svenska compliance-krav</li>
                    <li>• Leda organisatorisk transformation</li>
                    <li>• Optimera kostnader och prestanda</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Main Themes */}
          <Card>
            <CardHeader>
              <CardTitle>Bokens huvudteman</CardTitle>
              <CardDescription>
                27 kapitel som täcker alla aspekter av Architecture as Code
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {themes.map((theme, index) => (
                  <div key={index} className="p-4 bg-accent/10 rounded-lg border">
                    <span className="font-medium">{theme}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Authors */}
          <Card>
            <CardHeader>
              <CardTitle>Författare</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                {authors.map((author, index) => (
                  <div key={index} className="p-4 bg-accent/5 rounded-lg border">
                    <h3 className="font-semibold text-lg">{author.name}</h3>
                    <p className="text-muted-foreground">{author.title}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Book Structure */}
          <Card>
            <CardHeader>
              <CardTitle>Bokens struktur och progression</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                  <h3 className="font-semibold mb-2">Del 1: Grunder</h3>
                  <p className="text-sm text-muted-foreground mb-2">Kapitel 1-4</p>
                  <p className="text-sm">Grundläggande koncept, principer och dokumentationspraxis</p>
                </div>
                
                <div className="p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                  <h3 className="font-semibold mb-2">Del 2: Teknisk implementation</h3>
                  <p className="text-sm text-muted-foreground mb-2">Kapitel 5-11</p>
                  <p className="text-sm">Automation, molnarkitektur, säkerhet och compliance</p>
                </div>
                
                <div className="p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
                  <h3 className="font-semibold mb-2">Del 3: Testning & drift</h3>
                  <p className="text-sm text-muted-foreground mb-2">Kapitel 12-15</p>
                  <p className="text-sm">Teststrategier, praktisk implementation och kostnadsoptimering</p>
                </div>
                
                <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                  <h3 className="font-semibold mb-2">Del 4: Organisation & framtid</h3>
                  <p className="text-sm text-muted-foreground mb-2">Kapitel 16-24</p>
                  <p className="text-sm">Organisationsförändring, team, digitalisering och framtidsperspektiv</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Call to Action */}
          <Card className="bg-gradient-to-r from-primary/10 to-accent/10 border-primary/20">
            <CardContent className="text-center py-8">
              <h2 className="text-2xl font-bold mb-4">Redo att börja din IaC-resa?</h2>
              <p className="text-lg text-muted-foreground mb-6">
                Utforska kapitel, ladda ner resurser eller kontakta oss för mer information
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" className="gap-2" asChild>
                  <Link to="/chapters">
                    Börja läsa
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </Button>
                <Button size="lg" variant="outline" className="gap-2" asChild>
                  <Link to="/contact">
                    Kontakta oss
                  </Link>
                </Button>
                <Button size="lg" variant="outline" className="gap-2" asChild>
                  <Link to="/ai-agent-team">
                    <Users className="h-4 w-4" />
                    Utforska AI-teamet
                  </Link>
                </Button>
              </div>
            </CardContent>
          </Card>

        </div>
      </main>
    </div>
  );
};

export default BookOverview;