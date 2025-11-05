from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
from pydantic import BaseModel
import io
import base64
import PyPDF2

from tools import tools
from function import *
from system_prompt import system_prompt
from tool_registry import TOOL_REGISTRY


# ---------- ENV SETUP ----------
load_dotenv()
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME_")

# ---------- OPENAI CLIENT ----------
client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url=BASE_URL
)

# ---------- FASTAPI APP ----------
app = FastAPI()

# ---------- CONVERSATION STATE ----------
conversation_histories: Dict[str, List[Dict]] = {}


# ---------- MODELS ----------
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


# ---------- HELPERS ----------
def initialize_conversation(session_id: str):
    """Initialize a new conversation history."""
    conversation_histories[session_id] = [
        {"role": "system", "content": system_prompt},
    ]


def process_tool_calls(tool_calls):
    """Execute tool calls and return results."""
    tool_responses = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        logging.info(f"🛠️ Tool called: {tool_name} with args: {args}")

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
    """Handle incoming chat messages and manage tool calls."""
    if session_id not in conversation_histories:
        initialize_conversation(session_id)

    conversation_history = conversation_histories[session_id]
    conversation_history.append({"role": "user", "content": user_input})

    while True:
        truncated_conversation = [conversation_history[0]] + conversation_history[-10:]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=truncated_conversation,
            tools=tools,
            tool_choice="auto",
            temperature=0.9,
            max_tokens=5000
        )

        message = response.choices[0].message
        tool_calls = getattr(message, "tool_calls", None)
        ai_text = message.content if message.content else ""

        logging.info(f"Model response: {response}")

        # If the model requests a tool call
        if tool_calls:
            assistant_message = {"role": "assistant", "content": None, "tool_calls": tool_calls}
            conversation_history.append(assistant_message)

            tool_responses = process_tool_calls(tool_calls)
            conversation_history.extend(tool_responses)
            continue

        # Otherwise, normal text reply
        assistant_message = {"role": "assistant", "content": ai_text}
        conversation_history.append(assistant_message)
        return ai_text


# ---------- ROUTES ----------

@app.get("/")
async def root():
    return {"message": "Ollama FastAPI Chat Server 🚀"}


