import chromadb
from .schemas import Document

client = chromadb.PersistentClient()
collection = client.get_or_create_collection("my_collection")

def add_document(document:str, metadata: dict, id: str) -> bool:
    try:
        collection.add(documents=[document], metadatas=[metadata], ids=[id])
        return True
    except ValueError:
        return False

def get_all_documents() -> list[Document]:
    documents = collection.get()
    doc_list = list()
    for id,metadata in zip(documents['ids'],documents['metadatas']):
        document = Document(id=id,metadata=metadata)
        doc_list.append(document)
    return doc_list

def query_documents(query: str) -> Document|None:
    result = collection.query(
        query_texts=query,
        n_results=1
    )
    if result['ids'] != [[]]:
        return Document(id=result['ids'][0][0],metadata=result['metadatas'][0][0],content=result['documents'][0][0])
    else:
        return None

def remove_document(id: str):
    collection.delete(ids=[id])

def get_document_by_id(id:str):
    return collection.get(ids=[id])