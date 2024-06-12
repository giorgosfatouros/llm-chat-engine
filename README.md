This is a [LlamaIndex](https://www.llamaindex.ai/) project using [FastAPI](https://fastapi.tiangolo.com/) bootstrapped with [`create-llama`](https://github.com/run-llama/LlamaIndexTS/tree/main/packages/create-llama).

## Getting Started

First, set up the environment:

```
poetry install
poetry shell
```

By default, we use the OpenAI LLM (though you can customize, see `app/context.py`). As a result you need to specify an `OPENAI_API_KEY` in an .env file in this directory.

Example `.env` file:

```
OPENAI_API_KEY=<openai_api_key>
```

Second, run the development server:

```
python main.py
```

Third, upload any PDF document/manual that you would like to test your chat with
making sure you provide the document type, document title, the document's author/ manual's manufacturer like so:

```
 curl -X 'POST'   'http://0.0.0.0:8000/api/upload/upload_document/' 
  -H 'accept: application/json'
  -H 'Content-Type: multipart/form-data'  
  -F 'doc_type = example_manual'  
  -F 'manufacturer = example_Cisco'  
  -F 'doc_title = example_Series'
  -F 'uploaded_file=@/home/user/Documents/example.pdf'

```

Then call the API endpoint `/api/chat` to chat:

```
curl --location 'localhost:8000/api/chat' \
--header 'Content-Type: application/json' \
--data '{ "messages": [{ "role": "user", "content": "Hello" }] }'
```

You can start editing the API by modifying `app/api/routers/chat.py`. The endpoint auto-updates as you save the file.

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the Swagger UI of the API.

The API allows CORS for all origins to simplify development. You can change this behavior by setting the `ENVIRONMENT` environment variable to `prod`:

```
ENVIRONMENT=prod uvicorn main:app
```

## Learn More

To learn more about LlamaIndex, take a look at the following resources:

- [LlamaIndex Documentation](https://docs.llamaindex.ai) - learn about LlamaIndex.

You can check out [the LlamaIndex GitHub repository](https://github.com/run-llama/llama_index) - your feedback and contributions are welcome!
