from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from schema.models import Expenses, Income
from database.database import get_db, db_dependency

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


# Method: GET
# Route: api/analysis
# Description: Analyze expenses based on income
@router.get("/", status_code=status.HTTP_200_OK)
def analysis(db: db_dependency):
    # all expenses
    totalExpense = 0
    TotalIncome = 0

    dataIncome = db.query(Income).all()
    dataExpense = db.query(Expenses).all()

    for x in dataIncome:
        TotalIncome += x.ammount

    for x in dataExpense:
        totalExpense += x.ammount

    spending_percentage = (totalExpense / TotalIncome) * 100
    res = round(spending_percentage, 2)
    return {"message": f"You do spend {res}% of your income"}
