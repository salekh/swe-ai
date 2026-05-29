# Chapter 11: Reliability & Operations for AI Systems

> *"An AI system that's 95% accurate sounds great—until you realize that at 10,000 requests per hour, you're producing 500 wrong answers every hour, and you have no way to know which ones they are."*

---

## Deployment Strategies

Every AI deployment is described by a **deployment tuple**: `(app_version, prompt_version, model_version, index_version, guardrail_config)`. Any change to any element is a deployment that must go through the evaluation pipeline.

Pipeline: Pre-deployment evaluation → Shadow deployment → Canary rollout (5% → 25% → 50% → 100%)

## Monitoring AI Systems

### Three Monitoring Layers

1. **Infrastructure metrics** (every request): Latency, token usage, error rates, cost
2. **Quality metrics** (5–10% sample, async): Rubric scores, schema compliance, refusal rate, groundedness
3. **Business metrics** (daily): User satisfaction, task completion, regeneration rate

## Incident Response

| Category | Detection Signal | Response |
|----------|-----------------|----------|
| Quality regression | Score drop >0.3 | Check for model/prompt changes; roll back |
| Hallucination spike | Groundedness drops >5% | Check RAG index freshness |
| Prompt injection | Safety filter triggers | Update guardrails |
| Cost overrun | Token usage exceeds budget | Enable circuit breaker |
| Provider outage | API errors >5% | Activate fallback model |

## Cost Management

**Cost drivers**: Model selection (10–50× range), context length, retry loops, agent reasoning, evaluation overhead.

**Optimization**: Model routing, prompt optimization, semantic caching (20–40% hit rate), batching (50–80% discount), self-hosting for high-volume workloads.

## Graceful Degradation

Three tiers: Full service → Degraded service (fallback model) → Static fallback (pre-computed responses + human escalation).

## Operational Maturity Model

L1 (Prototype) → L2 (Deployed) → L3 (Monitored) → L4 (Governed) → L5 (Excellent)
