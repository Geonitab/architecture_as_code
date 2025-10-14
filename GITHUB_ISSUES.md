# GitHub Issues for Architecture as Code Book Improvements

This document contains GitHub issues to be created based on feedback for improving the Architecture as Code book. All issues are written in English.

---

## Issue 1: Add Management as Code to Introduction Chapter

**Title:** Add Management as Code as one of the core aspects in Introduction chapter

**Labels:** documentation, enhancement

**Description:**

The Introduction chapter (01_introduction.md) should include "Management as Code" as one of the different aspects of Architecture as Code methodology.

**Current State:**
The introduction mentions various "as Code" practices (Requirements as Code, Compliance as Code, Documentation as Code, Design as Code, Infrastructure as Code) but does not explicitly highlight Management as Code.

**Requested Change:**
Add Management as Code to the list of interconnected aspects, given that chapter 19 extensively covers this topic. This should be reflected in:
- The text describing the Architecture as Code scope
- The Architecture as Code Flow diagram if applicable
- Any enumeration of the different aspects

**Acceptance Criteria:**
- [ ] Management as Code is mentioned in the introduction text
- [ ] The concept is properly integrated with other "as Code" aspects
- [ ] Reference to Chapter 19 is added where appropriate

**Files to Update:**
- `docs/01_introduction.md`
- Potentially `docs/images/diagram_01_aac_flow.mmd` or related diagram

---

## Issue 2: Make ADR Lifecycle Diagram Vertical

**Title:** Convert ADR lifecycle diagram from horizontal to vertical orientation

**Labels:** documentation, design, enhancement

**Description:**

The ADR lifecycle diagram in the ADR chapter needs to be reoriented from horizontal to vertical layout for better readability and consistency with other diagrams in the book.

**Current State:**
The ADR lifecycle diagram (referenced at line 77 in `docs/04_adr.md`) appears to have a horizontal orientation.

**Requested Change:**
Redesign the diagram with a vertical flow, showing the lifecycle stages:
- Proposed → Accepted → Deprecated/Superseded

This vertical orientation will make it easier to follow the progression and better fit the page layout.

**Acceptance Criteria:**
- [ ] Diagram flows top to bottom instead of left to right
- [ ] All lifecycle states are clearly visible
- [ ] Transitions between states are clearly marked
- [ ] The diagram maintains consistency with the book's visual style

**Files to Update:**
- `docs/images/diagram_04_adr_lifecycle.png` or corresponding `.mmd` file
- Verify the reference in `docs/04_adr.md` still works correctly

---

## Issue 3: Replace Sweden-Focused ADR Example

**Title:** Replace Example 2 in ADR chapter with internationally relevant example

**Labels:** documentation, content, internationalization

**Description:**

The ADR chapter contains "Example 2: Security Architecture for Swedish Organisations" which is too focused on Swedish-specific regulations and requirements. This should be replaced with a more internationally applicable example.

**Current State:**
Example 2 in the ADR chapter (around line 260 in `docs/04_adr.md`) focuses specifically on Swedish organizations and their compliance requirements.

**Requested Change:**
Replace Example 2 with a security architecture decision example that:
- Addresses universal security concerns (e.g., zero trust architecture, cloud security, API security)
- Applies to organizations globally, not just Sweden
- Maintains the same educational value and depth
- Uses international standards (ISO 27001, NIST frameworks) rather than country-specific regulations

**Suggested Topics for New Example:**
- Choosing between different authentication methods (OAuth2 vs SAML)
- Selecting a secrets management solution
- Implementing zero trust network architecture
- API gateway selection for microservices

**Acceptance Criteria:**
- [ ] New example does not focus on Sweden-specific regulations
- [ ] Example maintains similar structure and depth as current Example 1
- [ ] References international standards and best practices
- [ ] Code examples and templates are universally applicable

**Files to Update:**
- `docs/04_adr.md` (Example 2 section)

---

## Issue 4: Remove infrastructure/ Prefix from ADR Git Structure Example

**Title:** Remove infrastructure/ directory from ADR git structure example

**Labels:** documentation, content, enhancement

**Description:**

The git repository structure example in the ADR chapter includes an `infrastructure/` directory prefix that should be removed for simplicity and broader applicability.

**Current State:**
The git structure example in the ADR chapter likely shows ADR files organized under an `infrastructure/` directory.

**Requested Change:**
Simplify the directory structure example to show ADR files at a more logical level, such as:
- `docs/adr/` or
- `adr/` at the root level or
- `architecture/decisions/`

This makes the structure applicable to more project types, not just infrastructure-focused projects.

