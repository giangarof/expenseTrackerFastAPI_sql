from fastapi import FastAPI

# db
from database.database import engine, SessionLocal

# routes
import routes.expenses as expensesRoutes
import routes.income as incomeRoutes
import routes.analysis as analysisRoutes

# models
import schema.models as models

app = FastAPI()

app.include_router(expensesRoutes.router)
app.include_router(incomeRoutes.router)
app.include_router(analysisRoutes.router)

models.Base.metadata.create_all(bind=engine)
