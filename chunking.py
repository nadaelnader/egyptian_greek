# chunking.py

from preprocessing import documents, preprocess_for_bm25


def chunk_text(text, chunk_size=200, overlap=50):
    """
    Split documents into overlapping chunks optimized for embedding retrieval.
    """

    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(words):

        end = start + chunk_size

        chunks.append(
            " ".join(words[start:end])
        )

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks


def build_chunks():

    rows = []

    for document in documents:

        chunks = chunk_text(document["text"])

        for chunk_number, chunk in enumerate(chunks):

            rows.append(
                {
                    "chunk_id": f"{document['id']}_{chunk_number}",

                    "document_id": document["id"],

                    "title": document["title"],

                    "is_current": document["is_current"],

                    "chunk_text": chunk,

                    # Used for BM25 + Embedding retrieval
                    "search_text": preprocess_for_bm25(
                        f"{document['title']} {chunk}"
                    ),
                }
            )

    return rows


if __name__ == "__main__":

    chunks = build_chunks()

    print(f"Total Chunks: {len(chunks)}")
    print("-" * 80)
    print(chunks[0])
