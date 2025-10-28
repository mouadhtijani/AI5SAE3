from pydantic import BaseModel
from datetime import date

class RapportBase(BaseModel):
    titre: str
    description: str
    auteur: str
    type_export: str = "PDF"

class RapportCreate(RapportBase):
    pass

class RapportResponse(RapportBase):
    id: int
    date_creation: date

    class Config:
        from_attributes = True  # updated for Pydantic v2
