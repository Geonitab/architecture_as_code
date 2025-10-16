# Source Gaps Identified on https://aac.geon.se

The following statements published on the Architecture as Code site lack explicit citations. Each entry lists the affected passage, explains the risk of leaving the assertion unsourced, and supplies candidate references that either support or challenge the claim.

## 1. Global digital transformation investment figure
- **Location**: `docs/21_digitalization.md`, lines 27-33.
- **Unsourced statement**: "According to recent industry reports, organisations globally have invested over £500 billion in digital transformation initiatives in the past five years, yet many projects fail due to inadequate infrastructure governance and accumulating technical debt."
- **Why a citation is required**: The claim combines a precise investment total with a causal explanation for project failure; without attribution it is impossible for readers to verify either the financial estimate or the stated reason for failures. This weakens the credibility of the argument about governance gaps.
- **Potential supporting source**: Mordor Intelligence estimates the global digital transformation market size will reach USD 1.65 trillion in 2025, comfortably exceeding the £500 billion threshold claimed on the site.【643925†L1-L25】
- **Counterpoint / nuance source**: Research on digital transformation challenges highlights persistent change-management, communication, and legacy-system barriers, indicating that failure modes are multifaceted and not solely the product of infrastructure governance weaknesses.【4a016f†L1-L18】

## 2. Manual effort reduction attributed to Infrastructure as Code
- **Location**: `docs/21_digitalization.md`, lines 33-35.
- **Unsourced statement**: "Studies demonstrate that Infrastructure as Code reduces manual effort by up to 70%, enabling organisations to reallocate skilled personnel to higher-value activities whilst reducing operational expenses."
- **Why a citation is required**: Quoting a maximum percentage improvement implies empirical measurement; without a named study, the figure could be misinterpreted or contested, which undermines the persuasiveness of the cost-efficiency argument.
- **Potential supporting source**: Mordor Intelligence notes that Amazon Web Services attributes a 450,000-hour reduction in manual developer effort to automation initiatives, illustrating the scale of labour savings achievable through codified operations.【643925†L19-L25】
- **Counterpoint / nuance source**: The Infrastructure as Code entry on Wikipedia flags that widely cited benefits such as cost reductions and manual effort savings still carry "[citation needed]" notices, and it documents large-scale template vulnerabilities, underscoring the need for careful evidentiary backing and security consideration.【703d60†L1-L40】【703d60†L80-L96】

## 3. Capital One performance metrics attributed to Infrastructure as Code
- **Location**: `docs/21_digitalization.md`, lines 59-67.
- **Unsourced statement**: "Capital One... achieving 99.99% uptime for critical banking systems whilst reducing infrastructure costs by 40% and accelerating feature deployment by 70%."
- **Why a citation is required**: The triple set of quantitative outcomes (uptime, cost reduction, deployment speed) implies access to proprietary operational metrics. Without corroborating evidence, readers cannot assess whether the figures reflect official disclosures, marketing claims, or estimates.
- **Potential supporting source**: AWS highlights that Capital One's adoption of cloud-native services improved resilience and accelerated workloads, including cutting specific processing times by up to 80%, suggesting that substantial efficiency gains are plausible when supported by observable case studies.【80af63†L11-L34】
- **Counterpoint / nuance source**: Capital One experienced a major 2019 data breach affecting 106 million customers, leading to regulatory actions and reputational damage, which complicates claims of near-perfect uptime and demonstrates that operational excellence metrics should be contextualised with security incidents.【f9462d†L70-L122】

## 4. Claimed 20–40% cloud cost reduction for EU organisations
- **Location**: `docs/15_cost_optimization.md`, lines 108-115.
- **Unsourced statement**: "EU organisations that implement these strategies can achieve 20-40% cost reduction in their cloud operations whilst ensuring regulatory compliance and performance requirements."
- **Why a citation is required**: The statement presents a precise savings range as an achievable baseline, which can mislead readers if the estimate is anecdotal. Documenting the source is vital for readers evaluating the feasibility of the prescribed optimisation roadmap.
- **Potential supporting source**: Market analyses on cloud transformation outline trillion-dollar value opportunities, reinforcing that significant savings are available when optimisation levers are executed effectively.【643925†L1-L18】
- **Counterpoint / nuance source**: Independent reviews of cloud adoption show many organisations overspend by an average of 15% without strong governance, implying that cost savings are not guaranteed and hinge on disciplined practices.【bffbb0†L41-L90】
