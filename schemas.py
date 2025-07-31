from pydantic import BaseModel
from typing import List, Optional

# === Schemas for Pi ===
class PiBase(BaseModel):
    IDPi: str
    DDNS: str
    NguoiSoHuu: Optional[str] = None

class PiCreate(PiBase):
    pass

class Pi(PiBase):
    ID: int

    class Config:
        from_attributes = True

# === Schemas for Patients ===
class BenhNhanBase(BaseModel):
    MaBenhNhan: str
    HoVaTen: str
    NamSinh: Optional[int] = None
    IDPi: str

class BenhNhanCreate(BenhNhanBase):
    pass

class BenhNhan(BenhNhanBase):
    class Config:
        from_attributes = True

# === Schema for Patient Lookup ===
class PatientLookupResult(BenhNhanBase):
    # This will inherit fields from BenhNhanBase and add Pi's info
    DDNS: str
    NguoiSoHuu: Optional[str] = None
