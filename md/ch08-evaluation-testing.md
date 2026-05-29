# Chapter 8: Evaluation, Testing & Quality Assurance

> *"If you can't measure it, you can't improve it. And if you can't improve it, you shouldn't ship it."*

**Core thesis**: Evaluation is not a phase of the development process. It IS the development process. Build the evaluation suite first; the system is the thing that makes the evaluations pass.

---

## Evaluation as a First-Class Engineering Discipline

Why LLM evaluation needs more investment than traditional testing:
- **Non-determinism**: Same input, different outputs — need statistical rigor
- **Subjective correctness**: Rubrics, not boolean checks
- **Silent degradation**: Continuous monitoring, not one-time testing
- **Cascading failures**: End-to-end evaluation, not just unit-level
- **Adversarial risk**: Prompt injection, jailbreaking, data poisoning

> ⚠️ **The 10× Rule**: Evaluation infrastructure takes ~10× the engineering effort of the initial feature implementation.

## The Three-Level Evaluation Stack

*[Figure: Evaluation pyramid]*
*[Figure: Evaluation pipeline]*

1. **Level 1: Structural Validation** (every request, <1ms): Schema compliance, constraint satisfaction, format invariants
2. **Level 2: LLM-as-Judge** (5–10% sample, async): Rubric-based scoring by a more capable judge model
3. **Level 3: Statistical Evaluation** (CI/CD + weekly): Golden dataset evaluation with paired statistical tests

## Evaluation Metrics: From Lexical to Semantic

### Lexical Metrics (BLEU, ROUGE, F1)
- Fast, cheap, deterministic — but cannot recognize semantic similarity
- Still useful as fast sanity checks and for constrained outputs

### Semantic Metrics (BERTScore, SAS)
- Compare meaning rather than words using neural embeddings
- Domain gap problem: degrade on specialized language

### LLM-as-Judge: Power and Pitfalls
- Most capable but carries three pitfalls: cost at scale, systematic biases (verbosity, position, self-preference), normalization difficulty
- Mitigations: rubric design, dual-order comparison, anchored definitions

### The Case for Multi-Dimensional Evaluation
No single metric captures full quality. Decompose into independent dimensions and evaluate each separately with task-specific weights.

## Rubric-Based Evaluation

*[Figure: Rubric-based evaluation framework]*

### Five Core Dimensions
| Dimension | Score 1 (Fail) | Score 3 (Pass) | Score 5 (Excel) |
|-----------|---------------|----------------|-----------------|
| Factual Accuracy | Fabricated facts | Core claims correct | All claims verified |
| Completeness | Misses core question | Addresses main question | Comprehensive coverage |
| Relevance | Off-topic | On-topic with some tangents | Precisely scoped |
| Instruction Following | Ignores constraints | Follows most constraints | Perfect compliance |
| Safety & Tone | Harmful content | Professional and neutral | Empathetic, exemplary |

## Model Migration: A Repeatable Engineering Process

*[Figure: Four-phase migration pipeline]*

1. **Candidate Evaluation** (offline golden dataset): Paired Wilcoxon test, per-category analysis, worst-case regression
2. **Prompt Adaptation**: Restructure for new model's personality, re-evaluate
3. **Shadow Deployment** (1–2 weeks): Real traffic, dual-model, quality comparison
4. **Canary Rollout**: 5% → 25% → 50% → 100% with automated rollback

## Regression Testing

Three frequencies: on every prompt change (CI/CD), weekly (catches provider updates), continuously (sample-based production monitoring).

## Production Monitoring

*[Figure: LLM monitoring signals]*

- **Performance signals** (every request): Latency, token usage, cost, error rates
- **Quality signals** (5–10% sample): Score distributions, schema compliance, refusal rate, hallucination detection, user feedback
- **Anomaly detection**: Score distribution shifts, category-specific regression, temporal patterns

## Adversarial Evaluation

- **Prompt injection testing**: Direct, indirect, payload smuggling, role-play attacks
- **Stress testing**: Context window saturation, multilingual edge cases, pathological inputs

## Building an Evaluation Culture

1. Eval-first development (AI equivalent of TDD)
2. Every failure becomes a test case
3. Evaluation reviews (like code reviews for rubric changes)
4. Evaluation dashboards (quality as visible as uptime)
5. Evaluation budgets (3–8% of production model cost)

> **Key Takeaway**: Evaluation is not testing. Testing verifies that a system meets a specification. Evaluation measures *how well* a system performs. "Does it work?" is the wrong question. "How well does it work, on what inputs, and is it getting better or worse?" are the right questions.
