import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Mail, Phone, MapPin, Home, Send, CheckCircle, User, MessageSquare, Building2 } from "lucide-react";
import { Link } from "react-router-dom";

const Contact = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    organization: "",
    subject: "",
    message: "",
    inquiryType: "general"
  });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate form submission
    setTimeout(() => {
      setIsSubmitted(true);
    }, 1000);
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const inquiryTypes = [
    { value: "general", label: "Allmän förfrågan" },
    { value: "licensing", label: "Licensiering och användning" },
    { value: "training", label: "Utbildning och workshops" },
    { value: "consulting", label: "Konsulttjänster" },
    { value: "speaking", label: "Föreläsningar och presentationer" },
    { value: "media", label: "Media och press" }
  ];

  if (isSubmitted) {
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
              <div className="flex items-center gap-2">
                <Mail className="h-5 w-5 text-primary" />
                <h1 className="text-xl font-semibold">Kontakt</h1>
              </div>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-12">
          <div className="max-w-2xl mx-auto">
            <Card className="text-center border-green-500/20 bg-green-500/5">
              <CardContent className="py-12">
                <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold mb-4">Tack för ditt meddelande!</h2>
                <p className="text-muted-foreground mb-6">
                  Vi har mottagit din förfrågan och kommer att återkomma inom 2-3 arbetsdagar.
                </p>
                <Button asChild>
                  <Link to="/">Tillbaka till startsidan</Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    );
  }

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
              <Mail className="h-5 w-5 text-primary" />
              <h1 className="text-xl font-semibold">Kontakt</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          
          {/* Page Header */}
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Kontakta oss</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Har du frågor om boken, vill diskutera konsulttjänster eller är intresserad av 
              utbildning inom Infrastructure as Code? Vi hjälper gärna till!
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            
            {/* Contact Form */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Skicka ett meddelande</CardTitle>
                  <CardDescription>
                    Fyll i formuläret nedan så återkommer vi så snart som möjligt
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    
                    {/* Inquiry Type */}
                    <div>
                      <label className="text-sm font-medium mb-2 block">Typ av förfrågan</label>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                        {inquiryTypes.map((type) => (
                          <button
                            key={type.value}
                            type="button"
                            onClick={() => handleInputChange("inquiryType", type.value)}
                            className={`p-2 text-sm border rounded-md transition-colors ${
                              formData.inquiryType === type.value
                                ? "bg-primary text-primary-foreground border-primary"
                                : "hover:bg-accent"
                            }`}
                          >
                            {type.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Personal Information */}
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="name" className="text-sm font-medium mb-2 block">
                          Namn *
                        </label>
                        <div className="relative">
                          <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                          <Input
                            id="name"
                            required
                            value={formData.name}
                            onChange={(e) => handleInputChange("name", e.target.value)}
                            className="pl-10"
                            placeholder="Ditt fullständiga namn"
                          />
                        </div>
                      </div>
                      <div>
                        <label htmlFor="email" className="text-sm font-medium mb-2 block">
                          E-post *
                        </label>
                        <div className="relative">
                          <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                          <Input
                            id="email"
                            type="email"
                            required
                            value={formData.email}
                            onChange={(e) => handleInputChange("email", e.target.value)}
                            className="pl-10"
                            placeholder="din.epost@example.com"
                          />
                        </div>
                      </div>
                    </div>

                    <div>
                      <label htmlFor="organization" className="text-sm font-medium mb-2 block">
                        Organisation
                      </label>
                      <div className="relative">
                        <Building2 className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="organization"
                          value={formData.organization}
                          onChange={(e) => handleInputChange("organization", e.target.value)}
                          className="pl-10"
                          placeholder="Ditt företag eller organisation"
                        />
                      </div>
                    </div>

                    <div>
                      <label htmlFor="subject" className="text-sm font-medium mb-2 block">
                        Ämne *
                      </label>
                      <Input
                        id="subject"
                        required
                        value={formData.subject}
                        onChange={(e) => handleInputChange("subject", e.target.value)}
                        placeholder="Kort beskrivning av din förfrågan"
                      />
                    </div>

                    <div>
                      <label htmlFor="message" className="text-sm font-medium mb-2 block">
                        Meddelande *
                      </label>
                      <div className="relative">
                        <MessageSquare className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Textarea
                          id="message"
                          required
                          value={formData.message}
                          onChange={(e) => handleInputChange("message", e.target.value)}
                          className="pl-10 min-h-[120px]"
                          placeholder="Beskriv ditt behov eller din fråga i detalj..."
                        />
                      </div>
                    </div>

                    <Button type="submit" size="lg" className="w-full gap-2">
                      <Send className="h-4 w-4" />
                      Skicka meddelande
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Contact Information */}
            <div className="space-y-6">
              
              {/* Authors Contact */}
              <Card>
                <CardHeader>
                  <CardTitle>Författarna</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold">Dr. Anna Bergström</h4>
                    <p className="text-sm text-muted-foreground">Senior Cloud Architect</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Mail className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm">anna.bergstrom@example.com</span>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold">Marcus Andersson</h4>
                    <p className="text-sm text-muted-foreground">DevOps Engineer</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Mail className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm">marcus.andersson@example.com</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Response Time */}
              <Card>
                <CardHeader>
                  <CardTitle>Svarstider</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">Allmänna frågor</Badge>
                      <span className="text-sm text-muted-foreground">2-3 arbetsdagar</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">Konsulttjänster</Badge>
                      <span className="text-sm text-muted-foreground">1-2 arbetsdagar</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">Media/Press</Badge>
                      <span className="text-sm text-muted-foreground">Samma dag</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Location */}
              <Card>
                <CardHeader>
                  <CardTitle>Baserad i Sverige</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-start gap-2">
                    <MapPin className="h-4 w-4 text-muted-foreground mt-1" />
                    <div>
                      <p className="text-sm">Stockholm, Sverige</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Vi arbetar med organisationer över hela Norden och resten av Europa
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Privacy Notice */}
              <Card className="bg-accent/5">
                <CardContent className="pt-6">
                  <p className="text-xs text-muted-foreground">
                    <strong>Integritet:</strong> Vi behandlar dina personuppgifter enligt GDPR och 
                    använder endast informationen för att svara på din förfrågan. 
                    Vi delar aldrig dina uppgifter med tredje part.
                  </p>
                </CardContent>
              </Card>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Contact;