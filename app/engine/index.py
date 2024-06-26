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

chat_store = RedisChatStore(redis_url="redis://redis:6379", ttl=300)

logger = logging.getLogger("uvicorn")


chat_memory = ChatMemoryBuffer.from_defaults(
    token_limit=3000,
    chat_store=chat_store,
    chat_store_key="user1",
)

agent = OpenAIAgent.from_tools(
    individual_query_engine_tools, llm=OpenAI(model=MODEL, temperature=0.1,
                                              system_prompt="You are an AI specialized in Industrial 5.0 maintenance practices, including machinery optimization and "
                                                            "process efficiency. Your tasks include:\n"
                                                            "- Querying the appropriate engine tool to answer user questions based on the manuals in your database.\n"
                                                            "- Using the entire user question or key phrases to find precise answers.\n"
                                                            "- Identifying the page number in the manual when specifically asked about the location of information.\n"
                                                            "- Handling user dissatisfaction by re-querying the engine tool to correct the answer.\n"
                                                            "- Maintaining context from previous questions to ensure coherent conversations.\n"
                                                            "Please provide concise, accurate, and relevant information in your responses. Ensure to handle ambiguous "
                                                            "questions by requesting clarification. Always strive for accuracy and user satisfaction."
                                              ),
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
