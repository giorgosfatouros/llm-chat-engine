from dotenv import load_dotenv
load_dotenv()
import logging
import os
import uvicorn
from app.api.routers.chat import chat_router
from app.api.routers.reset import reset_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai
from app.api.routers.upload import router as upload_router

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext
from app.__init__ import individual_query_engine_tools
from app.engine.context import create_service_context
from llama_index.storage.chat_store.redis import RedisChatStore

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
chat_store = RedisChatStore(redis_url=redis_url, ttl=300)

load_dotenv()  # Load environment variables from a .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
# Set the OpenAI API key
openai.api_key = openai_api_key

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

logger.info("inside main")

service_context = create_service_context()

directory_path = "./vector_store"
if not individual_query_engine_tools:
    for dir_name in os.listdir(directory_path):
        dir_path = os.path.join(directory_path, dir_name)
        if os.path.isdir(dir_path):
            storage_context = StorageContext.from_defaults(persist_dir=f"{dir_path}")
            index = load_index_from_storage(storage_context)

            # Assuming directory name has the same format as filename in your example
            parts = dir_name.split('_', 2)

            doc_type = parts[0]
            manufacturer = parts[1]
            doc_title = parts[2]

            this_query_engine_tool = QueryEngineTool(
                query_engine=index.as_query_engine(),
                metadata=ToolMetadata(
                    name=dir_name,
                    description=(f'Document type is {doc_type}. Manufacturer is {manufacturer}. '
                                 f'Document name is {doc_title}')
                )
            )

            individual_query_engine_tools.append(this_query_engine_tool)
# Add test endpoint for Redis
@app.get("/test-redis")
async def test_redis():
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    chat_store = RedisChatStore(redis_url=redis_url, ttl=300)
    try:
        chat_store.redis_client.set("test_key", "test_value")
        value = chat_store.redis_client.get("test_key")
        return {"test_key": value.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}

# Add test endpoint for OpenAI
@app.get("/test-openai")
async def test_openai():
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "This is a test."}
            ]
        )
        return {"response": response.choices[0].message['content']}
    except Exception as e:
        return {"error": str(e)}

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.info("Current individual_query_engine_tools in memory:")
    for tool in individual_query_engine_tools:
        logger.info(f"Tool name: {tool.metadata.name}, description: {tool.metadata.description}")

app.include_router(chat_router, prefix="/api/chat")
app.include_router(upload_router, prefix="/api/upload")
app.include_router(reset_router, prefix="/api/chat/reset")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
