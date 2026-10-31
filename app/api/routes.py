from fastapi import APIRouter, HTTPException
from app.schemas.query import QuestionRequest, QuestionResponse
from app.services.business_query_service import BusinessQueryService

router = APIRouter(prefix="/api/v1", tags=["Business Intelligence"])

query_service = BusinessQueryService()


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        response = query_service.answer_question(request.question)
        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))