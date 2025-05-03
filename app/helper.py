from fastapi import UploadFile

def extract_metadata(file: UploadFile) -> dict:
    return {
        "filename": file.filename,
        "content_type": file.content_type,
    }
