from openvals.metrics.semantic import semantic_score


def reliability_score(model, prompt, runs=3):

    responses = []

    for _ in range(runs):

        try:

            response = model.generate(prompt)

        except Exception:

            response = ""

        responses.append(response)


    similarities = []


    for i in range(len(responses)):

        for j in range(i + 1, len(responses)):

            similarity = semantic_score(
                responses[i],
                responses[j]
            )

            similarities.append(similarity)


    if not similarities:
        return 0.0


    reliability = sum(similarities) / len(similarities)

    return round(float(reliability), 4)