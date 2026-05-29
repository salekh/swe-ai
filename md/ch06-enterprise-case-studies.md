# Chapter 6: LLMs at Enterprise Scale — Case Studies

In early 2024, a major bank's innovation team built a chatbot prototype in two weeks using a frontier LLM. It could answer customer questions, summarize account activity, and even draft personalized financial advice. The demo was so impressive that the CEO demanded it go to production immediately. Two years later, the project had finally shipped—but only after solving the boring problems: PII redaction, audit logging, latency budgets, graceful degradation, and explaining to regulators how a black-box model was making financial recommendations.

The gap between "it works in a demo" and "it works in production at enterprise scale" is where most LLM projects die. This chapter examines organizations that have crossed that gap.

---

## GitHub Copilot: AI-Assisted Development at Scale

The most widely deployed LLM-powered developer tool in the world—millions of active users, billions of completions.

### Architecture

Copilot's architecture manages the tension between quality and latency: useful completions in under 300ms.

**Key engineering decisions**:

- **Smaller, specialized models**: Copilot does NOT use GPT-5.5 for completions. It uses smaller, distilled models (~12-15B params) optimized for low-latency code completion. Quality-per-token is lower but latency-per-token is 10× better.
- **Context window management**: Prioritizes current file (most tokens), recently edited files, import statements, and type signatures from referenced files.
- **Acceptance rate as north star**: The primary metric is whether the developer accepts the completion—not BLEU or pass@k.

### Lessons

1. **Latency is a feature**: A mediocre answer in 200ms beats a perfect answer in 2 seconds
2. **Use the right-sized model**: Profile your task, use the cheapest model that meets quality
3. **Invest in context assembly**: Context quality matters more than model size

---

## Stripe: LLMs in Financial Infrastructure

Stripe processes hundreds of billions of dollars annually. Their LLM adoption illustrates deploying AI where correctness isn't negotiable.

### Fraud Detection with LLMs

*[Figure: Stripe's tiered fraud detection]*

Traditional fraud detection uses gradient-boosted trees on structured features. Stripe augmented this with LLMs that analyze *unstructured* signals—natural-language descriptions, merchant names, customer support transcripts.

**Architecture**: Fast ML path (<10ms, always runs) handles clear accept/reject. Gray zone (~8% of transactions) triggers LLM analysis for deeper context.

### Documentation Agent

Built an internal agent that:
1. Indexes all API documentation via RAG pipeline
2. Understands user's specific integration context
3. Generates tailored code examples
4. Routes complex questions to humans with full context

**Result**: 65% of queries resolved without human intervention; remaining 35% resolved 40% faster.

---

## LinkedIn: Content Moderation at Billion-User Scale

LinkedIn moderates hundreds of millions of posts, comments, and messages daily.

### Tiered Moderation Architecture

Three tiers:
- **Tier 1 (~92%)**: Fast classifiers (<5ms) — regex, keyword lists, small BERT models
- **Tier 2 (~7%)**: LLM analysis (50-200ms) — sarcasm, coded language, context-dependent violations
- **Tier 3 (~1%)**: Human review with LLM pre-analysis

The LLM handles the *hardest* 7%—where context matters, where sarcasm might be confused with hate speech, where "shooting" might be about basketball.

### Cost Engineering at Scale

- **Cascade architecture**: Only 7% reaches LLM tier
- **Prompt caching**: Similar content patterns share cached analyses
- **Batch processing**: Non-urgent moderation batched during off-peak hours
- **Self-hosted models**: Fine-tuned 7B models for highest-volume patterns

---

## Uber: The Centralized GenAI Gateway

*[Figure: Uber's GenAI Gateway architecture]*

By 2024, hundreds of Uber teams wanted to use LLMs. Solution: a centralized GenAI Gateway by the Michelangelo team.

**Key decisions**:
- **Go-based gateway**: Low-latency proxying with unified API wrapping third-party clients
- **MCP-based tooling ("Toolshed")**: 400+ internal tools via Model Context Protocol, scoped per use case
- **LangEffect framework**: Opinionated wrapper enforcing deterministic gates (linters, unit tests, validation) between reasoning steps
- **Zero-trust identity**: Cryptographic agent identity tied to Uber's zero-trust architecture

**Result**: Idea to production LLM feature in days instead of months.

---

## Patterns Across Enterprise Deployments

| Pattern | Description |
|---------|-------------|
| Tiered architecture | Cheapest/fastest model first; escalate to expensive models for difficult cases |
| Hybrid ML + LLM | Combine traditional ML (fast, cheap, interpretable) with LLMs (flexible, contextual) |
| Human-in-the-loop | LLMs handle easy/medium; humans handle edge cases and provide training signal |
| Metric-driven deployment | Define acceptance criteria before deployment; measure relentlessly |
| Context is king | Better context assembly yields more ROI than upgrading to a larger model |

## Chapter Summary

Enterprise LLM deployment is 20% model selection and 80% systems engineering:

1. Start with a clear problem and measurable success metric—not "we should use AI"
2. Use the cheapest model that meets quality bar
3. Build tiered architectures reserving expensive LLM calls for maximum-value cases
4. Invest heavily in context assembly and evaluation infrastructure
5. Plan for failure: graceful degradation, fallback paths, human escalation
