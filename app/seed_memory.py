import os, sys
from memory import Memory

def main(text: str):
    mem = Memory(url=os.environ.get("QDRANT_URL","http://localhost:6333"),
                 embedding_model=os.environ.get("EMBEDDING_MODEL","BAAI/bge-m3"))
    mem.remember(text)
    print("Added to memory.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app/seed_memory.py "text to remember"")
        raise SystemExit(1)
    main(sys.argv[1])
