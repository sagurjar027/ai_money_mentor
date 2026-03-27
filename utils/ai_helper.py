import os
from functools import lru_cache
from typing import Any, Dict

try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False


# ==============================
# 🧠 SYSTEM PROMPT
# ==============================
SYSTEM_PROMPT = (
    "You are a financial advisor for Indian users. "
    "Give practical, personalized, and beginner-friendly advice. "
    "Do NOT calculate numbers. Use only provided data. "
    "Treat all monetary values as Indian Rupees unless explicitly stated otherwise. "
    "Never convert values into USD or dollars. "
    "Use INR, rupees, lakh, and crore formatting where helpful. "
    "Never contradict the provided calculated output. "
    "If a score, category, tax, SIP, or corpus is provided, use that exact value as truth."
)

GENERAL_CHAT_SYSTEM_PROMPT = (
    "You are AI Money Mentor, a helpful assistant for Indian users. "
    "Answer general user questions in a clear, friendly, and practical way. "
    "If the question is about money, personal finance, tax, saving, debt, or investing, "
    "keep the answer educational and beginner-friendly. "
    "Treat money amounts as Indian Rupees by default. "
    "Never answer in USD or dollars unless the user explicitly asks for that currency. "
    "Prefer INR or rupees, and use lakh or crore wording where useful. "
    "Do not pretend to know personal account data you were not given. "
    "If the user asks for regulated financial, legal, or medical decisions, "
    "suggest consulting a qualified professional."
)


# ==============================
# 🔧 TOOL 1: HEALTH SCORE
# ==============================
def health_score_tool(user_payload: Dict[str, Any]) -> Dict[str, Any]:
    income = user_payload.get("income", 0)
    expenses = user_payload.get("expenses", 0)

    savings = income - expenses

    if income == 0:
        score = 0
    else:
        ratio = savings / income

        if ratio >= 0.4:
            score = 85
        elif ratio >= 0.2:
            score = 70
        else:
            score = 50

    return {
        "score": score,
        "monthly_savings": savings
    }


# ==============================
# 🔧 TOOL 2: FIRE PLANNER
# ==============================
def calculate_fire_corpus(monthly_expense: float) -> float:
    return monthly_expense * 12 * 25  # 25x rule


def calculate_sip(target: float, current_savings: float, years: int, rate: float = 0.10) -> float:
    r = rate / 12
    n = years * 12

    future_savings = current_savings * (1 + rate) ** years
    remaining = max(target - future_savings, 0)

    if remaining == 0:
        return 0

    sip = remaining * r / ((1 + r) ** n - 1)
    return round(sip, 2)


def fire_planner_tool(user_payload: Dict[str, Any]) -> Dict[str, Any]:
    expense = user_payload.get("expenses", 0)
    savings = user_payload.get("savings", 0)
    age = user_payload.get("age", 25)
    target_age = user_payload.get("target_age", 50)

    years = max(target_age - age, 1)

    corpus = calculate_fire_corpus(expense)
    sip = calculate_sip(corpus, savings, years)

    return {
        "target_corpus": round(corpus),
        "monthly_sip": sip,
        "years": years
    }


# ==============================
# 🔧 TOOL 3: TAX CALCULATOR
# ==============================
def tax_calculator_tool(user_payload: Dict[str, Any]) -> Dict[str, Any]:
    income = user_payload.get("income", 0)

    if income <= 250000:
        tax = 0
    elif income <= 500000:
        tax = income * 0.05
    elif income <= 1000000:
        tax = income * 0.2
    else:
        tax = income * 0.3

    return {
        "estimated_tax": round(tax),
        "regime": "basic_estimation"
    }


def sip_calculator_tool(user_payload: Dict[str, Any]) -> Dict[str, Any]:
    monthly_investment = float(user_payload.get("monthly_investment", 0) or 0)
    years = int(user_payload.get("years", 0) or 0)
    expected_annual_return = float(user_payload.get("expected_annual_return", 0) or 0)
    current_savings = float(user_payload.get("current_savings", 0) or 0)

    months = years * 12
    monthly_rate = expected_annual_return / 100 / 12 if expected_annual_return > 0 else 0
    invested_amount = monthly_investment * months

    if monthly_rate == 0:
        estimated_value = invested_amount + current_savings
    else:
        estimated_value = (
            monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        ) + (current_savings * ((1 + monthly_rate) ** months))

    return {
        "invested_amount": round(invested_amount, 2),
        "estimated_value": round(estimated_value, 2),
    }


