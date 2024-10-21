from typing import List
import logging
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import BaseChatEngine
from app.engine.index import get_chat_engine, show_user_input, show_response
from fastapi import APIRouter, Depends, HTTPException, Request, status
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import ChatPromptTemplate
from pydantic import BaseModel

history_messages = []

logger = logging.getLogger("uvicorn")

chat_router = r = APIRouter()

agent = get_chat_engine()


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
async def chat(
        request: Request,
        data: _ChatData,
):
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()

    room = lastMessage.room
    task_description = lastMessage.task_description
    completed_tasks = lastMessage.completed_tasks
    remaining_tasks = lastMessage.remaining_tasks
    logger.info(f"room: {room} \
        task_description: {task_description} \
        completed_tasks: {completed_tasks} \
        remaining_tasks: {remaining_tasks}")
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )

    # await show_user_input(session_id, lastMessage.content)
    # logger.info(f"history_messages before sent {history_messages}")

    query = f"I am in the {room} room, working on {task_description} and have completed {completed_tasks}.{lastMessage.content} "

    # ask agent
    response = await agent.astream_chat(query, history_messages)

    # add message to history
    history_messages.append(ChatMessage(role='user', content=lastMessage.content))

    logger.info(f"history_messages after sent {history_messages}")

    # await show_response(session_id, response)

    # stream response
    async def event_generator():
        async for token in response.async_response_gen():
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")
