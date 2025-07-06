
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import AzureOpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure OpenAI setup using API key
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "your-api-key-here")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-endpoint.openai.azure.com/")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "your-deployment-name")

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="6VxkgheS2bkn1upOXNW2JohIAH5n7Twqf9oB30wMIlr4ya507KEdJQQJ99BCACHYHv6XJ3w3AAAAACOGm9lG",  # ← use Key1 or Key2 here
    azure_endpoint="https://ai-dakaplhubeus2789868823382.openai.azure.com/",
    api_version="2025-01-01-preview"
)

class Query(BaseModel):
    inputs: str

@app.post("/invoke")
async def invoke(query: Query):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that helps users find accurate and pertinent information efficiently."
            },
            {
                "role": "user",
                "content": query.inputs
            }
        ]

        completion = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )

        return {"response": completion.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
