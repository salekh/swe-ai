# Chapter 5: LLM Application Architecture Patterns

> *"Architecture is the decisions you wish you could get right early."*
> — Ralph Johnson

---

Building a prototype with an LLM takes hours. Building a production system takes months. The gap between the two is almost entirely architectural: how you manage prompts, assemble context, route requests, validate outputs, handle failures, and maintain quality at scale. This chapter describes the architecture patterns that have emerged from the first wave of production LLM applications.

## The Canonical LLM Application Stack

*[Figure: The canonical LLM application stack]*

The stack has six layers, each with its own design challenges:

1. **Request handling**: Input validation, rate limiting, authentication
2. **Context assembly**: Retrieving relevant information (RAG, tool calls, conversation history)
3. **Prompt construction**: Templating, few-shot example selection, instruction formatting
4. **Model interaction**: Model selection, routing, retry logic, streaming
5. **Output processing**: Parsing, validation, guardrails, formatting
6. **Observability**: Logging, tracing, evaluation, cost tracking

## Prompt Engineering as Software Engineering

Prompts are the new source code. In a traditional application, business logic lives in functions and classes. In an LLM application, a significant portion of the business logic lives in prompts.

### The Prompt Lifecycle

*[Figure: Prompt lifecycle: draft → test → shadow mode → promote → monitor → iterate]*

A production prompt management system needs five capabilities:

1. **Version control**: Every prompt identified by name, version, and content hash
2. **Model binding**: Prompts are written *for* a specific model
3. **Automated evaluation**: Every change runs against a golden dataset before deployment
4. **Canary deployment**: New versions initially serve 5–10% of traffic
5. **Instant rollback**: Previous version restored within seconds

### Structured Outputs and Function Calling

One of the most important patterns: constraining the model's output to a specific structure. This eliminates fragile output parsing and makes LLM calls behave like traditional API calls.

## Retrieval-Augmented Generation (RAG)

RAG is the most important architecture pattern for LLM applications that need access to private, recent, or specialized knowledge.

### The RAG Pipeline

*[Figure: RAG pipeline: ingestion → embedding → indexing → retrieval → generation]*

Five stages with key design decisions at each.

### Chunking Strategy

*[Figure: Three chunking strategies compared]*

- **Fixed-size**: Best for homogeneous text. Simple but splits mid-sentence.
- **Boundary-aware**: Best for structured content. Respects paragraph/section boundaries.
- **Parent-child**: Best for high-stakes apps. Small chunks for search, full parent for context.

### Hybrid Search: Dense + Sparse

*[Figure: Hybrid search architecture with RRF fusion and cross-encoder re-ranking]*

Key decisions:
- Dense-to-sparse weight ratio (start 0.7 / 0.3)
- Fusion: Reciprocal Rank Fusion (RRF) is the industry standard
- Re-ranking: Cross-encoder examines (query, document) pairs jointly
- Query expansion: LLM generates 3–5 reformulations

## Multi-Model Architectures

*[Figure: Multi-model routing with semantic cache and quality-based fallback]*

### Model Routing Design

- ~70% simple requests → Gemini 3.5 Flash ($0.15/M tokens)
- ~25% moderate → GPT-5.5 or Claude Opus 4.8 ($2–5/M tokens)
- ~5% complex → Premium reasoning models ($10–15/M tokens)

**Quality-based fallback**: When a fast model fails validation, auto-retry with a higher-tier model.

---

## Design Patterns for the Foundation Model Era

The Gang of Four gave us a shared vocabulary for object-oriented design. The distributed systems community gave us circuit breakers, sagas, and event sourcing. Now the foundation model era demands its own pattern language.

*[Figure: Nine design patterns catalog organized by category]*

### Pattern 1: The Validator-Corrector Proxy

**Category**: Reliability | **Also known as**: Reflective Retry, Self-Healing Parser

**Intent**: Coerce probabilistic output into strict schemas via a reflective retry loop.

*[Figure: Validator-Corrector Proxy flow]*

**Mechanism**: Wrap the LLM in a Proxy. On each call: send prompt → validate response → if valid, return typed result; if invalid, inject the exact error message into the conversation and re-invoke. Bounded by `max_retries` (typically 3).

**Trade-offs**: 92% → 99.5%+ schema compliance. But multiplies token cost during error states.

