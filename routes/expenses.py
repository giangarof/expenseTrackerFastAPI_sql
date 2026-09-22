from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from schema.models import Expenses, ExpenseRequest
from database.database import get_db, db_dependency

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


# Method: GET
# Route: api/expenses/
# Description: Retrieve all expenses
@router.get("/", status_code=status.HTTP_200_OK)
def getAllExpenses(db: db_dependency):
    data = db.query(Expenses).all()
    if not data:
        raise HTTPException(status_code=404, detail="nothing found")

    return {"message": "found", "data": data}


# Method: GET
# Route: api/expenses/{id}
# Description: Retrieve expenses by id
@router.get("/{id}", status_code=status.HTTP_200_OK)
def getById(db: db_dependency, id: int = Path(gt=0)):
    expense_id = Expenses.id == id
    data = db.query(Expenses).filter(expense_id).first()

    if not data:
        raise HTTPException(status_code=404, detail="nothing found")

    return {"message": "found", "data": data}


# Method: POST
# Route: api/expenses
# Description: Add a new expense
@router.post("/", status_code=status.HTTP_201_CREATED)
def addExpense(db: db_dependency, theExpense: ExpenseRequest):

    # gets the last element id plus 1 to generate the new expense id
    newId = db.query(Expenses).all()[-1].id + 1
    # data = Expenses(**theExpense.model_dump())

    data = Expenses(newId, theExpense.name, theExpense.ammount)
    # prints location in memory
    # print(data)

    # prints the actual data
    # print(theExpense)

    # Add to the db
    db.add(data)
    db.commit()
    return {"message": "added successfully", "data": theExpense}


# Method: PUT
# Route: api/expenses/update/{id}
# Description: Update expenses by id
@router.put("/{id}", status_code=status.HTTP_200_OK)
def updateById(db: db_dependency, theExpense: ExpenseRequest, id: int):

    # Fetch all expenses
    expenses = db.query(Expenses).all()

    # Loop over
    for x in expenses:
        # if there is a id match, replace the fields and commit changes
        if id == x.id:
            x.name = theExpense.name
            x.ammount = theExpense.ammount

            db.commit()
            return {"message": "Updated successfully", "data": theExpense}

    raise HTTPException(status_code=404, detail="No found")


# Method: DELETE
# Route: api/expenses/{id}
# Description: Delete expenses by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def deleteById(db: db_dependency, id: int):
    # Fetch all expenses
    expenses = db.query(Expenses).all()
    for x in expenses:
        if id == x.id:
            db.delete(x)
            db.commit()
            return {"message": "Deleted successfully"}

    raise HTTPException(status_code=404, detail="No found")
