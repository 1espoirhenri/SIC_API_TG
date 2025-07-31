# main.py
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Central Directory API")

# === ENDPOINT ĐỒNG BỘ TỪ PI --- BỔ SUNG LẠI --- ===
@app.post("/api/vitals/sync", tags=["Synchronization"])
def sync_vitals_from_pi(data: schemas.VitalSync, db: Session = Depends(get_db)):
    """
    Endpoint để nhận dữ liệu từ Raspberry Pi và lưu vào DB trung gian.
    """
    return crud.sync_vitals(db=db, data=data)

# === API cho Thiết bị Pi ===
@app.post("/pis/", response_model=schemas.Pi, tags=["Thiết bị Pi"])
def create_new_pi(pi: schemas.PiCreate, db: Session = Depends(get_db)):
    return crud.create_pi(db=db, pi=pi)

@app.get("/pis/", response_model=List[schemas.Pi], tags=["Thiết bị Pi"])
def read_all_pis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_pis(db, skip=skip, limit=limit)

# === API cho Danh bạ Bệnh nhân ===
@app.get("/pis/{id_pi}/patients/", response_model=List[schemas.BenhNhan], tags=["Danh bạ Bệnh nhân"])
def read_patients_from_pi(id_pi: str, db: Session = Depends(get_db)):
    return crud.get_patients_by_pi(db, id_pi=id_pi)

@app.get("/lookup/patient/{ma_benh_nhan}", response_model=schemas.PatientLookupResult, tags=["Danh bạ Bệnh nhân"])
def lookup_patient_address(ma_benh_nhan: str, db: Session = Depends(get_db)):
    patient_details = crud.get_patient_details_for_lookup(db, ma_benh_nhan=ma_benh_nhan)
    if not patient_details:
        raise HTTPException(status_code=404, detail="Không tìm thấy bệnh nhân trong danh bạ trung gian")
    
    # Quan trọng: Cần đảm bảo mối quan hệ 'pi' đã được load
    if not patient_details.pi:
         raise HTTPException(status_code=500, detail="Lỗi dữ liệu: Bệnh nhân không được liên kết với Pi nào.")

    return schemas.PatientLookupResult(
        MaBenhNhan=patient_details.MaBenhNhan,
        HoVaTen=patient_details.HoVaTen,
        NamSinh=patient_details.NamSinh,
        IDPi=patient_details.IDPi,
        DDNS=patient_details.pi.DDNS,
        NguoiSoHuu=patient_details.pi.NguoiSoHuu
    )
