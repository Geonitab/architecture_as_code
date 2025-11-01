# Evidence as Code

Evidence is the currency that allows Architecture as Code to demonstrate trustworthiness at scale. Treating evidence as code means the artefacts that prove compliance are generated automatically, stored alongside the controls they verify, and versioned so that their provenance is unquestionable. Combined with the **assure once, comply many** principle, evidence captured for a single control objective can be replayed across multiple regulatory frameworks without repeating manual audits.

## Machine-collected, versioned artefacts

Evidence as Code systems collect machine-readable outputs—policy evaluation reports, Terraform plans, cloud configuration snapshots, build logs—directly from delivery pipelines. Artefacts are stored in immutable storage with cryptographic signing and metadata that references the originating control, environment, and timestamp. By keeping these artefacts in the same repositories as policies and blueprints, teams create a living catalogue that auditors can browse without requesting ad hoc exports.

Key characteristics include:

- **Deterministic capture:** Evidence is generated from automated checks, not manual screenshots.
- **Traceability:** Artefacts link back to commit SHAs, pull requests, and ticket references.
- **Reusability:** Metadata enumerates which frameworks and obligations each artefact supports, avoiding duplicate test runs.
- **Version control:** Evidence follows the same branching strategy as code so historic attestations remain discoverable.

## Pipeline example: exporting MFA evidence

The following pseudo-CI configuration shows how one control—the enforcement of multi-factor authentication for human identities—produces artefacts that downstream reporting systems can reuse.

```yaml
jobs:
  verify-mfa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Evaluate MFA policy
        run: opa test policies/identity --format=json > artefacts/policy-report.json
      - name: Snapshot cloud identities
        run: >
          python scripts/export_mfa_snapshot.py \
            --accounts production \
            --output artefacts/mfa-snapshot-$(date +%Y%m).json
      - name: Publish evidence package
        run: |
          jq '{
            "control_id": "SEC-ID-001",
            "framework_mappings": {
              "iso_27001": ["A.5", "A.8"],
              "soc_2": ["CC6.1", "CC6.6"],
              "nist_800_53": ["IA-2(1)", "AC-2"],
              "gdpr": ["Article 32"],
              "internal": ["SEC-ID-001"]
            },
            "artefacts": [
              "artefacts/policy-report.json",
              "artefacts/mfa-snapshot-$(date +%Y%m).json"
            ]
          }' > artefacts/manifest.json
      - name: Upload evidence bundle
        uses: actions/upload-artifact@v4
        with:
          name: sec-id-001
          path: artefacts/
```

The job produces a manifest and two evidence files. Governance and compliance teams consume the manifest to update the [Control Mapping Matrix](appendix_i_control_mapping_matrix_template.md) and to demonstrate coverage across ISO 27001, SOC 2, NIST 800-53, GDPR, and internal catalogues. Because the artefacts live alongside the policy, they can be retrieved for regulator-specific attestations without re-running the control unless configuration changes occur.

## Integrating with governance and blueprints

[Governance as Code](11_governance_as_code.md) defines the approval guardrails that keep evidence pipelines authoritative. [Policy and Security as Code](10_policy_and_security.md) contributes reusable policy modules enriched with metadata for framework mapping. [Security Fundamentals](09_security_fundamentals.md) explains how control objectives become executable assertions, while [Compliance and Regulatory Adherence](12_compliance.md) uses the Control Mapping Matrix to translate artefacts into regulator-friendly language. Platform teams embed these patterns into their blueprints, as described in [FINOS Project Blueprint](appendix_e_finos_project_blueprint.md), so that every environment exports evidence in a predictable manner. Together these chapters show how evidence captured once can sustain multiple obligations throughout the delivery lifecycle.
