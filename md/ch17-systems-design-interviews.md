# Chapter 17: Systems Design for AI/ML at Scale

> 60 systems design interview questions spanning AI infrastructure, ML platforms, and production AI systems. Starred questions include architecture diagrams (compiled DOT→PDF), detailed interviewer follow-ups covering metrics/SLOs, testing strategy, traffic splitting, model routing, load balancing, and failure mode analysis.

---

## The ACRES Framework

Structure every answer using:
- **A**sk clarifying questions (scope, scale, latency, quality bar)
- **C**omponent design (architecture diagram)
- **R**easoning about trade-offs
- **E**valuation strategy (metrics, SLOs)
- **S**caling and failure modes

## RAG Systems (Q1–Q3)
- **Q1★ Customer Support RAG** — 50K articles, 10K daily queries, 95% accuracy target. ✅ Architecture diagram, metrics/SLOs, testing, traffic splitting, model routing, load balancing
- Q2 Multi-tenant RAG platform (500 enterprise customers)
- Q3 Real-time RAG with streaming data (financial news)

## AI Application Architecture (Q4–Q6)
- **Q4★ Model Gateway** — routing, failover, circuit breakers, cost controls. ✅ Architecture diagram, metrics, chaos testing, model migration, traffic splitting
- **Q5★ LLM Evaluation Platform** — 50 teams, golden datasets, Wilcoxon testing. ✅ Metrics, judge validation, traffic splitting, model routing, scale
- Q6 Semantic cache design

## AI Infrastructure (Q7–Q9)
- Q7★ Feature store (batch + real-time, 100K req/s)
- Q8 Model serving (20 models from classifiers to 70B LLMs)
- Q9 Continuous fine-tuning pipeline

## Agent Systems (Q10–Q11)
- Q10★ Code review agent (500 engineers, 200 PRs/day)
- Q11 Multi-agent research system

## Data Systems (Q12–Q13)
- Q12★ Embedding pipeline at scale (50M documents)
- Q13 Data labeling platform with active learning

## Production AI (Q14–Q17)
- Q14★ Content moderation (10M posts/day)
- Q15 Recommendation system with LLM explanations
- Q16 AI incident response system
- Q17 LLM cost optimization ($500K/month → $300K/month)

## Brief Design Prompts (Q18–Q40)
- 23 additional practice questions: plagiarism detection, multilingual chatbot, fraud detection, document summarization, search systems, ML CI/CD, A/B testing, web crawl deduplication, model registry, privacy-preserving inference, knowledge graph construction, speech-to-text, prompt management, multi-modal QA, coding agent, email generation, log analysis, competitive intelligence, data validation, federated learning, real-time translation, code migration, AI observability

## GPU/Inference Infrastructure (Q41–Q45)
- **Q41★ High-Throughput LLM Inference** — 70B model, 100K req/s, H100 fleet. ✅ Architecture diagram, back-of-envelope, continuous batching, PagedAttention, speculative decoding, metrics, traffic splitting
- **Q42★ Distributed Training Platform** — 1,024 GPUs, 3D parallelism, fault tolerance. ✅ Metrics, testing, cost optimization, debugging, load balancing
- Q43★ Multi-region LLM serving (200ms p99 globally)
- **Q44★ AI Safety Guardrails Pipeline** — input/output classifiers, injection defense, regional compliance. ✅ Architecture diagram, red-team testing, metrics, traffic splitting
- Q45 AI alignment evaluation system

## Safety-Critical AI (Q46–Q48)
- Q46★ Healthcare clinical decision support (HIPAA compliant)
- **Q47★ Real-Time Fraud Detection (Stripe)** — 50K TPS, <100ms, multi-stage cascade. ✅ Metrics, testing, traffic splitting, model routing
- Q48 AI transaction categorization

## DevTools & Code Intelligence (Q49–Q51)
- **Q49★ AI Code Completion (GitHub Copilot)** — <200ms latency, context-aware, privacy. ✅ Metrics, testing, traffic splitting, real-time model selection, load balancing
- **Q50 Agentic Coding System** — auto-PR from Jira ticket, sandboxed execution. ✅ Metrics, testing, traffic splitting, model routing, safety
- **Q51★ AI Job Matching (LinkedIn)** — two-tower embeddings, fairness, 500M profiles. ✅ Metrics, testing, traffic splitting, model routing, load balancing

## Enterprise AI (Q52–Q55)
- Q52 Enterprise knowledge management (500M documents, ACL)
- Q53 Enterprise AI gateway (10K employees)
- Q54★ AI-powered search (1B web pages)
- Q55★ Foundation model fine-tuning platform (multi-tenant)

## Frontier/Research (Q56–Q60)
- Q56★ Multi-modal reasoning system
- Q57★ Mixture-of-experts inference (1T params sparse model)
- Q58★ Model cascading with confidence-based routing
- **Q59★ Prompt Injection Defense** — multi-layer detection, canary tokens, red-team automation. ✅ Metrics, testing, traffic splitting
- **Q60★ Foundation Model Training Data Curation** — 50+ domains, PII, copyright, quality filters. ✅ Metrics, testing, data mix ablations, load balancing

---

## Golden Answer Format

Each diagram-equipped answer includes:
1. **Scenario & constraints** — company, scale, latency requirements
2. **Architecture diagram** (DOT→PDF, embedded in LaTeX)
3. **Key design decisions** — with trade-off analysis
4. **Failure modes** — what goes wrong and how to handle it
5. **Interviewer Follow-ups** — metrics/SLOs, testing strategy, traffic splitting, model routing, load balancing, scaling

## Architecture Diagrams Created
- `rag-system.pdf` — Customer support RAG (Q1)
- `model-gateway.pdf` — Centralized model gateway (Q4)
- `llm-inference.pdf` — High-throughput inference fleet (Q41)
- `safety-pipeline.pdf` — AI safety guardrails cascade (Q44)

## Target Companies
Google DeepMind, Anthropic, OpenAI, Meta FAIR, Stripe, LinkedIn, GitHub
