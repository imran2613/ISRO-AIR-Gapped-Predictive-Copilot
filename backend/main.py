from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.database.sqlite import init_db
from app.simulators.mpls_simulator import network_simulator
from app.utils.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Air-gapped predictive copilot for simulated secure MPLS operations.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()
    network_simulator.bootstrap()


app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": settings.ai_provider, "air_gapped_ready": True}
