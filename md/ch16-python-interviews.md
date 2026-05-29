# Chapter 16: Python Programming for AI/ML Interviews

> 80 carefully selected Python interview questions organized by topic and difficulty. Each question tests deep language fluency and systems thinking. ★ = common at top-tier AI companies. Questions with golden answers include complete working code, testing strategy, interviewer follow-ups (metrics, traffic splitting, load balancing, model routing), and production scaling considerations.

---

## Sections

### 1. Data Structures & Algorithmic Thinking (Q1–Q5)
- **Q1★ LRU Cache** — `OrderedDict` with O(1) get/put. ✅ Full code, testing, follow-ups
- **Q2 Streaming Top-K** — min-heap (`heapq`) with bounded memory. ✅ Full code, follow-ups
- Q3 Efficient deduplication (50M strings)
- Q4 Sliding window on token log-probabilities
- Q5 Python dict collision resolution (open addressing)

### 2. Python Internals (Q6–Q10)
- Q6★ The GIL and its implications for AI/ML workloads
- Q7 Memory management and `__slots__`
- **Q8★ Generator Pipeline** — lazy 200GB data loader with composable stages. ✅ Full code, follow-ups
- Q9 Context managers for GPU memory
- **Q10★ Retry Decorator** — 3-level nested function with async support. ✅ Full code, follow-ups

### 3. Concurrency & Parallelism (Q11–Q13)
- **Q11★ Async Rate-Limited API Calls** — `asyncio.Semaphore` with batching. ✅ Full code, follow-ups
- Q12 multiprocessing for data preprocessing
- Q13 Producer-consumer pipeline with backpressure

### 4. Object-Oriented Design (Q14–Q16)
- **Q14★ Strategy Pattern** — model routing with provider abstraction. ✅ Full code, follow-ups
- Q15 ABC vs. Protocol (nominal vs. structural typing)
- Q16 Dataclasses vs. Pydantic vs. attrs

### 5. Functional & Metaprogramming (Q17–Q20)
- Q17 Pipeline composition with higher-order functions
- Q18 Descriptors for parameter validation
- Q19 `__init_subclass__` for plugin registration
- Q20 Generic types with `Generic[T]`

### 6. Testing & Debugging (Q21–Q23)
- Q21★ Testing non-deterministic LLM functions
- Q22 Debugging memory leaks (tracemalloc)
- Q23 Profiling slow data pipelines

### 7. AI/ML-Specific (Q24–Q27)
- **Q24★ BPE Tokenizer** — from-scratch with merge rules and encoding. ✅ Full code, follow-ups
- Q25 Cosine similarity at scale (matrix multiplication)
- Q26 Numerically stable softmax
- Q27 Dynamic batching for API calls

### 8. System Design with Python (Q28–Q30)
- **Q28★ Token Bucket Rate Limiter** — thread-safe with metrics. ✅ Full code, follow-ups
- **Q29 Circuit Breaker** — 3-state machine (CLOSED/OPEN/HALF_OPEN). ✅ Full code, follow-ups
- Q30 Configuration management

### 9. Advanced Topics: Quick-Fire Round (Q31–Q35)
- `is` vs `==`, mutable defaults, `yield from`, `__all__`

### 10. Coding Challenges (Q36–Q50)
- JSON Schema Validator, Trie, Async Retry, Rolling Statistics, Thread-Safe Singleton, Topological Sort, Paginated API Iterator, Merge K Sorted Lists, Text Chunker, Consistent Hashing, Levenshtein Distance, Bloom Filter, Custom GroupBy, Bounded Thread Pool, LLM Response Parser

### 11. CPython Internals Deep Dive (Q51–Q55)
- Q51★ Free-threaded Python (PEP 703) — memory model, biased refcounting, C extensions
- Q52 Reference counting vs. garbage collection
- Q53 Import system and `__import__`
- Q54★ MRO and C3 linearization
- Q55 `__new__` vs. `__init__` and immutable types

### 12. Advanced Async Patterns (Q56–Q60)
- **Q56★ TaskGroup vs. gather** — structured concurrency with cancellation. ✅ Full code, follow-ups
- Q57 Async generators for streaming LLM responses
- Q58 Event loop internals
- Q59 Cancellation and timeouts
- Q60 Async connection pool

### 13. Data Engineering with Python (Q61–Q65)
- Q61★ NumPy broadcasting and vectorization
- Q62 Pandas performance anti-patterns
- Q63 Apache Arrow and zero-copy exchange
- Q64 Memory-mapped files for large datasets
- Q65 MapReduce in Python

### 14. Production Python (Q66–Q70)
- **Q66★ Dependency Injection** — type-hint auto-wiring, singleton/transient scopes. ✅ Full code, follow-ups
- Q67 Structured logging and observability
- **Q68★ Graceful Shutdown** — signal handling, draining, cancellation. ✅ Full code, follow-ups
- Q69 Feature flags in Python
- Q70 Zero-downtime deployment

### 15. Company-Specific Coding Challenges (Q71–Q80)
- **Q71★ Semantic Cache (Anthropic/OpenAI)** — cosine similarity, TTL, LRU eviction. ✅ Full code, follow-ups
- **Q72★ Structured Output Validator (OpenAI/DeepMind)** — JSON repair pipeline with re-prompt. ✅ Full code, follow-ups
- **Q73 Distributed Task Queue (Meta/Stripe)** — priority queue, heartbeats, dead letter. ✅ Full code, follow-ups
- **Q74 Token-Aware Text Splitter (Google/Anthropic)** — sentence boundaries, overlap, metadata. ✅ Full code, follow-ups
- **Q75★ Model Router with Fallback (Stripe/LinkedIn)** — circuit breaker, A/B testing, cost tracking. ✅ Full code, follow-ups
- **Q76 HNSW Embedding Index (DeepMind/Meta)** — multi-layer graph, beam search, pruning. ✅ Full code, follow-ups
- Q77 Prompt Template Engine (Anthropic/OpenAI)
- Q78 Streaming Aggregation Pipeline (LinkedIn/Stripe)
- **Q79★ Inference Request Scheduler (DeepMind/Meta)** — dynamic batching, priority, padding. ✅ Full code, follow-ups
- **Q80 End-to-End Eval Harness (Anthropic/Google)** — bootstrap CI, Wilcoxon test, model migration. ✅ Full code, follow-ups

---

## Golden Answer Format

Each starred golden answer follows this structure:
1. **Question statement** — what the interviewer asks
2. **What interviewers look for** — the key concepts being tested
3. **Complete Python code** — production-quality, working implementation
4. **Interviewer Follow-ups** — testing strategy, production metrics, traffic splitting, load balancing, model routing, and scaling considerations

## Target Companies
Google DeepMind, Anthropic, OpenAI, Meta, Stripe, LinkedIn, GitHub
