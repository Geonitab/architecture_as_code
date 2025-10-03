# Version Control and Code structure

Effective version control forms the backbone in Infrastructure as Code implementations. By applying the same methods as software development to infrastructure definitions provides traceability, collaboration opportunities and quality control.

![Version Control and Code structure](images/diagram_03_kapitel2.png)

The diagram illustrates the typical flow from Git repository through branching strategy and code review to final deployment, that ensures controlled and traceable infrastructure development.

## Git-based workflow for infrastructure

Git is the standard for version control of IaC-code and enables distributed collaboration between team members. each change is documented with commit messages that describes what was changed and why, which creates a complete history of infrastructure development.

## Code organization and module structure

Well-organized code structure is crucial for maintainability and collaboration in larger IaC projects. Modular design enables reuse of infrastructure components across different projects and environments.

Sources:
- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation.