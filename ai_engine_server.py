# app.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import ollama_tools
from system_prompt import system_prompt

# ✅ Load environment variables
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# ✅ Initialize OpenAI (Ollama-compatible) client
client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OPENAI_API_KEY,
)

# ✅ Initialize FastAPI app
app = FastAPI(title="Ollama FastAPI Chat Server", version="1.0")

# ✅ In-memory store for conversations
#    Key: session_id or websocket id; Value: conversation history list
conversation_store = {}


# ✅ Request model for REST API
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = "default"  # optional session id


# ✅ REST Chat Endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.session_id or "default"
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Get or create conversation history
    if session_id not in conversation_store:
        conversation_store[session_id] = [{"role": "system", "content": system_prompt}]

    conversation = conversation_store[session_id]

    # Append user message
    conversation.append({"role": "user", "content": user_message + "/no_think"})

    try:
        # ✅ Generate response from Ollama/OpenAI
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation,
            tools=ollama_tools,
            tool_choice="auto",
            temperature=0.9,
        )

        assistant_message = response.choices[0].message.content

        # Add to history
        conversation.append({"role": "assistant", "content": assistant_message})

        return JSONResponse(content={"response": assistant_message, "session_id": session_id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ WebSocket Chat Endpoint
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session_id = str(id(websocket))
    conversation_store[session_id] = [{"role": "system", "content": system_prompt}]
    await websocket.send_text("✅ Connected to Ollama Chat WebSocket")

    try:
        while True:
            # Wait for user message
            user_message = await websocket.receive_text()

            if user_message.lower() in ["exit", "quit"]:
                await websocket.send_text("👋 Session closed.")
                break

            # Append user message
            conversation = conversation_store[session_id]
            conversation.append({"role": "user", "content": user_message + "/no_think"})

            # Send typing indicator
            await websocket.send_text("🤖 Thinking...")

            try:
                # Generate assistant reply
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=conversation,
                    tools=ollama_tools,
                    tool_choice="auto",
                    temperature=0.9,
                )
                assistant_message = response.choices[0].message.content

                # Add to history
                conversation.append({"role": "assistant", "content": assistant_message})

                # Send response
                await websocket.send_text(assistant_message)

            except Exception as e:
                await websocket.send_text(f"❌ Error: {str(e)}")

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {session_id}")
    finally:
        # Clean up conversation store
        conversation_store.pop(session_id, None)
        await websocket.close()


# ✅ Root endpoint
@app.get("/")
async def root():
    return {"message": "Ollama FastAPI Chat Server is running 🚀"}


# # # ✅ Run the server
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("ai_engine_server:app", host="0.0.0.0", port=8000, reload=True)

# # app.py
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# from tools import ollama_tools
# from system_prompt import system_prompt

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
# app = FastAPI(title="Ollama FastAPI Chat Server")

# # ✅ Store conversation history (in-memory per session)
# conversation_history = [
#     {"role": "system", "content": system_prompt}
# ]

# # ✅ Request schema
# class ChatRequest(BaseModel):
#     message: str


# # ✅ Chat endpoint
# @app.post("/chat")
# async def chat(request: ChatRequest):
#     user_input = request.message.strip()
#     if not user_input:
#         raise HTTPException(status_code=400, detail="Message cannot be empty")

#     # Append user message to conversation
#     conversation_history.append({"role": "user", "content": user_input + "/no_think"})

#     try:
#         # ✅ Send to Ollama/OpenAI backend
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=conversation_history,
#             tools=ollama_tools,
#             tool_choice="auto",
#             temperature=0.9,
#         )

#         message = response.choices[0].message.content

#         # ✅ Append assistant reply to conversation
#         conversation_history.append({"role": "assistant", "content": message})

#         return {"response": message}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ✅ Root endpoint
# @app.get("/")
# async def root():
#     return {"message": "Ollama FastAPI Chat Server is running 🚀"}


# # ✅ Run the server (if executed directly)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("ai_engine_server:app", host="0.0.0.0", port=8000, reload=True)
