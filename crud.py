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

def sync_vitals(db: Session, data: schemas.VitalSync):
    # --- PHẦN SỬA ĐỔI QUAN TRỌNG ---
    
    # 1. Kiểm tra xem bệnh nhân đã tồn tại trong DB trung gian chưa
    db_patient = db.query(models.BenhNhan).filter(models.BenhNhan.MaBenhNhan == data.ma_benh_nhan).first()
    
    # 2. Nếu chưa tồn tại, tạo mới
    if not db_patient:
        print(f"Benh nhan {data.ma_benh_nhan} chua co tren server. Dang tao moi...")
        # Lấy thông tin bệnh nhân từ Pi cục bộ (bạn sẽ cần tạo endpoint này trên Pi)
        # Hoặc tạo với thông tin mặc định
        new_patient_info = models.BenhNhan(
            MaBenhNhan=data.ma_benh_nhan,
            IDPi=data.id_pi,
            HoVaTen=f"Bệnh nhân {data.ma_benh_nhan}", # Tên mặc định
            NamSinh=2000 # Năm sinh mặc định
        )
        db.add(new_patient_info)
        db.commit()
        db.refresh(new_patient_info)
        print(f"Da tao moi benh nhan {data.ma_benh_nhan}.")

    # 3. Tạo bản ghi chỉ số mới (giữ nguyên)
    db_chiso = models.ChiSo(
        MaBenhNhan=data.ma_benh_nhan,
        NhietDo=data.nhietdo,
        NhipTim=data.nhip_tim,
        SpO2=data.spo2
    )
    db.add(db_chiso)
    db.commit()
    db.refresh(db_chiso)
    return db_chiso
