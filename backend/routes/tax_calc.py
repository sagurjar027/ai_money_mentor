from fastapi import APIRouter, Depends

try:
    from backend.auth import get_current_user
    from backend.db import MongoService
    from backend.models import TaxCalcRequest
except ModuleNotFoundError:
    from auth import get_current_user
    from db import MongoService
    from models import TaxCalcRequest
from utils.ai_helper import generate_advice
from utils.calculations import calculate_tax

router = APIRouter()
db = MongoService()


@router.post("/tax_calc")
def tax_calc(data: TaxCalcRequest, current_user: dict = Depends(get_current_user)):
    payload = data.model_dump()
    result = calculate_tax(
        salary=data.salary,
        investments_80c=data.investments_80c,
        deductions=data.deductions,
    )
    result["ai_advice"] = generate_advice("tax_calc", payload, result)
    db.save_record("tax_calc", payload, result, user_id=current_user["id"])
    return result
