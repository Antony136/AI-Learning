def build_context(results):
    parts = []

    for result in results:
        parts.append(
            f"[Source: {result['source']}, "
            f"Page: {result['page']}, "
            f"Chunk: {result['chunk_index']}]\n"
            f"{result['content']}"
        )

    return "\n\n".join(parts)