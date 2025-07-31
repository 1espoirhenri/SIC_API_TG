from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# --- Schemas cho Bệnh nhân trong danh bạ ---
class BenhNhanBase(BaseModel):
    MaBenhNhan: str
    HoVaTen: str
    NamSinh: Optional[int] = None
    IDPi: str


class BenhNhan(BenhNhanBase):
    model_config = ConfigDict(from_attributes=True)


# --- Schemas cho Pi ---
class PiBase(BaseModel):
    IDPi: str
    DDNS: str
    NguoiSoHuu: Optional[str] = None


class PiCreate(PiBase):
    pass


class Pi(PiBase):
    ID: int
    model_config = ConfigDict(from_attributes=True)


# Schema trả về khi tra cứu, chứa cả thông tin Pi và DDNS
class PatientLookupResult(BenhNhan):
    pi: Pi