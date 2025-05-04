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
- Docker Desktop (for container deployment)
- Microsoft Visual C++ 14.0 (for windows deployment, https://visualstudio.microsoft.com/de/visual-cpp-build-tools/)

## Installation 


### Steps (local deployment)

```bash
git clone https://github.com/Gusse-dev/API_VDB
python -m venv env
env/Scripts/activate
pip install -r ./requirements.txt 
# pip install -r ./requirements_windows.txt if running on windows
fastapi run app/main.py
```

### Steps (container deployment)

```bash
git clone https://github.com/Gusse-dev/API_VDB
docker build . -t api_vdb   
docker run -d --name api_vdb -p 8000:8000 api_vdb 
# docker start api_vdb
docker stop api_vdb
```

## Documentation

View the Swagger-Documentation by running the app and accessing http://127.0.0.1:8000/docs#