**Acceptance Criteria:**
- [ ] Git structure example no longer includes `infrastructure/` prefix
- [ ] New structure is clearly documented and logical
- [ ] Any code examples or references are updated accordingly

**Files to Update:**
- `docs/04_adr.md` (Git Integration and Workflow section)

---

## Issue 5: Remove Sweden-Focused Content from ADR Chapter

**Title:** Internationalize ADR chapter by removing Sweden-specific content

**Labels:** documentation, content, internationalization

**Description:**

The ADR chapter contains multiple references to Swedish organizations, regulations, and specific Swedish requirements that limit the book's international applicability.

**Current State:**
The ADR chapter (docs/04_adr.md) includes:
- References to "Swedish organizations" specifically
- Swedish digitalisation strategy mentions
- Swedish-specific compliance requirements
- Swedish Authority for Privacy Protection (Integritetsskyddsmyndigheten)

**Requested Change:**
Replace Sweden-specific content with:
- Generic references to "organizations" or "enterprises"
- International regulations and frameworks (GDPR at EU level, ISO standards)
- Universal compliance and governance examples
- Best practices applicable globally

Where regional examples are needed, provide diverse examples from multiple regions or keep examples generic.

**Acceptance Criteria:**
- [ ] All references to "Swedish organizations" are replaced with generic terms
- [ ] Swedish-specific regulations are replaced with international equivalents
- [ ] Examples are internationally applicable
- [ ] The chapter maintains its educational value and depth

**Files to Update:**
- `docs/04_adr.md` (throughout the chapter)

**Related Issues:** This is part of a broader internationalization effort across the book.

---

## Issue 6: Make Timeline Diagram Taller for Better Readability

**Title:** Increase height of Architecture as Code implementation timeline diagram

**Labels:** documentation, design, enhancement

**Description:**

The Gantt timeline diagram showing the Architecture as Code implementation timeline needs to be made taller to improve readability.

**Current State:**
The timeline diagram (`docs/images/diagram_05_gantt_timeline.mmd`) is referenced in the Automation chapter and shows phases 1-3 of implementation, but the current height makes it difficult to read clearly.

**Requested Change:**
Redesign the diagram with:
- Increased vertical spacing between timeline items
- Larger font sizes for phase names and task descriptions
- More vertical space for each phase section
- Better visibility of dates and durations

Consider:
- Increasing the overall diagram height
- Adjusting the bar heights in the Gantt chart
- Improving label positioning and font sizes

**Acceptance Criteria:**
- [ ] Diagram is clearly readable when rendered in the book
- [ ] All text labels are easily legible
- [ ] Phase sections are clearly distinguished
- [ ] Timeline dates and durations are clear

**Files to Update:**
- `docs/images/diagram_05_gantt_timeline.mmd`
- Regenerate corresponding PNG if it exists

---

## Issue 7: Split Automation Chapter into Smaller Focused Chapters

**Title:** Restructure Automation chapter by splitting into multiple focused chapters

**Labels:** documentation, content, restructuring, major

**Description:**

The Automation, DevOps and CI/CD chapter (`docs/05_automation_devops_cicd.md`) is currently too large and covers too many distinct topics. It should be split into smaller, more focused chapters.

**Current State:**
The chapter is ~663 lines and covers:
- CI/CD fundamentals
- DevOps practices
- Governance as Code (extensive section)
- GDPR compliance
- CI/CD pipelines for Architecture as Code
- Swedish-specific content

**Requested Changes:**

### 1. Create New Chapter: Governance as Code
Extract the "Governance as Code" sections from the current chapter into a dedicated chapter. This content appears in:
- "Deep dive: Governance as Code in practice" section
- "Policy lifecycle automation and continuous assurance" section
- "Measuring and iterating on governance value" section

The new chapter should:
- Expand on governance principles
- Provide comprehensive examples
- Link to related chapters (Policy and Security, Compliance)

### 2. Create New Chapter: GDPR and Data Protection
Extract GDPR-specific content into a separate chapter focused on data protection compliance:
- GDPR requirements in Architecture as Code
- Data residency and sovereignty
- Privacy by design principles
- Automated compliance checking

Note: Make this chapter internationally focused by covering other data protection frameworks too (CCPA, etc.)

### 3. Create New Chapter: CI/CD Pipelines for Architecture as Code
Extract the CI/CD pipeline implementation details:
- Architecture as Code pipeline architecture
- Pipeline stages and automation
- Testing in pipelines
- Deployment strategies

### 4. Streamline Core Chapter
The remaining `05_automation_devops_cicd.md` should focus on:
- Core CI/CD and DevOps concepts
- Automation theory and principles
- DevOps culture and practices
- Integration with Architecture as Code

