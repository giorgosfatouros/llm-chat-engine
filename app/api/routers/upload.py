from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter, Form
from fastapi.responses import JSONResponse
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.readers.smart_pdf_loader import SmartPDFLoader
import logging
import shutil
from app.engine.context import create_service_context

from app.__init__ import individual_query_engine_tools

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("The OpenAI API key must be set as an environment variable 'OPENAI_API_KEY'")

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/upload_document/")
async def upload_document(
        doc_type: str = Form(...),
        manufacturer: str = Form(...),
        doc_title: str = Form(...),
        uploaded_file: UploadFile = File(...)
):
    collection_name = f"{doc_type}_{manufacturer}_{doc_title}"
    collection_name = collection_name[:63]
    collection_metadata = {'doc_type': doc_type, 'manufacturer': manufacturer, 'collection_name': collection_name}

    # Define the target directory and ensure it exists
    target_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../data')
    os.makedirs(target_dir, exist_ok=True)

    # Define the full file path
    file_path = os.path.join(target_dir, uploaded_file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(uploaded_file.file, f)

    embed_model = OpenAIEmbedding()
    storage_context = StorageContext.from_defaults(index_store=SimpleIndexStore())

    llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
    pdf_loader = SmartPDFLoader(llmsherpa_api_url=llmsherpa_api_url)

    service_context = create_service_context()

    docs = pdf_loader.load_data(file_path)
    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context, embed_model=embed_model, service_context=service_context)
    index.storage_context.persist(persist_dir=f"./vector_store/{collection_name}")

    for query_engine_tool in individual_query_engine_tools:
        if query_engine_tool.metadata.name == collection_name:
            # this_query_engine_tool = query_engine_tool
            break
    else:
        this_query_engine_tool = QueryEngineTool(
            query_engine=index.as_query_engine(),
            metadata=ToolMetadata(
                name=collection_name,
                description=(f'Document type is {doc_type}. Manufacturer is {manufacturer}. '
                             f'Document name is {doc_title}')
            )
        )
        individual_query_engine_tools.append(this_query_engine_tool)

    logger.info("Current individual_query_engine_tools after update:")
    for tool in individual_query_engine_tools:
        logger.info(f"Tool name: {tool.metadata.name}, description: {tool.metadata.description}")

    # query_engine = index.as_query_engine()
    # response = query_engine.query(f"What is {collection_name} document about ?")

# Ensure to include this router in your main app
# In your main.py, you would add the following line
# app.include_router(upload_router, prefix="/api/upload")
