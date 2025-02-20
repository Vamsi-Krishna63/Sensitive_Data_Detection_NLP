from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from bag_of_words import load_bag_of_words
import bag_of_words
from knowledge_graphs import query_similar_terms
from transformers import pipeline
import re

app = FastAPI()
nlp = pipeline("ner", model="dslim/bert-base-NER")

class TextData(BaseModel):
    text: str

@app.post("/detect/")
async def detect_sensitive_data(data: TextData):
    text = data.text
    bag_of_words = load_bag_of_words()
    
    detected_terms = [
        term for term in bag_of_words if term in text.lower()
    ]

    return {"detected": detected_terms}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        text = await websocket.receive_text()
        detected_terms = [
            term for term in bag_of_words if term in text.lower()
        ]
        await websocket.send_json({"detected": detected_terms})
