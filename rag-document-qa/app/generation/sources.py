def build_sources(results):
    sources = []

    for result in results:
        print("SOURCE RESULT:", result)

        sources.append(
            {
                "document_id": result["document_id"],
                "source": result["source"],
                "page": result["page"],
                "chunk": result["chunk_index"],
                "snippet": result["content"],
            }
        )

    return sources