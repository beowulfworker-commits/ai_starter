import os, sys
from dotenv import load_dotenv
from memory import Memory

load_dotenv()

def main(text: str):
    mem = Memory(
        url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        embedding_model=os.environ.get("EMBEDDING_MODEL", "intfloat/multilingual-e5-base"),
    )
    mem.remember(text)
    print("Added to memory.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python app/seed_memory.py "text to remember"')
        raise SystemExit(1)
    main(sys.argv[1])
