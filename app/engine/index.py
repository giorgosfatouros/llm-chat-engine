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


 #service context??? ????????????????????????????????????/



def get_chat_engine():
    service_context = create_service_context()
    # # check if storage already exists
    # if not os.path.exists(STORAGE_DIR):
    #     raise Exception(
    #         "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
    #     )
    # logger = logging.getLogger("uvicorn")
    # # load the existing index
    # logger.info(f"Loading index from {STORAGE_DIR}...")
    # storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    # index = load_index_from_storage(storage_context, service_context=service_context)
    # logger.info(f"Finished loading index from {STORAGE_DIR}")
    # query_engine_tool = QueryEngineTool(
    #     query_engine=index.as_query_engine(),
    #     metadata=ToolMetadata(
    #         name="Routers",
    #         description="Provides specific technical information about Cisco ME4924-10E SW and Juniper EX9204 SW",
    #     )
    #     # metadata=ToolMetadata(
    #     #     name=filename,
    #     #     description=(f'Document type is {doc_type}. Manufacturer is {manufacturer}. '
    #     #                  f'Document name is {doc_title}')
    #     # )
    # )
    #
    # individual_query_engine_tools.append(query_engine_tool)
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
        verbose=True
    )
    return agent
