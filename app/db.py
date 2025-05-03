import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient()
collection = client.get_or_create_collection("my_collection")

def add_document(document:str, metadata: dict, id: str):
    collection.add(documents=[document], metadatas=[metadata], ids=[id])

def get_all_documents() -> list:
    documents = collection.get()
    doc_list = list()
    for id,metadata in zip(documents['ids'],documents['metadatas']):
        document = dict()
        document['id'] = id
        document['metadata'] = metadata
        doc_list.append(document)
    return doc_list

def query_documents(query: str) -> dict|None:
    result = collection.query(
        query_texts=query,
        n_results=1
    )
    if result['ids'] != [[]]:
        return {'ID': result['ids'][0][0], 'Metadata': result['metadatas'][0][0], 'Content': result['documents'][0][0]}
    else:
        return None

def remove_document(id: str):
    collection.delete(ids=[id])

def get_document_by_id(id:str):
    return collection.get(ids=[id])