**Acceptance Criteria:**
- [ ] New chapter created: Governance as Code (suggest `11_governance_as_code.md` or similar)
- [ ] New chapter created: GDPR and Data Protection (suggest `12_gdpr_data_protection.md`)
- [ ] New chapter created: CI/CD Pipelines for Architecture as Code
- [ ] Core automation chapter streamlined and refocused
- [ ] All internal references updated across chapters
- [ ] Table of contents updated
- [ ] No content is lost in the restructuring

**Files to Create/Update:**
- Create new chapter files for Governance, GDPR, and CI/CD Pipelines
- Update `docs/05_automation_devops_cicd.md`
- Update table of contents/index
- Update cross-references throughout the book

**Note:** This is a major restructuring task that may require coordination with other issues.

---

## Issue 8: Remove Sweden-Focused Content from Automation Chapter

**Title:** Internationalize Automation chapter by removing Sweden-specific content

**Labels:** documentation, content, internationalization

**Description:**

The Automation, DevOps and CI/CD chapter contains numerous Sweden-specific references that should be removed or made internationally relevant.

**Current State:**
The chapter includes:
- "Swedish organisations" specific mentions
- Swedish kronor (SEK) currency references
- Swedish data-management legislation
- Swedish Civil Contingencies Agency (MSB) references
- Swedish Authority for Privacy Protection mentions
- Stockholm region examples in CI/CD pipeline code
- Swedish organization variables (`ORGANISATION_NAME: 'swedish-org'`)

**Requested Change:**
Replace all Sweden-specific content with:
- Generic "organizations" or "enterprises"
- Multiple currency examples or generic cost references
- International regulatory frameworks (EU GDPR, ISO standards, NIST)
- Generic regional examples or multiple regions
- Remove country-specific code configurations

**Acceptance Criteria:**
- [ ] All "Swedish" references replaced with generic alternatives
- [ ] Currency references are internationalized
- [ ] Regulatory references use international standards
- [ ] Code examples use generic organization names and regions
- [ ] The chapter remains comprehensive and educational

**Files to Update:**
- `docs/05_automation_devops_cicd.md`
- `docs/30_appendix_code_examples.md` (related CI/CD examples)

**Search Terms to Replace:**
- "Swedish organisation"
- "Swedish company"
- "Sweden"
- "Swedish kronor"
- "SEK"
- "Stockholm region"
- "eu-north-1"
- "MSB"
- "Integritetsskyddsmyndigheten"

---

## Issue 9: Remove Swedish Architecture Testing Framework Section

**Title:** Remove Swedish Architecture testing framework section from Automation chapter

**Labels:** documentation, content, removal

**Description:**

The Automation chapter contains a section about a Swedish Architecture testing framework that should be removed as it's too country-specific.

**Current State:**
There is a section titled "Swedish Architecture testing framework" in the Automation, DevOps and CI/CD chapter.

**Requested Change:**
Remove this entire section. If testing frameworks need to be discussed:
- Use internationally recognized frameworks
- Provide examples from multiple countries/regions
- Focus on universal testing principles rather than country-specific implementations

**Alternatives:**
- Replace with a section on "Architecture Testing Frameworks" that covers international options
- Include examples like:
  - ArchUnit (Java)
  - Terratest (Infrastructure)
  - InSpec (Compliance)
  - Generic testing approaches applicable globally

**Acceptance Criteria:**
- [ ] Swedish Architecture testing framework section is removed
- [ ] If replaced, new content covers international frameworks
- [ ] Testing principles remain well-documented
- [ ] No broken references to the removed section

**Files to Update:**
- `docs/05_automation_devops_cicd.md`

---

## Issue 10: Move Cost Optimization to FinOps Chapter

**Title:** Move cost optimization content from Automation chapter to FinOps chapter and internationalize

**Labels:** documentation, content, restructuring

**Description:**

The "Cost optimization and budget control" section in the Automation chapter should be moved to the FinOps chapter and ensure it's not Sweden-focused.

**Current State:**
Cost optimization content appears in the Automation, DevOps and CI/CD chapter and may contain Sweden-specific references (SEK currency, Swedish budget practices).

**Requested Change:**

### 1. Move Content
Relocate the cost optimization and budget control section to the FinOps chapter (likely `docs/15_cost_optimization.md` or similar).

### 2. Internationalize Content
Ensure the moved content:
- Uses multiple currency examples or generic cost references
- Avoids country-specific budget practices
- References international FinOps frameworks and standards
- Provides examples applicable to organizations globally

### 3. Integrate with FinOps
Ensure the content properly integrates with existing FinOps content:
- Aligns with FinOps principles
- Complements existing cost optimization strategies
- Links to relevant Architecture as Code automation practices

