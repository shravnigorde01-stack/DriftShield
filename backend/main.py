from fastapi import FastAPI

# API Routers
from backend.api.projects import router as projects_router
from backend.api.datasets import router as datasets_router
from backend.api.monitoring import router as monitoring_router
from backend.api.alerts import router as alerts_router
from backend.api.reports import router as reports_router

# Database
from backend.database.connection import engine, Base
from backend.database.projects import Project
from backend.database.monitoring_runs import MonitoringRun
from backend.database.alerts import Alert

# Configuration
from config.settings import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_TAGLINE
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=PROJECT_TAGLINE
)

# Register API routers
app.include_router(projects_router)
app.include_router(datasets_router)
app.include_router(monitoring_router)
app.include_router(alerts_router)
app.include_router(reports_router)


@app.get("/")
def home():
    return {
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION,
        "message": "Welcome to DriftShield!",
        "tagline": PROJECT_TAGLINE,
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": PROJECT_NAME
    }