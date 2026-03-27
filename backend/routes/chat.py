from fastapi import APIRouter, Depends

try:
    from backend.auth import get_current_user
    from backend.db import MongoService
    from backend.models import ChatRequest
except ModuleNotFoundError:
    from auth import get_current_user
    from db import MongoService
    from models import ChatRequest
from utils.ai_helper import answer_general_question

router = APIRouter()
db = MongoService()


@router.post("/chat")
def chat(data: ChatRequest, current_user: dict = Depends(get_current_user)):
    payload = data.model_dump()
    result = {"answer": answer_general_question(data.question)}
    db.save_record("chat", payload, result, user_id=current_user["id"])
    return result
