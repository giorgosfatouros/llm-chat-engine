from app.engine.constants import CHUNK_SIZE, CHUNK_OVERLAP, OPENAI_EMBED_MODEL, CONTEXT_WINDOW, OUTPUT_TOKENS, MODEL
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


def create_base_context():
    Settings.llm = OpenAI(model=MODEL)
    Settings.embed_model = OpenAIEmbedding(model=OPENAI_EMBED_MODEL)
    Settings.node_parser = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    Settings.num_output = OUTPUT_TOKENS
    Settings.context_window = CONTEXT_WINDOW
    return Settings
