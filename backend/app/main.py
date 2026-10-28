
from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.services.ai_service import analyze_complaint

# Store the database inside the backend folder.
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "civicroute.db"

Category = Literal[
    "pothole",
    "road_damage",
    "open_manhole",
    "flooding",
    "traffic_signal",
    "signage",
    "debris",
    "drainage",
    "public_transport",
    "other",
]

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize_database():
    with get_connection() as connection:

        # 1. Citizen complaints
        connection.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                location_zone TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                status TEXT NOT NULL DEFAULT 'SUBMITTED',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. AI analysis results
        connection.execute("""
            CREATE TABLE IF NOT EXISTS ai_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                predicted_category TEXT NOT NULL,
                urgency INTEGER NOT NULL
                    CHECK (urgency BETWEEN 1 AND 5),
                severity TEXT NOT NULL,
                summary TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                review_status TEXT NOT NULL DEFAULT 'PENDING',
                model_name TEXT NOT NULL,
                prompt_version TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id)
                    REFERENCES reports(id)
            )
        """)

        # 3. Complaint status history
        connection.execute("""
            CREATE TABLE IF NOT EXISTS status_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                old_status TEXT,
                new_status TEXT NOT NULL,
                changed_by TEXT NOT NULL DEFAULT 'system',
                note TEXT,
                changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id)
                    REFERENCES reports(id)
            )
        """)

        # 4. Administrator notes
        connection.execute("""
            CREATE TABLE IF NOT EXISTS report_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                note TEXT NOT NULL,
                author TEXT NOT NULL DEFAULT 'admin',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id)
                    REFERENCES reports(id)
            )
        """)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="CivicRoute AI API",
    description="AI-assisted road maintenance reporting system",
    version="0.1.0",
    lifespan=lifespan,
)

class ReportCreate(BaseModel):
    category: Category
    description: str = Field(min_length=5, max_length=3000)
    location_zone: str = Field(min_length=1, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

@app.get("/")
def home():
    return {
        "message": "Welcome to CivicRoute AI",
        "docs": "/docs",
    }

@app.get("/api/v1/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/reports", status_code=201)
def create_report(report: ReportCreate):
    try:
        # Step 1: Analyze the complaint
        analysis = analyze_complaint(report.description)

        # Step 2: Save the complaint and its analysis
        with get_connection() as connection:

            cursor = connection.execute(
                """
                INSERT INTO reports (
                    category,
                    description,
                    location_zone,
                    latitude,
                    longitude
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    report.category,
                    report.description,
                    report.location_zone,
                    report.latitude,
                    report.longitude,
                ),
            )

            report_id = cursor.lastrowid

            # Step 3: Record the initial complaint status
            connection.execute(
                """
                INSERT INTO status_history (
                    report_id,
                    old_status,
                    new_status,
                    changed_by,
                    note
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    report_id,
                    None,
                    "SUBMITTED",
                    "system",
                    "Complaint submitted by citizen",
                ),
            )

            # Step 4: Save the AI analysis
            connection.execute(
                """
                INSERT INTO ai_analyses (
                    report_id,
                    predicted_category,
                    urgency,
                    severity,
                    summary,
                    recommended_action,
                    review_status,
                    model_name,
                    prompt_version
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report_id,
                    analysis["predicted_category"],
                    analysis["urgency"],
                    analysis["severity"],
                    analysis["summary"],
                    analysis["recommended_action"],
                    analysis["review_status"],
                    analysis["model_name"],
                    analysis["prompt_version"],
                ),
            )

        # Step 5: Return the complaint and AI result
        return {
            "id": report_id,
            "message": "Report submitted successfully",
            "status": "SUBMITTED",
            "ai_analysis": analysis,
        }

    except sqlite3.Error as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not save the report",
        ) from exc


@app.get("/api/v1/reports")
def list_reports():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM reports ORDER BY id DESC"
        ).fetchall()

    return [dict(row) for row in rows]


@app.get("/api/v1/reports/{report_id}/analysis")
def get_report_analysis(report_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                r.id AS report_id,
                r.description,
                r.location_zone,
                r.status AS report_status,
                a.predicted_category,
                a.urgency,
                a.severity,
                a.summary,
                a.recommended_action,
                a.review_status,
                a.model_name,
                a.prompt_version,
                a.created_at AS analysis_created_at
            FROM reports r
            LEFT JOIN ai_analyses a
                ON r.id = a.report_id
            WHERE r.id = ?
            ORDER BY a.id DESC
            LIMIT 1
            """,
            (report_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    result = dict(row)

    if result["predicted_category"] is None:
        raise HTTPException(
            status_code=404,
            detail="AI analysis not found for this report",
        )

    return result