### Pattern 2: The Semantic Circuit Breaker

**Category**: Resilience / Security | **Also known as**: Hallucination Loop Detector, Budget Guardian

**Intent**: Prevent agents from entering infinite loops or burning API budgets ("Denial of Wallet").

*[Figure: Semantic Circuit Breaker with three states]*

**Mechanism**: Monitor "semantic velocity" — compute embedding similarity of consecutive actions. If cosine_similarity > 0.95 for 3+ loops, or budget exceeded, trip to Open state. Three states: Closed (normal), Open (suspended), Half-Open (probe).

**Trade-offs**: Prevents runaway costs but requires threshold tuning for iterative tasks.

### Pattern 3: The Contextual Garbage Collector

**Category**: Memory / State Management

**Intent**: Maintain the illusion of infinite memory within finite context windows.

**Mechanism**: Three-tier eviction policy:
1. **Evict**: Drop filler, intermediate scratchpads
2. **Compress**: Summarize older blocks into dense "episodic mementos" using a fast model
3. **Pin**: Retain system instructions and compressed summaries permanently

### Pattern 4: The Cognitive Router (Complexity Cascade)

**Category**: Architectural / Optimization

**Intent**: Optimize cost/latency/quality trade-off per-request.

**Mechanism**: Ultra-fast classifier assigns complexity tier. **The Cascade**: if a cheap model fails validation or expresses low confidence, auto-escalate to a higher tier.

### Pattern 5: The Generator-Critic Loop

**Category**: Structural / Quality Assurance

**Intent**: Decouple generation from validation to bypass LLM confirmation bias.

**Mechanism**: Generator (positive prompt, focused on task) + Critic (adversarial rubric, different model). Loop until Critic approves or max iterations reached.

**Trade-offs**: 2–3× cost but near-deterministic quality for high-stakes outputs.

### Pattern 6: The Speculative Stream Interceptor

**Category**: Concurrency / UX Performance

**Intent**: Execute side-effects concurrently with token generation.

**Mechanism**: Observer listens to raw token stream. Partial parser detects when arguments are structurally complete and fires background actions before generation finishes.

### Pattern 7: The Event-Sourced Agent

**Category**: State Management / Auditing

**Intent**: Capture reasoning state for resumption, auditing, and time-travel debugging.

*[Figure: Event-Sourced Agent with replay capabilities]*

**Mechanism**: Every Observe→Think→Act cycle persisted as an immutable event. Enables: resume from any checkpoint, full audit trail, branch to explore alternatives, time-travel debugging.

### Pattern 8: The Semantic Cache

**Category**: Cost Optimization

**Intent**: Serve cached responses for semantically similar (not just identical) queries.

**Mechanism**: Embed queries, search cache for cosine similarity > threshold (0.92–0.97). Include prompt version and model ID in cache key.

**Trade-offs**: 20–40% cost reduction for repetitive patterns. Threshold tuning is critical.

### Pattern 9: The Confidence Gate

**Category**: Cross-Cutting / Human-AI Collaboration

**Intent**: Triage outputs into auto-serve, human review, or reject based on calibrated confidence.

**Mechanism**: Compute confidence from logprobs, self-consistency (N=5 generations), or calibration model:
- High confidence (>0.9): Auto-serve
- Medium (0.6–0.9): Queue for human review
- Low (<0.6): Reject / escalate

### Composing Patterns

Real systems compose multiple patterns:

- **Cognitive Router** + **Validator-Corrector Proxy** + cascade on exhausted retries
- **Event-Sourced Agent** + **Semantic Circuit Breaker** + **Contextual GC** for autonomous agents
- **Semantic Cache** + **Generator-Critic** + **Confidence Gate** for customer-facing chatbots
- **Speculative Stream Interceptor** + **Validator-Corrector** for real-time coding assistants

## Chapter Summary

1. **Treat prompts as code**: Version, test, review, deploy through CI/CD
2. **Use structured outputs**: Eliminate parsing fragility
3. **Build RAG right**: Chunking, hybrid search, and re-ranking determine quality
4. **Route intelligently**: Cheapest model that meets quality; cascade on failure
5. **Apply design patterns**: 9 patterns provide a shared vocabulary for AI engineering
6. **Compose patterns**: Real systems combine multiple patterns as building blocks
