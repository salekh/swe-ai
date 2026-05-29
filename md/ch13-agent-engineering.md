# Chapter 13: Agent Engineering — From Prototype to Production

> *"Building an agent that works in a demo takes a weekend. Building an agent that works in production takes six months. The difference is entirely engineering."*

**Central thesis**: Production agents are 20% LLM and 80% traditional software engineering.

---

## The Production Agent Skeleton

### Structured Reasoning Traces
Every reasoning step must be a structured, serializable object. Enables: debugging, auditing, replay, evaluation of intermediate steps.

### Tool Execution Framework
- **Input validation**: Validate tool arguments before execution
- **Timeout and retry**: Every tool call has a timeout with exponential backoff
- **Permission scoping**: Minimum necessary permissions per agent
- **Output normalization**: Consistent format for tool outputs
- **Cost tracking**: Cumulative cost per agent session

### Termination Conditions
1. Goal completion (verified externally, not by self-assessment)
2. Step limit (15–50 steps)
3. Cost budget
4. Time budget
5. Error threshold
6. Semantic stall detection (Circuit Breaker)

## Multi-Agent Systems

**When to use**: Different expertise required, separation of concerns, parallel work, adversarial validation.

**Failure modes**: Circular delegation, conflicting actions, context fragmentation, cascading failures.

## Agent Observability

Every session produces a structured trace: session metadata, reasoning chain, tool calls, context snapshots, quality assessments.

## Testing Agents

- **Unit tests**: Tool functions, input validators, output parsers, termination conditions
- **Scenario tests**: 50–100 representative tasks, run N=5 times each, pass = 4/5 runs
- **Adversarial tests**: Prompt injection through tools, tool failures, ambiguous goals, resource exhaustion

## Human-in-the-Loop Patterns

- **Approval gates**: Always approve (delete, financial, production), approve above threshold, auto-approve (reads, tests)
- **Confidence-based routing**: High (>0.9) → auto-execute, Medium (0.6–0.9) → execute + flag, Low (<0.6) → queue for human
