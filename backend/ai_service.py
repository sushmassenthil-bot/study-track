import math
import re


NOTES = [
    {
        "id": 1,
        "text": (
            "Binary search requires a sorted array and repeatedly halves "
            "the search range using a midpoint comparison."
        ),
    },
    {
        "id": 2,
        "text": (
            "Insertion sort builds a sorted list one element at a time "
            "by shifting larger elements to the right."
        ),
    },
    {
        "id": 3,
        "text": (
            "FastAPI uses Pydantic models to validate request bodies "
            "and automatically generates Swagger documentation."
        ),
    },
    {
        "id": 4,
        "text": (
            "SQL joins combine rows from two tables using a matching "
            "column, such as inner join, left join, and full join."
        ),
    },
    {
        "id": 5,
        "text": (
            "Prompt engineering structures a task, context, constraints, "
            "and desired output format to guide an LLM's response."
        ),
    },
]


VOCABULARY = [
    "sort",
    "search",
    "binary",
    "insertion",
    "sql",
    "join",
    "fastapi",
    "pydantic",
    "prompt",
    "llm",
    "database",
    "validate",
]


def summarize_notes(raw_text: str) -> dict:
    text = raw_text.strip()

    if not text:
        return {
            "topic": "untitled",
            "key_points": [],
            "difficulty": "easy",
        }

    first_line = text.splitlines()[0].strip()

    if first_line:
        topic = first_line
    else:
        topic = "untitled"

    sentences = re.split(r"[.!?]", text)

    key_points = []

    for sentence in sentences:
        cleaned = sentence.strip()

        if cleaned:
            key_points.append(cleaned)

        if len(key_points) == 3:
            break

    words = text.split()
    word_count = len(words)

    if word_count < 40:
        difficulty = "easy"
    elif word_count <= 100:
        difficulty = "medium"
    else:
        difficulty = "hard"

    return {
        "topic": topic,
        "key_points": key_points,
        "difficulty": difficulty,
    }


def mock_embed(text: str) -> list[float]:
    vector = [0.0] * len(VOCABULARY)

    tokens = re.split(r"[^A-Za-z0-9]+", text.lower())

    for token in tokens:
        if token in VOCABULARY:
            index = VOCABULARY.index(token)
            vector[index] += 1.0

    return vector


def cosine_similarity(vec_a, vec_b) -> float:
    magnitude_a = math.sqrt(
        sum(value * value for value in vec_a)
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vec_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    dot_product = 0.0

    for a, b in zip(vec_a, vec_b):
        dot_product += a * b

    return dot_product / (magnitude_a * magnitude_b)


def search_notes(query: str):
    query_vector = mock_embed(query)

    results = []

    for note in NOTES:
        note_vector = mock_embed(note["text"])

        score = cosine_similarity(
            query_vector,
            note_vector,
        )

        results.append(
            {
                "id": note["id"],
                "text": note["text"],
                "score": score,
            }
        )

    if all(value == 0.0 for value in query_vector):
        return results

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )