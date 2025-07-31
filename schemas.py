# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# === Schemas cho Pi ===
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

# === Schemas cho Bệnh nhân ===
class BenhNhanBase(BaseModel):
    MaBenhNhan: str
    HoVaTen: str
    NamSinh: Optional[int] = None
    IDPi: str

class BenhNhan(BenhNhanBase):
    class Config:
        from_attributes = True

# === Schema cho tra cứu chi tiết (kết hợp Pi và Bệnh nhân) ===
class PatientLookupResult(BenhNhanBase):
    DDNS: str
    NguoiSoHuu: Optional[str] = None

# === Schema cho đồng bộ chỉ số (vital sync) --- BỔ SUNG LẠI --- ===
class VitalSync(BaseModel):
    id_pi: str
    ma_benh_nhan: str
    nhietdo: float
    nhip_tim: int
    spo2: int

# === Schema cho chỉ số (để lưu vào DB) --- BỔ SUNG LẠI --- ===
class ChiSoCreate(BaseModel):
    NhietDo: float
    NhipTim: int
    SpO2: int
