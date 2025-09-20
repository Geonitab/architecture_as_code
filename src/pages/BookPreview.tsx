import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ChevronLeft, ChevronRight, BookOpen, Home, Eye } from "lucide-react";
import { Link } from "react-router-dom";

const BookPreview = () => {
  const [currentChapter, setCurrentChapter] = useState(0);

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
                </div>
              </CardHeader>
              
              <CardContent className="p-8">
                <div className="prose prose-slate max-w-none">
                  <div className="bg-muted/30 p-6 rounded-lg border-l-4 border-primary">
                    <p className="text-muted-foreground mb-0">
                      <strong>Förhandsvisning:</strong> Detta är kapitel {currentChapterData.id} - {currentChapterData.title}
                    </p>
                    <p className="text-sm text-muted-foreground mt-2 mb-0">
                      Markdown-innehåll från docs/{String(currentChapterData.id).padStart(2, '0')}_kapitel{currentChapterData.id}.md skulle visas här.
                    </p>
                  </div>
                  
                  <div className="mt-8 space-y-4">
                    <h2>Exempel på innehåll</h2>
                    <p>
                      Detta kapitel behandlar {currentChapterData.title.toLowerCase()} inom ramen för Infrastructure as Code.
                      Här skulle det riktiga innehållet från markdown-filen visas med full formatering.
                    </p>
                    
                    <h3>Huvudavsnitt</h3>
                    <p>
                      Kapitlet fokuserar på {currentChapterData.area.toLowerCase()} och ger läsaren djupgående kunskap
                      inom detta område av Infrastructure as Code.
                    </p>
                    
                    <div className="bg-accent/10 p-4 rounded-lg border">
                      <h4 className="text-sm font-medium text-accent-foreground mb-2">💡 Tips</h4>
                      <p className="text-sm text-muted-foreground mb-0">
                        I den riktiga implementationen skulle markdown-innehållet läsas från docs-mappen
                        och renderas med en markdown-parser som react-markdown.
                      </p>
                    </div>
                  </div>
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
    </div>
  );
};

export default BookPreview;