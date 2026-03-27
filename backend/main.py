import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    from backend.routes.auth_routes import router as auth_router
    from backend.routes.chat import router as chat_router
    from backend.routes.fire_plan import router as fire_router
    from backend.routes.health_score import router as health_router
    from backend.routes.sip_calc import router as sip_router
    from backend.routes.tax_calc import router as tax_router
except ModuleNotFoundError:
    # Allows running from `backend/` with: uvicorn main:app --reload
    from routes.auth_routes import router as auth_router
    from routes.chat import router as chat_router
    from routes.fire_plan import router as fire_router
    from routes.health_score import router as health_router
    from routes.sip_calc import router as sip_router
    from routes.tax_calc import router as tax_router

app = FastAPI(title="AI Money Mentor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth & Admin"])
app.include_router(chat_router, tags=["Chat"])
app.include_router(health_router, tags=["Health Score"])
app.include_router(fire_router, tags=["FIRE Planner"])
app.include_router(sip_router, tags=["SIP Calculator"])
app.include_router(tax_router, tags=["Tax Calculator"])


@app.get("/")
def root():
    return {"message": "AI Money Mentor API is running."}
