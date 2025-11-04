from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import json
from tools import ollama_tools
from function import *
from system_prompt import system_prompt
from tool_registry import TOOL_REGISTRY
import logging
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
from openai_client.client import client, client_bricks


load_dotenv()

# Constants
MODEL_NAME = os.getenv("MODEL_NAME")

app = FastAPI()

# Store conversation histories per session
conversation_histories: Dict[str, List[Dict]] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

def initialize_conversation(session_id: str):
    """Initialize a new conversation history"""
    conversation_histories[session_id] = [
        {"role": "system", "content": system_prompt},
    ]

def process_tool_calls(tool_calls):
    """Process tool calls and return results using dynamic dispatch."""
    tool_responses = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        logging.info(f"🛠️  Tool called: {tool_name} with args: {args}")

        # Get the function from the dispatcher
        func = TOOL_REGISTRY.get(tool_name)

        if func:
            try:
                result = func(**args)
            except Exception as e:
                result = f"Error while executing {tool_name}: {str(e)}"
        else:
            result = f"Error: Unknown tool {tool_name}"

        tool_responses.append({
            "role": "tool",
            "name": tool_name,
            "content": str(result),
            "tool_call_id": tool_call.id
        })

    return tool_responses

async def handle_chat_message(session_id: str, user_input: str):
    """Handle incoming chat message and generate response"""
    if session_id not in conversation_histories:
        initialize_conversation(session_id)
    
    conversation_history = conversation_histories[session_id]
    user_input = user_input + " " + "/no_think"
    conversation_history.append({"role": "user", "content": user_input})

    while True:
        # Prepare messages: system prompt + last 10 items
        truncated_conversation = [conversation_history[0]] + conversation_history[-10:]

        # Get model response
        response = client.chat.completions.create(
            messages=truncated_conversation,
            model=MODEL_NAME,
            tools=ollama_tools,
            tool_choice="auto",
            temperature=0.9
        )

        message = response.choices[0].message
        response_content = message.content.strip() if message.content else ""
        clean_response = response_content.replace("<think>\n\n</think>", "").strip()

        # Add assistant response to full history
        assistant_message = {
            "role": "assistant",
            "content": clean_response,
        }
        if hasattr(message, 'tool_calls') and message.tool_calls:
            assistant_message["tool_calls"] = message.tool_calls
        
        conversation_history.append(assistant_message)

        # If there are tool calls, process them and continue
        if hasattr(message, 'tool_calls') and message.tool_calls:
            tool_responses = process_tool_calls(message.tool_calls)
            conversation_history.extend(tool_responses)
        else:
            # No more tool calls, return response
            return clean_response




@app.get("/")
async def root():
    """
    Root endpoint to confirm the server is running.
    """
    return {"message": "Ollama FastAPI Chat Server is  🚀"}
# WebSocket endpoint
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    initialize_conversation(session_id)

    try:
        while True:
            # Receive user message
            user_input = await websocket.receive_text()
            
            # Process message and get response
            response = await handle_chat_message(session_id, user_input)
            
            # Send response back to client
            await websocket.send_text(response)
            
    except WebSocketDisconnect:
        # Clean up on disconnect
        conversation_histories.pop(session_id, None)
        logging.info(f"Client {session_id} disconnected")

# HTTP POST endpoints for testing
@app.post("/chat", response_model=ChatResponse)
async def http_chat_endpoint(chat_request: ChatRequest):
    """HTTP endpoint for chat (for testing purposes)"""
    response = await handle_chat_message(chat_request.session_id, chat_request.message)
    return ChatResponse(response=response, session_id=chat_request.session_id)

@app.post("/new_session")
async def new_session(session_id: str = "default"):
    """Initialize a new conversation session"""
    initialize_conversation(session_id)
    return {"message": f"New session {session_id} initialized", "session_id": session_id}

@app.get("/session_history")
async def get_session_history(session_id: str = "default"):
    """Get the conversation history for a session"""
    if session_id not in conversation_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse(content=conversation_histories[session_id])

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)