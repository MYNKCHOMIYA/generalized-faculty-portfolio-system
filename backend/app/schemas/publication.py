from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PublicationBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the publication")
    publication_type: str = Field(..., description="Journal, Conference, Book, etc.")
    publisher: Optional[str] = None
    publication_year: int
    doi: Optional[str] = None
    citations: int = 0

class PublicationCreate(PublicationBase):
    pass

class PublicationUpdate(BaseModel):
    title: Optional[str] = None
    publication_type: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    citations: Optional[int] = None

class PublicationResponse(PublicationBase):
    id: str
    faculty_id: str

    model_config = ConfigDict(from_attributes=True)