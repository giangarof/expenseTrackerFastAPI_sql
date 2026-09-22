from pydantic import BaseModel, Field

from database.database import Base
from sqlalchemy import Column, Integer, String


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ammount = Column(Integer)

    def __init__(self, id, name, ammount):
        self.id = id
        self.name = name
        self.ammount = ammount


class ExpenseRequest(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    ammount: int = Field(gt=0, lt=10000)

    model_config = {
        "json_schema_extra": {"example": {"name": "expense name", "ammount": 1}}
    }


class Income(Base):
    __tablename__ = "income"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ammount = Column(Integer)

    def __init__(self, id, name, ammount):
        self.id = id
        self.name = name
        self.ammount = ammount


class IncomeRequest(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    ammount: int = Field(gt=0, lt=10000)

    model_config = {
        "json_schema_extra": {"example": {"name": "income name", "ammount": 1}}
    }
