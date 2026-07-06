# AI KMS Domain Feasibility Scorecard

## Purpose

Use this scorecard to assess whether a small team or bounded domain is a good candidate for an AI-enabled knowledge system. 

This scorecard evaluates two dimensions:
- **Value:** How useful the domain would be if AI could retrieve and connect knowledge/data well
- **Readiness:** How suitable the current knowledge/data is for AI use without excessive curation.


## When to Use This Scorecard

Before investing in building a RASCAL instance, run through this assessment to:
- Validate domain fit for this framework pattern
- Identify gaps in the current knowledge structure that would require remediation
- Set realistic expectations about curation effort and value
- Compare multiple candidate domains for prioritization


## Scoring Scale

Score each dimention from **1** to **5**:

| Score | Meaning |
| :---- | :---- |
| 1 | Very poor/very difficult |
| 2 | Weak |
| 3 | Moderate |
| 4 | Good |
| 5 | Excellent/Ideal |


## Value Scorecard

The **Value** dimension assesses the business/operational benefit of an AI knowledge system for your domain.


## Value Dimensions to Evaluate

| Dimension | Description | Scoring Guidance |
| :---- | :---- | :---- |
| **Reuse Frequency** | How often is knowledge in this domain looked up or needed? | Score high (4-5) if people frequently ask similar questions or look up the same concepts. Score low (1-2) if the knowledge is rarely needed or each question is unique |
| **Retrieval Pain Today** | How difficult is it to find the right answer in your domain right now? | Score high (4-5) if finding answers takes significant time, requires multiple sources, or jumps between systems. Score low (1-2) if answers are easy to find. |
| **Knowledge Concentration Risk** | If a key person leaves, how much knowledge would be lost? | Score high (4-5) if critical knowledge lives in one or two people’s heads or scattered tribal documents. Score low (1-2) if knowledge is well documented and distributed. |
| **Decision Impact** | How consequential are decisions made in this domain? | Score high (4-5) if incorrect answers lead to compliance risk, financial loss, or operational failure. Score low (1-2) if errors are low-consequence. |
| **Repeatability Burden** | How often do people repeat the same research or decision-making? | Score high (4-5) if similar research/decisions happen regularly and consume significant time. Score low (1-2) if each scenario is unique. |

**Value Score Interpretation:**
- **21-25**: High value - Strong case for AI KMS investment
- **16-20**: Moderate-to-high value - Good fit if readiness score is also solid
- **11-15**: Moderate value - Viable if readiness is high, and pain points are acute
- **6-10**: Low value - Consider other solutions or domain redesign first


## Readiness Scorecard

The **Readiness** dimension assesses whether your current knowledge artifacts are suitable for AI extraction and retrieval.


## Readiness Dimension to Evaluate

| Dimension | Description | Scoring Guidance |
| :---- | :---- | :---- |
| **Structural Coherence** | Are documents organized with a clear hierarchy, sections, and navigation? | Score high (4-5) if docs follow a consistent structure, use clear headings, and have a table of contents. Score low (1-2) if docs are unstructured prose or highly variable in format. |
| **Semantic Clarity** | Are concepts, terms, and relationships clearly defined and consistent? | Score high (4-5) if terminology is consistent, concepts are well explained, and ambiguity is minimal. Score low (1-2) if terms are overloaded, undefined, or inconsistently used. |
| **AI Chunkability** | Can documents be meaningfully split into retrievable knowledge units? | Score high (4-5) if sections are discrete, self-contained, and can be understood independently. Score low (1-2) if knowledge is heavily interlinked, sparse, or requires a large context to understand. |
| **Factual Completeness** | Is knowledge documented comprehensively or scattered across tribal/external sources? | Score high (4-5) if most critical knowledge is already documented internally. Score low (1-2) if much knowledge exists only in people’s heads or external systems. |
| **Currency and Maintenance** | How up to date is the documentation, and who maintains it? | Score high (4-5) if docs are regularly updated, have clear ownership, and versioning. Score low (1-2) if docs are stale, orphaned, or contradicted by newer sources. |

**Readiness Score Interpretation:**
- **21-25**: High readiness - Minimal curation needed; framework can extract and retrieve effectively
- **16-20**: Moderate-to-high readiness - Some curation/cleanup needed; manageable effort
- **11-15**: Moderate readiness - Significant curation required; plan for 20-40% effort allocation
- **6-10**: Low readiness - Major restructuring and documentation work required; consider domain redesign


## Combined Assessment Matrix

Use both scores together to make a go/no-go decision:

| Value Score | Readiness 21-25 | Readiness 16-20 | Readiness 11-15 | Readiness 6-10 |
| :---- | :---- | :---- | :---- | :---- |
| **21-25** | ✅Strong Fit | ✅Go | ⚠️Go (with planning) | 🛑Redesign the domain first |
| **16-20** | ✅Go | ✅Go | ⚠️Consider | 🛑Not recommended |
| **11-15** | ✅Go if acute | ⚠️Consider | ⚠️Conditional | 🛑Not recommended |
| **6-10** | 🛑Low priority | 🛑Not recommended | 🛑Not recommended | 🛑Not recommended |


## How to Run This Assessment

### Step 1: Gather Stakeholders
- Include subject matter experts who know the domain deeply
- Include someone who manages or curates the documentation
- Include a user who frequently needs this knowledge

### Step 2: Review Each Dimension
For each dimension (value + readiness), discuss:
- What does the current state look like?
- What would change if we had an AI system?
- Why that score, and what assumptions went into it?

### Step 3: Document Scores and Blockers
- Record each dimension score
- Note any high-priority gaps or curation needs
- Identify quick wins vs. long-term improvements

### Step 4: Make a Decision
- Add up Value and Readiness score
- Check the combined matrix above
- If the assessment is borderline, consider a **time-boxed pilot** to validate assumptions


## What Happens After Assessment

**If Go (combined score ≥32, or strong strategic alignment)**
1. Estimate curation effort based on readiness gaps
2. Plan a short ingestion sprint (1-4 weeks) to compile the initial wiki
3. Set up feedback loops so answers improve over time
4. Plan metrics to track reuse, time saved, and citation accuracy

**If Conditional (score 24-31, or mixed signals)
1. Run a time-boxed pilot (2-4 weeks) on a subset of the knowledge
2. Build a minimal wiki and test retrieval quality on real user questions
3. Measure and decide: Did it reduce research time? Improve answer quality?
4. If the pilot succeeds, commit to full rollout; if not, reconsider priorities

**If No-Go (score <24, or low value + low readiness)
1. Consider alternative solutions: better documentation practices, searchable index, knowledge graph for relationships
2. Revisit in 6-12 months after domain improvements
3. Use this assessment to drive the roadmap: define what readiness and value improvements would make it viable


## Sample Scorecard Scenarios

Scenario 1: Highly Structured Compliance Domain
Value Score: 24 (high reuse, high stakes, moderate pain)
Readiness Score: 22 (well-structured docs, clear ownership, strong terminology)
Decision: ✅ Strong Go - Build full system immediately

Scenario 2: Tribal Knowledge Domain with Low Structure
Value Score: 20 (high pain, high reuse, but scattered ownership)
Readiness Score: 12 (mostly unstructured, in people's heads, inconsistent terminology)
Decision: ⚠️ Conditional - Run a 2-week pilot on one subset; define curation roadmap in parallel

Scenario 3: Niche Technical Domain with Few Users
Value Score: 14 (low reuse, low stakes, moderate pain)
Readiness Score: 20 (well-documented, clear structure)
Decision: 🛑 No-Go (for now) - ROI not strong enough; revisit if user base grows
