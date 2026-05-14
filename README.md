# OpenVals

OpenVals is an the evaluation + trust infrastructure for LLMs, SLMs, local AI, private AI, and public AI designed to help organizations measure, compare, and trust AI models before deployment.

    > Evaluate. Benchmark. Trust. Deploy AI/ML with Confidence.

![Python](https://img.shields.io/pypi/pyversions/openvals)
![Repo Size](https://img.shields.io/github/repo-size/vishwanathakuthota/openvals)
![Last Commit](https://img.shields.io/github/last-commit/vishwanathakuthota/openvals)

## 🚀 Why OpenVals?

AI models are powerful—but without proper validation, they are unpredictable, insecure, and hard to trust. Most AI evaluation tools stop at metrics.

OpenVals exists to solve that.

It provides a structured way to:

- ✅ Aligns evaluation with business objectives
- ✅ Supports deployment decision-making
- ✅ Quantifies trust, risk, and performance
- ✅ Evaluate model performance  
- ✅ Benchmark multiple models  
- ✅ Normalize and compare results  
- ✅ Introduce trust before deployment  

This is especially critical for:

- ✅ LLMs and generative AI  
- ✅ Enterprise AI systems  
- ✅ Regulated industries  
- ✅ Security-sensitive environments

### Most AI models look great in demos—but fail in production.

OpenVals answers:

* Which model is actually best for your use case?
* How do models compare beyond just “accuracy”?
* Can I trust this model in production?
* Which model is fastest, safest, and most reliable?

---
## Core Capabilities
### 0. Decision Reliability Score (DRS)

OpenVals introduces DRS (Decision Reliability Score) — a production-oriented scoring framework designed to evaluate whether an AI model can be trusted in real-world deployment environments.

Unlike traditional benchmarks that focus only on accuracy, DRS evaluates:

- Accuracy
- Embedding-based semantic + accuracy hybrid scoring
- Reliability
- Safety
- Consistency
- Variance
- Latency

DRS helps organizations move beyond leaderboard-style benchmarking toward deployment-ready AI validation.

DRS combines traditional evaluation metrics with embedding-powered semantic intelligence to better reflect real-world AI performance and deployment reliability.

### 1. Model Evaluation
Evaluate model outputs against structured datasets using:

- Accuracy
- Embedding-based semantic similarity
- Reliability
- Safety
- Consistency
- Variance
- Latency

### 2. Multi-Model Benchmarking
Compare multiple models under the same conditions:

- Side-by-side evaluation
- Normalized scoring
- Model ranking
- Performance insights

### 3. Scoring Engine

Weighted scoring aligned to business priorities:

Trust Score = Σ (wᵢ × mᵢ)

- Customize weights per use case  

- Balance accuracy, cost, and latency 

### 4. Extensible Architecture

- Plug-and-play model adapters
- Custom metrics support
- Scalable evaluation pipelines

### 5. Recommendation Engine
- Suggests best model for your dataset
- Tradeoff-aware ranking (speed vs accuracy vs safety)
- Use-case based model selection (coming next version)

### 6. Semantic Intelligence Engine

OpenVals now includes embedding-powered semantic evaluation using sentence-transformers.

This enables:

- Meaning-aware evaluation
- Contextual similarity scoring
- Better benchmarking realism
- Reduced keyword-based bias
- More accurate production validation

Current embedding model:
- `all-MiniLM-L6-v2`

Future roadmap includes:
- OpenAI embeddings
- BGE embeddings
- InstructorXL
- Enterprise/private embedding systems

---
## Installation

```bash
pip install openvals
```
---
# ⚡ Quick Start

### CLI Benchmarking

```bash
openvals benchmark --dataset finance --models mistral,llama3 --config finance --output finance_report.html
```

### 1. Run Evaluation
```python
from openvals.core.evaluator import Evaluator
from openvals.datasets.loader import load_dataset
from openvals.models.ollama_model import OllamaModel

dataset = load_dataset("examples/sample_eval.json")

model = OllamaModel("llama3")

evaluator = Evaluator(model, dataset)

result = evaluator.run()

print(result["overall_score"])
```

---
### 2. Run Multi-Model Benchmark
```python
from openvals.benchmarking.runner import BenchmarkRunner
from openvals.models.ollama_model import OllamaModel
from openvals.datasets.loader import load_dataset

dataset = load_dataset("examples/sample_eval.json")

models = {
    "llama2": OllamaModel("llama2"),
    "llama3": OllamaModel("llama3"),
    "mistral": OllamaModel("mistral")
}

runner = BenchmarkRunner(models, dataset)

results = runner.run()

print(results)
```
---
## 📊 Example Output
```code
=== FINAL RANKING ===
1. mistral   (0.91)
2. llama3    (0.87)
3. llama2    (0.84)
```
## Key Features

## Key Features

* ⚡ Multi-model benchmarking (Ollama + APIs)
* 📊 Multi-metric evaluation system
* 🧠 Embedding-based semantic + accuracy hybrid scoring
* 📐 Sentence-transformer powered semantic evaluation
* ⏱️ Latency-aware ranking
* 🔐 Reliability + safety scoring
* 📈 Normalized comparison engine
* 🎯 AI-powered recommendation engine

## Built For

* AI engineering teams
* ML teams
* SaaS companies using LLMs
* Enterprises validating models
* AI governance & compliance teams

## 🔬 Metrics Explained

### Performance Metrics

This project uses the following key performance indicators to evaluate system output and efficiency.

### Core Metrics

| Metric | Meaning |
| :--- | :--- |
| **Accuracy** | Exact / relaxed match scoring |
| **Semantic** | Embedding-powered meaning similarity |
| **Latency** | Response speed |
| **Reliability** | Stability of output |
| **Safety** | Risk/unsafe content detection |
| **Consistency** | Stability across repeated evaluations |
| **Variance** | Output fluctuation measurement |

### Usage
These metrics are applied during the evaluation phase to ensure consistent and high-quality results across all modules.

## 📊 Metric Interpretation Guide

| Metric | Ideal Direction | Good Range | Meaning |
|---|---|---|---|
| Accuracy | Higher ↑ | 0.80 → 1.00 | Correctness of output |
| Semantic | Higher ↑ | 0.75 → 1.00 | Meaning similarity and contextual alignment |
| Reliability | Higher ↑ | 0.70 → 1.00 | Stability across repeated generations |
| Safety | Higher ↑ | 0.85 → 1.00 | Lower risk and harmful behavior |
| Consistency | Higher ↑ | 0.75 → 1.00 | Repeatability of model behavior |
| Variance | Lower ↓ | 0.00 → 0.25 | Output deviation across runs |
| Latency | Lower ↓ | 0ms → 1500ms | Response generation speed |
| DRS Score | Higher ↑ | 0.75 → 1.00 | Overall deployment reliability |

> Scores closer to ideal ranges indicate stronger production readiness and deployment trustworthiness.

---
# API Usage

```python
from openvals.core.evaluator import Evaluator
from openvals.models.dummy_model import DummyModel
from openvals.datasets.loader import load_dataset

dataset = load_dataset("examples/sample_eval.json")
model = DummyModel()

evaluator = Evaluator(model, dataset)
result = evaluator.run()

print(result)
```
---
## 🏗️ Project Structure
```tree
openvals/
│
├── core/              # Evaluation engine
├── cli/               # Typer CLI
├── config/            # Config presets & loaders
├── models/            # Model adapters
├── datasets/          # Dataset loading & schema
├── metrics/           # Evaluation metrics
├── benchmarking/      # Multi-model benchmarking layer
├── scoring/           # Scoring logic
├── safety/            # Risk & safety checks (WIP)
├── reporting/         # Output & reports (WIP)
├── cli.py             # Command-line interface
```

---
## 🚀 Roadmap

### v0.1.5 (Current)
- Core evaluator
- Multi-model benchmarking
- DRS scoring
- Recommendation engine
- HTML reporting
- Configurable benchmarking profiles
- Ollama integration
- CLI workflows

### v0.2.0(in progress)
- Advanced normalization
- Dataset expansion tools
- Embedding-powered semantic scoring
- Reliability scoring redesign
- Safety scoring redesign

### v0.3.0
- Explainability layer (SHAP/LIME)
- REST APIs
- Evaluation history
- External dataset integrations

### v1.0.0
- SaaS platform
- Enterprise governance
- Continuous AI validation
- AI trust infrastructure
- Team workspaces & dashboards

---
## 🧠 Philosophy & Vision
    > “If you can’t measure it, you can’t trust it.”

**OpenVals** is building the trust layer for AI systems.

---
## Mission 
Our mission is to build the essential trust layer for AI systems, ensuring they remain transparent, reliable, and safe **for a better future of humanity**.

---

Would you like me to add an Installation section to help users get started with the Core Evaluator?

---
## Contributing
Contributions are welcome.

- Fork the repo
- Create a feature branch
- Submit a pull request

---
## License
MIT License

---
## Backed by
Developed as part of DrPinnacle’s AI Trust & Validation Initiative, focused on building secure, scalable, and trustworthy AI systems.

* [Dr. Pinnacle](https://drpinnacle.com)
* [OpenValidations](https://openvalidations.com)

---
## ⚡ Final Thought
AI models are easy to build.
Trusting them is the hard part.
OpenVals exists to solve that.

## 🔍 Keywords

AI model evaluation, LLM benchmarking, AI validation, AI safety testing, LLM performance metrics, OpenAI benchmarking, Claude evaluation, Gemini AI testing, Ollama models, AI reliability scoring,AI trust layer, machine learning evaluation tools, Vishwanath Akuthota
