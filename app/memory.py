from __future__ import annotations
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

load_dotenv()

COLLECTION = "memory"

def _ensure_collection(qdr: QdrantClient, dim: int) -> None:
    try:
        cols = qdr.get_collections().collections
        if COLLECTION not in [c.name for c in cols]:
            qdr.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )
    except Exception:
        pass

class Memory:
    def __init__(self, url: str, embedding_model: str):
        self.qdr = QdrantClient(url=url)
        self.emb = TextEmbedding(model_name=embedding_model)
        dim = len(list(self.emb.embed(["dim_probe"]))[0])
        _ensure_collection(self.qdr, dim)

    def remember(self, text: str) -> None:
        v = list(self.emb.embed([text]))[0]
        self.qdr.upsert(
            collection_name=COLLECTION,
            points=[PointStruct(id=None, vector=v, payload={"text": text})],
        )

    def recall(self, query: str, k: int = 5) -> List[str]:
        v = list(self.emb.embed([query]))[0]
        hits = self.qdr.search(collection_name=COLLECTION, query_vector=v, limit=k)
        return [h.payload.get("text", "") for h in hits]
