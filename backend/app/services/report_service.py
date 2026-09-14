from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ReportService:
    def list_reports(self) -> list[dict]:
        return [
            {"type": "incident", "title": "PDF Incident Report", "description": "Critical alerts, root cause, and NOC actions."},
            {"type": "daily_health", "title": "Daily Health Report", "description": "Router health, telemetry trends, and risk ranking."},
            {"type": "executive", "title": "Executive Summary", "description": "Leadership-ready operational posture summary."},
        ]

    def generate_pdf(self, report_type: str, snapshot: dict) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, title=f"{report_type} report")
        styles = getSampleStyleSheet()
        story = [
            Paragraph("ISRO Secure MPLS Operations Report", styles["Title"]),
            Paragraph(f"Report type: {report_type.replace('_', ' ').title()}", styles["Heading2"]),
            Paragraph(f"Generated: {datetime.utcnow().isoformat()}Z", styles["Normal"]),
            Spacer(1, 16),
            Paragraph("Network Health", styles["Heading2"]),
        ]
        summary = snapshot["metrics"]["summary"]
        story.append(
            Table(
                [["Active", "Healthy", "Warning", "Critical"], [summary["active_routers"], summary["healthy_routers"], summary["warning_routers"], summary["critical_routers"]]],
                style=self._table_style(),
            )
        )
        story.extend([Spacer(1, 16), Paragraph("Top Router Risks", styles["Heading2"])])
        rows = [["Router", "State", "Risk", "Outage ETA"]]
        for item in snapshot["predictions"][:6]:
            rows.append([item["router_id"], item["predicted_state"], item["risk_score"], item["predicted_outage_time"]])
        story.append(Table(rows, style=self._table_style()))
        story.extend([Spacer(1, 16), Paragraph("Recent Alerts", styles["Heading2"])])
        alert_rows = [["Router", "Severity", "Category", "Message"]]
        for alert in snapshot["alerts"][:8]:
            alert_rows.append([alert["router_id"], alert["severity"], alert["category"], alert["message"][:70]])
        story.append(Table(alert_rows, style=self._table_style()))
        story.extend([Spacer(1, 16), Paragraph("Recommended NOC Actions", styles["Heading2"])])
        top_router = max(snapshot["routers"], key=lambda item: item["prediction"]["risk_score"])
        for action in top_router["recommendations"]:
            story.append(Paragraph(f"- {action}", styles["Normal"]))
        doc.build(story)
        return buffer.getvalue()

    @staticmethod
    def _table_style() -> TableStyle:
        return TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9ca3af")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )


report_service = ReportService()
