# Chapter 12: Building High-Quality AI Agents

> *"An agent is software that decides what to do next."*

---

The word "agent" is the most overloaded term in AI. In this chapter, we define it precisely, examine the architectures that work in production, and build the engineering intuition required to design agents that are reliable, controllable, and actually useful.

## What Makes an Agent an Agent?

An agent is an LLM-powered system that operates in a loop: it observes the current state of the world, reasons about what to do next, takes an action, and repeats until a goal is achieved or a termination condition is met. The critical distinction from a simple LLM application: **the model decides the control flow**.

*[Figure: The canonical agent loop: Observe → Think → Act → repeat]*

This loop gives agents extraordinary flexibility—they can adapt their approach based on intermediate results, recover from errors, and solve problems that weren't anticipated at design time. It also makes them fundamentally harder to test, debug, and control.

### The Autonomy Spectrum

Not all agents need the same level of autonomy:

| Level | Agent Type | Human Role | Risk |
|-------|-----------|------------|------|
| L1 | Copilot | Human decides, agent suggests | Low |
| L2 | Task Agent | Human approves, agent executes | Medium |
| L3 | Autonomous | Agent executes, human monitors | High |
| L4 | Multi-Agent | Agents coordinate, human oversees | Very High |

**Start at L1 and promote carefully.** Most production agent failures come from granting too much autonomy too early.

## Agent Architecture Patterns

*[Figure: Three core agent architectures compared]*

### ReAct: Reasoning + Acting

The ReAct pattern interleaves reasoning (Thought) with tool use (Action) and observation. The key advantage is *interpretability*: you can read the agent's reasoning trace to understand why it took each action.

### Plan-and-Execute

For complex, multi-step tasks, plan first, then execute. A planner LLM decomposes the goal, then an executor works through each step. Can re-plan when steps fail.

### Reflexion: Learning from Mistakes

Reflexion adds self-evaluation after each attempt. If output doesn't meet quality standards, the agent reflects on what went wrong and retries with the reflection as context.

> **Key Takeaway**: Production agents often combine elements of all three: plan first (Plan-and-Execute), reason transparently at each step (ReAct), and retry with reflection when things fail (Reflexion).

## The Evolution of Reasoning Paradigms

*[Figure: Four eras of reasoning paradigms, from Chain-of-Thought (2022) through reasoning models (2026)]*

### Era 1: Prompting Paradigms (2022)

- **Chain-of-Thought (CoT)**: "Let's think step by step" dramatically improved reasoning
- **Self-Ask**: Model asks itself follow-up questions explicitly
- **Least-to-Most**: Curriculum-style decomposition, simple → complex

Engineering lesson: *how you ask matters as much as what you ask*.

### Era 2: Agents and Tool Use (2023)

- **ReAct**: Combined CoT with tool use (Thought → Action → Observation)
- **Toolformer**: Model learns *when* to call tools through fine-tuning
- **Reflexion**: Self-improvement loop. HumanEval accuracy: 67% → 91% through iteration
- **Voyager**: Skill library + curriculum learning (Minecraft agent)
- **Generative Agents**: Memory + reflection → emergent social behaviors

### Era 3: Search and Planning (2023–2024)

- **Tree of Thoughts (ToT)**: BFS/DFS over reasoning paths. 3–5× more LLM calls, dramatically better on exploration tasks
- **Graph of Thoughts (GoT)**: Generalized to DAGs—branches can merge and refine
- **LATS**: Monte Carlo Tree Search + LLM scoring. Outperformed ReAct by 22–45% on benchmarks
- **MetaGPT**: Multi-agent with SOPs and role assignment

### Era 4: Reasoning Models & Flow Engineering (2024–2026)

- **Reasoning Models** (o1, o3, o4-mini): Internal chain-of-thought, test-time compute scaling
- **SWE-Agent**: Domain-specialized agent interface for code, SOTA on SWE-Bench
- **Flow Engineering**: Structured multi-step workflows with quality gates between stages
- **MCP + A2A**: Standardized tool protocols and inter-agent communication

### Choosing the Right Paradigm

- **Simple Q&A**: Direct prompting or CoT
- **Tasks requiring external data**: ReAct with tools
- **Known multi-step workflows**: Plan-and-Execute or Flow Engineering
- **Quality over cost**: Reflexion or Tree of Thoughts
- **Hard reasoning**: Reasoning models (o4-mini for cost, o3 for quality)
- **Multiple expertise areas**: Multi-agent with A2A

## Tool Use and the MCP Ecosystem

### The Model Context Protocol (MCP)

*[Figure: MCP + A2A + Skills ecosystem]*

MCP provides a universal protocol for connecting agents to tools:

- **MCP Servers** expose capabilities (Git, databases, search)
- **MCP Clients** discover and call servers dynamically
- **Three primitives**: Tools (functions), Resources (data), Prompts (templates)

Key insight: MCP separates tool implementation from agent implementation.

### Skills and Plugins

Skills provide higher-level capabilities—bundles of instructions, scripts, and examples:
- `SKILL.md` with detailed instructions
- Helper scripts the agent can execute
- Example patterns and reference implementations

### Agent-to-Agent Communication (A2A)

*[Figure: A2A protocol between specialized agents]*

A2A enables inter-agent communication via:
- **Agent Cards**: Capability advertisements
- **Task delegation**: Hierarchical task routing
- **Result streaming**: Async updates as work progresses

## Memory and Context Management

*[Figure: Memory tiers: working → episodic → semantic → procedural]*

### Working Memory
The current context window. Managed by the Contextual Garbage Collector pattern.

### Episodic Memory
Record of past interactions, stored in a database or vector store.

### Semantic Memory
Facts, knowledge, and learned relationships. Populated via RAG at query time.

### Procedural Memory
Skills and learned procedures. Implemented as code, not natural language.

## Safety and Guardrails

*[Figure: Agent guardrails architecture]*

Five layers:
1. **Input guardrails**: PII detection, injection filtering
2. **Action guardrails**: Allowlists, confirmation gates for destructive actions
3. **Output guardrails**: Content policy, factuality checks
4. **Budget guardrails**: Token/cost limits per task (Semantic Circuit Breaker)
5. **Scope guardrails**: Goal drift detection

## Chapter Summary

1. **Agents = LLMs that decide the control flow**: The loop (observe → think → act) is simple; making it reliable is not
2. **Start with low autonomy**: Copilot mode first, promote to autonomous only with strong guardrails
3. **The paradigm evolved rapidly**: From CoT to reasoning models in 4 years. Choose based on task characteristics
4. **MCP + Skills + A2A**: The composable infrastructure layer for modern agents
5. **Memory is engineering**: Four tiers, each with different implementation strategies
6. **Safety is non-negotiable**: Five layers of guardrails, from input filtering to goal drift detection
