def format_sources(results):
    sources = []

    for result in results:
        sources.append(
            {
                "source": result["source"],
                "page": result["page"],
                "chunk": result["chunk_index"],
                "rerank_score": result["rerank_score"]
            }
        )

    return sources