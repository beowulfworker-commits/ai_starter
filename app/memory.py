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

class _EmbeddingAdapter:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._mode = "fastembed"
        try:
            self._model = TextEmbedding(model_name=model_name)
        except ValueError:
            self._mode = "sentence_transformers"
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as err:  # pragma: no cover - defensive branch
                raise RuntimeError(
                    "sentence-transformers is required for non-fastembed models"
                ) from err
            self._model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self._mode == "fastembed":
            return [
                vector.tolist() if hasattr(vector, "tolist") else list(vector)
                for vector in self._model.embed(texts)
            ]

        vectors = self._model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return [vector.tolist() if hasattr(vector, "tolist") else list(vector) for vector in vectors]


class Memory:
    def __init__(self, url: str, embedding_model: str):
        self.qdr = QdrantClient(url=url)
        self.emb = _EmbeddingAdapter(model_name=embedding_model)
        dim = len(self.emb.embed(["dim_probe"])[0])
        _ensure_collection(self.qdr, dim)

    def remember(self, text: str) -> None:
        v = self.emb.embed([text])[0]
        self.qdr.upsert(
            collection_name=COLLECTION,
            points=[PointStruct(id=None, vector=v, payload={"text": text})],
        )

    def recall(self, query: str, k: int = 5) -> List[str]:
        v = self.emb.embed([query])[0]
        hits = self.qdr.search(collection_name=COLLECTION, query_vector=v, limit=k)
        return [h.payload.get("text", "") for h in hits]
