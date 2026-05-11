import typer

from openvals.datasets.loader import load_builtin_dataset
from openvals.datasets.metadata import load_dataset_metadata
from openvals.datasets.registry import DATASETS

from openvals.models.ollama_model import OllamaModel

from openvals.benchmarking.benchmark import BenchmarkRunner

from openvals.recommendation.engine import RecommendationEngine

from openvals.reporting.html_report import generate_html_report


app = typer.Typer(
    help="OpenVals - AI Evaluation & Benchmarking Framework"
)


# =========================================================
# BENCHMARK COMMAND
# =========================================================

@app.command("benchmark")
def benchmark(
    dataset: str = typer.Option(..., help="Dataset name"),
    models: str = typer.Option(..., help="Comma-separated model names"),
    report: bool = typer.Option(True, help="Generate HTML report")
):
    """
    Run OpenVals benchmark.
    """

    typer.echo("\n🚀 OpenVals Benchmark Starting...\n")


    # =====================================================
    # LOAD DATASET
    # =====================================================

    dataset_data = load_builtin_dataset(dataset)

    metadata = load_dataset_metadata(dataset)

    weights = metadata["recommended_weights"]


    typer.echo("📦 Dataset Loaded")
    typer.echo(f"Dataset : {metadata['name']}")
    typer.echo(f"Domain  : {metadata['domain']}")
    typer.echo(f"Version : {metadata['version']}\n")


    # =====================================================
    # LOAD MODELS
    # =====================================================

    model_names = [m.strip() for m in models.split(",")]

    loaded_models = {}

    for model_name in model_names:
        loaded_models[model_name] = OllamaModel(model_name)

    typer.echo(f"🤖 Models Loaded: {', '.join(model_names)}\n")


    # =====================================================
    # RUN BENCHMARK
    # =====================================================

    runner = BenchmarkRunner(
        models=loaded_models,
        dataset=dataset_data,
        weights=weights,
        debug=False
    )

    results = runner.run()


    # =====================================================
    # DRS RANKING
    # =====================================================

    ranking = sorted(
        [
            (model_name, results[model_name]["drs_score"])
            for model_name in results
        ],
        key=lambda x: x[1],
        reverse=True
    )


    # =====================================================
    # FINAL TABLE
    # =====================================================

    typer.echo("\n=== MODEL BENCHMARK (DRS Ranked) ===\n")

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


    # =====================================================
    # RECOMMENDATION ENGINE
    # =====================================================

    engine = RecommendationEngine(results)

    recommendation = engine.recommend(
        use_case=dataset
    )


    typer.echo("\n=== AI ADVISOR REPORT ===\n")

    typer.echo(
        f"✅ Recommended Model : "
        f"{recommendation['recommended_model']}"
    )

    typer.echo(
        f"📊 Score             : "
        f"{recommendation['score']}"
    )

    typer.echo(
        f"🧠 DRS               : "
        f"{recommendation['drs']}"
    )

    typer.echo(
        f"🎯 Confidence        : "
        f"{recommendation['confidence']}"
    )

    typer.echo("\nWhy:")
    typer.echo(f"→ {recommendation['reason']}")

    typer.echo("\nTrade-offs:")
    typer.echo(f"→ {recommendation['tradeoffs']}")

    typer.echo("\nRisks:")

    for risk in recommendation["risks"]:
        typer.echo(f"→ {risk}")


    # =====================================================
    # GENERATE HTML REPORT
    # =====================================================

    if report:

        generate_html_report(
            results,
            recommendation,
            output_file="report.html"
        )

        typer.echo("\n✅ HTML report generated: report.html")


# =========================================================
# DATASETS COMMAND
# =========================================================

@app.command("datasets")
def datasets():
    """
    List available datasets.
    """

    typer.echo("\n📦 Available OpenVals Datasets\n")

    print(
        f"{'Dataset':<15} "
        f"{'Domain':<15} "
        f"{'Description'}"
    )

    print("-" * 70)

    for name, info in DATASETS.items():

        print(
            f"{name:<15} "
            f"{info['domain']:<15} "
            f"{info['description']}"
        )

# =========================================================
# ENTRYPOINT
# =========================================================

def main():
    app()


if __name__ == "__main__":
    main()