from fastapi import APIRouter, Depends

try:
    from backend.auth import get_current_user
    from backend.db import MongoService
    from backend.models import HealthScoreRequest
except ModuleNotFoundError:
    from auth import get_current_user
    from db import MongoService
    from models import HealthScoreRequest
from utils.ai_helper import generate_advice
from utils.calculations import calculate_health_score

router = APIRouter()
db = MongoService()


@router.post("/health_score")
def health_score(data: HealthScoreRequest, current_user: dict = Depends(get_current_user)):
    payload = data.model_dump()
    result = calculate_health_score(
        monthly_income=data.monthly_income,
        monthly_expenses=data.monthly_expenses,
        savings=data.savings,
        debt=data.debt,
        investments=data.investments,
        insurance=data.insurance,
    )
    result["ai_advice"] = generate_advice("health_score", payload, result)
    db.save_record("health_score", payload, result, user_id=current_user["id"])
    return result
