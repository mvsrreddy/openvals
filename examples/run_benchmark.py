from openvals.benchmarking.benchmark import BenchmarkRunner
from openvals.benchmarking.normalization import normalize_scores
from openvals.datasets.loader import load_builtin_dataset
from openvals.datasets.metadata import load_dataset_metadata

from openvals.models.ollama_model import OllamaModel

from openvals.recommendation.engine import RecommendationEngine
from openvals.reporting.html_report import generate_html_report


# =========================================================
# LOAD DATASET + METADATA
# =========================================================

dataset_name = "finance"

dataset = load_builtin_dataset(dataset_name)
metadata = load_dataset_metadata(dataset_name)

weights = metadata["recommended_weights"]

print("\n=== DATASET METADATA ===\n")
print(metadata)


# =========================================================
# LOAD MODELS
# =========================================================

models = {
    "llama2": OllamaModel("llama2"),
    "mistral": OllamaModel("mistral"),
    "llama3": OllamaModel("llama3")
}


# =========================================================
# RUN BENCHMARK
# =========================================================

runner = BenchmarkRunner(
    models=models,
    dataset=dataset,
    weights=weights,
    debug=False
)

results = runner.run()


# =========================================================
# SANITY CHECK
# =========================================================

print("\n=== SANITY CHECK ===\n")

for model, data in results.items():

    print(f"\nModel: {model}")

    if data is None:
        print("❌ ERROR: No data returned")
        continue

    print("Metrics Keys :", list(data.get("metrics", {}).keys()))
    print("DRS Score    :", data.get("drs_score", "MISSING"))


# =========================================================
# NORMALIZATION
# =========================================================

normalized = normalize_scores(results)

print("\n=== NORMALIZED ===\n")
print(normalized)


# =========================================================
# DRS RANKING (PRIMARY)
# =========================================================

ranking = sorted(
    [
        (model_name, results[model_name]["drs_score"])
        for model_name in results
    ],
    key=lambda x: x[1],
    reverse=True
)


# =========================================================
# FINAL TABLE
# =========================================================

print("\n=== MODEL BENCHMARK (DRS Ranked) ===\n")

print(
    f"{'Rank':<5} "
    f"{'Model':<10} "
    f"{'Acc':<8} "
    f"{'Sem':<8} "
    f"{'Rel':<8} "
    f"{'Safe':<8} "
    f"{'Cons':<8} "
    f"{'Var':<8} "
    f"{'Lat(ms)':<12} "
    f"{'DRS':<8}"
)

for rank, (model_name, drs_score) in enumerate(ranking, start=1):

    metrics = results[model_name]["metrics"]

    print(
        f"{rank:<5} "
        f"{model_name:<10} "
        f"{metrics['accuracy']:<8.3f} "
        f"{metrics['semantic']:<8.3f} "
        f"{metrics['reliability']:<8.3f} "
        f"{metrics['safety']:<8.3f} "
        f"{metrics['consistency']:<8.3f} "
        f"{metrics['variance']:<8.3f} "
        f"{metrics['latency']:<12.2f} "
        f"{drs_score:<8.3f}"
    )


# =========================================================
# RECOMMENDATION ENGINE
# =========================================================

engine = RecommendationEngine(results)

recommendation = engine.recommend(
    use_case=dataset_name
)


# =========================================================
# AI ADVISOR REPORT
# =========================================================

print("\n=== AI ADVISOR REPORT ===\n")

print(f"Recommended Model : {recommendation['recommended_model']}")
print(f"Score             : {recommendation['score']}")
print(f"DRS               : {recommendation['drs']}")
print(f"Confidence        : {recommendation['confidence']}")

print("\nWhy:")
print(f"→ {recommendation['reason']}")

print("\nTrade-offs:")
print(f"→ {recommendation['tradeoffs']}")

print("\nRisks:")

for risk in recommendation["risks"]:
    print(f"→ {risk}")


# =========================================================
# GENERATE HTML REPORT
# =========================================================

generate_html_report(
    results,
    recommendation,
    output_file="report.html"
)

print("\n✅ HTML report generated: report.html")