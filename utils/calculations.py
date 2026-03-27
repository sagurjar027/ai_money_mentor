import math
from typing import Dict, List


def _clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, value))


def calculate_health_score(
    monthly_income: float,
    monthly_expenses: float,
    savings: float,
    debt: float,
    investments: float,
    insurance: float,
) -> Dict:
    if monthly_income <= 0:
        return {
            "score": 0,
            "category": "Poor",
            "insights": ["Income must be greater than zero to calculate score."],
            "recommendations": ["Start with stable income and strict budgeting."],
        }

    emergency_ratio = savings / (6 * monthly_expenses) if monthly_expenses > 0 else 1.0
    debt_ratio = debt / monthly_income
    investment_ratio = investments / monthly_income
    insurance_ok = insurance >= (monthly_income * 12 * 10)
    discipline_ratio = (monthly_income - monthly_expenses) / monthly_income

    emergency_score = _clamp(emergency_ratio) * 30
    debt_score = _clamp(1 - debt_ratio) * 20
    investment_score = _clamp(investment_ratio / 0.20) * 20
    insurance_score = 15 if insurance_ok else 5
    discipline_score = _clamp(discipline_ratio / 0.30) * 15

    total_score = round(emergency_score + debt_score + investment_score + insurance_score + discipline_score)
    category = "Poor" if total_score < 40 else "Average" if total_score < 70 else "Good"

    insights = [
        f"Emergency score is based on {emergency_ratio:.2f}x of the 6-month buffer target.",
        f"Debt-to-income ratio is {debt_ratio:.2%}; lower than 35% is healthier.",
        f"Investment ratio is {investment_ratio:.2%}; 20%+ of income is ideal for growth.",
        "Insurance appears adequate." if insurance_ok else "Insurance appears below 10x annual income benchmark.",
        f"Savings discipline is {discipline_ratio:.2%} of income after expenses.",
    ]

    recommendations: List[str] = []
    if emergency_ratio < 1:
        recommendations.append("Build emergency fund to 6 months of expenses via auto-transfer.")
    if debt_ratio > 0.35:
        recommendations.append("Reduce debt burden below 35% of income; pay high-interest loans first.")
    if investment_ratio < 0.20:
        recommendations.append("Increase SIP/investment amount toward 20% of monthly income.")
    if not insurance_ok:
        recommendations.append("Buy/upgrade term insurance to around 10x annual income.")
    if discipline_ratio < 0.20:
        recommendations.append("Improve savings discipline with a monthly budget and spending caps.")
    if not recommendations:
        recommendations.append("You are on track. Review and rebalance every quarter.")

    return {
        "score": total_score,
        "category": category,
        "insights": insights,
        "recommendations": recommendations,
        "breakdown": {
            "emergency_score": round(emergency_score, 2),
            "debt_score": round(debt_score, 2),
            "investment_score": round(investment_score, 2),
            "insurance_score": round(insurance_score, 2),
            "discipline_score": round(discipline_score, 2),
        },
    }


def calculate_fire_plan(age: int, income: float, expenses: float, savings: float, retirement_age: int) -> Dict:
    years_left = max(retirement_age - age, 0)
    annual_expenses = expenses * 12
    target_corpus = annual_expenses * 25

    if years_left == 0:
        monthly_sip = 0.0
    else:
        expected_return_annual = 0.10
        monthly_rate = expected_return_annual / 12
        months = years_left * 12
        future_value_current_savings = savings * ((1 + monthly_rate) ** months)
        needed_future_value = max(target_corpus - future_value_current_savings, 0)
        denominator = ((1 + monthly_rate) ** months - 1) / monthly_rate
        monthly_sip = needed_future_value / denominator if denominator > 0 else 0.0

    savings_rate = (income - expenses) / income if income > 0 else 0
    if savings_rate >= 0.4:
        strategy = "Aggressive: 70% equity index funds, 20% debt funds, 10% gold."
    elif savings_rate >= 0.2:
        strategy = "Balanced: 60% equity index funds, 30% debt funds, 10% gold."
    else:
        strategy = "Conservative start: build emergency fund first, then 50/40/10 allocation."

    return {
        "target_corpus": round(target_corpus, 2),
        "monthly_sip": round(max(monthly_sip, 0), 2),
        "years_left": years_left,
        "investment_strategy": strategy,
    }


