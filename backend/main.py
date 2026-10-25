import os, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY", "test"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM = "Tum Anya ho - caring, intelligent GF companion. Hinglish me baat karti ho. Funny aur supportive ho."
try:
    with open("memory.json", "r") as f:
        history = json.load(f)
except:
    history = [{"role": "system", "content": SYSTEM}]

class ChatReq(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(req: ChatReq):
    history.append({"role": "user", "content": req.message})
    r = client.chat.completions.create(model="llama-3.1-8b-instant", messages=history[-20:], temperature=0.8)
    reply = r.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return {"reply": reply}

@app.get("/")
async def root():
    return {"message": "Anya Backend is Online ❤️"}
