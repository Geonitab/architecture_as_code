workspace "Architecture as Code Reference" "Curated Structurizr workspace aligned to the book's C4 guidance." {

    model {
        user = person "Digital Service User" "Citizen or customer interacting with the public-facing capabilities." {
            tags "External Person"
        }

        editor = person "Book Editor" "Curates narrative updates and approves publication-ready material." {
            tags "Internal Person"
        }

        platformEngineer = person "Platform Engineer" "Maintains the automation platform and contributes new capabilities." {
            tags "Internal Person"
        }

        aacPlatform = softwareSystem "Architecture as Code Platform" "Automates manuscript generation, diagram rendering, and publication assets." {
            tags "Core System"
        }

        analyticsService = softwareSystem "Analytics Service" "Delivers telemetry about readership and pipeline health." {
            tags "Supporting System"
        }

        paymentGateway = softwareSystem "Payment Gateway" "Processes book orders for print-on-demand partners." {
            tags "External System"
        }

        model { aacPlatform -> analyticsService "Publishes build telemetry and readership events." }
        model { paymentGateway -> analyticsService "Shares purchase signals for aggregated reporting." }

        aacPlatform {
            authoringPortal = container "Authoring Portal" "Markdown-first editorial tooling exposed to contributors." "Next.js" {
                tags "Web Application"
            }

            diagramService = container "Diagram Service" "Converts Structurizr and Mermaid definitions into publishable assets." "Node.js" {
                tags "Service"
            }

            contentPipeline = container "Content Pipeline" "Generates book artefacts, validates diagrams, and assembles releases." "Python" {
                tags "Pipeline"
            }

            knowledgeGraph = container "Knowledge Graph" "Stores relationships between chapters, diagrams, and review decisions." "Neo4j" {
                tags "Data"
            }

            observabilityHub = container "Observability Hub" "Aggregates telemetry, alerts, and architecture fitness scores." "Grafana" {
                tags "Operations"
            }

            # Container relationships
            authoringPortal -> contentPipeline "Submits chapter updates and diagram changes." "HTTPS/JSON"
            contentPipeline -> diagramService "Requests diagram renders and Structurizr exports." "gRPC"
            contentPipeline -> knowledgeGraph "Persists narrative and diagram metadata." "Bolt"
            diagramService -> knowledgeGraph "Indexes rendered diagrams for traceability." "Bolt"
            observabilityHub -> analyticsService "Synchronises usage metrics." "REST"
            observabilityHub -> knowledgeGraph "Queries historical architecture decisions." "Bolt"
            contentPipeline -> observabilityHub "Emits build and validation telemetry." "OTLP"
            authoringPortal -> observabilityHub "Displays health dashboards." "HTTPS"

            diagramService {
                dslParser = component "DSL Parser" "Validates Structurizr DSL syntax and resolves workspace fragments." "Kotlin"
                renderer = component "Diagram Renderer" "Calls Structurizr Lite for PNG/SVG generation." "Java"
                versioningAdapter = component "Versioning Adapter" "Synchronises workspace snapshots with Git repositories." "Python"
                policyEvaluator = component "Policy Evaluator" "Applies architecture fitness functions to proposed changes." "Python"

                dslParser -> renderer "Produces normalised model definitions for." 
                renderer -> versioningAdapter "Publishes rendered diagrams and metadata." 
                policyEvaluator -> dslParser "Receives parsed workspace structures." 
                policyEvaluator -> observabilityHub "Emits compliance scores." "HTTPS"
            }
        }

        analyticsService {
            reportingWarehouse = container "Reporting Warehouse" "Holds consolidated analytics events." "BigQuery"
            reportingWarehouse -> observabilityHub "Feeds curated dashboards." "Scheduled ETL"
        }

        # External interactions
        user -> authoringPortal "Reads previews and contributes errata." "Browser"
        editor -> authoringPortal "Reviews submissions and manages releases." "Browser"
        platformEngineer -> contentPipeline "Implements automation enhancements." "Git Push"
        contentPipeline -> paymentGateway "Triggers royalty reconciliation." "REST"
    }

    views {
        systemContext aacPlatform "AaC-SystemContext" "Context view showing collaborators and neighbouring systems." {
            include *
            autoLayout lr
        }

        container aacPlatform "AaC-Containers" "Container view of the Architecture as Code platform." {
            include authoringPortal
            include diagramService
            include contentPipeline
            include knowledgeGraph
            include observabilityHub
            include analyticsService
            include paymentGateway
            include user
            include editor
            include platformEngineer
            autoLayout lr
        }

        component diagramService "AaC-DiagramService" "Component view describing Structurizr automation internals." {
            include *
            autoLayout lr
        }

        dynamic aacPlatform "AaC-ChangeReview" "Dynamic view covering a diagram change review." {
            user -> authoringPortal "Submits revised workspace fragment." "Change request"
            authoringPortal -> contentPipeline "Creates pull request for workspace update." "Git integration"
            contentPipeline -> diagramService "Runs Structurizr validation job." "CI step"
            diagramService -> policyEvaluator "Executes architecture fitness functions." "Async task"
            policyEvaluator -> observabilityHub "Publishes scores and rule outcomes." "Event"
            observabilityHub -> editor "Alerts reviewers if thresholds fail." "Notification"
            editor -> authoringPortal "Requests adjustments or approves change." "Review decision"
        }

        deployment aacPlatform "AaC-Deployment" "Deployment view for production." {
            include contentPipeline
            include diagramService
            include knowledgeGraph
            include observabilityHub
            include analyticsService
            autoLayout lr
        }

        styles {
            element "Software System" {
                background "#0b3d91"
                colour "#ffffff"
                shape RoundedBox
            }
            element "Container" {
                background "#205493"
                colour "#ffffff"
            }
            element "Component" {
                background "#5778a3"
                colour "#ffffff"
            }
            element "External System" {
                background "#c4d4f2"
                colour "#1f2a44"
            }
            element "External Person" {
                background "#f4f6fc"
                colour "#1f2a44"
            }
            element "Internal Person" {
                background "#2e8540"
                colour "#ffffff"
            }
            element "Pipeline" {
                background "#7f9bb3"
                colour "#ffffff"
            }
            element "Operations" {
                background "#485c6d"
                colour "#ffffff"
            }
            element "Data" {
                background "#485c6d"
                colour "#ffffff"
                shape Cylinder
            }
            relationship "REST" {
                dashed false
                thickness 2
            }
        }
    }

    configuration {
        properties {
            structurizr.cli.version "2024.03.01"
        }
        branding {
            logo "../images/diagram_06_structurizr_overview.png"
        }
    }
}
