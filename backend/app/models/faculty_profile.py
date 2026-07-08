from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import uuid


class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    # Personal Information
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    designation: Mapped[str] = mapped_column(String, nullable=False)
    department: Mapped[str | None] = mapped_column(String)
    skills: Mapped[str | None] = mapped_column(String)
    phone_number: Mapped[str | None] = mapped_column(String)
    bio: Mapped[str | None] = mapped_column(Text)
    profile_image_url: Mapped[str | None] = mapped_column(String)

    # --- NEW FIELDS FROM AUDIT ---
    employee_id: Mapped[str | None] = mapped_column(String, unique=True, index=True)
    website: Mapped[str | None] = mapped_column(String)
    linkedin: Mapped[str | None] = mapped_column(String)
    google_scholar: Mapped[str | None] = mapped_column(String)
    orcid: Mapped[str | None] = mapped_column(String)
    office_location: Mapped[str | None] = mapped_column(String)
    specialization: Mapped[str | None] = mapped_column(String)
    areas_of_interest: Mapped[str | None] = mapped_column(String)

    # --- Relationships ---
    user = relationship("User", back_populates="profile")

    publications = relationship(
        "Publication", back_populates="faculty", cascade="all, delete-orphan"
    )
    education = relationship(
        "Education", back_populates="faculty", cascade="all, delete-orphan"
    )
    experience = relationship(
        "Experience", back_populates="faculty", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="faculty", cascade="all, delete-orphan"
    )
    achievements = relationship(
        "Achievement", back_populates="faculty", cascade="all, delete-orphan"
    )
    # New Sprint 1 Relationships
    patents = relationship(
        "Patent", back_populates="faculty_profile", cascade="all, delete-orphan"
    )
    certifications = relationship(
        "Certification", back_populates="faculty_profile", cascade="all, delete-orphan"
    )
    teaching = relationship(
        "Teaching", back_populates="faculty_profile", cascade="all, delete-orphan"
    )
    student_guidance = relationship(
        "StudentGuidance",
        back_populates="faculty_profile",
        cascade="all, delete-orphan",
    )
    workshops = relationship(
        "Workshop", back_populates="faculty_profile", cascade="all, delete-orphan"
    )
