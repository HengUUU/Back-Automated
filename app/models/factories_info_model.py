from pydantic import BaseModel
from typing import Optional

class Factory(BaseModel):
    Id: str | None = None           # <-- change from int to str
    name: str
    address: str | None = None
    district: str | None = None
    location: str | None = None
    business: str | None = None
    mapLatLong: str | None = None
    
class FactoryUpdate(BaseModel):
    Id: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    location: Optional[str] = None
    business: Optional[str] = None
    mapLatLong: Optional[str] = None
