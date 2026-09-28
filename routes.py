from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = ""
    dates: str = Field(..., min_length=2)

@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        document = generator.generate_document(
            request.document_type, request.parties, request.terms, request.dates
        )
        return {"document": document}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
