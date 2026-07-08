from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# This single line forces SQLAlchemy to load all models from __init__.py at startup
import app.models

from app.api.auth import router as auth_router
from app.core.config import settings
from app.api.faculty_profile import router as profile_router
from app.api.publication import router as publication_router
from app.api.education import router as education_router
from app.api.experience import router as experience_router
from app.api.project import router as project_router
from app.api.achievement import router as achievement_router
from app.api.export import router as export_router
from app.api import patent, certification
from app.api import patent, certification, teaching, student_guidance

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Configure CORS for the frontend React application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication Routers
app.include_router(
    auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"]
)
app.include_router(
    profile_router, prefix=f"{settings.API_V1_STR}/profile", tags=["Faculty Profile"]
)
app.include_router(
    publication_router,
    prefix=f"{settings.API_V1_STR}/publications",
    tags=["Publications"],
)
app.include_router(
    education_router, prefix=f"{settings.API_V1_STR}/education", tags=["Education"]
)
app.include_router(
    experience_router, prefix=f"{settings.API_V1_STR}/experience", tags=["Experience"]
)
app.include_router(
    project_router, prefix=f"{settings.API_V1_STR}/projects", tags=["Projects"]
)
app.include_router(
    achievement_router,
    prefix=f"{settings.API_V1_STR}/achievements",
    tags=["Achievements"],
)
app.include_router(
    export_router, prefix=f"{settings.API_V1_STR}/export", tags=["Data Export"]
)
app.include_router(patent.router, prefix="/api/patents", tags=["Patents"])
app.include_router(
    certification.router, prefix="/api/certifications", tags=["Certifications"]
)
app.include_router(teaching.router, prefix="/api/teaching", tags=["Teaching"])
app.include_router(
    student_guidance.router, prefix="/api/student-guidance", tags=["Student Guidance"]
)


@app.get("/")
def root():
    return {"message": "Welcome to the GFPMS API"}
