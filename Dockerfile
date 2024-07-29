FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install Poetry
RUN pip install poetry

# Configure Poetry:
# - Do not create a virtual environment inside the container
# - Install only package dependencies (skip dev-dependencies)
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev -vvv
RUN pip install llama_index


# Set environment variables
ENV OPENAI_API_KEY="sk-proj-JZm15xUo65pLTIFrX0lOT3BlbkFJ5AaO3MI3OF3c1C6sdJtM"

EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
