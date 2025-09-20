import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BookOpen, Code, Layers, GitBranch, CheckCircle, Clock, Download } from "lucide-react";
import { Link } from "react-router-dom";

const Index = () => {
  const chapters = [
    { id: "01", title: "Introduction", area: "Fundamental concepts", status: "completed" },
    { id: "02", title: "Basic principles for Infrastructure as Code", area: "System development", status: "completed" },
    { id: "03", title: "Version control and code structure", area: "System development", status: "completed" },
    { id: "04", title: "Automation and CI/CD pipelines", area: "System development", status: "completed" },
    { id: "05", title: "Cloud architecture as code", area: "Architecture", status: "completed" },
    { id: "06", title: "Security in Infrastructure as Code", area: "Security", status: "completed" },
    { id: "07", title: "Monitoring and observability", area: "System development", status: "completed" },
    { id: "08", title: "Scalability and performance", area: "Architecture", status: "completed" },
    { id: "09", title: "Digitalization through code-based infrastructure", area: "Digitalization", status: "completed" },
    { id: "10", title: "Organizational change and team structures", area: "Organizational development", status: "completed" },
    { id: "11", title: "Project management for IaC initiatives", area: "Project management", status: "completed" },
    { id: "12", title: "Innovation through infrastructure transformation", area: "Innovation", status: "completed" },
    { id: "13", title: "Product development with IaC tools", area: "Product and service development", status: "completed" },
    { id: "14", title: "Compliance and regulatory adherence", area: "Security", status: "completed" },
    { id: "15", title: "Cost optimization and resource management", area: "Architecture", status: "completed" },
    { id: "16", title: "Testing strategies for infrastructure code", area: "System development", status: "completed" },
    { id: "17", title: "Migration from traditional infrastructure", area: "Digitalization", status: "completed" },
    { id: "18", title: "Future trends and technologies", area: "Innovation", status: "completed" },
    { id: "19", title: "Best practices and lessons learned", area: "Governance", status: "completed" },
    { id: "20", title: "Case studies and practical examples", area: "System development", status: "completed" },
    { id: "21", title: "Conclusion", area: "Summary", status: "completed" },
    { id: "22", title: "Glossary", area: "Reference", status: "completed" },
    { id: "23", title: "About the authors", area: "Biography", status: "completed" }
  ];

  const areas = [
    "System development", "Digitalization", "Product and service development", 
    "Innovation", "Architecture", "Organizational development", "Security", "Project management"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3 mb-2">
            <BookOpen className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Architecture as Code
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            A comprehensive book about Infrastructure as Code - from fundamental principles to advanced implementation
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
                <CardTitle>Project Overview</CardTitle>
              </div>
              <CardDescription>
                English edition: Comprehensive Infrastructure as Code guide
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-accent/10 p-4 rounded-lg">
                  <h3 className="font-semibold text-accent-foreground">Total chapters</h3>
                  <p className="text-2xl font-bold text-primary">{chapters.length}</p>
                </div>
                <div className="bg-secondary/10 p-4 rounded-lg">
                  <h3 className="font-semibold text-secondary-foreground">Focus areas</h3>
                  <p className="text-2xl font-bold text-primary">{areas.length}</p>
                </div>
                <div className="bg-muted/20 p-4 rounded-lg">
                  <h3 className="font-semibold text-muted-foreground">Status</h3>
                  <p className="text-2xl font-bold text-primary">In development</p>
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
                <CardTitle>Chapter Structure</CardTitle>
              </div>
              <CardDescription>
                All planned chapters for the book on architecture as code
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
                      {chapter.status === "completed" ? "Complete" : "Planned"}
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
                <CardTitle>Technical Requirements</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Markdown files for each chapter
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Pandoc-compatible files for PDF/EPUB conversion
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Python script for generating all content
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Mermaid diagrams (max 5 elements, horizontal orientation)
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full"></div>
                  Complete terminology list in English
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
                Automatic book building via GitHub Actions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">Workflow configuration</h3>
                      <p className="text-sm text-muted-foreground">GitHub Actions YAML created</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">Ready</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">Markdown files</h3>
                      <p className="text-sm text-muted-foreground">Book structure and content</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">Ready</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">GitHub repository</h3>
                      <p className="text-sm text-muted-foreground">CI/CD pipeline enabled</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">Active</Badge>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-card border rounded-lg">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <div>
                      <h3 className="font-medium">Latest translation</h3>
                      <p className="text-sm text-muted-foreground">English edition in progress</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">✓ In progress</Badge>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-accent/10 rounded-lg">
                <h4 className="font-medium mb-2">The build process will:</h4>
                <ul className="text-sm space-y-1 text-muted-foreground">
                  <li>• Convert Mermaid diagrams to PNG</li>
                  <li>• Build PDF with Pandoc and Eisvogel template</li>
                  <li>• Create automatic releases on main branch</li>
                  <li>• Save PDF as downloadable artifacts</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button size="lg" className="gap-2" variant="default" asChild>
              <Link to="/preview">
                <BookOpen className="h-4 w-4" />
                Preview book
              </Link>
            </Button>
            <Button size="lg" className="gap-2" variant="outline">
              <GitBranch className="h-4 w-4" />
              Connect to GitHub
            </Button>
            <Button size="lg" className="gap-2" variant="outline">
              <Download className="h-4 w-4" />
              Download local script
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;