from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import uuid


class User(Base):
    __tablename__ = "users"

    # Using UUIDs for enterprise security instead of sequential IDs
    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, default="faculty")  # admin, hod, faculty

    department_id: Mapped[str | None] = mapped_column(ForeignKey("departments.id"))

    # Relationships
    department = relationship("Department", back_populates="users")
    profile = relationship("FacultyProfile", back_populates="user", uselist=False)
