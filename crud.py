from sqlalchemy.orm import Session
import models, schemas

def get_pi_by_id(db: Session, pi_id: str):
    return db.query(models.Pi).filter(models.Pi.IDPi == pi_id).first()

def get_all_pis(db: Session):
    return db.query(models.Pi).all()

def create_pi(db: Session, pi: schemas.PiCreate):
    db_pi = models.Pi(**pi.model_dump())
    db.add(db_pi)
    db.commit()
    db.refresh(db_pi) # This line is crucial
    return db_pi

def get_benh_nhan_by_ma(db: Session, ma_benh_nhan: str):
    return db.query(models.BenhNhan).filter(models.BenhNhan.MaBenhNhan == ma_benh_nhan).first()

def get_patients_by_pi(db: Session, pi_id: str):
    return db.query(models.BenhNhan).filter(models.BenhNhan.IDPi == pi_id).all()

def get_all_patients(db: Session):
    return db.query(models.BenhNhan).all()

def update_patient_name(db: Session, ma_benh_nhan: str, new_name: str):
    db_patient = get_benh_nhan_by_ma(db, ma_benh_nhan=ma_benh_nhan)
    if not db_patient:
        return None
    db_patient.HoVaTen = new_name
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_with_vitals(db: Session, ma_benh_nhan: str):
    patient = get_benh_nhan_by_ma(db, ma_benh_nhan)
    if not patient:
        return None
    
    latest_vitals = db.query(models.ChiSo)\
                     .filter(models.ChiSo.MaBenhNhan == ma_benh_nhan)\
                     .order_by(models.ChiSo.ThoiGianDo.desc())\
                     .first()
                     
    response_data = schemas.BenhNhan.from_orm(patient).model_dump()
    if latest_vitals:
        response_data.update({
            "nhietdo": latest_vitals.NhietDo,
            "nhip_tim": latest_vitals.NhipTim,
            "spo2": latest_vitals.SpO2,
            "thoi_gian_do": latest_vitals.ThoiGianDo
        })
    return schemas.PatientVitalsResponse(**response_data)

def sync_vitals(db: Session, data: schemas.VitalSync):
    db_patient = get_benh_nhan_by_ma(db, ma_benh_nhan=data.ma_benh_nhan)
    
    if not db_patient:
        new_patient = models.BenhNhan(
            MaBenhNhan=data.ma_benh_nhan,
            HoVaTen=f"Bệnh nhân {data.ma_benh_nhan}",
            IDPi=data.id_pi,
            NamSinh=2000
        )
        db.add(new_patient)
        db.commit()

    db_chiso = models.ChiSo(
        MaBenhNhan=data.ma_benh_nhan,
        NhietDo=data.nhietdo,
        NhipTim=data.nhip_tim,
        SpO2=data.spo2
    )
    db.add(db_chiso)
    db.commit()
    return db_chiso
