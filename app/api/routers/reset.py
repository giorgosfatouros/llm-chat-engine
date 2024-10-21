from typing import List
import logging
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from llama_index.core.llms import ChatMessage, MessageRole
from app.api.routers.chat import history_messages
from app.engine.index import get_chat_engine
# Initialize the Redis chat store
from llama_index.storage.chat_store.redis import RedisChatStore
import os


redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
chat_store = RedisChatStore(redis_url=redis_url, ttl=300)

reset_router = r = APIRouter()

logger = logging.getLogger("uvicorn")


class _Message(BaseModel):
    role: MessageRole
    content: str
    room: str
    task_description: str
    completed_tasks: str
    remaining_tasks: str

class _ChatData(BaseModel):
    messages: List[_Message]

@r.post("")
async def reset(
        request: Request,
        data: _ChatData,
):
    try:
        # Clear Redis chat history
        chat_store.delete_messages("user1")

        # Reset agent memory
        agent = get_chat_engine()

        history_messages.clear()
        logger.info(f"Inside reset")

        room = data.messages.pop().room

        question = f"Hello! I am in room {room}. What is the purpose of this room?"

        response = await agent.astream_chat(question, history_messages)
        # Stream the reset message
        # stream response
        async def event_generator():
            async for token in response.async_response_gen():
                # If client closes connection, stop sending events
                if await request.is_disconnected():
                    break
                yield token

        return StreamingResponse(event_generator(), media_type="text/plain")
    except Exception as e:
        return {"error": str(e)}

