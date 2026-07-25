# Egyptian & Greek Mythology RAG System

An AI-powered Retrieval-Augmented Generation (RAG) system that answers questions about ancient Egyptian and Greek mythology using a knowledge base of historical and mythological texts.

## Project Overview

This project uses RAG architecture to retrieve relevant information from mythology documents and generate accurate answers using an AI language model.

The system covers:
- Ancient Egyptian mythology
- Ancient Greek mythology
- Gods, heroes, myths, stories, and historical references

## RAG Pipeline

Documents  
⬇️  
Text Preprocessing  
⬇️  
Chunking  
⬇️  
Text Embedding  
⬇️  
Vector Database (ChromaDB)  
⬇️  
Similarity Retrieval  
⬇️  
Prompt Engineering  
⬇️  
LLM Response Generation


## Project Files

- `preprocessing.py`
  - Cleans and prepares mythology documents.

- `chunking.py`
  - Splits documents into smaller text chunks.

- `embedding.py`
  - Generates embeddings for text chunks.

- `chroma_store.py`
  - Stores embeddings in ChromaDB vector database.

- `retrieve.py`
  - Retrieves the most relevant mythology information.

- `prompting.py`
  - Creates prompts using retrieved context.

- `model.py`
  - Handles the language model response generation.

- `test.py`
  - Tests the complete RAG pipeline.


## Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- LangChain
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)


## Example Questions

- Who is Osiris in Egyptian mythology?
- What is the story of Zeus and the Titans?
- Compare Ra and Apollo.
- Who are the main gods in Egyptian mythology?


## Future Improvements

- Add more mythology sources.
- Support multilingual questions.
- Add a web interface for interaction.
