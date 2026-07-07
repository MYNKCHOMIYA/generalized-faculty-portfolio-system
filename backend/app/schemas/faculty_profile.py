from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# 1. Shared Properties
# These are the fields that are common across creating, reading, and updating.
class FacultyProfileBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Faculty's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Faculty's last name")
    designation: str = Field(..., min_length=2, max_length=100, description="e.g., Assistant Professor, HOD")
    phone_number: Optional[str] = Field(default=None, max_length=20)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None

# 2. Properties to receive on Profile Creation
# Notice we do NOT include user_id here. We will extract user_id securely 
# from the JWT token in the backend so users cannot spoof other accounts.
class FacultyProfileCreate(FacultyProfileBase):
    pass

# 3. Properties to receive on Profile Update
# When updating, a user might only change their bio, so all fields must be Optional.
class FacultyProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    designation: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None

# 4. Properties to return to the React Frontend
# This includes the auto-generated database IDs.
class FacultyProfileResponse(FacultyProfileBase):
    id: str
    user_id: str

    # This tells Pydantic to read data directly from the SQLAlchemy ORM model
    model_config = ConfigDict(from_attributes=True)