const SEARCH_INDEX = [
  {
    title: "Introduction",
    url: "index.html",
    content: "OpenVals is the evaluation + trust infrastructure for LLMs, SLMs, and private AI. Measure, compare, and trust your models before deployment. Core capabilities include model evaluation, multi-model benchmarking, recommendation engine, safety detection, and HTML reporting.",
    tags: ["home", "intro", "overview", "trust", "infrastructure"]
  },
  {
    title: "Getting Started",
    url: "getting-started.html",
    content: "Learn how to install OpenVals using pip install openvals and run your first evaluation. Native support for local models via Ollama. Quick start guide for evaluating models and running benchmarks.",
    tags: ["install", "setup", "quickstart", "pip", "ollama"]
  },
  {
    title: "Core Concepts",
    url: "core-concepts.html",
    content: "Understand the architecture of OpenVals. Evaluation pipeline, metrics, scoring, and benchmarking flow. How trust scores are calculated using weighted metrics. Introduction to Dynamic Response Scoring (DRS), Safety Engine, and the Recommendation Engine.",
    tags: ["architecture", "trust score", "pipeline", "concepts", "drs", "recommendation", "safety"]
  },
  {
    title: "Evaluator API",
    url: "api/evaluator.html",
    content: "API reference for the core Evaluator class. Constructor parameters, weights, debug mode, and the run() method which produces metrics, samples, and DRS scores.",
    tags: ["api", "evaluator", "core", "run", "debug", "drs"]
  },
  {
    title: "Models API",
    url: "api/models.html",
    content: "Documentation for BaseModel, DummyModel, and OllamaModel. Learn how to implement custom adapters or use local models via Ollama.",
    tags: ["api", "models", "basemodel", "dummymodel", "ollama"]
  },
  {
    title: "Datasets API",
    url: "api/datasets.html",
    content: "Learn how to use built-in datasets or load your own JSON evaluation data. Access the dataset registry and use the datasets CLI command.",
    tags: ["api", "datasets", "loader", "json", "registry"]
  },
  {
    title: "Metrics API",
    url: "api/metrics.html",
    content: "Detailed reference for accuracy, semantic_similarity, latency, reliability, safety, consistency, embeddings, and similarity metrics.",
    tags: ["api", "metrics", "accuracy", "semantic", "latency", "safety", "embeddings"]
  },
  {
    title: "Benchmarking API",
    url: "api/benchmarking.html",
    content: "Reference for BenchmarkRunner, normalization, and ranking. Compare multiple models side-by-side with normalized scoring.",
    tags: ["api", "benchmarking", "ranking", "normalization"]
  },
  {
    title: "Scoring API",
    url: "api/scoring.html",
    content: "Weighted scoring logic reference and Dynamic Response Scoring (DRS). How multiple metrics are combined into a single overall performance score.",
    tags: ["api", "scoring", "weights", "drs"]
  },
  {
    title: "Recommendation API",
    url: "api/recommendation.html",
    content: "Reference for RecommendationEngine. Analyze benchmark results to suggest the best model based on industry-specific profiles (finance, healthcare, developer).",
    tags: ["api", "recommendation", "engine", "profiles", "tradeoffs"]
  },
  {
    title: "Reporting API",
    url: "api/reporting.html",
    content: "Generate professional HTML leaderboard reports and recommendation summaries using generate_html_report.",
    tags: ["api", "reporting", "html", "leaderboard", "report"]
  },
  {
    title: "Safety API",
    url: "api/safety.html",
    content: "Documentation for the Safety Engine. Detect jailbreaks, toxicity, and unsafe content patterns natively in your outputs.",
    tags: ["api", "safety", "jailbreak", "toxicity", "risk"]
  },
  {
    title: "CLI Guide",
    url: "guides/cli.html",
    content: "Command-line interface usage. New Typer-based commands like benchmark, datasets, and version. Rapidly compare local Ollama models.",
    tags: ["guide", "cli", "terminal", "commands", "typer"]
  },
  {
    title: "Configuration Guide",
    url: "guides/configuration.html",
    content: "Learn how to use YAML presets (finance, legal, healthcare) and custom weights to configure your evaluations.",
    tags: ["guide", "config", "yaml", "presets", "weights"]
  },
  {
    title: "Custom Models Guide",
    url: "guides/custom-model.html",
    content: "Tutorial on creating custom model adapters for OpenAI, Ollama, or HuggingFace models by subclassing BaseModel.",
    tags: ["guide", "tutorial", "custom", "adapter"]
  },
  {
    title: "Custom Metrics Guide",
    url: "guides/custom-metrics.html",
    content: "How to add your own evaluation metrics to the OpenVals framework. Implementing metric functions and integrating them with the Evaluator.",
    tags: ["guide", "tutorial", "metrics", "custom"]
  },
  {
    title: "Examples",
    url: "examples.html",
    content: "Complete working examples of OpenVals in action. Python API usage and CLI demonstrations with sample datasets including Ollama and Recommendation Engine.",
    tags: ["examples", "samples", "code", "tutorial", "ollama"]
  },
  {
    title: "Roadmap",
    url: "roadmap.html",
    content: "Future development plans for OpenVals. Upcoming features like advanced normalization, dataset expansion, and enterprise governance.",
    tags: ["roadmap", "future", "version", "vision"]
  }
];
];

function search(query) {
  if (!query) return [];
  const q = query.toLowerCase();
  
  // Get relative path prefix if we are in a subdirectory
  const pathParts = window.location.pathname.split('/');
  let prefix = '';
  if (pathParts.includes('api') || pathParts.includes('guides')) {
    prefix = '../';
  }

  return SEARCH_INDEX.filter(item => 
    item.title.toLowerCase().includes(q) || 
    item.content.toLowerCase().includes(q) ||
    item.tags.some(tag => tag.toLowerCase().includes(q))
  ).map(item => {
    let score = 0;
    if (item.title.toLowerCase().includes(q)) score += 10;
    if (item.tags.some(tag => tag.toLowerCase() === q)) score += 5;
    return { ...item, url: prefix + item.url, score };
  }).sort((a, b) => b.score - a.score);
}
