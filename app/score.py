"""Scores a personal-loan application. Below the cut-off the application is declined automatically, with reason
codes; above it, it goes to an underwriter."""
from dataclasses import dataclass
from datetime import date

import mlflow.xgboost
import pandas as pd

CUT_OFF = 0.62
model = mlflow.xgboost.load_model("models:/loan-decisions/Production")


@dataclass
class Application:
    applicant_id: str
    date_of_birth: date
    monthly_income: float
    monthly_debt: float
    amount: float
    term_months: int
    missed_payments_12m: int
    credit_history_months: int


def features(a: Application) -> pd.DataFrame:
    age = (date.today() - a.date_of_birth).days // 365
    return pd.DataFrame([{
        "age": age,
        "debt_to_income": a.monthly_debt / max(a.monthly_income, 1),
        "repayment_to_income": (a.amount / a.term_months) / max(a.monthly_income, 1),
        "missed_payments_12m": a.missed_payments_12m,
        "credit_history_months": a.credit_history_months,
    }])


def reason_codes(row: pd.Series) -> list[str]:
    codes = []
    if row.repayment_to_income > 0.35:
        codes.append("R01")
    if row.missed_payments_12m > 0:
        codes.append("R02")
    if row.credit_history_months < 12:
        codes.append("R03")
    if row.debt_to_income > 0.45:
        codes.append("R04")
    return codes or ["R01"]


def decide(a: Application) -> dict:
    x = features(a)
    score = float(model.predict_proba(x)[0][1])
    if score < CUT_OFF:
        return {"decision": "declined", "score": score, "reasons": reason_codes(x.iloc[0])}
    return {"decision": "to_underwriter", "score": score}