def _slab_tax(income: float, slabs: List[tuple]) -> float:
    tax = 0.0
    previous_limit = 0.0
    for upper_limit, rate in slabs:
        if income > previous_limit:
            taxable_in_slab = min(income, upper_limit) - previous_limit
            tax += taxable_in_slab * rate
            previous_limit = upper_limit
    if income > previous_limit:
        tax += (income - previous_limit) * slabs[-1][1]
    return tax


def calculate_tax(salary: float, investments_80c: float, deductions: float) -> Dict:
    standard_deduction = 50000.0
    max_80c = min(investments_80c, 150000.0)
    other_deductions = max(deductions, 0.0)

    taxable_old = max(salary - standard_deduction - max_80c - other_deductions, 0)
    old_slabs = [
        (250000, 0.0),
        (500000, 0.05),
        (1000000, 0.20),
        (math.inf, 0.30),
    ]
    tax_old = _slab_tax(taxable_old, old_slabs)

    taxable_new = max(salary - standard_deduction, 0)
    new_slabs = [
        (400000, 0.0),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (math.inf, 0.30),
    ]
    tax_new = _slab_tax(taxable_new, new_slabs)

    cess_rate = 0.04
    tax_old_total = tax_old * (1 + cess_rate)
    tax_new_total = tax_new * (1 + cess_rate)

    best_regime = "Old Regime" if tax_old_total < tax_new_total else "New Regime"
    suggestions = [
        "ELSS: Equity-linked, 3-year lock-in, good for growth + 80C.",
        "PPF: 15-year lock-in, sovereign-backed, stable long-term savings.",
        "NPS: Extra tax benefit under 80CCD(1B) up to Rs 50,000.",
    ]
    if max_80c < 150000:
        suggestions.insert(0, f"You can still invest Rs {150000 - max_80c:.0f} more under 80C.")

    return {
        "tax_old": round(tax_old_total, 2),
        "tax_new": round(tax_new_total, 2),
        "best_regime": best_regime,
        "suggestions": suggestions,
        "taxable_income_old": round(taxable_old, 2),
        "taxable_income_new": round(taxable_new, 2),
    }


def calculate_sip_plan(
    monthly_investment: float,
    years: int,
    expected_annual_return: float,
    current_savings: float = 0.0,
) -> Dict:
    monthly_rate = expected_annual_return / 100 / 12
    months = years * 12
    invested_amount = monthly_investment * months

    if monthly_rate == 0:
        future_value_sip = monthly_investment * months
        future_value_lump_sum = current_savings
    else:
        future_value_sip = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        future_value_lump_sum = current_savings * ((1 + monthly_rate) ** months)

    estimated_value = future_value_sip + future_value_lump_sum
    total_invested = invested_amount + current_savings
    estimated_gains = estimated_value - total_invested

    if years >= 15 and expected_annual_return >= 12:
        outlook = "High-growth projection with equity-heavy assumptions. Review risk tolerance regularly."
    elif years >= 10:
        outlook = "Strong long-term compounding setup if you stay disciplined with monthly investing."
    elif years >= 5:
        outlook = "Balanced medium-term SIP plan with visible compounding benefits."
    else:
        outlook = "Shorter horizon plan. Returns can vary, so keep expectations realistic."

    return {
        "monthly_investment": round(monthly_investment, 2),
        "years": years,
        "expected_annual_return": round(expected_annual_return, 2),
        "current_savings": round(current_savings, 2),
        "invested_amount": round(invested_amount, 2),
        "total_invested": round(total_invested, 2),
        "estimated_value": round(estimated_value, 2),
        "estimated_gains": round(estimated_gains, 2),
        "wealth_multiplier": round(estimated_value / total_invested, 2) if total_invested > 0 else 0,
        "outlook": outlook,
    }
