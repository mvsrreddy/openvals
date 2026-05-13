import math


METRICS = [

    "accuracy",
    "semantic",
    "latency",
    "reliability",
    "safety",
    "consistency",
    "variance"

]


def clip(value, min_value=0.0, max_value=1.0):

    return max(min(value, max_value), min_value)


def normalize_scores(results):

    values = {
        metric: []
        for metric in METRICS
    }


    # =====================================================
    # COLLECT METRICS
    # =====================================================

    for model_name in results:

        metrics = results[model_name]["metrics"]

        for metric in METRICS:

            values[metric].append(
                metrics.get(metric, 0.0)
            )


    # =====================================================
    # COMPUTE STATS
    # =====================================================

    min_vals = {
        metric: min(values[metric])
        for metric in METRICS
    }

    max_vals = {
        metric: max(values[metric])
        for metric in METRICS
    }


    normalized = {}


    # =====================================================
    # NORMALIZE
    # =====================================================

    for model_name in results:

        normalized[model_name] = {}

        metrics = results[model_name]["metrics"]


        for metric in METRICS:

            value = metrics.get(metric, 0.0)

            min_v = min_vals[metric]
            max_v = max_vals[metric]


            # ==============================================
            # HANDLE IDENTICAL VALUES
            # ==============================================

            if max_v == min_v:

                norm = 1.0


            else:

                # ==========================================
                # LATENCY NORMALIZATION
                # ==========================================

                if metric == "latency":

                    value = math.log(value + 1)

                    min_log = math.log(min_v + 1)
                    max_log = math.log(max_v + 1)

                    norm = (
                        (max_log - value)
                        /
                        (max_log - min_log)
                    )


                # ==========================================
                # VARIANCE NORMALIZATION
                # LOWER VARIANCE IS BETTER
                # ==========================================

                elif metric == "variance":

                    norm = (
                        (max_v - value)
                        /
                        (max_v - min_v)
                    )


                # ==========================================
                # NORMAL METRICS
                # ==========================================

                else:

                    norm = (
                        (value - min_v)
                        /
                        (max_v - min_v)
                    )


            normalized[model_name][metric] = round(
                clip(norm),
                4
            )


    return normalized