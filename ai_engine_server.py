from openai import OpenAI
import os
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
import re

load_dotenv()

# How to get your Databricks token: https://docs.databricks.com/en/dev-tools/auth/pat.html
DATABRICKS_TOKEN = os.environ.get('DATABRICKS_TOKEN')
BASE_URL = os.environ.get('BASE_URL')
MODEL_NAME = os.environ.get('MODEL_NAME_')



client = OpenAI(
    api_key=DATABRICKS_TOKEN ,
    base_url=BASE_URL
)







from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
import json
from tools import ollama_tools, tools 
from function import *
from system_prompt import system_prompt
from tool_registry import TOOL_REGISTRY
import logging
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
from pydantic import BaseModel



load_dotenv()

# Constants
# MODEL_NAME = os.getenv("MODEL_NAME")

app = FastAPI()

# Store conversation histories per session
conversation_histories: Dict[str, List[Dict]] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str


client = OpenAI(
    api_key=DATABRICKS_TOKEN ,
    base_url=BASE_URL
)
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
    # user_input = user_input + " " + "/no_think"
    user_input = user_input 

    conversation_history.append({"role": "user", "content": user_input})

    while True:
        # Prepare messages: system prompt + last 10 items
        truncated_conversation = [conversation_history[0]] + conversation_history[-10:]

        # Get model response

        response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=truncated_conversation,
        # tools=tools,
        # tool_choice="auto",
        temperature=0.9,
        max_tokens=5000
        )




        # print(response.choices[0].message)
        message  = response
        content_parts = response.choices[0].message.content

        # content_parts is a list like: [{'type': 'reasoning', ...}, {'type': 'text', 'text': 'Hello! How can I help you today?'}]
        ai_text = next(
            (part.get('text') for part in content_parts if isinstance(part, dict) and part.get('type') == 'text'),
            None
        )
        ai_text = re.sub(r"\*\*(.*?)\*\*", r"\1", ai_text)

        print(ai_text)



        # Add assistant response to full history
        assistant_message = {
            "role": "assistant",
            "content": ai_text,
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
            return ai_text




@app.get("/")
async def root():
    """
    Root endpoint to confirm the server is running.
    """
    return {"message": "Ollama FastAPI Chat Server iss  🚀"}
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

# # app.py
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# from tools import ollama_tools
# from system_prompt import system_prompt
# from function import *


# # ✅ Load environment variables
# load_dotenv()

# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# MODEL_NAME = os.getenv("MODEL_NAME")

# # ✅ Initialize OpenAI (Ollama-compatible) client
# client = OpenAI(
#     base_url=OLLAMA_BASE_URL,
#     api_key=OPENAI_API_KEY,
# )

# # ✅ Initialize FastAPI app
# app = FastAPI(title="Ollama FastAPI Chat Server", version="1.0")

# # ✅ In-memory store for conversations
# #    Key: session_id or websocket id; Value: conversation history list
# conversation_store = {}


# # ✅ Request model for REST API
# class ChatRequest(BaseModel):
#     message: str
#     session_id: str | None = "default"  # optional session id

# # --- Refactored Helper Functions ---

# def get_and_update_conversation(session_id: str, user_message: str) -> list:
#     """
#     Retrieves or initializes a conversation history for a given session_id
#     and appends the new user message to it.
#     """
#     # Get or create conversation history
#     if session_id not in conversation_store:
#         conversation_store[session_id] = [{"role": "system", "content": system_prompt}]
    
#     conversation = conversation_store[session_id]
    
#     # Append user message
#     conversation.append({"role": "user", "content": user_message + "/no_think"})
    
#     return conversation

# def generate_assistant_reply(conversation: list) -> str:
#     """
#     Calls the LLM with the conversation, appends the assistant's
#     reply to the history, and returns the assistant's message.
    
#     Propagates exceptions to be handled by the caller.
#     """
#     # ✅ Generate response from Ollama/OpenAI
#     #    (Exceptions are intentionally not caught here,
#     #     so they can be handled by the endpoint)
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=conversation,
#         tools=ollama_tools,
#         tool_choice="auto",
#         temperature=0.9,
#     )

#     # assistant_message = response.choices[0].message.content

#     # response_content = message.content.strip() if message.content else ""
#     # clean_response = response_content.replace("<think>\n\n</think>", "").strip()
    
#     message = response.choices[0].message
#     response_content = message.content.strip() if message.content else ""
#     assistant_message  = response_content.replace("<think>\n\n</think>", "").strip()



#     # Add to history
#     conversation.append({"role": "assistant", "content": assistant_message})
    
#     return assistant_message

# # --- Endpoints ---

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     """
#     Handles a single chat message via REST API.
#     """
#     user_message = request.message.strip()
#     if not user_message:
#         raise HTTPException(status_code=400, detail="Message cannot be empty")

#     session_id = request.session_id or "default"

#     try:
#         # Get history and add user message
#         conversation = get_and_update_conversation(session_id, user_message)
        
#         # Generate and add assistant reply
#         assistant_message = generate_assistant_reply(conversation)
        
#         return JSONResponse(content={"response": assistant_message, "session_id": session_id})

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.websocket("/ws/chat")
# async def websocket_chat(websocket: WebSocket):
#     """
#     Handles a persistent chat session via WebSocket.
#     """
#     await websocket.accept()
#     session_id = str(id(websocket))
    
#     # Initialize conversation store for this new session
#     conversation_store[session_id] = [{"role": "system", "content": system_prompt}]
    
#     await websocket.send_text("✅ Connected to Ollama Chat WebSocket")

#     try:
#         while True:
#             # Wait for user message
#             user_message = await websocket.receive_text()

#             if user_message.lower() in ["exit", "quit"]:
#                 await websocket.send_text("👋 Session closed.")
#                 break

#             # Send typing indicator
#             # await websocket.send_text("🤖 Thinking...")

#             try:
#                 # Get history and add user message
#                 conversation = get_and_update_conversation(session_id, user_message)
                
#                 # Generate and add assistant reply
#                 assistant_message = generate_assistant_reply(conversation)

#                 # Send response
#                 await websocket.send_text(assistant_message)

#             except Exception as e:
#                 await websocket.send_text(f"❌ Error: {str(e)}")

#     except WebSocketDisconnect:
#         print(f"WebSocket disconnected: {session_id}")
#     finally:
#         # Clean up conversation store
#         conversation_store.pop(session_id, None)
#         await websocket.close()


# @app.get("/")
# async def root():
#     """
#     Root endpoint to confirm the server is running.
#     """
#     return {"message": "Ollama FastAPI Chat Server is running 🚀"}
# # # app.py
# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
# # from fastapi.responses import JSONResponse
# # from pydantic import BaseModel
# # from openai import OpenAI
# # from dotenv import load_dotenv
# # import os
# # from tools import ollama_tools
# # from system_prompt import system_prompt

# # # ✅ Load environment variables
# # load_dotenv()

# # OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # MODEL_NAME = os.getenv("MODEL_NAME")

# # # ✅ Initialize OpenAI (Ollama-compatible) client
# # client = OpenAI(
# #     base_url=OLLAMA_BASE_URL,
# #     api_key=OPENAI_API_KEY,
# # )

# # # ✅ Initialize FastAPI app
# # app = FastAPI(title="Ollama FastAPI Chat Server", version="1.0")

# # # ✅ In-memory store for conversations
# # #    Key: session_id or websocket id; Value: conversation history list
# # conversation_store = {}


# # # ✅ Request model for REST API
# # class ChatRequest(BaseModel):
# #     message: str
# #     session_id: str | None = "default"  # optional session id


# # # ✅ REST Chat Endpoint
# # @app.post("/chat")
# # async def chat(request: ChatRequest):
# #     session_id = request.session_id or "default"
# #     user_message = request.message.strip()
# #     if not user_message:
# #         raise HTTPException(status_code=400, detail="Message cannot be empty")

# #     # Get or create conversation history
# #     if session_id not in conversation_store:
# #         conversation_store[session_id] = [{"role": "system", "content": system_prompt}]

# #     conversation = conversation_store[session_id]

# #     # Append user message
# #     conversation.append({"role": "user", "content": user_message + "/no_think"})

# #     try:
# #         # ✅ Generate response from Ollama/OpenAI
# #         response = client.chat.completions.create(
# #             model=MODEL_NAME,
# #             messages=conversation,
# #             tools=ollama_tools,
# #             tool_choice="auto",
# #             temperature=0.9,
# #         )

# #         assistant_message = response.choices[0].message.content

# #         # Add to history
# #         conversation.append({"role": "assistant", "content": assistant_message})

# #         return JSONResponse(content={"response": assistant_message, "session_id": session_id})

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# # # ✅ WebSocket Chat Endpoint
# # @app.websocket("/ws/chat")
# # async def websocket_chat(websocket: WebSocket):
# #     await websocket.accept()
# #     session_id = str(id(websocket))
# #     conversation_store[session_id] = [{"role": "system", "content": system_prompt}]
# #     await websocket.send_text("✅ Connected to Ollama Chat WebSocket")

# #     try:
# #         while True:
# #             # Wait for user message
# #             user_message = await websocket.receive_text()

# #             if user_message.lower() in ["exit", "quit"]:
# #                 await websocket.send_text("👋 Session closed.")
# #                 break

# #             # Append user message
# #             conversation = conversation_store[session_id]
# #             conversation.append({"role": "user", "content": user_message + "/no_think"})

# #             # Send typing indicator
# #             await websocket.send_text("🤖 Thinking...")

# #             try:
# #                 # Generate assistant reply
# #                 response = client.chat.completions.create(
# #                     model=MODEL_NAME,
# #                     messages=conversation,
# #                     tools=ollama_tools,
# #                     tool_choice="auto",
# #                     temperature=0.9,
# #                 )
# #                 assistant_message = response.choices[0].message.content

# #                 # Add to history
# #                 conversation.append({"role": "assistant", "content": assistant_message})

# #                 # Send response
# #                 await websocket.send_text(assistant_message)

# #             except Exception as e:
# #                 await websocket.send_text(f"❌ Error: {str(e)}")

# #     except WebSocketDisconnect:
# #         print(f"WebSocket disconnected: {session_id}")
# #     finally:
# #         # Clean up conversation store
# #         conversation_store.pop(session_id, None)
# #         await websocket.close()


# # # ✅ Root endpoint
# # @app.get("/")
# # async def root():
# #     return {"message": "Ollama FastAPI Chat Server is running 🚀"}


# # # # ✅ Run the server
# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("ai_engine_server:app", host="0.0.0.0", port=8000, reload=True)

# # # app.py
# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # from openai import OpenAI
# # from dotenv import load_dotenv
# # import os
# # from tools import ollama_tools
# # from system_prompt import system_prompt

# # # ✅ Load environment variables
# # load_dotenv()

# # OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
# # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # MODEL_NAME = os.getenv("MODEL_NAME")

# # # ✅ Initialize OpenAI (Ollama-compatible) client
# # client = OpenAI(
# #     base_url=OLLAMA_BASE_URL,
# #     api_key=OPENAI_API_KEY,
# # )

# # # ✅ Initialize FastAPI app
# # app = FastAPI(title="Ollama FastAPI Chat Server")

# # # ✅ Store conversation history (in-memory per session)
# # conversation_history = [
# #     {"role": "system", "content": system_prompt}
# # ]

# # # ✅ Request schema
# # class ChatRequest(BaseModel):
# #     message: str


# # # ✅ Chat endpoint
# # @app.post("/chat")
# # async def chat(request: ChatRequest):
# #     user_input = request.message.strip()
# #     if not user_input:
# #         raise HTTPException(status_code=400, detail="Message cannot be empty")

# #     # Append user message to conversation
# #     conversation_history.append({"role": "user", "content": user_input + "/no_think"})

# #     try:
# #         # ✅ Send to Ollama/OpenAI backend
# #         response = client.chat.completions.create(
# #             model=MODEL_NAME,
# #             messages=conversation_history,
# #             tools=ollama_tools,
# #             tool_choice="auto",
# #             temperature=0.9,
# #         )

# #         message = response.choices[0].message.content

# #         # ✅ Append assistant reply to conversation
# #         conversation_history.append({"role": "assistant", "content": message})

# #         return {"response": message}

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# # # ✅ Root endpoint
# # @app.get("/")
# # async def root():
# #     return {"message": "Ollama FastAPI Chat Server is running 🚀"}


# # # ✅ Run the server (if executed directly)
# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("ai_engine_server:app", host="0.0.0.0", port=8000, reload=True)
