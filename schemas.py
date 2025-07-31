from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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

class BenhNhanBase(BaseModel):
    MaBenhNhan: str
    HoVaTen: str
    NamSinh: Optional[int] = None
    IDPi: str

class BenhNhan(BenhNhanBase):
    class Config:
        from_attributes = True

class BenhNhanUpdate(BaseModel):
    HoVaTen: str

class VitalSync(BaseModel):
    id_pi: str
    ma_benh_nhan: str
    nhietdo: float
    nhip_tim: int
    spo2: int

class PatientVitalsResponse(BenhNhanBase):
    nhietdo: Optional[float] = None
    nhip_tim: Optional[int] = None
    spo2: Optional[int] = None
    thoi_gian_do: Optional[datetime] = None
