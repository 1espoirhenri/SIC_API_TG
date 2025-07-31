# crud.py
from sqlalchemy.orm import Session
import models, schemas

# === CRUD cho Pi ===
def get_all_pis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DanhSachPi).offset(skip).limit(limit).all()

def create_pi(db: Session, pi: schemas.PiCreate):
    db_pi = models.DanhSachPi(**pi.model_dump())
    db.add(db_pi)
    db.commit()
    db.refresh(db_pi)
    return db_pi

# === CRUD cho Bệnh nhân ===
def get_patients_by_pi(db: Session, id_pi: str):
    return db.query(models.DanhBaBenhNhan).filter(models.DanhBaBenhNhan.IDPi == id_pi).all()

def get_patient_details_for_lookup(db: Session, ma_benh_nhan: str):
    return db.query(models.DanhBaBenhNhan).filter(models.DanhBaBenhNhan.MaBenhNhan == ma_benh_nhan).first()

# === CRUD cho đồng bộ chỉ số --- BỔ SUNG LẠI --- ===
def sync_vitals(db: Session, data: schemas.VitalSync):
    """
    Hàm này xử lý việc đồng bộ: kiểm tra và tạo bệnh nhân nếu chưa có,
    sau đó thêm bản ghi chỉ số mới.
    """
    # 1. Kiểm tra xem bệnh nhân đã có trong danh bạ trung gian chưa
    db_patient = db.query(models.DanhBaBenhNhan).filter(models.DanhBaBenhNhan.MaBenhNhan == data.ma_benh_nhan).first()

    # 2. Nếu chưa có, tạo mới bệnh nhân trong danh bạ
    if not db_patient:
        print(f"Benh nhan {data.ma_benh_nhan} chua co, tao moi...")
        new_patient = models.DanhBaBenhNhan(
            MaBenhNhan=data.ma_benh_nhan,
            HoVaTen=f"Bệnh nhân {data.ma_benh_nhan}", # Tên tạm thời
            IDPi=data.id_pi,
            NamSinh=2000 # Năm sinh mặc định
        )
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

    # 3. Thêm bản ghi chỉ số mới vào bảng ChiSo (bạn cần có model ChiSo)
    # Giả sử bạn có model ChiSo trong models.py
    # db_chiso = models.ChiSo(
    #     MaBenhNhan=data.ma_benh_nhan,
    #     NhietDo=data.nhietdo,
    #     NhipTim=data.nhip_tim,
    #     SpO2=data.spo2
    # )
    # db.add(db_chiso)
    # db.commit()
    
    # Tạm thời chỉ in ra để xác nhận
    print(f"Da nhan du lieu dong bo cho: {data.ma_benh_nhan}")
    
    return {"status": "success"}
