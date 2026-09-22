from fastapi import FastAPI, APIRouter, Path, status, HTTPException
from database.database import db_dependency
from schema.models import Income, IncomeRequest

router = APIRouter(prefix="/api/income", tags=["Income"])


# Method: GET
# Route: api/income/
# Description: Retrieve all incomes
@router.get("/", status_code=status.HTTP_200_OK)
def getAll(db: db_dependency):
    data = db.query(Income).all()

    if not data:
        raise HTTPException(status_code=200, detail="Nothing found")

    return {"message": "Your income list", "data": data}


# Method: GET
# Route: api/income/{id}
# Description: Retrieve the first income by id
@router.get("/{id}", status_code=status.HTTP_200_OK)
def getOneById(db: db_dependency, id: int = Path(gt=0)):
    income_id = Income.id == id
    data = db.query(Income).filter(income_id).first()

    if not data:
        raise HTTPException(status_code=404, detail="Nothing found")

    return {"message": "Your income list", "data": data}


# Method: POST
# Route: api/income/
# Description: Add new income
@router.post("/", status_code=status.HTTP_201_CREATED)
def addNewIncome(db: db_dependency, theIncome: IncomeRequest):

    data = db.query(Income).all()

    newId = 1 if len(data) == 0 else data[-1].id + 1

    newIncome = Income(newId, theIncome.name, theIncome.ammount)
    db.add(newIncome)
    db.commit()

    return {"message": "Income added successfully", "data": theIncome}


# Method: PUT
# Route: api/income/update/{id}
# Description: Update income by id
@router.put("/{id}", status_code=status.HTTP_200_OK)
def updateIncome(db: db_dependency, theIncome: IncomeRequest, id: int = Path(gt=0)):
    # Find income
    income_id = Income.id == id
    data = db.query(Income).filter(income_id).first()

    # If income doesnt exist
    if not data:
        raise HTTPException(status_code=404, detail="Id doesnt exist")

    # Update fields
    data.name = theIncome.name
    data.ammount = theIncome.ammount
    db.commit()

    return {"message": "Updated successfully", "data": theIncome}


# Method: DELETE
# Route: api/income/{id}
# Description: Delete income by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def updateIncome(db: db_dependency, id: int = Path(gt=0)):
    # Find income
    income_id = Income.id == id
    data = db.query(Income).filter(income_id).first()

    # If income doesnt exist
    if not data:
        raise HTTPException(status_code=404, detail="Id doesnt exist")

    # If income existe, proceed to delete
    db.delete(data)
    db.commit()

    return {"message": "Deleted successfully"}
