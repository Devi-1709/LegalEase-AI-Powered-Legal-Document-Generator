from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

try:
    gemini_generator = GeminiDocumentGenerator()
except Exception:
    gemini_generator = None

class DocumentRequest(BaseModel):
    document_type: str = Field(..., description="Type of document, e.g., Freelance Work Contract")
    parties: str = Field(..., description="Parties involved in the agreement")
    terms: str = Field(..., description="Terms and conditions separated by semicolons")
    dates: str = Field(..., description="Effective date of the agreement")

@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    if not request.document_type.strip():
        raise HTTPException(status_code=400, detail="document_type cannot be empty.")
    if not request.parties.strip():
        raise HTTPException(status_code=400, detail="parties cannot be empty.")

    global gemini_generator
    if gemini_generator is None:
        try:
            gemini_generator = GeminiDocumentGenerator()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI Core Initialization Failed: {str(e)}")

    try:
        doc = gemini_generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )
        return {"document": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document generation failed: {str(e)}")