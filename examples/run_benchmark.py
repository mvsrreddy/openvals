from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.benchmarking.normalization import normalize_scores
from openvals.benchmarking.ranking import rank_models
from openvals.datasets.loader import load_dataset
from openvals.models.ollama_model import OllamaModel
from openvals.recommendation.engine import RecommendationEngine
from openvals.reporting.html_report import generate_html_report
from openvals.datasets.loader import load_builtin_dataset

# 📦 Load dataset
dataset = load_builtin_dataset("finance")

# 🤖 Models
models = {
    "llama2": OllamaModel("llama2"),
    "mistral": OllamaModel("mistral"),
    "llama3": OllamaModel("llama3")
}

# 🚀 Run benchmark
runner = BenchmarkRunner(models, dataset, debug=False)
results = runner.run()

print("\n=== SANITY CHECK ===\n")

for model, data in results.items():
    print(f"\nModel: {model}")

    if data is None:
        print("❌ ERROR: No data returned")
        continue

    print("Metrics keys:", data.get("metrics", {}).keys())
    print("DRS:", data.get("drs_score", "MISSING"))

# 🔍 Normalize
normalized = normalize_scores(results)

# 🏆 Ranking using DRS (PRIMARY)
ranking = sorted(
    [(m, results[m]["drs_score"]) for m in results],
    key=lambda x: x[1],
    reverse=True
)
sorted_models = [m[0] for m in ranking]

# 🧠 Sort models by ranking
sorted_models = [m[0] for m in ranking]

# 📊 FINAL TABLE
print("\n=== MODEL BENCHMARK (DRS Ranked) ===\n")

print(f"{'Rank':<5} {'Model':<10} {'Acc':<6} {'Sem':<6} {'Rel':<6} {'Safe':<6} {'Cons':<6} {'Var':<6} {'Lat(ms)':<10} {'DRS':<6}")

for i, model_name in enumerate(sorted_models, 1):
    m = results[model_name]["metrics"]
    drs = results[model_name]["drs_score"]

    print(
        f"{i:<5} "
        f"{model_name:<10} "
        f"{m['accuracy']:<6.3f} "
        f"{m['semantic']:<6.3f} "
        f"{m['reliability']:<6.3f} "
        f"{m['safety']:<6.3f} "
        f"{m['consistency']:<6.3f} "
        f"{m['variance']:<6.3f} "
        f"{m['latency']:<10.2f} "
        f"{drs:<6.3f}"
    )

# 🧠 RECOMMENDATION ENGINE
engine = RecommendationEngine(results)

recommendation = engine.recommend(use_case="defaul")

print("\n=== RECOMMENDATION ===\n")
print(f"Best Model : {recommendation['recommended_model']}")
print(f"Score      : {recommendation['score']}")
print(f"DRS        : {recommendation['drs']}")
print(f"Reason     : {recommendation['reason']}")

#AI ADVISOR REPORT
print("\n=== AI ADVISOR REPORT ===\n")

print(f"Recommended Model : {recommendation['recommended_model']}")
print(f"Score             : {recommendation['score']}")
print(f"DRS               : {recommendation['drs']}")
print(f"Confidence        : {recommendation['confidence']}")

print(f"\nWhy:")
print(f"→ {recommendation['reason']}")

print(f"\nTrade-offs:")
print(f"→ {recommendation['tradeoffs']}")

print(f"\nRisks:")
for r in recommendation["risks"]:
    print(f"→ {r}")

# 🧠 Generate HTML report
generate_html_report(results, recommendation, output_file="report.html")