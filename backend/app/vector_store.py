import chromadb


# Create ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")


# Create or get collection
collection = client.get_or_create_collection(
    name="resume_collection"
)


def store_resume_chunks(chunks, embeddings):

    ids = [
        f"resume_chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(ids)


def search_resume(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results