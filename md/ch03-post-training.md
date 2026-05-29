# Chapter 3: Post-Training — Aligning LLMs with Human Intent

> *A pre-trained language model is a powerful but unruly beast. It can generate text in hundreds of languages, write code, and reason about complex problems—but it has no concept of "helpful," "harmless," or "honest." It will happily generate toxic content, fabricate facts, or ignore your instructions entirely. Post-training is how we tame it.*

---

## Supervised Fine-Tuning (SFT)

*[Figure: Post-training landscape: SFT → RLHF/DPO → Safety training]*

SFT teaches the model to follow instructions by training on high-quality (instruction, response) pairs. It transforms a raw text completion engine into a conversational assistant.

### The SFT Data Pipeline

The quality of SFT data matters enormously. Key characteristics:
- **Instruction diversity**: Cover the full range of tasks users will request
- **Response quality**: Responses must be genuinely excellent, not just adequate
- **Format consistency**: Consistent formatting teaches the model output conventions
- **Conversation structure**: Multi-turn conversations teach the model to maintain context

Modern SFT datasets range from 10K–100K high-quality examples. Quality over quantity: 10K expert-written examples often outperform 1M machine-generated ones.

### Training Mechanics

SFT is standard supervised learning with causal language modeling loss, but only on the response tokens (instruction tokens are masked). Key hyperparameters:
- Learning rate: 1e-5 to 5e-5 (much lower than pre-training)
- Epochs: 2–5 (risk of overfitting beyond this)
- Batch size: Typically smaller than pre-training

---

## Reinforcement Learning from Human Feedback (RLHF)

*[Figure: RLHF pipeline: SFT model → Reward model → PPO training]*

RLHF aligns the model with human preferences by training a reward model on human comparisons, then using that reward model to guide the language model via reinforcement learning (PPO).

### The RLHF Pipeline

1. **Collect comparisons**: Show human annotators two model outputs for the same prompt; they choose which is better
2. **Train reward model**: A model that scores outputs based on human preferences
3. **RL optimization (PPO)**: Fine-tune the SFT model to maximize the reward model's score while staying close to the SFT model (KL divergence penalty)

### The Engineering Challenges of RLHF

- **Reward hacking**: The model learns to exploit the reward model rather than genuinely improving
- **KL divergence collapse**: Without the KL penalty, the model produces degenerate outputs that score high but are nonsensical
- **Infrastructure complexity**: Running PPO requires 4 models simultaneously (policy, reference, reward, value)
- **Instability**: RL training is notoriously unstable; careful hyperparameter tuning is essential

---

## Direct Preference Optimization (DPO)

### How DPO Works

DPO eliminates the reward model entirely. Instead of the RL loop, it directly optimizes the language model on preference data using a closed-form loss function. The insight: the optimal RL solution can be expressed as a simple binary classification objective.

### DPO vs. RLHF: Engineering Trade-offs

| Aspect | RLHF | DPO |
|--------|------|-----|
| **Complexity** | 4 models, RL loop | Single fine-tuning run |
| **Stability** | Prone to reward hacking | More stable |
| **Memory** | 4× model memory | 2× model memory |
| **Performance** | Slightly better ceiling | Good enough for most uses |
| **Engineering effort** | Weeks of tuning | Days |

**In practice**: Most production teams use DPO unless they need the last few percentage points of quality that RLHF can provide.

---

## Safety Training and Alignment

### Red-Teaming

Systematic adversarial testing by human experts who try to elicit harmful outputs:
- Direct harmful requests
- Indirect/disguised harmful requests
- Multi-turn manipulation (grooming the model)
- Jailbreak attempts (prompt injection, role-play attacks)

### Constitutional AI (CAI)

Anthropic's approach: instead of using human labelers for every comparison, define a "constitution" (a set of principles) and use the model itself to evaluate whether outputs comply. The model critiques its own outputs, revises them, and trains on the improved versions.

---

## Evaluation: The Hardest Problem

### Benchmark Suites

Standard benchmarks: MMLU, HumanEval, GSM8K, HellaSwag, TruthfulQA, MT-Bench. Each measures a different capability (knowledge, coding, math, reasoning, truthfulness, conversation).

### The Limitations of Benchmarks

- **Contamination**: Models may have seen benchmark questions during training
- **Saturation**: Top models score 90%+ on many benchmarks, reducing discriminative power
- **Goodhart's Law**: When a benchmark becomes the target, it ceases to be a good measure
- **Narrow coverage**: Benchmarks miss real-world challenges like following complex instructions

### LLM-as-Judge

Using a more powerful model to evaluate outputs. Increasingly the standard for open-ended evaluation. Requires careful prompt design, dual-order comparison, and periodic calibration against human judgments.

---

## Chapter Summary

1. **SFT teaches instruction following**: High-quality (instruction, response) pairs; quality over quantity
2. **RLHF aligns with preferences**: Reward model + PPO; powerful but complex and unstable
3. **DPO is the pragmatic choice**: Same goal as RLHF, dramatically simpler engineering
4. **Safety training is ongoing**: Red-teaming, Constitutional AI, and adversarial evaluation
5. **Evaluation is the bottleneck**: No single benchmark captures real-world quality; LLM-as-Judge is the practical workhorse
