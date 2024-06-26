# LLM-Driven Industrial Maintenance Chatbot Assistant 
## Project Description
This project is designed to develop an AI-driven chatbot specialized in Industrial 5.0 maintenance practices, including
machinery optimization and process efficiency. The chatbot leverages OpenAI's GPT model for natural 
language understanding and responses, along with specialized tools for querying maintenance manuals and 
documents.

## Key Features
 - **Industrial Maintenance Expertise:** The chatbot is tailored to provide precise and accurate responses related to industrial machinery maintenance and process efficiency.
 - **Document Upload and Indexing:** Users can upload maintenance manuals and documents, which are then processed and indexed for querying.
 - **Contextual Conversation:** Maintains context from previous interactions to ensure coherent and relevant responses.
 - **Real-time Streaming Responses:** Provides real-time streaming of responses for a seamless user experience.

## Files and Directories
 - main.py: Entry point for the application.
 - Dockerfile: Docker configuration for containerizing the application.
 - pyproject.toml: Configuration file for managing project dependencies and metadata.
 - app/
   - api/
     - routers/
       - chat.py: Defines the API routes for interacting with the chat engine.
       - upload.py: API routes for uploading and processing documents.
   - engine/
     - context.py: Contains functions for setting up the service context, including language models and embedding models.
     - constants.py: Defines constants used throughout the application.
     - index.py: Handles the creation and management of the OpenAIAgent and its tools, including the chat engine.

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/giorgosfatouros/llm-chat-engine.git
cd llm-chat-engine.
```

2. Put your OpenAI API key in the Dockerfile and docker-compose.yml

3. Build the Docker image:
```bash
docker build -t llm-chat-engine .
```

4. Delete the .gitkeep files in ./data and ./vector-store directories

5. Run the Docker container:

```bash
docker run -p 8000:8000 llm-chat-engine
```


## Usage

Upload any PDF document/manual that you would like to test your chat with.
Make sure you provide the document type (One word without underscore), the document's author/ manual's manufacturer (One word without underscore) and the document's title (As many words as you like seperated by underscores) like so:

```bash
 curl -X 'POST' 'http://0.0.0.0:8000/api/upload/upload_document/' 
  -H 'accept: application/json'
  -H 'Content-Type: multipart/form-data'  
  -F 'doc_type = expl(Manual)'  
  -F 'manufacturer = exmpl(Cisco)'  
  -F 'doc_title = example_Series'
  -F 'uploaded_file=@/home/user/Documents/example.pdf'

```

Then call the API endpoint `/api/chat` to chat:

```bash
curl --location 'localhost:8000/api/chat' \
--header 'Content-Type: application/json' \
--data '{ "messages": [{ "role": "user", "content": "Hello" }] }'
```



You can start editing the API by modifying `app/api/routers/chat.py`. The endpoint auto-updates as you save the file.

Open [http://localhost:8000/api/docs](http://localhost:8000/docs) with your browser to see the Swagger UI of the API.

The API allows CORS for all origins to simplify development. You can change this behavior by setting the `ENVIRONMENT` environment variable to `prod`:

```
ENVIRONMENT=prod uvicorn main:app
```

## Learn More

To learn more about LlamaIndex, take a look at the following resources:

- [LlamaIndex Documentation](https://docs.llamaindex.ai) - learn about LlamaIndex.

You can check out [the LlamaIndex GitHub repository](https://github.com/run-llama/llama_index) - your feedback and contributions are welcome!


 curl -X 'POST'   'http://0.0.0.0:8000/api/upload/upload_document/' 
  -H 'accept: application/json'
  -H 'Content-Type: multipart/form-data'  
  -F 'doc_type = example_manual'  
  -F 'manufacturer = example_Cisco'  
  -F 'doc_title = example_Series'
  -F 'uploaded_file=@/home/user/Documents/example.pdf'
