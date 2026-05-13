from openvals.metrics.accuracy import accuracy
from openvals.metrics.semantic import semantic_similarity
from openvals.metrics.latency import measure_latency
from openvals.metrics.reliability import reliability_score
from openvals.metrics.safety import safety
from openvals.metrics.consistency import consistency
from openvals.metrics.variance import variance

from openvals.scoring.weighted import weighted_score
from openvals.scoring.drs import compute_drs


class Evaluator:
    def __init__(self, model, dataset, weights=None, debug=False):
        self.model = model
        self.dataset = dataset
        self.debug = debug

        self.weights = weights or {
            "accuracy": 0.35,
            "semantic": 0.30,
            "latency": 0.15,
            "reliability": 0.10,
            "safety": 0.10
        }

    def run(self):
        results = []

        agg = {
            "accuracy": 0.0,
            "semantic": 0.0,
            "latency": 0.0,
            "reliability": 0.0,
            "safety": 0.0,
            "consistency": 0.0,
            "variance": 0.0
        }

        for sample in self.dataset:
            expected = sample.get("expected_output", "")
            eval_config = sample.get("evaluation", {})
            task_type = sample.get("type", "default")

            try:
                output, latency = measure_latency(
                    self.model.generate,
                    sample["input"]
                )

                if output is None:
                    output = ""

                if isinstance(output, str) and output.startswith("ERROR"):
                    acc = sem = rel = saf = cons = var = 0.0

                else:
                    acc = accuracy(output, expected, eval_config)
                    sem = semantic_similarity(output, expected)

                    threshold = eval_config.get("semantic_threshold")
                    if threshold is not None and sem >= threshold:
                        sem = 1.0

                    if task_type == "classification":
                        sem = acc
                    elif task_type == "generation":
                        if len(output.split()) > 120:
                            sem *= 0.9

                    rel = reliability_score(self.model, sample["input"])
                    saf = safety(output)

                    # 🔥 NEW METRICS
                    cons = consistency(self.model, sample["input"])
                    var = variance([output])  # simple v1

            except Exception as e:
                output = f"ERROR: {str(e)}"
                latency = 0.0
                acc = sem = rel = saf = cons = var = 0.0

            if self.debug:
                print("\n-----------------------------")
                print(f"Input: {sample['input']}")
                print(f"Output: {output}")
                print(f"Accuracy: {acc:.3f}")
                print(f"Semantic: {sem:.3f}")
                print(f"Latency: {latency:.2f} ms")
                print(f"Reliability: {rel:.3f}")
                print(f"Safety: {saf:.3f}")
                print(f"Consistency: {cons:.3f}")
                print(f"Variance: {var:.3f}")

            agg["accuracy"] += acc
            agg["semantic"] += sem
            agg["latency"] += latency
            agg["reliability"] += rel
            agg["safety"] += saf
            agg["consistency"] += cons
            agg["variance"] += var

            results.append({
                "input": sample["input"],
                "output": output,
                "expected": expected,
                "accuracy": round(acc, 3),
                "semantic": round(sem, 3),
                "latency": round(latency, 2),
                "reliability": round(rel, 3),
                "safety": round(saf, 3),
                "consistency": round(cons, 3),
                "variance": round(var, 3)
            })

        n = len(self.dataset) if self.dataset else 1

        avg_metrics = {k: v / n for k, v in agg.items()}

        score = weighted_score(avg_metrics, self.weights)

        # 🔥 DRS SCORE
        drs_score = compute_drs(avg_metrics)

        return {
            "overall_score": round(score, 3),
            "drs_score": round(drs_score, 3),
            "metrics": {k: round(v, 3) for k, v in avg_metrics.items()},
            "samples": results
        }