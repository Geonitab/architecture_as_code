import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Download, FileText, Presentation, BookOpen, Home, ExternalLink, Calendar, Users, Target } from "lucide-react";
import { Link } from "react-router-dom";

const Resources = () => {
  const bookFormats = [
    {
      title: "PDF Version",
      description: "Fullständig bok i PDF-format med alla diagram och illustrationer",
      size: "~95KB",
      format: "PDF",
      icon: BookOpen,
      downloadUrl: "#", // This would be the actual download URL
      lastUpdated: "2024-03-15"
    }
  ];

  const whitepapers = [
    {
      title: "Svenska Compliance-krav för Architecture as Code",
      description: "Omfattande guide till GDPR, MSB säkerhetskrav och andra svenska regleringar som påverkar Architecture as Code-implementationer.",
      size: "2.1 MB",
      format: "PDF",
      category: "Compliance",
      downloadUrl: "#",
      releaseDate: "2024-03-01"
    },
    {
      title: "ROI Calculator för Architecture as Code-projekt",
      description: "Excel-mall för att beräkna avkastning på investering i Architecture as Code-initiativ, anpassad för svenska organisationer.",
      size: "450 KB",
      format: "XLSX",
      category: "Business Case",
      downloadUrl: "#",
      releaseDate: "2024-02-15"
    },
    {
      title: "Architecture as Code Security Checklist",
      description: "Detaljerad säkerhetschecklista för Architecture as Code med fokus på svenska säkerhetsstandarder och best practices.",
      size: "1.8 MB",
      format: "PDF",
      category: "Säkerhet",
      downloadUrl: "#",
      releaseDate: "2024-01-20"
    },
    {
      title: "Team Readiness Assessment",
      description: "Verktyg för att bedöma organisationens mognad och redo för Architecture as Code-transformation.",
      size: "650 KB",
      format: "PDF",
      category: "Assessment",
      downloadUrl: "#",
      releaseDate: "2024-01-10"
    }
  ];

  const presentations = [
    {
      title: "Architecture as Code för svenska organisationer - Introduktion",
      description: "Grundläggande presentation om Architecture as Code och dess relevans för svenska organisationer.",
      slides: 45,
      format: "PPTX",
      category: "Introduktion",
      audience: "Ledning och IT-arkitekter",
      downloadUrl: "#",
      releaseDate: "2024-03-10"
    },
    {
      title: "Teknisk implementation av Architecture as Code",
      description: "Djupgående teknisk presentation för utvecklare och DevOps-team om praktisk implementation.",
      slides: 78,
      format: "PPTX",
      category: "Teknisk",
      audience: "Utvecklare och DevOps",
      downloadUrl: "#",
      releaseDate: "2024-02-28"
    },
    {
      title: "Säkerhet i Architecture as Code",
      description: "Specialiserad presentation om säkerhetsaspekter och compliance i Architecture as Code-miljöer.",
      slides: 56,
      format: "PPTX",
      category: "Säkerhet",
      audience: "Säkerhetsspecialister",
      downloadUrl: "#",
      releaseDate: "2024-02-05"
    },
    {
      title: "Organisatorisk förändring och Architecture as Code",
      description: "Presentation om change management och organisatoriska aspekter av Architecture as Code-transformation.",
      slides: 42,
      format: "PPTX",
      category: "Change Management",
      audience: "Projektledare och chefer",
      downloadUrl: "#",
      releaseDate: "2024-01-15"
    }
  ];

  const codeExamples = [
    {
      title: "Terraform Templates för Azure Sverige",
      description: "Färdiga Terraform-templates för vanliga svenska cloud-scenarion i Azure Sverige-regioner.",
      language: "HCL",
      category: "Templates",
      downloadUrl: "#",
      lastUpdated: "2024-03-12"
    },
    {
      title: "AWS CloudFormation för GDPR-compliance",
      description: "CloudFormation templates som säkerställer GDPR-compliance för svenska organisationer.",
      language: "YAML",
      category: "Compliance",
      downloadUrl: "#",
      lastUpdated: "2024-03-08"
    },
    {
      title: "Kubernetes Manifests med svensk lokalisering",
      description: "Kubernetes deployment manifests anpassade för svenska språk- och tidszonsinsställningar.",
      language: "YAML",
      category: "Kubernetes",
      downloadUrl: "#",
      lastUpdated: "2024-02-25"
    },
    {
      title: "Ansible Playbooks för svenska servrar",
      description: "Ansible playbooks för konfiguration av svenska språkinställningar och tidszoner.",
      language: "YAML",
      category: "Configuration",
      downloadUrl: "#",
      lastUpdated: "2024-02-10"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-card/50 to-muted/30">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
              <Home className="h-4 w-4" />
              Hem
            </Link>
            <div className="text-muted-foreground">/</div>
            <div className="flex items-center gap-2">
              <Download className="h-5 w-5 text-primary" />
              <h1 className="text-xl font-semibold">Resurser och nedladdningar</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          
          {/* Page Header */}
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Resurser och nedladdningar</h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Ladda ner boken, whitepapers, presentationer och kodexempel för att fördjupa din kunskap 
              om Architecture as Code och stödja din organisations transformation.
            </p>
          </div>

          {/* Book Downloads */}
          <section className="mb-12">
            <h3 className="text-2xl font-bold mb-6">Ladda ner boken</h3>
            <div className="grid gap-4">
              {bookFormats.map((book, index) => (
                <Card key={index} className="border-primary/20">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="p-3 bg-primary/10 rounded-lg">
                          <book.icon className="h-8 w-8 text-primary" />
                        </div>
                        <div>
                          <h4 className="text-xl font-semibold">{book.title}</h4>
                          <p className="text-muted-foreground">{book.description}</p>
                          <div className="flex items-center gap-4 mt-2">
                            <Badge variant="outline">{book.format}</Badge>
                            <span className="text-sm text-muted-foreground">{book.size}</span>
                            <span className="text-sm text-muted-foreground">Uppdaterad: {book.lastUpdated}</span>
                          </div>
                        </div>
                      </div>
                      <Button size="lg" className="gap-2">
                        <Download className="h-4 w-4" />
                        Ladda ner
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Whitepapers */}
          <section className="mb-12">
            <h3 className="text-2xl font-bold mb-6">Whitepapers och guider</h3>
            <div className="grid md:grid-cols-2 gap-6">
              {whitepapers.map((paper, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <FileText className="h-5 w-5 text-primary" />
                        <div>
                          <CardTitle className="text-lg">{paper.title}</CardTitle>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="secondary" className="text-xs">{paper.category}</Badge>
                            <Badge variant="outline" className="text-xs">{paper.format}</Badge>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground mb-4">{paper.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span>{paper.size}</span>
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {paper.releaseDate}
                        </span>
                      </div>
                      <Button variant="outline" size="sm" className="gap-2">
                        <Download className="h-3 w-3" />
                        Ladda ner
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Presentations */}
          <section className="mb-12">
            <h3 className="text-2xl font-bold mb-6">Presentationer</h3>
            <div className="grid md:grid-cols-2 gap-6">
              {presentations.map((presentation, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <Presentation className="h-5 w-5 text-primary" />
                        <div>
                          <CardTitle className="text-lg">{presentation.title}</CardTitle>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="secondary" className="text-xs">{presentation.category}</Badge>
                            <Badge variant="outline" className="text-xs">{presentation.format}</Badge>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground mb-4">{presentation.description}</p>
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center gap-2 text-sm">
                        <Target className="h-3 w-3 text-muted-foreground" />
                        <span className="text-muted-foreground">Målgrupp:</span>
                        <span>{presentation.audience}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <FileText className="h-3 w-3 text-muted-foreground" />
                        <span className="text-muted-foreground">Antal slides:</span>
                        <span>{presentation.slides}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {presentation.releaseDate}
                      </span>
                      <Button variant="outline" size="sm" className="gap-2">
                        <Download className="h-3 w-3" />
                        Ladda ner
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Code Examples */}
          <section className="mb-12">
            <h3 className="text-2xl font-bold mb-6">Kodexempel och templates</h3>
            <div className="grid md:grid-cols-2 gap-6">
              {codeExamples.map((code, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-accent/10 rounded">
                          <span className="text-xs font-mono">&lt;/&gt;</span>
                        </div>
                        <div>
                          <CardTitle className="text-lg">{code.title}</CardTitle>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="secondary" className="text-xs">{code.category}</Badge>
                            <Badge variant="outline" className="text-xs">{code.language}</Badge>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground mb-4">{code.description}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        Uppdaterad: {code.lastUpdated}
                      </span>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="gap-2">
                          <ExternalLink className="h-3 w-3" />
                          GitHub
                        </Button>
                        <Button variant="outline" size="sm" className="gap-2">
                          <Download className="h-3 w-3" />
                          ZIP
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* License Information */}
          <Card className="bg-accent/5">
            <CardHeader>
              <CardTitle>Licensinformation</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">
                Alla resurser på denna sida är licensierade under Creative Commons Attribution-ShareAlike 4.0 International License. 
                Du är fri att använda, modifiera och distribuera materialet för både kommersiella och icke-kommersiella ändamål, 
                så länge du anger ursprunglig källa och använder samma licens för deriverade verk.
              </p>
              <div className="flex items-center gap-4">
                <Badge variant="outline">CC BY-SA 4.0</Badge>
                <Link to="#" className="text-sm text-primary hover:underline flex items-center gap-1">
                  Läs mer om licensen
                  <ExternalLink className="h-3 w-3" />
                </Link>
              </div>
            </CardContent>
          </Card>

        </div>
      </main>
    </div>
  );
};

export default Resources;