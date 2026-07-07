from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import uuid

class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Notice we link to the faculty_profile, NOT the user directly. 
    # This keeps academic data cleanly separated from authentication data.
    faculty_id: Mapped[str] = mapped_column(ForeignKey("faculty_profiles.id", ondelete="CASCADE"))
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    publication_type: Mapped[str] = mapped_column(String, nullable=False) # e.g., Journal, Conference, Book
    publisher: Mapped[str | None] = mapped_column(String)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    doi: Mapped[str | None] = mapped_column(String)
    citations: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    faculty = relationship("FacultyProfile", back_populates="publications")