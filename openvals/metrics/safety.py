from openvals.safety.safety_engine import (
    compute_safety_score
)


def safety(output):

    return compute_safety_score(output)