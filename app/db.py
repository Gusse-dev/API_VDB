import chromadb
from chromadb.utils import embedding_functions
from .schemas import Document, User

EMBED_MODEL = "all-MiniLM-L6-v2"


client = chromadb.PersistentClient()
embedding_func = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection("my_collection", embedding_function=embedding_func, metadata={"hnsw:space": "cosine"})

def add_document(document:str, metadata: dict, id: str) -> bool:
    try:
        collection.add(documents=[document], metadatas=[metadata], ids=[id])
        return True
    except ValueError:
        return False

def get_all_documents(user:User) -> list[Document]:
    documents = collection.get(where={"document_owner": user.username})
    doc_list = list()
    for id,metadata in zip(documents['ids'],documents['metadatas']):
        document = Document(id=id,metadata=metadata)
        doc_list.append(document)
    return doc_list

def query_documents(query: str, user:User) -> Document|None:
    result = collection.query(
        query_texts=query,
        n_results=1,
        where={"document_owner": user.username}
    )
    if result['ids'] != [[]]:
        return Document(id=result['ids'][0][0],metadata=result['metadatas'][0][0],content=result['documents'][0][0])
    else:
        return None

def remove_document(id: str):
    collection.delete(ids=[id])

def get_document_by_id(id:str, user:User):
    return collection.get(ids=[id],  where={"document_owner": user.username})