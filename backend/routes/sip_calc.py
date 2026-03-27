from fastapi import APIRouter, Depends

try:
    from backend.auth import get_current_user
    from backend.db import MongoService
    from backend.models import SipCalcRequest
except ModuleNotFoundError:
    from auth import get_current_user
    from db import MongoService
    from models import SipCalcRequest
from utils.ai_helper import generate_advice
from utils.calculations import calculate_sip_plan

router = APIRouter()
db = MongoService()


@router.post("/sip_calc")
def sip_calc(data: SipCalcRequest, current_user: dict = Depends(get_current_user)):
    payload = data.model_dump()
    result = calculate_sip_plan(
        monthly_investment=data.monthly_investment,
        years=data.years,
        expected_annual_return=data.expected_annual_return,
        current_savings=data.current_savings,
    )
    result["ai_advice"] = generate_advice("sip_calc", payload, result)
    db.save_record("sip_calc", payload, result, user_id=current_user["id"])
    return result
