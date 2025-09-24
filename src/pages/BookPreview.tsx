import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ChevronLeft, ChevronRight, BookOpen, Home, Eye, Loader2, Edit } from "lucide-react";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import MarkdownEditor from "@/components/MarkdownEditor";
import { useToast } from "@/hooks/use-toast";

const BookPreview = () => {
  const [currentChapter, setCurrentChapter] = useState(0);
  const [markdownContent, setMarkdownContent] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const { toast } = useToast();

  const chapters = [
    { id: "01", title: "Inledning", area: "Grundläggande konceptens" },
    { id: "02", title: "Grundläggande principer för Infrastructure as Code", area: "Systemutveckling" },
    { id: "03", title: "Versionhantering och kodstruktur", area: "Systemutveckling" },
    { id: "04", title: "Automatisering och CI/CD-pipelines", area: "Systemutveckling" },
    { id: "05", title: "Molnarkitektur som kod", area: "Arkitektur" },
    { id: "06", title: "Säkerhet i Infrastructure as Code", area: "Säkerhet" },
    { id: "07", title: "Monitering och observabilitet", area: "Systemutveckling" },
    { id: "08", title: "Skalbarhet och prestanda", area: "Arkitektur" },
    { id: "09", title: "Digitalisering genom kodbaserad infrastruktur", area: "Digitalisering" },
    { id: "10", title: "Organisatorisk förändring och teamstrukturer", area: "Organisationsutveckling" },
    { id: "11", title: "Projektledning för IaC-initiativ", area: "Projektledning" },
    { id: "12", title: "Innovation genom infrastrukturtransformation", area: "Innovation" },
    { id: "13", title: "Produktutveckling med IaC-verktyg", area: "Produkt- och tjänstutveckling" },
    { id: "14", title: "Compliance och regelefterlevnad", area: "Säkerhet" },
    { id: "15", title: "Kostnadsoptimering och resurshantering", area: "Arkitektur" },
    { id: "16", title: "Teststrategier för infrastrukturkod", area: "Systemutveckling" },
    { id: "17", title: "Migration från traditionell infrastruktur", area: "Digitalisering" },
    { id: "18", title: "Framtida trender och teknologier", area: "Innovation" },
    { id: "19", title: "Best practices och lärda läxor", area: "Styrning" },
    { id: "20", title: "Fallstudier och praktiska exempel", area: "Systemutveckling" },
    { id: "21", title: "Slutsats", area: "Sammanfattning" },
    { id: "22", title: "Ordlista", area: "Referens" },
    { id: "23", title: "Om författarna", area: "Biografi" }
  ];

  const currentChapterData = chapters[currentChapter];

  // Läs markdown-fil för aktuellt kapitel
  useEffect(() => {
    const loadMarkdown = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const chapterNumber = currentChapterData.id.padStart(2, '0');
        let fileName = '';
        
        if (currentChapterData.id === '01') {
          fileName = `01_inledning.md`;
        } else if (currentChapterData.id === '21') {
          fileName = `21_slutsats.md`;
        } else if (currentChapterData.id === '22') {
          fileName = `22_ordlista.md`;
        } else if (currentChapterData.id === '23') {
          fileName = `23_om_forfattarna.md`;
        } else {
          fileName = `${chapterNumber}_kapitel${parseInt(currentChapterData.id)}.md`;
        }
        
        const response = await fetch(`/docs/${fileName}`);
        
        if (!response.ok) {
          throw new Error(`Kunde inte läsa fil: ${fileName}`);
        }
        
        const content = await response.text();
        setMarkdownContent(content);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Fel vid läsning av kapitel');
        setMarkdownContent('');
      } finally {
        setLoading(false);
      }
    };

    loadMarkdown();
  }, [currentChapter, currentChapterData]);

  const goToPreviousChapter = () => {
    if (currentChapter > 0) {
      setCurrentChapter(currentChapter - 1);
    }
  };

  const goToNextChapter = () => {
    if (currentChapter < chapters.length - 1) {
      setCurrentChapter(currentChapter + 1);
    }
  };

  const handleEditContent = () => {
    setIsEditing(true);
  };

  const handleSaveContent = async (newContent: string) => {
    try {
      // For demo purposes, we'll just update the local state
      // In a real implementation, you'd save to your backend/file system
      setMarkdownContent(newContent);
      setIsEditing(false);
      toast({
        title: "Sparat",
        description: "Kapitlet har sparats framgångsrikt.",
      });
    } catch (err) {
      toast({
        title: "Fel",
        description: "Kunde inte spara kapitlet.",
        variant: "destructive",
      });
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-card/50 to-muted/30">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Link to="/" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                <Home className="h-4 w-4" />
                Tillbaka
              </Link>
              <div className="w-px h-6 bg-border"></div>
              <BookOpen className="h-5 w-5 text-primary" />
              <h1 className="text-xl font-bold">Bokförhandsvisning</h1>
            </div>
            <Badge variant="outline" className="font-mono">
              Kapitel {currentChapterData.id} av {chapters.length}
            </Badge>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Table of Contents Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-24">
              <CardHeader>
                <CardTitle className="text-sm flex items-center gap-2">
                  <Eye className="h-4 w-4" />
                  Innehållsförteckning
                </CardTitle>
              </CardHeader>
              <CardContent className="max-h-96 overflow-y-auto">
                <div className="space-y-1">
                  {chapters.map((chapter, index) => (
                    <button
                      key={chapter.id}
                      onClick={() => setCurrentChapter(index)}
                      className={`w-full text-left p-2 rounded-md text-sm transition-colors ${
                        index === currentChapter
                          ? "bg-primary text-primary-foreground"
                          : "hover:bg-muted"
                      }`}
                    >
                      <div className="font-medium">{chapter.id}. {chapter.title}</div>
                      <div className="text-xs opacity-70">{chapter.area}</div>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <Card className="min-h-[600px]">
              <CardHeader className="border-b">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="outline" className="font-mono">
                        Kapitel {currentChapterData.id}
                      </Badge>
                      <Badge variant="secondary" className="text-xs">
                        {currentChapterData.area}
                      </Badge>
                    </div>
                    <CardTitle className="text-2xl">{currentChapterData.title}</CardTitle>
                  </div>
                  <Button
                    onClick={handleEditContent}
                    variant="outline"
                    size="sm"
                    className="gap-2"
                  >
                    <Edit className="h-4 w-4" />
                    Redigera
                  </Button>
                </div>
              </CardHeader>
              
              <CardContent className="p-8">
                <div className="prose prose-slate max-w-none dark:prose-invert">
                  {loading ? (
                    <div className="flex items-center justify-center py-12">
                      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                      <span className="ml-2 text-muted-foreground">Läser kapitel...</span>
                    </div>
                  ) : error ? (
                    <div className="bg-destructive/10 p-6 rounded-lg border border-destructive/20">
                      <p className="text-destructive font-medium">Fel vid läsning av kapitel</p>
                      <p className="text-sm text-muted-foreground mt-2">{error}</p>
                    </div>
                  ) : markdownContent ? (
                    <ReactMarkdown 
                      components={{
                        h1: ({ children }) => <h1 className="text-3xl font-bold mt-8 mb-4 first:mt-0">{children}</h1>,
                        h2: ({ children }) => <h2 className="text-2xl font-semibold mt-6 mb-3">{children}</h2>,
                        h3: ({ children }) => <h3 className="text-xl font-semibold mt-5 mb-2">{children}</h3>,
                        p: ({ children }) => <p className="mb-4 leading-relaxed">{children}</p>,
                        ul: ({ children }) => <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>,
                        ol: ({ children }) => <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>,
                        blockquote: ({ children }) => (
                          <blockquote className="border-l-4 border-primary pl-4 my-4 italic text-muted-foreground">
                            {children}
                          </blockquote>
                        ),
                        code: ({ children, className }) => {
                          const isInline = !className;
                          return isInline ? (
                            <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono">{children}</code>
                          ) : (
                            <code className="block bg-muted p-4 rounded-lg overflow-x-auto text-sm font-mono">
                              {children}
                            </code>
                          );
                        }
                      }}
                    >
                      {markdownContent}
                    </ReactMarkdown>
                  ) : (
                    <div className="bg-muted/30 p-6 rounded-lg border-l-4 border-primary">
                      <p className="text-muted-foreground">
                        Inget innehåll tillgängligt för detta kapitel.
                      </p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between items-center mt-6">
              <Button
                variant="outline"
                onClick={goToPreviousChapter}
                disabled={currentChapter === 0}
                className="gap-2"
              >
                <ChevronLeft className="h-4 w-4" />
                Föregående kapitel
              </Button>
              
              <div className="text-sm text-muted-foreground">
                {currentChapter + 1} av {chapters.length} kapitel
              </div>
              
              <Button
                variant="outline"
                onClick={goToNextChapter}
                disabled={currentChapter === chapters.length - 1}
                className="gap-2"
              >
                Nästa kapitel
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
      
      {isEditing && (
        <MarkdownEditor
          content={markdownContent}
          title={currentChapterData.title}
          onSave={handleSaveContent}
          onCancel={handleCancelEdit}
        />
      )}
    </div>
  );
};

export default BookPreview;