# ---------- HTTP CHAT (Supports PDF Upload) ----------
@app.post("/chat", response_model=ChatResponse)
async def http_chat_endpoint(
    session_id: str = Form("default"),
    message: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Unified chat endpoint — handles both text messages and PDF uploads.
    """
    if session_id not in conversation_histories:
        initialize_conversation(session_id)

    text_content = ""

    # ----- Handle PDF file upload -----
    if file:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        pdf_bytes = await file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)

        for page in pdf_reader.pages:
            text_content += page.extract_text() or ""

        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

        # Merge message + PDF content
        if message:
            message = f"{message}\n\n---\n📄 PDF Content:\n{text_content[:10000]}"
        else:
            message = text_content[:10000]  # truncate if large

    if not message:
        raise HTTPException(status_code=400, detail="No message or file provided")

    # Send to LLM
    ai_response = await handle_chat_message(session_id, message)
    return ChatResponse(response=ai_response, session_id=session_id)


# ---------- WEBSOCKET CHAT (Supports Base64 PDF) ----------
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    initialize_conversation(session_id)

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            file_base64 = data.get("file_base64")

            # ----- Handle PDF from base64 -----
            if file_base64:
                try:
                    pdf_bytes = base64.b64decode(file_base64)
                    pdf_stream = io.BytesIO(pdf_bytes)
                    pdf_reader = PyPDF2.PdfReader(pdf_stream)

                    text_content = ""
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() or ""

                    if not text_content.strip():
                        raise ValueError("No readable text found in PDF")

                    if message:
                        message = f"{message}\n\n---\n📄 PDF Content:\n{text_content[:10000]}"
                    else:
                        message = text_content[:10000]

                except Exception as e:
                    await websocket.send_json({"error": f"Failed to process PDF: {str(e)}"})
                    continue

            if not message:
                await websocket.send_json({"error": "No message or file provided"})
                continue

            # ----- Send to model -----
            ai_response = await handle_chat_message(session_id, message)
            await websocket.send_json({
                "message": ai_response,
                "session_id": session_id,
                "format": "markdown"
            })

    except WebSocketDisconnect:
        conversation_histories.pop(session_id, None)
        logging.info(f"Client {session_id} disconnected")


# ---------- SESSION MGMT ----------
@app.post("/new_session")
async def new_session(session_id: str = "default"):
    initialize_conversation(session_id)
    return {"message": f"New session {session_id} initialized", "session_id": session_id}


@app.get("/session_history")
async def get_session_history(session_id: str = "default"):
    if session_id not in conversation_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse(content=conversation_histories[session_id])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import json
# import logging
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
# from fastapi.responses import JSONResponse
# from typing import Dict, List, Optional
# from pydantic import BaseModel

# from tools import tools
# from function import *
# from system_prompt import system_prompt
# from tool_registry import TOOL_REGISTRY

# # Load environment variables
# load_dotenv()

# DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
# BASE_URL = os.getenv("BASE_URL")
# MODEL_NAME = os.getenv("MODEL_NAME_")

# # Initialize client
# client = OpenAI(
#     api_key=DATABRICKS_TOKEN,
#     base_url=BASE_URL
# )

# # FastAPI app
# app = FastAPI()

# # Store per-session conversation histories
# conversation_histories: Dict[str, List[Dict]] = {}


# # ---------- MODELS ----------
# class ChatRequest(BaseModel):
#     message: str
#     session_id: Optional[str] = "default"


# class ChatResponse(BaseModel):
#     response: str
#     session_id: str


# # ---------- CONVERSATION UTILS ----------
# def initialize_conversation(session_id: str):
#     """Initialize a new conversation history."""
#     conversation_histories[session_id] = [
#         {"role": "system", "content": system_prompt},
#     ]


# def process_tool_calls(tool_calls):
#     """Execute tool calls and return results."""
#     tool_responses = []
#     for tool_call in tool_calls:
#         tool_name = tool_call.function.name
#         args = json.loads(tool_call.function.arguments)

#         logging.info(f"🛠️ Tool called: {tool_name} with args: {args}")

#         func = TOOL_REGISTRY.get(tool_name)
#         if func:
#             try:
#                 result = func(**args)
#             except Exception as e:
#                 result = f"Error while executing {tool_name}: {str(e)}"
#         else:
#             result = f"Error: Unknown tool {tool_name}"

#         tool_responses.append({
#             "role": "tool",
#             "name": tool_name,
#             "content": str(result),
#             "tool_call_id": tool_call.id
#         })

#     return tool_responses


# # ---------- MAIN CHAT LOOP ----------
# async def handle_chat_message(session_id: str, user_input: str):
#     """Handle incoming chat messages and manage tool calls."""
#     if session_id not in conversation_histories:
#         initialize_conversation(session_id)

#     conversation_history = conversation_histories[session_id]
#     conversation_history.append({"role": "user", "content": user_input})

#     while True:
#         truncated_conversation = [conversation_history[0]] + conversation_history[-10:]

#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=truncated_conversation,
#             tools=tools,
#             tool_choice="auto",
#             temperature=0.9,
#             max_tokens=5000
#         )

#         message = response.choices[0].message
#         tool_calls = getattr(message, "tool_calls", None)
#         ai_text = message.content if message.content else ""

#         # Log response
#         logging.info(f"Model response: {response}")

#         # If the model requests a tool call
#         if tool_calls:
#             assistant_message = {"role": "assistant", "content": None, "tool_calls": tool_calls}
#             conversation_history.append(assistant_message)

#             tool_responses = process_tool_calls(tool_calls)
#             conversation_history.extend(tool_responses)
#             continue  # Ask the model again after tool responses

#         # Otherwise, it's a normal text response
#         assistant_message = {"role": "assistant", "content": ai_text}
#         conversation_history.append(assistant_message)
#         return ai_text


# # ---------- ROUTES ----------
# @app.get("/")
# async def root():
#     return {"message": "Ollama FastAPI Chat Server 🚀"}


# @app.websocket("/ws/{session_id}")
# async def websocket_endpoint(websocket: WebSocket, session_id: str):
#     await websocket.accept()
#     initialize_conversation(session_id)

#     try:
#         while True:
#             user_input = await websocket.receive_text()
#             ai_response = await handle_chat_message(session_id, user_input)

#             await websocket.send_json({
#                 "message": ai_response,
#                 "format": "markdown"
#             })

#     except WebSocketDisconnect:
#         conversation_histories.pop(session_id, None)
#         logging.info(f"Client {session_id} disconnected")


# @app.post("/chat", response_model=ChatResponse)
# async def http_chat_endpoint(chat_request: ChatRequest):
#     response = await handle_chat_message(chat_request.session_id, chat_request.message)
#     return ChatResponse(response=response, session_id=chat_request.session_id)


# @app.post("/new_session")
# async def new_session(session_id: str = "default"):
#     initialize_conversation(session_id)
#     return {"message": f"New session {session_id} initialized", "session_id": session_id}


# @app.get("/session_history")
# async def get_session_history(session_id: str = "default"):
#     if session_id not in conversation_histories:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return JSONResponse(content=conversation_histories[session_id])


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": exc.detail},
#     )

# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import os
# from typing import Dict, List, Optional
# from pydantic import BaseModel
# import re

# load_dotenv()

# # How to get your Databricks token: https://docs.databricks.com/en/dev-tools/auth/pat.html
# DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')
# BASE_URL = os.environ.get('BASE_URL')
# MODEL_NAME = os.environ.get('MODEL_NAME_')



# client = OpenAI(
#     api_key=DATABRICKS_TOKEN ,
#     base_url=BASE_URL
# )




# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
# from fastapi.responses import JSONResponse
# from openai import OpenAI
# import json
# from tools import  tools 
# from function import *
# from system_prompt import system_prompt
# from tool_registry import TOOL_REGISTRY
# import logging
# from dotenv import load_dotenv
# import os
# from typing import Dict, List, Optional
# from pydantic import BaseModel



# load_dotenv()

# # Constants
# # MODEL_NAME = os.getenv("MODEL_NAME")

# app = FastAPI()

# # Store conversation histories per session
# conversation_histories: Dict[str, List[Dict]] = {}

# class ChatRequest(BaseModel):
#     message: str
#     session_id: Optional[str] = "default"

# class ChatResponse(BaseModel):
#     response: str
#     session_id: str


# client = OpenAI(
#     api_key=DATABRICKS_TOKEN ,
#     base_url=BASE_URL
# )
# def initialize_conversation(session_id: str):
#     """Initialize a new conversation history"""
#     conversation_histories[session_id] = [
#         {"role": "system", "content": system_prompt},
#     ]

# def process_tool_calls(tool_calls):
#     """Process tool calls and return results using dynamic dispatch."""
#     tool_responses = []
#     for tool_call in tool_calls:
#         tool_name = tool_call.function.name
#         args = json.loads(tool_call.function.arguments)

#         logging.info(f"🛠️  Tool called: {tool_name} with args: {args}")

#         # Get the function from the dispatcher
#         func = TOOL_REGISTRY.get(tool_name)

#         if func:
#             try:
#                 result = func(**args)
#             except Exception as e:
#                 result = f"Error while executing {tool_name}: {str(e)}"
#         else:
#             result = f"Error: Unknown tool {tool_name}"

#         tool_responses.append({
#             "role": "tool",
#             "name": tool_name,
#             "content": str(result),
#             "tool_call_id": tool_call.id
#         })

#     return tool_responses

# async def handle_chat_message(session_id: str, user_input: str):
#     """Handle incoming chat message and generate response"""
#     if session_id not in conversation_histories:
#         initialize_conversation(session_id)
    
#     conversation_history = conversation_histories[session_id]
#     # user_input = user_input + " " + "/no_think"
#     user_input = user_input 

#     conversation_history.append({"role": "user", "content": user_input})

#     while True:
#         # Prepare messages: system prompt + last 10 items
#         truncated_conversation = [conversation_history[0]] + conversation_history[-10:]

#         # Get model response

#         response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=truncated_conversation,
#         tools=tools,
#         tool_choice="auto",
#         temperature=0.9,
#         max_tokens=5000)


#         # print(response.choices[0].message)
#         message  = response
#         print(message)
#         content_parts = response.choices[0].message.content


#         if isinstance(content_parts, list):
#             ai_text = next(
#                 (part.get('text') for part in content_parts if isinstance(part, dict) and part.get('type') == 'text'),
#                 None
#             )
#         else:
#             ai_text = content_parts  # fallback to plain text

#         assistant_message = {"role": "assistant", "content": ai_text}

#         if hasattr(message, 'tool_calls') and message.tool_calls:
#             assistant_message["tool_calls"] = message.tool_calls
        
#         conversation_history.append(assistant_message)

#         # If there are tool calls, process them and continue
#         if hasattr(message, 'tool_calls') and message.tool_calls:
#             tool_responses = process_tool_calls(message.tool_calls)
#             conversation_history.extend(tool_responses)
#         else:
#             # No more tool calls, return response
#             return ai_text


# @app.get("/")
# async def root():
#     """
#     Root endpoint to confirm the server is running.
#     """
#     return {"message": "Ollama FastAPI Chat Server iss  🚀"}
# # WebSocket endpoint
# @app.websocket("/ws/{session_id}")
# async def websocket_endpoint(websocket: WebSocket, session_id: str):
#     await websocket.accept()
#     initialize_conversation(session_id)

#     try:
#         while True:
#             user_input = await websocket.receive_text()
#             ai_response = await handle_chat_message(session_id, user_input)

#             # send JSON message directly
#             await websocket.send_json({
#                 "message": ai_response,
#                 "format": "markdown"
#             })

#     except WebSocketDisconnect:
#         conversation_histories.pop(session_id, None)
#         logging.info(f"Client {session_id} disconnected")

# # HTTP POST endpoints for testing
# @app.post("/chat", response_model=ChatResponse)
# async def http_chat_endpoint(chat_request: ChatRequest):
#     """HTTP endpoint for chat (for testing purposes)"""
#     response = await handle_chat_message(chat_request.session_id, chat_request.message)
#     return ChatResponse(response=response, session_id=chat_request.session_id)

# @app.post("/new_session")
# async def new_session(session_id: str = "default"):
#     """Initialize a new conversation session"""
#     initialize_conversation(session_id)
#     return {"message": f"New session {session_id} initialized", "session_id": session_id}

# @app.get("/session_history")
# async def get_session_history(session_id: str = "default"):
#     """Get the conversation history for a session"""
#     if session_id not in conversation_histories:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return JSONResponse(content=conversation_histories[session_id])

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": exc.detail},
#     )
