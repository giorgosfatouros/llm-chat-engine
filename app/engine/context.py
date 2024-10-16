from llama_index.core import ServiceContext

from app.context import create_base_context
from app.engine.constants import CHUNK_SIZE, CHUNK_OVERLAP, OPENAI_EMBED_MODEL, CONTEXT_WINDOW, OUTPUT_TOKENS


def create_service_context():
    base = create_base_context()
    return ServiceContext.from_defaults(
        llm=base.llm,
        embed_model=base.embed_model,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )


