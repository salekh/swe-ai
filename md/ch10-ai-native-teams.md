# Chapter 10: Engineering Practices for AI-Native Teams

> *"The team that ships AI-powered features fastest isn't the team with the best models. It's the team with the best engineering practices around those models."*

---

## The New Team Structure: Centaur Pods

The traditional 8–12 person team is giving way to smaller, senior-weighted "Centaur Pods" (3–5 people + AI agents).

| Dimension | Traditional | AI-Native (2026) |
|-----------|-------------|-------------------|
| Team size | 8–12 members | 3–5 (Centaur Pod) |
| Seniority mix | 2 senior, 4 mid, 4–6 junior | 2–3 senior, 1–2 mid, AI agents |
| Bottleneck | Implementation speed | Design quality & review bandwidth |
| Junior role | Apprentice | AI reliability engineer |

## New Roles in AI-Native Engineering

- **AI Reliability Engineer**: Validates AI-generated code, maintains evaluation suites, runs security audits
- **AI Orchestrator**: Designs and manages multi-agent workflows, debugs agent failures
- **Product-Engineer Hybrid**: Translates user problems directly into working prototypes

## Engineering Practices That Change

- **Code review**: From syntax to semantics. Watch for architectural drift.
- **Documentation as infrastructure**: ADRs, API contracts, coding standards consumed by both humans and AI
- **Testing strategy**: AI-generated tests for broad coverage + human-written tests for critical paths
- **Knowledge management**: AI-native development forces externalization of tribal knowledge

## Scaling AI-Native Practices

- **Platform engineering**: Centralized AI infrastructure (model endpoints, evaluation frameworks, security scanning)
- **Governance without bureaucracy**: Risk-tiered review, automated guardrails, cost budgets
