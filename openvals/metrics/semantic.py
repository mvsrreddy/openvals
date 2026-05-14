from openvals.metrics.embeddings import EmbeddingModel
from openvals.metrics.similarity import cosine_similarity


def semantic_score(expected, predicted):

    if not expected or not predicted:
        return 0.0

    expected_embedding = EmbeddingModel.encode(expected)

    predicted_embedding = EmbeddingModel.encode(predicted)

    similarity = cosine_similarity(
        expected_embedding,
        predicted_embedding
    )

    return round(float(similarity), 4)


# ==========================================
# BACKWARD COMPATIBILITY
# ==========================================

def semantic_similarity(expected, predicted):

    return semantic_score(expected, predicted)