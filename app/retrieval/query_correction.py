from difflib import SequenceMatcher


COMMON_WORDS = {
    "what",
    "where",
    "when",
    "why",
    "how",
    "which",
    "who",
    "is",
    "are",
    "was",
    "were",
    "the",
    "a",
    "an",
    "of",
    "in",
    "to",
    "for",
    "and",
    "or",
    "explain",
    "describe",
}


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def edit_distance(a: str, b: str) -> int:
    a = a.lower()
    b = b.lower()

    rows = len(a) + 1
    cols = len(b) + 1

    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i

    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1],
                )

    return dp[-1][-1]


def is_suspicious_word(word: str) -> bool:
    clean_word = word.lower()

    if len(clean_word) < 4:
        return False

    if clean_word in COMMON_WORDS:
        return False

    if any(char.isdigit() for char in clean_word):
        return False

    return True


def find_best_candidate(
    word: str,
    vocabulary: set[str],
    similarity_threshold: float = 0.90,
    max_edit_distance: int = 2,
):
    clean_word = word.lower()

    if not is_suspicious_word(clean_word):
        return None

    if clean_word in vocabulary:
        return None

    best_candidate = None
    best_score = 0.0
    best_distance = None

    for candidate in vocabulary:
        distance = edit_distance(clean_word, candidate)

        if distance > max_edit_distance:
            continue

        score = similarity(clean_word, candidate)

        if score > best_score:
            best_score = score
            best_candidate = candidate
            best_distance = distance

    if best_candidate is None:
        return None

    if best_score < similarity_threshold:
        return None

    return {
        "original": word,
        "corrected": best_candidate,
        "score": best_score,
        "edit_distance": best_distance,
    }


def correct_query(
    query: str,
    vocabulary: set[str],
    similarity_threshold: float = 0.90,
    max_edit_distance: int = 2,
):
    words = query.split()

    corrected_words = []
    corrections = []

    for word in words:
        clean_word = word.strip(".,!?;:\"'()[]{}")

        candidate = find_best_candidate(
            clean_word,
            vocabulary,
            similarity_threshold=similarity_threshold,
            max_edit_distance=max_edit_distance,
        )

        if candidate:
            corrected_words.append(candidate["corrected"])

            corrections.append(candidate)
        else:
            corrected_words.append(word)

    corrected_query = " ".join(corrected_words)

    return corrected_query, corrections