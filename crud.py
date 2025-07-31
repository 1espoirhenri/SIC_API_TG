from sqlalchemy.orm import Session
import models, schemas

def get_all_pis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DanhSachPi).offset(skip).limit(limit).all()

def create_pi(db: Session, pi: schemas.PiCreate):
    db_pi = models.DanhSachPi(**pi.model_dump())
    # Trigger trên DB sẽ tự tạo IDPi, nên không cần gán ở đây
    # Tuy nhiên, script PostgreSQL tôi cung cấp trước đó đã có trigger
    # Nếu bạn dùng script không có trigger, bạn cần logic tạo IDPi ở đây
    db.add(db_pi)
    db.commit()
    db.refresh(db_pi)
    return db_pi

def get_patients_by_pi(db: Session, id_pi: str):
    return db.query(models.DanhBaBenhNhan).filter(models.DanhBaBenhNhan.IDPi == id_pi).all()

def get_patient_details_for_lookup(db: Session, ma_benh_nhan: str):
    # Dùng JOIN để lấy thông tin bệnh nhân và cả thông tin Pi (chứa DDNS)
    return db.query(models.DanhBaBenhNhan).filter(models.DanhBaBenhNhan.MaBenhNhan == ma_benh_nhan).first()

# === CRUD cho đồng bộ ===
def sync_vitals(db: Session, data: schemas.VitalSync):
    # Hàm này cần được bạn định nghĩa logic cụ thể
    # Ví dụ: kiểm tra và tạo mới bệnh nhân, sau đó thêm chỉ số
    print(f"Received data to sync: {data.model_dump_json()}")
    # Thêm logic ghi vào DB ở đây
    pass
