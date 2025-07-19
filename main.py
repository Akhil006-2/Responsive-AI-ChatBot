from fastapi import FastAPI, HTTPException # its a web backend framework 
from fastapi.middleware.cors import CORSMiddleware #allows the streamlit frontend to call this api
from fastapi.responses import StreamingResponse # used for streaming(chunk by chunk)
from typing import AsyncGenerator #type hint async
from pydantic import BaseModel
import anthropic
import asyncio #simulates a typing delay 
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL

app = FastAPI() #initializing the fastapi app instance 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)#this enables the cross origin requests so that streamlit frontend can make api calls to localhost without browser blocking them

class ChatRequest(BaseModel):
    message: str
    history: list = None  

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):# req accesses the class ChatRequest , which contains user's input , and past messages 
    #print(f"📥 Received stream request: {req.message}")

    async def stream_generator() -> AsyncGenerator[str, None]:# yields small text chunks from claude
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)#uses the api key to access anthroopic claude
        messages = []#will store the formatted conversation history 

        # Format history for Claude
        if req.history:
            for i, h in enumerate(req.history):
                if isinstance(h, dict) and "role" in h and "content" in h:
                    messages.append({"role": h["role"], "content": h["content"]})
                else:
                    role = "user" if i % 2 == 0 else "assistant"
                    messages.append({"role": role, "content": h})

        messages.append({"role": "user", "content": req.message})#soo now messages holds the full chat context claude needs
        #print(f"📤 Sending to Claude ({ANTHROPIC_MODEL}): {messages}")

        try:
            stream = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=512,
                messages=messages,
                stream=True,#tells the claude to send back the response token by token 
            )#stream is now an iterable object that yields chunks 

            for event in stream:
                if event.type == "content_block_delta":
                    yield event.delta.text#THIS yield event.delta.text is the exact place Claude's text is sent back to the frontend.
                    await asyncio.sleep(0.01)  # typing delay (optional)
        except Exception as e:
            yield f"\n[ERROR] {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/plain")#StreamingResponse(...) sends that data to Streamlit
