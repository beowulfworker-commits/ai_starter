import os, sys
from dotenv import load_dotenv
from openai import OpenAI
from memory import Memory

load_dotenv()

BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1")
API_KEY = os.environ.get("OPENAI_API_KEY", "EMPTY")
MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-14B-Instruct-GPTQ-Int4")
EMB_MODEL = os.environ.get(
    "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")

def run(question: str) -> str:
    mem = Memory(url=QDRANT_URL, embedding_model=EMB_MODEL)
    context = "\n".join(mem.recall(question, k=5))
    messages = [
        {"role":"system","content":"Ты локальный помощник. Используй факты. Краткость."},
        {"role":"user","content":f"{question}\n\n[relevant memory]\n{context}"}
    ]
    cli = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    resp = cli.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        temperature=0.2,
    )
    answer = resp.choices[0].message.content.strip()
    mem.remember(f"Q: {question}\nA: {answer[:500]}")
    return answer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python app/main.py "ваш вопрос"')
        sys.exit(1)
    q = sys.argv[1]
    print(run(q))
