# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Pi(Base):
    __tablename__ = "pis"
    IDPi = Column(String(50), primary_key=True, index=True)
    DDNS = Column(String(255), unique=True)
    NguoiSoHuu = Column(String(100))
    ID = Column(Integer, unique=True, autoincrement=True)
    
    benhnhans = relationship("BenhNhan", back_populates="pi")

class BenhNhan(Base):
    __tablename__ = "benhnhan"
    MaBenhNhan = Column(String(50), primary_key=True, index=True)
    HoVaTen = Column(String(100), nullable=False)
    NamSinh = Column(Integer)
    IDPi = Column(String(50), ForeignKey("pis.IDPi"))

    pi = relationship("Pi", back_populates="benhnhans")
    chisos = relationship("ChiSo", back_populates="benhnhan")

class ChiSo(Base):
    __tablename__ = "chiso"
    IDChiSo = Column(Integer, primary_key=True, autoincrement=True)
    MaBenhNhan = Column(String(50), ForeignKey("benhnhan.MaBenhNhan"))
    NhietDo = Column(Float)
    NhipTim = Column(Integer)
    SpO2 = Column(Integer)
    ThoiGianDo = Column(DateTime(timezone=True), server_default=func.now())
    
    benhnhan = relationship("BenhNhan", back_populates="chisos")
