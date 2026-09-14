from fastapi import APIRouter, Response

from app.ai.copilot import copilot
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.network_service import network_service
from app.services.report_service import report_service

router = APIRouter()


@router.get("/routers")
def get_routers() -> list[dict]:
    return network_service.get_routers()


@router.post("/routers/import")
def import_routers(data: list[dict]) -> dict:
    from app.simulators.mpls_simulator import network_simulator
    network_simulator.import_custom_data(data)
    return {"status": "success", "message": f"Successfully loaded {len(data)} custom routers"}


@router.post("/routers/reset")
def reset_routers() -> dict:
    from app.simulators.mpls_simulator import network_simulator
    network_simulator.reset_simulation()
    return {"status": "success", "message": "Simulation reset successfully"}


@router.get("/alerts")
def get_alerts(limit: int = 50) -> list[dict]:
    return network_service.get_alerts(limit=limit)


@router.get("/metrics")
def get_metrics() -> dict:
    return network_service.get_metrics()


@router.get("/predictions")
def get_predictions() -> list[dict]:
    return network_service.get_predictions()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    snapshot = network_service.get_snapshot()
    answer = copilot.answer(request.message, snapshot)
    return ChatResponse(**answer)


@router.get("/reports")
def list_reports() -> list[dict]:
    return report_service.list_reports()


@router.get("/reports/{report_type}")
def download_report(report_type: str) -> Response:
    pdf = report_service.generate_pdf(report_type, network_service.get_snapshot())
    filename = f"{report_type.replace('_', '-')}-report.pdf"
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
