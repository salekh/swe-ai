# Chapter 4: Fine-Tuning for Production — A SWE's Playbook

> *Fine-tuning is the most misused tool in the LLM engineer's toolkit. Not because it doesn't work—it works exceptionally well for the right problems. The issue is that teams reach for it before exhausting simpler alternatives.*

---

## The Decision Framework: When to Fine-Tune

*[Figure: Decision tree: Prompt engineering → RAG → Fine-tuning]*

### Start with Prompt Engineering

Before fine-tuning, try:
- Better system prompts with clear instructions
- Few-shot examples in the prompt
- Chain-of-thought reasoning
- Structured output formats

Prompt engineering solves 70% of cases. It's free, instant, and reversible.

### Consider RAG Before Fine-Tuning

If the model needs domain knowledge it doesn't have, RAG (retrieval-augmented generation) is usually better than fine-tuning:
- RAG: inject knowledge at inference time via retrieved documents
- Fine-tuning: bake knowledge into the model weights

RAG is better when knowledge changes frequently. Fine-tuning is better when you need to change the model's *behavior* or *style*, not just its knowledge.

### When Fine-Tuning Is the Right Choice

Fine-tune when:
- You need a specific output format consistently (structured data extraction)
- You need domain-specific terminology and reasoning patterns
- You need to reduce token costs (shorter prompts, no few-shot examples)
- Prompt engineering has hit its ceiling and you have quality data

---

## Parameter-Efficient Fine-Tuning (PEFT)

### LoRA: Low-Rank Adaptation

*[Figure: LoRA architecture — low-rank decomposition of weight updates]*

Full fine-tuning updates all model parameters. LoRA freezes the pre-trained weights and injects small, trainable low-rank matrices (rank 8–64) into attention layers.

**Key insight**: The weight update matrix during fine-tuning has low intrinsic rank. LoRA exploits this by decomposing ΔW = BA where B ∈ ℝ^(d×r), A ∈ ℝ^(r×d), and r << d.

Benefits:
- **Memory**: Trains 0.1–1% of parameters (vs. 100% for full fine-tuning)
- **Speed**: 2–3× faster training
- **Serving**: Swap LoRA adapters at inference without reloading the base model
- **Composition**: Multiple LoRA adapters for different tasks on the same base model

### QLoRA: Quantized LoRA

QLoRA combines 4-bit quantization of the base model with LoRA fine-tuning:
- Base model quantized to 4-bit (NF4 data type)
- LoRA adapters trained in bf16
- Fine-tune a 70B model on a single 48GB GPU (vs. 8× A100s for full fine-tuning)

---

## Dataset Preparation

### Quality Over Quantity

*[Figure: Fine-tuning pipeline from data preparation to deployment]*

The #1 mistake in fine-tuning: using too much low-quality data.

Rules of thumb:
- **500–5,000 high-quality examples** is usually sufficient for behavior change
- **10,000–50,000** for more complex tasks or domain adaptation
- Quality means: correctly formatted, diverse, representative, and verified by domain experts

### Data Formatting

Format data in the model's expected chat template. Common formats:
- OpenAI chat format: `{"role": "system/user/assistant", "content": "..."}`
- Alpaca format: `instruction`, `input`, `output` fields
- ShareGPT format: Multi-turn conversations

---

## Evaluation-Driven Development

### Building an Evaluation Suite

Before training, build your evaluation suite:
1. **Holdout test set**: 50–200 examples never used in training
2. **Rubric-based scoring**: Score on multiple dimensions (see Chapter 8)
3. **Baseline comparison**: Compare fine-tuned model vs. base model + prompt engineering
4. **Regression testing**: Ensure fine-tuning doesn't degrade general capabilities

---

## Deployment: Getting Fine-Tuned Models to Production

### Quantization for Inference

Production serving often uses quantized models:
- **INT8**: ~0.5% quality loss, 2× memory reduction
- **INT4 (GPTQ/AWQ)**: ~1–3% quality loss, 4× memory reduction
- **GGUF**: CPU-friendly quantization for edge deployment

### Model Serving

Serving options:
- **vLLM**: High-throughput serving with PagedAttention
- **TGI (Text Generation Inference)**: Hugging Face's production server
- **TensorRT-LLM**: NVIDIA's optimized inference engine
- **Cloud APIs**: Deploy via cloud provider managed endpoints

---

## Case Study: Fine-Tuning for Enterprise Code Generation

A fintech company fine-tuned a 13B model on their internal codebase:
- **Training data**: 3,000 examples of (code context, correct completion) pairs from PRs reviewed and approved by senior engineers
- **Result**: 40% higher acceptance rate than the base model on internal code completions
- **Key lesson**: The fine-tuned model learned the company's coding conventions, naming patterns, and internal API usage—things prompt engineering couldn't reliably capture

---

## Chapter Summary

1. **Exhaust simpler alternatives first**: Prompt engineering → RAG → Fine-tuning
2. **LoRA is the default**: Parameter-efficient, composable, and practical on modest hardware
3. **Quality over quantity**: 500–5,000 excellent examples beat 100K mediocre ones
4. **Evaluate before you train**: Build the evaluation suite first; the fine-tune is the thing that makes the evaluations pass
5. **Plan for deployment**: Quantization and serving infrastructure are non-trivial
6. **Monitor for regression**: Fine-tuning can degrade general capabilities; test broadly
