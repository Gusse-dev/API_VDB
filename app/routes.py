from fastapi import APIRouter, UploadFile, status, HTTPException, Response
from pypdf import PdfReader
import uuid
import io
from .schemas import EmbeddingInput, QueryInput
# TODO: Pydatic Objects hinzufügen
from .db import add_document, get_all_documents, query_documents, remove_document, get_document_by_id
from .helper import extract_metadata

router = APIRouter()

@router.put("/api/documents/",status_code=status.HTTP_201_CREATED)
def upload_document(file: UploadFile):
    file_extension = file.filename.split('.')[-1].lower()
    id = str(uuid.uuid4())

    if file_extension == 'txt' or file_extension =='md':
        content = file.file.read().decode("utf-8")
        metadata = extract_metadata(file)
        add_document(content,metadata,id)
    elif file_extension == 'pdf':
        reader = PdfReader(io.BytesIO(file.file.read()))
        metadata = reader.metadata
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        add_document(content,metadata,id)
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Filetype {file_extension} unsupported")
    return {'Message' : f"Document '{file.filename}' was added successfully",
             'ID': f"{id}"
            }

@router.delete("/api/documents/{id}",status_code=status.HTTP_200_OK)
def delete_document(id: str):
    document = get_document_by_id(id=id)
    if len(document['ids']) > 0:
        remove_document(id)
        return {'Message' : f"Document '{id}' was added successfully deleted'"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document with ID: {id} not found")

@router.get("/api/documents/",status_code=status.HTTP_200_OK)
def list_documents():
    documents = get_all_documents()
    return {'documents': documents}

@router.get("/api/documents/query",status_code=status.HTTP_200_OK)
def search_documents(text: str):
    document = query_documents(text)
    if document != None:
        return document
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)