# ==============================
# 🧠 TOOL ROUTER
# ==============================
def get_tool_result(feature: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
    if feature == "health_score":
        return health_score_tool(user_payload)

    elif feature == "fire_plan":
        return fire_planner_tool(user_payload)

    elif feature == "tax_calculator":
        return tax_calculator_tool(user_payload)

    elif feature == "sip_calc":
        return sip_calculator_tool(user_payload)

    return {}


# ==============================
# 🔁 FALLBACK
# ==============================
def _fallback():
    return "AI service temporarily unavailable. Please try again."


def _format_currency(amount: float) -> str:
    return f"Rs {amount:,.0f}"


def _build_health_score_advice(user_payload: Dict[str, Any], result: Dict[str, Any]) -> str:
    score = result.get("score", 0)
    category = result.get("category", "Unknown")
    monthly_income = float(user_payload.get("monthly_income", 0) or 0)
    monthly_expenses = float(user_payload.get("monthly_expenses", 0) or 0)
    savings = float(user_payload.get("savings", 0) or 0)
    debt = float(user_payload.get("debt", 0) or 0)
    investments = float(user_payload.get("investments", 0) or 0)
    insurance = float(user_payload.get("insurance", 0) or 0)

    emergency_target = monthly_expenses * 6
    emergency_gap = max(emergency_target - savings, 0)
    recommended_investment = monthly_income * 0.20
    investment_gap = max(recommended_investment - investments, 0)
    recommended_insurance = monthly_income * 12 * 10
    insurance_gap = max(recommended_insurance - insurance, 0)

    explanation = (
        f"Your health score is {score}/100, which puts you in the {category} category. "
        f"This result is based on your current savings, debt, monthly investing, insurance cover, "
        f"and how much of your income remains after expenses."
    )


def _build_sip_advice(user_payload: Dict[str, Any], result: Dict[str, Any]) -> str:
    monthly_investment = float(user_payload.get("monthly_investment", 0) or 0)
    years = int(user_payload.get("years", 0) or 0)
    expected_annual_return = float(user_payload.get("expected_annual_return", 0) or 0)
    current_savings = float(user_payload.get("current_savings", 0) or 0)

    estimated_value = float(result.get("estimated_value", 0) or 0)
    invested_amount = float(result.get("invested_amount", 0) or 0)
    estimated_gains = float(result.get("estimated_gains", 0) or 0)
    wealth_multiplier = float(result.get("wealth_multiplier", 0) or 0)
    outlook = result.get("outlook", "")

    explanation = (
        f"If you invest {_format_currency(monthly_investment)} every month for {years} years "
        f"at an assumed {expected_annual_return:.2f}% annual return, your projected value is "
        f"{_format_currency(estimated_value)}. "
        f"That includes about {_format_currency(invested_amount + current_savings)} contributed capital "
        f"and projected gains of {_format_currency(estimated_gains)}."
    )

    actions = [
        f"Automate your monthly SIP of {_format_currency(monthly_investment)} so compounding stays consistent.",
        f"Review the return assumption of {expected_annual_return:.2f}% once or twice a year and align it with your actual asset mix.",
        f"Track progress toward roughly {wealth_multiplier:.2f}x of invested capital over the plan horizon and increase SIP when income rises.",
    ]

    if current_savings > 0:
        actions[2] = (
            f"Keep your current invested base of {_format_currency(current_savings)} working, and step up the SIP whenever your income increases."
        )

    risk = (
        "This is a projection, not a guarantee. Real market returns can be lower or uneven, "
        "especially over shorter periods, so avoid committing to a plan that only works under perfect returns."
    )

    return "\n".join(
        [
            f"Explanation: {explanation}",
            "",
            "3 Actions:",
            *[f"{index}. {action}" for index, action in enumerate(actions, start=1)],
            "",
            f"Risk: {risk}",
            f"Plan Note: {outlook}" if outlook else "",
        ]
    ).strip()

    actions = []
    if emergency_gap > 0:
        actions.append(
            f"Build your emergency fund toward {_format_currency(emergency_target)}. "
            f"You are currently short by about {_format_currency(emergency_gap)}."
        )
    if debt > monthly_income * 0.35:
        actions.append("Reduce high-interest debt first so your debt burden moves below 35% of monthly income.")
    if investment_gap > 0:
        actions.append(
            f"Increase monthly investing toward {_format_currency(recommended_investment)}. "
            f"That is about {_format_currency(investment_gap)} more than your current level."
        )
    if insurance_gap > 0:
        actions.append(
            f"Review term insurance cover and work toward about {_format_currency(recommended_insurance)}."
        )
    if (monthly_income - monthly_expenses) / monthly_income < 0.20 if monthly_income > 0 else False:
        actions.append("Tighten your monthly budget so at least 20% of income is available for savings and investing.")

    if not actions:
        actions.append("Keep your current system running and review your budget, investments, and cover every quarter.")

    actions = actions[:3]

    risk = (
        "The main risk is that one weak area can pull down long-term stability even if the overall score is good. "
        "Focus first on the lowest scoring area from the breakdown."
    )

    return "\n".join(
        [
            f"Explanation: {explanation}",
            "",
            "3 Actions:",
            *[f"{index}. {action}" for index, action in enumerate(actions, start=1)],
            "",
            f"Risk: {risk}",
        ]
    )


# ==============================
# ⚙️ CLIENT
# ==============================
@lru_cache(maxsize=1)
def _get_client():
    if not HF_AVAILABLE:
        return None

    api_key = os.getenv("HUGGINGFACE_API_KEY", "")
    if not api_key:
        return None

    return InferenceClient(token=api_key)


def _run_chat_completion(system_prompt: str, user_prompt: str, max_tokens: int = 300) -> str:
    client = _get_client()

    if client is None:
        return _fallback()

    try:
        response = client.chat_completion(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print("HF ERROR:", str(e))
        return _fallback()


# ==============================
# 🚀 MAIN FUNCTION
# ==============================
def generate_advice(feature: str, user_payload: Dict[str, Any], result: Dict[str, Any] = None) -> str:
    tool_result = result if result is not None else get_tool_result(feature, user_payload)

    if feature == "health_score" and tool_result:
        return _build_health_score_advice(user_payload, tool_result)
    if feature == "sip_calc" and tool_result:
        return _build_sip_advice(user_payload, tool_result)

    return _run_chat_completion(
        SYSTEM_PROMPT,
        f"""
Feature: {feature}

User Input:
{user_payload}

Calculated Output:
{tool_result}

IMPORTANT:
- Do NOT calculate anything
- Use only given numbers
- Treat all money values as INR / Indian Rupees
- Do NOT convert or restate amounts in USD or dollars
- Treat the Calculated Output as the source of truth
- If Calculated Output includes a score, mention that exact score and do not replace it
- Do NOT invent a different score, ratio, or benchmark
- Do NOT say the score is 0 unless Calculated Output explicitly says score is 0

Provide:
1) Explanation
2) 3 actions
3) 1 risk
""",
    )


def answer_general_question(question: str) -> str:
    return _run_chat_completion(
        GENERAL_CHAT_SYSTEM_PROMPT,
        f"""
User question:
{question}

Respond with:
1) A direct answer
2) Short practical guidance when useful
3) A brief note if the user should verify with a professional
4) If mentioning money, use INR / rupees by default, not USD
""",
        max_tokens=400,
    )


# ==============================
# 🧪 TEST
# ==============================
if __name__ == "__main__":
    os.environ["HUGGINGFACE_API_KEY"] = "hf_your_key_here"

    user = {
        "income": 100000,
        "expenses": 50000,
        "age": 28,
        "target_age": 50,
        "savings": 400000
    }

    print("\n--- FIRE PLAN ---")
    print(generate_advice("fire_plan", user))

    print("\n--- HEALTH SCORE ---")
    print(generate_advice("health_score", user))

    print("\n--- TAX ---")
    print(generate_advice("tax_calculator", user))
