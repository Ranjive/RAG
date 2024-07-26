# Document Processing and Text Embedding API

## Overview

This project is a comprehensive system for processing PDF documents, embedding text, and performing similarity searches. It involves several key steps: extracting text from PDF files, chunking the text, generating embeddings, storing them in a database, and providing an API for similarity searches. The frontend is built with Streamlit for an interactive user experience.

## Features

- **Text Extraction**: Utilizes PyPDF to extract text from PDF documents.
- **Text Chunking**: Splits extracted text into chunks of 500 tokens for efficient processing.
- **Text Embedding**: Uses Azure OpenAI's Ada model to generate embeddings for text chunks.
- **Embedding Storage**: Stores text embeddings in a Chroma database for efficient retrieval.
- **Similarity Search API**: A Flask API that takes user queries and returns the most similar text chunks.
- **Interactive Frontend**: A Streamlit application that provides an easy-to-use interface for querying the API.

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Ranjive/document-processing-embedding-api.git
    cd document-processing-embedding-api
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Step 1: Extract Text from PDF
Use the `pypdf` library to extract text from your PDF documents.

### Step 2: Chunk Text
Chunk the extracted text into 500-token chunks.

### Step 3: Embed Text
Use Azure OpenAI's Ada model to generate embeddings for the text chunks.

### Step 4: Store Embeddings
Store the generated embeddings in a Chroma database.

### Step 5: Run the API
Start the Flask API to handle similarity search queries.
```bash
python api.py
