from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class DanhSachPi(Base):
    __tablename__ = "DanhSachPi"
    ID = Column(Integer, primary_key=True, index=True)
    IDPi = Column(String(10), unique=True, index=True, nullable=False)
    DDNS = Column(String(255), unique=True, nullable=False)
    NguoiSoHuu = Column(String(100))

    benhnhans = relationship("DanhBaBenhNhan", back_populates="pi")


class DanhBaBenhNhan(Base):
    __tablename__ = "DanhBaBenhNhan"
    MaBenhNhan = Column(String(20), primary_key=True, index=True)
    HoVaTen = Column(String(100), nullable=False)
    NamSinh = Column(Integer)
    IDPi = Column(String(10), ForeignKey("DanhSachPi.IDPi"))

    pi = relationship("DanhSachPi", back_populates="benhnhans")