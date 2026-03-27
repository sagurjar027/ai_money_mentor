from fastapi import APIRouter, Depends

try:
    from backend.auth import get_current_user
    from backend.db import MongoService
    from backend.models import FirePlanRequest
except ModuleNotFoundError:
    from auth import get_current_user
    from db import MongoService
    from models import FirePlanRequest
from utils.ai_helper import generate_advice
from utils.calculations import calculate_fire_plan

router = APIRouter()
db = MongoService()


@router.post("/fire_plan")
def fire_plan(data: FirePlanRequest, current_user: dict = Depends(get_current_user)):
    payload = data.model_dump()
    result = calculate_fire_plan(
        age=data.age,
        income=data.income,
        expenses=data.expenses,
        savings=data.savings,
        retirement_age=data.retirement_age,
    )
    result["ai_advice"] = generate_advice("fire_plan", payload, result)
    db.save_record("fire_plan", payload, result, user_id=current_user["id"])
    return result
