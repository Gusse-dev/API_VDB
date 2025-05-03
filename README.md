# Sample Excercise - Vectordatabase WebAPI

This projects implements a REST-API that interacts with a vector database. 


## About

**API_VDB** is a python-based project built with FastAPI and ChromaDB. It enables the user to upload text documents into a vector database and search for the most similar documents.

---

## API-Features

- Upload documents [txt, md, pdf]
- Delete Documents
- List all uploaded documents
- Text search that returns the most relevant document

---

## Prerequisites
- Python 3.12
- Docker Desktop(for container deployment)

## Installation 


### Steps (local deployment)

```bash
git clone Link
pip install -r ./requirements.txt 
# pip install -r ./requirements_windows.txt if running on windows
fastapi run app/main.py
```

### Steps (container deployment)

```bash
git clone link
docker build . -t api_vdb   
docker run -d --name api_vdb -p 8000:8000 api_vdb
docker stop api_vdb
```