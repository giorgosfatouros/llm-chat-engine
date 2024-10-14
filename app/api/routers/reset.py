from typing import List
import logging
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from llama_index.core.llms import ChatMessage, MessageRole

reset_router = r = APIRouter()

logger = logging.getLogger("uvicorn")


class _Message(BaseModel):
    role: MessageRole
    content: str

class _ChatData(BaseModel):
    messages: List[_Message]

@r.post("")
async def reset(
        request: Request,
        data: _ChatData,
):
    logger.info(f"Inside reset")
    return