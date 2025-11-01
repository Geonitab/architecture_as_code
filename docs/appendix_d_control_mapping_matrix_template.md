# Control Mapping Matrix Template {#control-mapping-matrix-template}

*Part of Appendix D – Templates and Tools.*

The Control Mapping Matrix provides a reusable structure for cataloguing how each control satisfies multiple regulatory frameworks. Populate the table below from your governance repository so that auditors, risk managers, and engineering teams can navigate the same source of truth. Combine the matrix with the evidence manifests defined in [Evidence as Code](15_evidence_as_code.md) to ensure every mapping references a verifiable artefact.

| Control ID | Control Title | Assurance Artefact(s) | ISO 27001 | SOC 2 | NIST 800-53 | GDPR | Other Frameworks / Internal |
|------------|---------------|-----------------------|-----------|-------|--------------|------|-----------------------------|
|            |               |                       |           |       |              |      |                             |

## How to use the template

1. **Identify the control:** Reference the control identifier used in source control and policy repositories (for example `SEC-ID-001`).
2. **Describe the control succinctly:** Keep titles short and action-oriented so readers can scan the matrix quickly.
3. **Link to assurance artefacts:** Point to machine-generated evidence such as CI reports, configuration snapshots, or signed policy evaluations.
4. **Map to frameworks:** Record the relevant clause or control identifier from each framework (ISO 27001 Annex A, SOC 2 Trust Services Criteria, NIST 800-53 controls, GDPR Articles, industry standards, or internal policies).
5. **Keep it evergreen:** Update the matrix when policies change, new artefacts are produced, or frameworks evolve. Automate validation where possible so missing mappings trigger pipeline failures.

Maintaining this matrix ensures that the "assure once, comply many" philosophy remains practical: each control is expressed, tested, and evidenced once, yet it can be traced confidently to every obligation your organisation must satisfy.
