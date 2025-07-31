from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, crud, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIC Central API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Central Health Monitoring API"}

@app.post("/pis/", response_model=schemas.Pi, tags=["Pi Devices"])
def create_new_pi(pi: schemas.PiCreate, db: Session = Depends(get_db)):
    db_pi = crud.get_pi_by_id(db, pi_id=pi.IDPi)
    if db_pi:
        raise HTTPException(status_code=400, detail="Pi ID already registered")
    return crud.create_pi(db=db, pi=pi)

@app.get("/pis/", response_model=List[schemas.Pi], tags=["Pi Devices"])
def read_all_pis(db: Session = Depends(get_db)):
    return crud.get_all_pis(db)

@app.get("/pis/{id_pi}/patients/", response_model=List[schemas.BenhNhan], tags=["Patient Management"])
def read_patients_from_pi(id_pi: str, db: Session = Depends(get_db)):
    return crud.get_patients_by_pi(db, pi_id=id_pi)

@app.get("/patients/all", response_model=List[schemas.BenhNhan], tags=["Patient Management"])
def read_all_patients(db: Session = Depends(get_db)):
    return crud.get_all_patients(db)

@app.get("/lookup/patient/{ma_benh_nhan}", response_model=schemas.PatientVitalsResponse, tags=["Patient Management"])
def lookup_patient_vitals(ma_benh_nhan: str, db: Session = Depends(get_db)):
    patient_data = crud.get_patient_with_vitals(db, ma_benh_nhan=ma_benh_nhan)
    if patient_data is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bệnh nhân trong danh bạ trung gian")
    return patient_data

@app.put("/patients/{ma_benh_nhan}/rename", response_model=schemas.BenhNhan, tags=["Patient Management"])
def rename_patient(ma_benh_nhan: str, data: schemas.BenhNhanUpdate, db: Session = Depends(get_db)):
    updated_patient = crud.update_patient_name(db, ma_benh_nhan=ma_benh_nhan, new_name=data.HoVaTen)
    if updated_patient is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy bệnh nhân để đổi tên")
    return updated_patient

@app.post("/api/vitals/sync", tags=["Synchronization"])
def sync_vitals_from_pi(data: schemas.VitalSync, db: Session = Depends(get_db)):
    result = crud.sync_vitals(db=db, data=data)
    if result is None:
        raise HTTPException(status_code=400, detail=f"Pi ID {data.id_pi} không tồn tại.")
    return {"status": "success", "message": f"Data for {data.ma_benh_nhan} synchronized."}
