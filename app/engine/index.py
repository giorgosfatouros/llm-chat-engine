import logging
import os
from llama_index.agent.openai.base import OpenAIAgent
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI

from app.engine.constants import STORAGE_DIR, MODEL
from app.engine.context import create_service_context
from app.__init__ import individual_query_engine_tools
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.redis import RedisChatStore


redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
chat_store = RedisChatStore(redis_url=redis_url, ttl=300)

logger = logging.getLogger("uvicorn")


chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)
with open('app/engine/system_prompt.md', 'r') as file:
    base_prompt = file.read()
agent = OpenAIAgent.from_tools(
    individual_query_engine_tools, llm=OpenAI(model=MODEL, temperature=0.1),
    system_prompt = base_prompt,
    verbose=True,
    memory=chat_memory
)


# Helper Functions
async def show_user_input(session_id: str, user_input: str):
    logger.info(f"------------BEFORE --------------------")
    agent_memory = agent.memory.get_all()
    logger.info(f"agent_memory: {agent_memory}")
    session_messages = chat_store.get_messages('user1')
    logger.info(f"session_messages of user: {session_messages}")


async def show_response(session_id: str, response):
    logger.info(f"------------AFTER --------------------")
    agent_memory = agent.memory.get_all()
    logger.info(f"agent_memory: {agent_memory}")
    session_messages = chat_store.get_messages('user1')
    logger.info(f"session_messages of user: {session_messages}")


def get_chat_engine():
    return agent
