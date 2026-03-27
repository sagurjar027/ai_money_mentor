from pydantic import BaseModel, Field


class HealthScoreRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    monthly_income: float = Field(gt=0)
    monthly_expenses: float = Field(ge=0)
    savings: float = Field(ge=0)
    debt: float = Field(ge=0, description="Total monthly debt obligations")
    investments: float = Field(ge=0, description="Monthly investment amount")
    insurance: float = Field(ge=0, description="Total life insurance cover in INR")


class FirePlanRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    income: float = Field(gt=0)
    expenses: float = Field(ge=0)
    savings: float = Field(ge=0)
    retirement_age: int = Field(ge=30, le=100)


class TaxCalcRequest(BaseModel):
    salary: float = Field(ge=0)
    investments_80c: float = Field(ge=0)
    deductions: float = Field(ge=0, description="Other deductible amount")


class SipCalcRequest(BaseModel):
    monthly_investment: float = Field(gt=0, description="Monthly SIP amount in INR")
    years: int = Field(ge=1, le=50)
    expected_annual_return: float = Field(gt=0, le=30, description="Expected annual return in percent")
    current_savings: float = Field(ge=0, default=0, description="Current lump sum already invested in INR")


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(default="user")


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=6, max_length=128)


class ToggleUserStatusRequest(BaseModel):
    is_active: bool


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
