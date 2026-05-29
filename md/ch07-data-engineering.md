# Chapter 7: Data Engineering for LLM Applications

> *There's an uncomfortable truth that the AI industry prefers not to advertise: for most production LLM applications, the data engineering work is two to three times harder than the actual LLM integration.*

A RAG pipeline that works beautifully on your demo dataset of 50 clean markdown files will collapse spectacularly when pointed at your company's actual knowledge base: 30,000 PDFs (half scanned images), a Confluence wiki with 8 years of cruft, Slack messages mixing code with emoji, and a Jira backlog where the same bug has been filed 17 times.

---

## The Document Processing Pipeline

*[Figure: Document processing pipeline: heterogeneous sources → format-specific extraction → universal processing → dual indexing]*

### The Dirty Truth About PDFs

PDFs are the bane of every RAG system. They're not designed for text extraction—they're designed for visual rendering.

Real stats from a legal firm migration:
- 40% simple text (PyMuPDF handles fine)
- 25% multi-column (need layout analysis)
- 20% tables (need table extraction)
- 10% scanned (need OCR)
- 5% mixed (need all of the above)

Common post-processing fixes:
- Fix hyphenation from line breaks ("impor-\ntant" → "important")
- Fix ligatures (ﬁ → fi, ﬂ → fl)
- Remove page headers/footers (heuristic)
- Normalize whitespace

### Chunking Strategies

Chunking—splitting documents into pieces for retrieval—is where most RAG pipelines quietly fail. Wrong chunking means the most relevant information is split across two chunks, and neither has enough context.

**Semantic chunking**: Split at meaning boundaries, not character counts. Compute embeddings for each sentence, find natural break points where semantic similarity drops.

> **Chunking Rules of Thumb**:
> 1. **Chunk code differently than prose**: Code at function/class boundaries, not by token count
> 2. **Include overlapping context**: 10–15% overlap prevents information loss at boundaries
> 3. **Add metadata headers**: Prepend source document title, section heading, page number
> 4. **Don't chunk too small**: Under 100 tokens lacks context for meaningful retrieval
> 5. **Don't chunk too large**: Over 1024 tokens dilutes semantic signal and wastes context window

---

## Embedding Pipelines at Scale

Computing embeddings for a large corpus is a batch processing problem with specific engineering challenges.

**Key challenge**: Keeping the index up-to-date as documents are added, modified, and deleted.

**Incremental updates**: Use content hashing to detect changes. Only re-embed documents whose content hash has changed. This saves 60–80% of embedding API costs for documentation that updates daily.

Pipeline pattern:
1. Full index on initial load
2. Incremental updates on a schedule (hourly/daily)
3. Content hash comparison to skip unchanged documents
4. Delete-and-replace for modified documents

---

## Vector Database Operations

### Choosing the Right Vector Database

| Database | Best For | Latency (p99) | Key Trade-off |
|----------|---------|---------------|---------------|
| **pgvector** | Teams on PostgreSQL; <5M vectors | 10–50ms | Easy adoption, limited scale |
| **Pinecone** | Managed service, fast setup | 5–20ms | Vendor lock-in, cost at scale |
| **Weaviate** | Hybrid search, multi-tenancy | 10–40ms | Complex config, heavier infra |
| **Qdrant** | On-prem, large datasets, filtering | 5–30ms | More operational overhead |
| **ChromaDB** | Prototyping, local development | N/A | Not for production |

> ⚠️ **The pgvector Trap**: pgvector works fine for <1M vectors. Beyond that, HNSW index struggles: queries slow down, memory spikes, VACUUM operations become painful. Plan your migration path before you hit this wall.

---

## Data Quality Monitoring

The hardest part isn't building the pipeline—it's maintaining it. Data quality degrades silently.

**Daily quality checks**:
1. **Freshness**: Is the index actually being updated? Alert if last update >24h ago
2. **Completeness**: Spot-check that known "canary" documents are findable in the index
3. **Quality**: Sample random chunks, check for corruption (empty chunks, null bytes, garbled text)
4. **Drift**: Monitor embedding distribution for sudden shifts (new document types, format changes)

---

## Chapter Summary

1. **Document processing is 80% of the work**: PDFs, Confluence, Slack, Jira—each format has unique extraction challenges
2. **Chunking strategy determines retrieval quality**: Semantic chunking outperforms fixed-size, but requires more engineering
3. **Incremental indexing saves money**: Content-hash-based updates reduce embedding API costs by 60–80%
4. **Choose vector database based on scale**: pgvector for <1M vectors, purpose-built databases for larger datasets
5. **Monitor data quality continuously**: Canary documents, freshness checks, and sample-based validation catch silent degradation
