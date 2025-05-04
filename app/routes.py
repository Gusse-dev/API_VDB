from fastapi import APIRouter, UploadFile, status, HTTPException, Response
from pypdf import PdfReader
import uuid
import io
from .schemas import Document, Documents, Message
from .db import add_document, get_all_documents, query_documents, remove_document, get_document_by_id
from .helper import extract_metadata

router = APIRouter()


@router.get("/api/documents/",
            summary="List all documents",
            description="Fetches all available documents. This endpoint returns a complete list of document records of the vector database.",
            response_description="Success - Returns a list of documents. Each document contains the document id and document metadata.",
            status_code=status.HTTP_200_OK, 
            response_model=Documents)
def list_documents(): 
    documents: list[Document] = get_all_documents()
    return {'documents': documents}

@router.put("/api/documents/",
            summary="Upload a document",
            description="Uploads a document into the vector database. Document is tagged with a unique id.",
            response_description="Created - Returns a success message and the assigned doucment id",
            responses={
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Unsupported Media Type - Given filetype is not supported","content": {"application/json": {"example": {"detail": "Filetype {file_extension} unsupported"}}}},
            status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Unprocessable Entity - File cant be processed to be added to the vector database","content": {"application/json": {"example": {"detail": "{filename} is not processable"}}}},
            },
            status_code=status.HTTP_201_CREATED,
            response_model=Message)
def upload_document(file: UploadFile):
    file_extension = file.filename.split('.')[-1].lower()
    id = str(uuid.uuid4())

    if file_extension == 'txt' or file_extension =='md':
        content = file.file.read().decode("utf-8")
        metadata = extract_metadata(file)
        success = add_document(content,metadata,id)
    elif file_extension == 'pdf':
        reader = PdfReader(io.BytesIO(file.file.read()))
        metadata = reader.metadata
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        success = add_document(content,metadata,id)
    else:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Filetype {file_extension} unsupported")
    if success:
        return Message(message= f"Document {file.filename} was added successfully", id=id)
    else: 
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{file.filename} is not processable")



@router.delete("/api/documents/{id}",
               summary="Delete a document",
               description="Deletes a document from the vector by given id.",
               response_description="Success - Document was succesfully deleted",
               responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found - No document for given id","content": {"application/json": {"example": {"detail": "Document with ID: {id} not found"}}}}},
               status_code=status.HTTP_200_OK,
               response_model=Message)
def delete_document(id: str):
    document = get_document_by_id(id=id)
    if len(document['ids']) > 0:
        remove_document(id)
        return Message(message="Document was successfully deleted")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document with ID: {id} not found")


@router.get("/api/documents/query",
            summary="Search for a document",
            description="Seraches for a document within the vector database based on a query. Returns the document with the highest similarity.",
            response_description="Success - Returns a document. Contains the id, document metadata and the document content.",
            status_code=status.HTTP_200_OK, 
            responses={status.HTTP_204_NO_CONTENT: {"description": "No Content - No content in the database to compare against","content": {"application/json": { "example": {"detail": "No documents in the database"}}}}},
            response_model=Document)
def search_documents(text: str):
    document: Document = query_documents(text)
    if document != None:
        return document
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)