**Acceptance Criteria:**
- [ ] Cost optimization section moved from Automation chapter to FinOps chapter
- [ ] Content is internationalized (no Sweden-specific references)
- [ ] Content integrates well with existing FinOps chapter content
- [ ] Cross-references updated throughout the book
- [ ] No content is duplicated or lost

**Files to Update:**
- `docs/05_automation_devops_cicd.md` (remove section)
- `docs/15_cost_optimization.md` (add section)
- Update any cross-references

---

## Issue 11: Split Security Mindmap into Multiple Diagrams

**Title:** Split security architecture mindmap into one overview and four detailed mindmaps

**Labels:** documentation, design, major

**Description:**

The security architecture dimensions mindmap contains too much information to be easily digestible. It should be split into multiple mindmaps: one overview with four main branches, and four detailed mindmaps for each branch.

**Current State:**
The current mindmap (`docs/images/mindmap_10_security.mmd`) contains all security dimensions in a single diagram:
- Threat Modeling
- Zero Trust Architecture
- Policy as Code
- Risk Assessment

**Requested Change:**

### 1. Create Overview Mindmap
Create a high-level overview mindmap showing:
- Central node: "Security in Architecture as Code"
- Four main branches:
  - Threat Modeling
  - Zero Trust Architecture
  - Policy as Code
  - Risk Assessment
- Each branch with only 2-3 sub-items maximum

### 2. Create Four Detailed Mindmaps

**Mindmap 1: Threat Modeling**
- Threat Landscape (Supply Chain Attacks, Code Injection, Insider Threats, Infrastructure Exploits)
- STRIDE Methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)

**Mindmap 2: Zero Trust Architecture**
- Core Principles (Never Trust Always Verify, Continuous Validation, Granular Access Control, Least Privilege)
- Implementation (Network Segmentation, Service Mesh Policies, IAM Configurations, Trust as Code)

**Mindmap 3: Policy as Code**
- Automated Governance (OPA/Rego Policies, HashiCorp Sentinel, Cloud-native Policies, Real-time Enforcement)
- Compliance Automation (GDPR Article 32, PCI-DSS Requirements, ISO 27001, [remove Swedish Regulations])

**Mindmap 4: Risk Assessment**
- Continuous Evaluation (Blast Radius Calculation, Impact Assessment, Dependency Analysis, Dynamic Risk Scoring)
- Regulatory Compliance (Data Protection by Design, Automated Audit Trails, Compliance-as-code, Regulatory Requirements)

### 3. Update Documentation
Update the security chapter to reference all five mindmaps at appropriate sections.

**Acceptance Criteria:**
- [ ] Overview mindmap created with four main branches only
- [ ] Four detailed mindmaps created, one for each security dimension
- [ ] All mindmaps are clearly readable and well-organized
- [ ] Security chapter updated to include all five mindmaps at relevant sections
- [ ] Old single mindmap is removed or archived
- [ ] Visual style is consistent across all mindmaps

**Files to Create/Update:**
- Create: `docs/images/mindmap_10_security_overview.mmd`
- Create: `docs/images/mindmap_10_threat_modeling.mmd`
- Create: `docs/images/mindmap_10_zero_trust.mmd`
- Create: `docs/images/mindmap_10_policy_as_code.mmd`
- Create: `docs/images/mindmap_10_risk_assessment.mmd`
- Update: `docs/09_security.md` (to reference all new mindmaps)
- Archive or remove: `docs/images/mindmap_10_security.mmd`

**Note:** When creating the detailed mindmaps, ensure that country-specific references (like "Swedish Regulations") are either removed or made more generic (e.g., "Regional Regulations").

---

## Summary

These 11 issues address the feedback provided for improving the Architecture as Code book:

**Introduction:**
- Issue 1: Add Management as Code reference

**ADR Chapter:**
- Issue 2: Vertical ADR lifecycle diagram
- Issue 3: Replace Sweden-focused example
- Issue 4: Remove infrastructure/ from git structure
- Issue 5: Remove Sweden-specific content

**Automation Chapter:**
- Issue 6: Taller timeline diagram
- Issue 7: Split into multiple chapters (major restructuring)
- Issue 8: Remove Sweden-specific content
- Issue 9: Remove Swedish testing framework section
- Issue 10: Move cost optimization to FinOps chapter

**Security Chapter:**
- Issue 11: Split mindmap into multiple diagrams (major restructuring)

**Priority:**
- High Priority: Issues 7, 11 (major restructuring)
- Medium Priority: Issues 5, 8 (internationalization)
- Low Priority: Issues 2, 6 (diagram improvements)
- Quick Wins: Issues 1, 3, 4, 9, 10 (focused content changes)
