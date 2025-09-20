#!/usr/bin/env python3
"""
PowerPoint Presentation Generator
Generated automatically from book content.
"""

# Note: This would require python-pptx library
# pip install python-pptx

from pptx import Presentation
from pptx.util import Inches

def create_presentation():
    """Create PowerPoint presentation with book content."""
    prs = Presentation()
    
    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Arkitektur som kod"
    subtitle.text = "En omfattande guide för svenska organisationer"
    

    # Chapter: Inledning till arkitektur som kod
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Inledning till arkitektur som kod"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Bakgrund och motivation**: Infrastructure as Code uppstod som svar på de utmaningar som organisati..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Definition och omfattning**: Infrastructure as Code definieras som praktiken att hantera och tillh..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Svenska företags IaC-resa**: Svenska organisationer har tagit olika approaches till Infrastructure..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Bokens syfte och målgrupp**: Denna bok vänder sig till systemarkitekter, utvecklare, devops-ingenj..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Teknologisk evolution och IaC**: Infrastructure as Code utvecklas kontinuerligt som response till ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Infrastructure as Code representerar en fundamental transformation från traditio..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - HashiCorp. \"Infrastructure as Code: A Guide.\" HashiCorp Learn. - AWS...."

    # Chapter: Grundläggande principer för Infrastructure as Code
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Grundläggande principer för Infrastructure as Code"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Deklarativ vs imperativ approach**: Den deklarativa approachen innebär att beskriva önskat slutläg..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Idempotens och konvergens**: Idempotens säkerställer att upprepade körningar av samma IaC-kod prod..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Immutable infrastruktur**: Principen om immutable infrastruktur innebär att infrastrukturkomponent..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Testbarhet och kvalitetssäkring**: IaC-kod ska behandlas som vilken annan kod som helst, vilket in..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Säkerhet by design**: Infrastructure as Code möjliggör implementation av security controls från bö..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: De grundläggande principerna för Infrastructure as Code - deklarativ approach, i..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Puppet Labs. \"Infrastructure as Code: A Brief Introduction.\" Puppet D..."

    # Chapter: Versionhantering och kodstruktur
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Versionhantering och kodstruktur"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Git-baserad arbetsflöde för infrastruktur**: Git utgör standarden för versionhantering av IaC-kod ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kodorganisation och modulstruktur**: Välorganiserad kodstruktur är avgörande för maintainability o..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Code review-processer för infrastruktur**: Infrastructure code review kräver specialiserade approa..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Infrastructure Change Request**: <!-- Beskriv vad som ändras och varför --> - [ ] Development......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Allmänna principer**: - Kommentarer och documentation på svenska - Resource names på engelska (för..."
    
    p = text_frame.add_paragraph()
    p.text = "• **State management och collaboration**: Terraform state management utgör en kritisk komponent för te..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: Ett verkligt exempel på hur svenska organisationer implementerar end-to-end G..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Versionhantering och kodstruktur för Infrastructure as Code kräver samma rigor o..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Atlassian. \"Git Workflows for Infrastructure as Code.\" Atlassian Git ..."

    # Chapter: Automatisering och CI/CD-pipelines
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Automatisering och CI/CD-pipelines"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **CI/CD-fundamentals för svenska organisationer**: Svenska organisationer står inför unika utmaninga..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Månadskostnader per miljö**: EOF for summary_file in cost-summary-*.txt; do......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Kostnadskontroller**: - ✅ GDPR-compliant kryptering aktiverad - ✅ Svenska data residency-krav uppf..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Rekommendationer**: 1. Använd reserved instances för production workloads 2. Aktivera auto-scaling..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Pipeline design principles**: Effektiva IaC-pipelines bygger på principerna för fail-fast feedback..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Månadskostnad**: - **Total:** ${monthlyCostSEK} SEK - **Budget:** ${maxBudget} SEK......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Kostnadsnedbrytning**: ${readFile('cost-summary.txt')}......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Rekommendationer**: - Använd Reserved Instances för production workloads - Aktivera auto-scaling f..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Automated testing strategier**: Multi-level testing strategies för IaC inkluderar syntax validatio..."
    
    p = text_frame.add_paragraph()
    p.text = "• **✅ GDPR Compliance**: - Personal data scanning: Genomförd ✅ - Data residency Sverige: Bekräftad ✅....."

    # Chapter: Molnarkitektur som kod
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Molnarkitektur som kod"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Molnleverantörers ekosystem för IaC**: Svenska organisationer står inför ett rikt utbud av molnlev..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Cloud-native IaC patterns**: Cloud-native Infrastructure as Code patterns utnyttjar molnspecifika ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Multi-cloud strategier**: Multi-cloud Infrastructure as Code strategier möjliggör distribution av ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Serverless infrastruktur**: Serverless Infrastructure as Code fokuserar på function definitions, e..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska implementationsexempel**: För att demonstrera molnarkitektur som kod i praktiken för sve..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Molnarkitektur som kod representerar en fundamental evolution av Infrastructure ..."

    # Chapter: Säkerhet i Infrastructure as Code
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Säkerhet i Infrastructure as Code"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Säkerhet inom Infrastructure as Code kräver en fundamental förskjutnin..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Security-by-design principer**: Security-by-design innebär att säkerhetshänsyn integreras från för..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Policy as Code implementation**: Policy as Code representerar paradigmskiftet från manuella säkerh..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Secrets management och data protection**: Comprehensive secrets management utgör foundationen för ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Nätverkssäkerhet och mikrosegmentering**: Network security design genom IaC möjliggör systematic i..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```hcl terraform {......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Säkerhet inom Infrastructure as Code kräver systematisk integration av säkerhets..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - NIST. \"Cybersecurity Framework för Infrastructure as Code.\" NIST Spec..."

    # Chapter: DevOps och CI/CD för Infrastructure as Code
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "DevOps och CI/CD för Infrastructure as Code"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **DevOps-kulturens betydelse för IaC**: DevOps representerar en fundamental förändring i organisator..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kontinuerlig integration för infrastrukturkod**: CI för Infrastructure as Code säkerställer att in..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Deployment automation och orchestration**: Automated deployment för infrastruktur kräver sofistike..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Monitoring och feedback loops**: Comprehensive monitoring av både infrastructure state och deploym..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml name: 'Svenska Infrastructure CI/CD'......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Compliance Status**: - ✅ GDPR-compliant kryptering aktiverad - ✅ Svenska data residency-krav uppfy..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Infrastruktur Komponenter**: $(terraform output -json | jq -r 'to_entries[] | \"- \(.key): \(.valu..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Nästa Steg**: 1. Verifiera application deployment 2. Kör smoke tests......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Test Resultat**: EOF echo \"📋 Skapar test rapport: $TEST_REPORT\"......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: DevOps och CI/CD för Infrastructure as Code skapar grunden för modern, skalbar i..."

    # Chapter: Infrastruktur som kod i praktiken
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Infrastruktur som kod i praktiken"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Implementation roadmap och strategier**: Successful IaC adoption följer vanligen en phased approac..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Tool selection och ecosystem integration**: Technology stack selection balanserar organizational r..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Production readiness och operational excellence**: Security-first approach implementerar comprehen..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Common challenges och troubleshooting**: State management complexity grows significantly som infra..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Enterprise integration patterns**: Multi-account/subscription strategies för cloud environments pr..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```hcl variable \"environment\" {......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Practical Infrastructure as Code implementation balanserar technical excellence ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - HashiCorp. \"Terraform Best Practices.\" HashiCorp Learn Platform. - AW..."

    # Chapter: Digitalisering genom kodbaserad infrastruktur
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Digitalisering genom kodbaserad infrastruktur"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Digitalisering handlar inte enbart om att införa ny teknik, utan om en..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Cloud-first strategier för svensk digitalisering**: Sverige har utvecklat en stark position inom m..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Automatisering av affärsprocesser**: IaC möjliggör automatisering som sträcker sig långt bortom tr..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Digital transformation i svenska organisationer**: Svenska organisationer genomgår för närvarande ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml terraform {......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Digitalisering genom kodbaserad infrastruktur representerar en fundamental förän..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Digitaliseringsstyrelsen. \"Digitaliseringsstrategi för Sverige.\" Rege..."

    # Chapter: Organisatorisk förändring och teamstrukturer
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Organisatorisk förändring och teamstrukturer"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Implementering av Infrastructure as Code kräver djupgående organisator..."
    
    p = text_frame.add_paragraph()
    p.text = "• **DevOps-kulturtransformation**: DevOps representerar fundamental kulturförändering från \"us vs the..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Cross-funktionella team strukturer**: Cross-functional teams för IaC implementation måste include ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kompetenshöjning och utbildning**: Comprehensive training program för IaC adoption måste cover tec..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Rollförändring och karriärutveckling**: Traditional system administrator roles evolve toward Infra..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Change management strategier**: Change management för IaC adoption måste address both technical oc..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml team_structure:......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Organisatorisk förändring utgör den mest kritiska komponenten för successful Inf..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Puppet. \"State of DevOps Report.\" Puppet Labs, 2023. - Google. \"DORA..."

    # Chapter: Containerisering och orkestrering som kod
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Containerisering och orkestrering som kod"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Container-teknologiens roll inom IaC**: Containers erbjuder application-level virtualization som p..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kubernetes som orchestration platform**: Kubernetes har emergerat som leading container orchestrat..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Service mesh och advanced networking**: Service mesh architectures som Istio och Linkerd implement..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Infrastructure automation med container platforms**: Container-native infrastructure tools som Cro..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Persistent storage och data management**: Persistent volume management för containerized applicati..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml apiVersion: apps/v1......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Containerisering och orkestrering som kod transformerar application deployment f..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Kubernetes Documentation. \"Concepts and Architecture.\" The Kubernetes..."

    # Chapter: Policy och säkerhet som kod i detalj
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Policy och säkerhet som kod i detalj"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Policy as Code transformerar hur organisationer hanterar säkerhet och ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Open Policy Agent (OPA) och Rego**: Open Policy Agent har etablerats som de facto standarden för p..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Gatekeeper och Kubernetes Policy Enforcement**: Kubernetes-miljöer kräver specialiserade policy en..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Terraform Policy Integration**: Terraform policy enforcement implementeras genom flera verktyg och..."
    
    p = text_frame.add_paragraph()
    p.text = "• **🔒 Policy Compliance Report**: **Compliance Score:** ${report.compliance_score}/100 **Violations:**..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Automatiserad Compliance Monitoring**: Kontinuerlig compliance monitoring kräver real-time övervak..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska implementationsexempel**: Verkliga implementationer av Policy as Code kräver integration..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Policy as Code representerar kritisk evolution inom Infrastructure as Code som m..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Open Policy Agent. \"Policy as Code Documentation.\" OPA Community, 202..."

    # Chapter: Microservices-arkitektur som kod
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Microservices-arkitektur som kod"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Microservices design principles för IaC**: Microservices architecture bygger på principen om loose..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Service discovery och communication patterns**: Service discovery mechanisms möjliggör dynamic loc..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Data management i distribuerade system**: Database per service pattern säkerställer data ownership..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Service mesh implementation**: Service mesh infrastructure abstracts network communication concern..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Deployment och scaling strategies**: Independent deployment capabilities för microservices kräver ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Monitoring och observability**: Distributed tracing systems som Jaeger eller Zipkin track requests..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml apiVersion: apps/v1......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Microservices-arkitektur som kod möjliggör skalbar, resilient system design geno..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Martin Fowler. \"Microservices Architecture.\" Martin Fowler's Blog. - ..."

    # Chapter: Compliance och regelefterlevnad
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Compliance och regelefterlevnad"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **AI och maskininlärning för infrastrukturautomatisering**: Artificiell intelligens revolutionerar I..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Cloud-native och serverless utveckling**: Serverless computing fortsätter att utvecklas bortom enk..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Policydriven infrastruktur och styrning**: Policy as Code blir allt mer sofistikerat med automatis..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kvantdatorer och nästa generations teknologier**: Kvantdatorers påverkan på Infrastructure as Code..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Hållbarhet och grön databehandling**: Miljöhållbarhet blir central övervägande för infrastrukturde..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```python import tensorflow as tf......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Framtida Infrastructure as Code-utveckling kommer att drivas av AI-automation, s..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - IEEE Computer Society. \"Quantum Computing Impact on Infrastructure.\" ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```python import tensorflow as tf......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Framtida Infrastructure as Code utveckling kommer att drivas av AI automation, s..."

    # Chapter: Team-struktur och kompetensutveckling för IaC
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Team-struktur och kompetensutveckling för IaC"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Organisatorisk transformation för IaC**: Traditionella organisationsstrukturer med separata utveck..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kompetensområden för IaC-specialister**: Infrastructure as Code professionals behöver hybrid skill..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Utbildningsstrategier och certifieringar**: Strukturerade utbildningsprogram kombinerar theoretica..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Agile team models för infrastructure**: Cross-functional infrastructure teams inkluderar cloud eng..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kunskapsdelning och communities of practice**: Documentation strategies för Infrastructure as Code..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Performance management och career progression**: Technical career ladders för Infrastructure as Co..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml teams:......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Technical Skills**: - [ ] Basic Git operations (clone, commit, push, pull) - [ ] Understanding of ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Soft Skills**: - [ ] Technical writing and documentation - [ ] Presentation and training delivery...."
    
    p = text_frame.add_paragraph()
    p.text = "• **Purpose**: Foster knowledge sharing, collaboration, and continuous learning in Infrastructure as C..."

    # Chapter: Kostnadsoptimering och resurshantering
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Kostnadsoptimering och resurshantering"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Kostnadsoptimering utgör en kritisk komponent i Infrastructure as Code..."
    
    p = text_frame.add_paragraph()
    p.text = "• **FinOps och cost governance**: FinOps representerar en växande disciplin som kombinerar finansiell ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Automatisk resursskalning och rightsizing**: Automatisk resursskalning utgör kärnan i kostnadseffe..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Cost monitoring och alerting**: Comprehensive cost monitoring kräver integration av monitoring-ver..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Multi-cloud cost optimization**: Multi-cloud strategier kompliserar kostnadsoptimering men erbjude..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```hcl terraform {......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Kostnadsoptimering inom Infrastructure as Code kräver systematisk approach som k..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - AWS. \"AWS Cost Optimization Guide.\" Amazon Web Services Documentation..."

    # Chapter: Teststrategier för infrastruktukod
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Teststrategier för infrastruktukod"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Testning av Infrastructure as Code skiljer sig fundamentalt från tradi..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Unit testing för infrastrukturkod**: Unit testing för Infrastructure as Code fokuserar på validati..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Integrationstesting och miljövalidering**: Integration testing för Infrastructure as Code verifier..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Security och compliance testing**: Security testing för Infrastructure as Code måste validate både..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Performance och skalbarhetstesting**: Performance testing för Infrastructure as Code fokuserar på ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```go // test/terraform_test.go......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Comprehensive testing strategies för Infrastructure as Code är essential för att..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - Terratest Documentation. \"Infrastructure Testing for Terraform.\" Grun..."

    # Chapter: Migration från traditionell infrastruktur
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Migration från traditionell infrastruktur"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Migration från traditionell, manuellt konfigurerad infrastruktur till ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Assessment och planning faser**: Comprehensive infrastructure assessment utgör foundationen för su..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Lift-and-shift vs re-architecting**: Lift-and-shift migration representerar den snabbaste vägen ti..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Gradvis kodifiering av infrastruktur**: Infrastructure inventory automation genom tools som Terraf..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Team transition och kompetensutveckling**: Skills development programs måste prepare traditional s..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```python import boto3......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Executive Summary**: - **Totalt antal resurser att migrera:** {assessment_results['summary']['tota..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Fas 1: Förberedelse (Vecka 1-2)**: - [ ] IaC grundutbildning för alla teammedlemmar - [ ] Terrafor..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Fas 2: Pilot Migration (Vecka 3-4)**: - [ ] Migrera development/test miljöer först - [ ] Validera ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Fas 3: Production Migration (Vecka 5-12)**: - [ ] Non-critical production systems - [ ] Critical s..."

    # Chapter: Framtida trender och teknologier
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Framtida trender och teknologier"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Infrastructure as Code står inför omfattande transformation driven av ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Artificiell intelligens och maskininlärning integration**: AI och ML-integration i Infrastructure ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Edge computing och distribuerad infrastruktur**: Edge computing förändrar fundamentalt hur Infrast..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sustainability och green computing**: Environmental sustainability blir allt viktigare inom Infras..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Nästa generations IaC-verktyg och paradigm**: DevOps evolution fortsätter med nya verktyg och meth..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Quantum computing påverkan på säkerhet**: Quantum computing development hotar current cryptographi..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Sammanfattning**: Framtiden för Infrastructure as Code karakteriseras av intelligent automation, e..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Källor och referenser**: - NIST. \"Post-Quantum Cryptography Standards.\" National Institute of St..."

    # Chapter: Best practices och lärda läxor
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Best practices och lärda läxor"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Övergripande beskrivning**: Infrastructure as Code best practices representerar culminationen av c..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Kod organisation och modulstruktur**: Effective code organization utgör foundationen för maintaina..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Säkerhet och compliance patterns**: Security-first design patterns have emerged as fundamental req..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Performance och skalning strategier**: Infrastructure performance optimization patterns focus på c..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Governance och policy enforcement**: Governance frameworks för Infrastructure as Code must balance..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Internationella erfarenheter och svenska bidrag**: Global best practice evolution has been signifi..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Praktiska exempel**: ```yaml governance_framework:......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Översikt**: **Kategori:** {Security/Performance/Cost/Compliance} **Svårighetsgrad:** {Beginner/Int..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Problem Statement**: {Clear description of the problem this practice solves}......"
    
    p = text_frame.add_paragraph()
    p.text = "• **Recommended Solution**: {Detailed explanation of the best practice}......"

    # Chapter: Slutsats
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Slutsats"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Viktiga lärdomar från vår IaC-resa**: Implementering av IaC kräver både teknisk excellens och orga..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Framtida utveckling och teknologiska trender**: Cloud-native technologies, edge computing och arti..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Rekommendationer för organisationer**: Baserat på vår genomgång från grundläggande principer till ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Slutord**: Infrastructure as Code representerar mer än bara teknisk evolution - det är en fundamen..."

    # Chapter: Ordlista
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Ordlista"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    

    # Chapter: Om författarna
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Om författarna"
    
    # Add key points
    text_frame = content.text_frame
    text_frame.text = "Viktiga punkter:"
    
    
    p = text_frame.add_paragraph()
    p.text = "• **Gunnar Nordqvist**: **Certifierad Chefsarkitekt och IT-säkerhetsspecialist** Gunnar Nordqvist är e..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Architecture Decision Records (ADRs)**: - Kontext och problem statement på svenska - Beslut och ra..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Runbooks för Operational Excellence**: - Step-by-step procedures för incident response - Disaster ..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Code Documentation Standards**: - Inline comments på svenska för business logic - Technical commen..."
    
    p = text_frame.add_paragraph()
    p.text = "• **Bidragsgivare och community**: **Open Source Philosophy**: Denna bok är utvecklad med open source ..."

    
    # Save presentation
    prs.save("arkitektur_som_kod_presentation.pptx")
    print("Presentation saved to presentations/arkitektur_som_kod_presentation.pptx")

if __name__ == "__main__":
    create_presentation()
