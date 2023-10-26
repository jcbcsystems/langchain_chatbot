from fastapi import HTTPException, status, Security, FastAPI, Request, Body
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import os
from dotenv import load_dotenv

from chat import *
load_dotenv()

api_keys = [
    "EW2Yl7NOOsYV7v8bxB1cO7WgAPSb5h56"
]

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(
    api_key_header: str = Security(api_key_header),
)->str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chatbot")
async def chatbot(request: Request, api_key: str = Security(get_api_key)):
    data = await request.json()
    prompt = data["prompt"] 
    response = chat(prompt)
    return {"success": True, "message":response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("SERVER_PORT", 8001)))