import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ChevronLeft, ChevronRight, BookOpen, Home, Eye, Loader2, FileText } from "lucide-react";
import ReactMarkdown from "react-markdown";

const ChapterDetail = () => {
  const { chapterId } = useParams<{ chapterId: string }>();
  const [markdownContent, setMarkdownContent] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const chapters = [
    { id: "01", title: "Inledning till arkitektur som kod", area: "Grundläggande koncept", filename: "01_inledning.md" },
    { id: "02", title: "Grundläggande principer för Architecture as Code", area: "Grundläggande koncept", filename: "02_grundlaggande_principer.md" },
    { id: "03", title: "Versionhantering och kodstruktur", area: "Grundläggande koncept", filename: "03_versionhantering.md" },
    { id: "04", title: "Architecture Decision Records (ADR)", area: "Grundläggande koncept", filename: "04_adr.md" },
    { id: "05", title: "Automatisering, DevOps och CI/CD för Infrastructure as Code", area: "Systemutveckling", filename: "05_automatisering_devops_cicd.md" },
    { id: "06", title: "Molnarkitektur som kod", area: "Arkitektur", filename: "06_molnarkitektur.md" },
    { id: "07", title: "Containerisering och orkestrering som kod", area: "Arkitektur", filename: "07_containerisering.md" },
    { id: "08", title: "Microservices-arkitektur som kod", area: "Arkitektur", filename: "08_microservices.md" },
    { id: "09", title: "Säkerhet i Architecture as Code", area: "Säkerhet", filename: "09_sakerhet.md" },
    { id: "10", title: "Policy och säkerhet som kod i detalj", area: "Säkerhet", filename: "10_policy_sakerhet.md" },
    { id: "11", title: "Compliance och regelefterlevnad", area: "Säkerhet", filename: "11_compliance.md" },
    { id: "12", title: "Teststrategier för infrastruktukod", area: "Systemutveckling", filename: "12_teststrategier.md" },
    { id: "13", title: "Architecture as Code i praktiken", area: "Systemutveckling", filename: "13_praktisk_implementation.md" },
    { id: "14", title: "Kostnadsoptimering och resurshantering", area: "Arkitektur", filename: "14_kostnadsoptimering.md" },
    { id: "15", title: "Migration från traditionell infrastruktur", area: "Arkitektur", filename: "15_migration.md" },
    { id: "16", title: "Organisatorisk förändring och teamstrukturer", area: "Organisationsutveckling", filename: "16_organisatorisk_forandring.md" },
    { id: "17", title: "Team-struktur och kompetensutveckling för IaC", area: "Organisationsutveckling", filename: "17_team_struktur.md" },
    { id: "18", title: "Digitalisering genom kodbaserad infrastruktur", area: "Digitalisering", filename: "18_digitalisering.md" },
    { id: "19", title: "Använd Lovable för att skapa mockups för svenska organisationer", area: "Produkt- och tjänstutveckling", filename: "19_lovable_mockups.md" },
    { id: "20", title: "Framtida trender och teknologier", area: "Innovation", filename: "20_framtida_trender.md" },
    { id: "21", title: "Best practices och lärda läxor", area: "Systemutveckling", filename: "21_best_practices.md" },
    { id: "22", title: "Slutsats", area: "Sammanfattning", filename: "22_slutsats.md" },
    { id: "23", title: "Ordlista", area: "Referenser", filename: "23_ordlista.md" },
    { id: "24", title: "Om författarna", area: "Referenser", filename: "24_om_forfattarna.md" },
    { id: "25", title: "Framtida utveckling och trender", area: "Innovation", filename: "25_framtida_utveckling.md" },
    { id: "26", title: "Appendix: Kodexempel och tekniska implementationer", area: "Referenser", filename: "26_appendix_kodexempel.md" },
    { id: "27", title: "Teknisk uppbyggnad för bokproduktion", area: "Teknik", filename: "27_teknisk_uppbyggnad.md" }
  ];

  const currentChapterIndex = chapters.findIndex(chapter => chapter.id === chapterId);
  const currentChapterData = chapters[currentChapterIndex];

  useEffect(() => {
    const loadMarkdown = async () => {
      if (!currentChapterData) {
        setError("Kapitel hittades inte");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        // Try to fetch from the docs directory
        const response = await fetch(`/docs/${currentChapterData.filename}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const content = await response.text();
        setMarkdownContent(content);
      } catch (err) {
        console.error("Failed to load markdown:", err);
        setError("Kunde inte ladda kapitelinnehållet. Försök igen senare.");
        // Fallback content for demonstration
        setMarkdownContent(`
# ${currentChapterData.title}

*Kapitel ${currentChapterData.id} - ${currentChapterData.area}*

![Kapiteldiagram](images/diagram_${currentChapterData.id}_${currentChapterData.filename.split('_')[1]?.split('.')[0] || 'kapitel'}.png)

Det här kapitlet täcker viktiga aspekter av Infrastructure as Code inom området **${currentChapterData.area}**.

## Översikt

Detta kapitel ger en djupgående förklaring av koncepten och metoderna inom detta specifika område av Infrastructure as Code.

## Nyckelämnen

- Grundläggande principer och koncept
- Praktiska implementationsstrategier  
- Best practices och rekommendationer
- Svenska compliance-krav och anpassningar
- Verktyg och teknologier
- Exempel och fallstudier

## Praktisk tillämpning

Kapitlet innehåller konkreta exempel och kodexempel som kan användas direkt i svenska organisationer.

## Sammanfattning

Detta kapitel ger läsaren de verktyg och kunskaper som behövs för att framgångsrikt implementera dessa aspekter av Infrastructure as Code.

---

*För mer information och praktiska exempel, se de relaterade kapitlen i boken.*
        `);
      } finally {
        setLoading(false);
      }
    };

    loadMarkdown();
  }, [currentChapterData]);

  const goToPreviousChapter = () => {
    if (currentChapterIndex > 0) {
      const prevChapter = chapters[currentChapterIndex - 1];
      return `/chapter/${prevChapter.id}`;
    }
    return null;
  };

  const goToNextChapter = () => {
    if (currentChapterIndex < chapters.length - 1) {
      const nextChapter = chapters[currentChapterIndex + 1];
      return `/chapter/${nextChapter.id}`;
    }
    return null;
  };

  if (!currentChapterData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-card/50 to-muted/30">
        <header className="border-b bg-card/80 backdrop-blur-sm">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center gap-3">
              <Link to="/" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                <Home className="h-4 w-4" />
                Hem
              </Link>
              <div className="text-muted-foreground">/</div>
              <Link to="/chapters" className="text-muted-foreground hover:text-foreground transition-colors">
                Kapitel
              </Link>
            </div>
          </div>
        </header>
        <main className="container mx-auto px-4 py-12">
          <Card>
            <CardContent className="text-center py-12">
              <h2 className="text-2xl font-bold mb-4">Kapitel hittades inte</h2>
              <p className="text-muted-foreground mb-6">Det begärda kapitlet kunde inte hittas.</p>
              <Button asChild>
                <Link to="/chapters">Tillbaka till kapitel</Link>
              </Button>
            </CardContent>
          </Card>
        </main>
      </div>
    );
  }

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
              <Link to="/chapters" className="text-muted-foreground hover:text-foreground transition-colors">
                Kapitel
              </Link>
              <div className="text-muted-foreground">/</div>
              <div className="flex items-center gap-2">
                <FileText className="h-4 w-4 text-primary" />
                <span className="font-medium">{currentChapterData.id}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-xs">
                {currentChapterData.area}
              </Badge>
              <Badge variant="outline" className="text-xs">
                Kapitel {currentChapterData.id}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          
          {/* Chapter Header */}
          <div className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <Badge variant="outline" className="font-mono">
                Kapitel {currentChapterData.id}
              </Badge>
              <Badge variant="secondary">
                {currentChapterData.area}
              </Badge>
            </div>
            <h1 className="text-3xl font-bold mb-2">{currentChapterData.title}</h1>
            <p className="text-muted-foreground">
              Kapitel {currentChapterIndex + 1} av {chapters.length} i "Arkitektur som kod"
            </p>
          </div>

          {/* Content */}
          <Card className="mb-8">
            <CardContent className="p-8">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                  <span className="ml-2 text-muted-foreground">Laddar kapitel...</span>
                </div>
              ) : error ? (
                <div className="text-center py-12">
                  <p className="text-destructive mb-4">{error}</p>
                  <Button onClick={() => window.location.reload()}>
                    Försök igen
                  </Button>
                </div>
              ) : (
                <div className="prose prose-lg max-w-none">
                  <ReactMarkdown
                    components={{
                      img: ({ node, ...props }) => (
                        <img 
                          {...props} 
                          className="max-w-full h-auto rounded-lg shadow-md my-6"
                          style={{ maxHeight: '500px', objectFit: 'contain' }}
                        />
                      ),
                      h1: ({ node, ...props }) => (
                        <h1 {...props} className="text-3xl font-bold mb-6 text-foreground" />
                      ),
                      h2: ({ node, ...props }) => (
                        <h2 {...props} className="text-2xl font-semibold mb-4 mt-8 text-foreground" />
                      ),
                      h3: ({ node, ...props }) => (
                        <h3 {...props} className="text-xl font-semibold mb-3 mt-6 text-foreground" />
                      ),
                      p: ({ node, ...props }) => (
                        <p {...props} className="mb-4 text-foreground leading-relaxed" />
                      ),
                      code: ({ node, ...props }) => (
                        <code {...props} className="bg-muted px-2 py-1 rounded text-sm font-mono" />
                      ),
                      pre: ({ node, ...props }) => (
                        <pre {...props} className="bg-muted p-4 rounded-lg overflow-x-auto mb-4" />
                      ),
                      ul: ({ node, ...props }) => (
                        <ul {...props} className="list-disc list-inside mb-4 space-y-2" />
                      ),
                      ol: ({ node, ...props }) => (
                        <ol {...props} className="list-decimal list-inside mb-4 space-y-2" />
                      ),
                      blockquote: ({ node, ...props }) => (
                        <blockquote {...props} className="border-l-4 border-primary pl-4 italic my-4" />
                      )
                    }}
                  >
                    {markdownContent}
                  </ReactMarkdown>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Navigation */}
          <div className="flex justify-between items-center">
            <div>
              {goToPreviousChapter() && (
                <Button variant="outline" className="gap-2" asChild>
                  <Link to={goToPreviousChapter()!}>
                    <ChevronLeft className="h-4 w-4" />
                    Föregående kapitel
                  </Link>
                </Button>
              )}
            </div>
            
            <div className="text-center">
              <div className="text-sm text-muted-foreground mb-2">
                Kapitel {currentChapterIndex + 1} av {chapters.length}
              </div>
              <Button variant="outline" size="sm" asChild>
                <Link to="/chapters">
                  <BookOpen className="h-4 w-4 mr-2" />
                  Alla kapitel
                </Link>
              </Button>
            </div>
            
            <div>
              {goToNextChapter() && (
                <Button variant="outline" className="gap-2" asChild>
                  <Link to={goToNextChapter()!}>
                    Nästa kapitel
                    <ChevronRight className="h-4 w-4" />
                  </Link>
                </Button>
              )}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
};

export default ChapterDetail;