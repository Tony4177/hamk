import requests
import os

HF_TOKEN = os.getenv("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")

def get_ai_response(question):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": f"Bearer {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}"}
    
    payload = {"inputs": question}

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "AI temporarily unavailable."
