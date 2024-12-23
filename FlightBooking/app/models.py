import string
from datetime import timedelta
from multiprocessing.reduction import duplicate
from random import random

from cloudinary.utils import unique
from pycparser import CParser
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, Date, column, nullsfirst, DateTime, \
    Index, PrimaryKeyConstraint, UniqueConstraint
from datetime import date, time, datetime  # Import đúng kiểu datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.testing import fails

from app import db, app, db_sub
import hashlib
from enum import Enum as RoleEnum
from flask_login import UserMixin

# # Database subdb
# class CategoryPage(db_sub.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
#     ico = Column(String(100), nullable=True)


# Database Flight Booking System
class VaiTro(RoleEnum):
    ADMIN = 1
    USER = 2
    EMPLOYEE = 3


class HangThanhVien(RoleEnum):
    BAC = 1
    VANG = 2
    KIMCUONG = 3


class HangVe(RoleEnum):
    PHOTHONG = 1
    THUONGGIA = 2

    @classmethod
    def from_value(cls, value):
        try:
            return cls(value).name  # Trả về tên từ giá trị
        except ValueError:
            return None


class LoaiVe(RoleEnum):
    MOTCHIEU = 1
    KHUHOI = 2

# Hàm tạo mã tự động cho các đối tượng
def generate_code(prefix, length=10):
    # Tạo một mã ngẫu nhiên gồm chữ và số
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class NguoiDung(db.Model, UserMixin):
    __tablename__ = 'NguoiDung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fname = Column(String(50), nullable=False, unique=False)
    lname = Column(String(50), nullable=False)
    dia_chi = Column(String(200))
    email = Column(String(100), nullable=False, unique=False)
    so_dien_thoai = Column(String(15), nullable=True)
    ngay_sinh = Column(Date)
    so_CCCD = Column(String(12), unique=True, nullable=True)
    tai_khoan = relationship("TaiKhoan", backref='NguoiDung', uselist=False)

    ve = relationship("Ve", backref='NguoiDung')

    def __str__(self):
        return self.lname

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'TaiKhoan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_dang_nhap = Column(String(50), nullable=False, unique=True)
    mat_khau = Column(String(100), nullable=False)
    trang_thai = Column(db.Boolean, default=True)
    vai_tro = Column(Enum(VaiTro), default=VaiTro.USER, nullable=False)

    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)

    @property
    def lname(self):
        return self.nguoi_dung.lname if self.nguoi_dung else None

    @property
    def fname(self):
        return self.nguoi_dung.fname if self.nguoi_dung else None

    @property
    def dia_chi(self):
        return self.nguoi_dung.dia_chi if self.nguoi_dung else None

    @property
    def so_CCCD(self):
        return self.nguoi_dung.so_CCCD if self.nguoi_dung else None

    @property
    def email(self):
        return self.nguoi_dung.email if self.nguoi_dung else None

    @property
    def so_dien_thoai(self):
        return self.nguoi_dung.so_dien_thoai if self.nguoi_dung else None

    def get_id(self):
        return str(self.id)


class Admin(NguoiDung, UserMixin):
    __tablename__ = 'Admin'
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    ngay_vao_lam = Column(Date)
    kinh_nghiem = Column(String(200))


    __mapper_args__ = {
        'inherit_condition': id == NguoiDung.id
    }


class KhachHang(NguoiDung, UserMixin):
    __tablename__ = 'KhachHang'
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    hang_thanh_vien = Column(Enum(HangThanhVien), default=HangThanhVien.BAC, nullable=False)
    don_hang = relationship('DonHang', backref='KhachHang')


    __mapper_args__ = {
        'inherit_condition': id == NguoiDung.id
    }


class NhanVien(NguoiDung, UserMixin):
    __tablename__ = 'NhanVien'
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    luong = Column(Float, nullable=False)
    ngay_vao_lam = Column(Date, nullable=False)
    ghi_chu = Column(String(200))
    don_hang = relationship('DonHang', backref='NhanVien')


    __mapper_args__ = {
        'inherit_condition': id == NguoiDung.id
    }


class HangMayBay(db.Model):
    __tablename__ = 'HangMayBay'
    so_hieu_hangmb = Column(String(10), primary_key=True)
    ten_hang = Column(String(50), nullable=False)
    lo_go = Column(String(500))
    may_bay = relationship("MayBay", backref='HangMayBay')

    def __str__(self):
        return self.ten_hang

class MayBay(db.Model):
    __tablename__ = 'MayBay'
    so_hieu_mb = Column(String(10), primary_key=True)
    hang_may_bay_ID = Column(String(10), ForeignKey(HangMayBay.so_hieu_hangmb), nullable=False)
    ghe = relationship('Ghe', backref='MayBay')
    chuyen_bay = relationship('ChuyenBay', backref='MayBay')

    def __init__(self, so_hieu_mb, hang_may_bay_ID):
        self.so_hieu_mb = so_hieu_mb
        self.hang_may_bay_ID = hang_may_bay_ID


class HanhLy(db.Model):
    __tablename__ = 'HanhLy'
    ma_HL = Column(String(10), primary_key=True)
    loai_HL = Column(String(20), nullable=True)
    trong_luong = Column(Integer, nullable=False)
    chi_phi = Column(Float, nullable=False)
    ve = relationship("Ve", backref='HanhLy', uselist=False)



class KhuyenMai(db.Model):
    __tablename__ = 'KhuyenMai'
    ma_KM = Column(String(10), primary_key=True, default=lambda: generate_code('KM'))
    mo_ta = Column(String(50), nullable=True)
    ty_le_giam = Column(Float, nullable=False)
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)
    don_hang = relationship('DonHang', backref='KhuyenMai')
    dieu_kien_KM = relationship('DieuKienKM', backref='KhuyenMai')


class DieuKienKM(db.Model):
    __tablename__ = 'DieuKienKM'
    ma_DK = Column(String(10), primary_key=True)
    noi_dung = Column(String(200), nullable=True)
    ghi_chu = Column(String(200), nullable=True)
    khuyen_mai_id = Column(String(10), ForeignKey(KhuyenMai.ma_KM), nullable=False)


class Ghe(db.Model):
    __tablename__ = 'Ghe'
    ma_ghe = Column(String(10), primary_key=True)
    hang_ve = Column(Enum(HangVe), default=HangVe.PHOTHONG, nullable=False)
    vi_tri = Column(String(10), nullable=False)
    may_bay = Column(String(10), ForeignKey(MayBay.so_hieu_mb), nullable=False)
    gia_ghe = Column(Float, nullable=False)
    trang_thai = Column(Boolean, default=False, nullable=False)

    ve = relationship('Ve', backref='Ghe')

    def __init__(self, ma_ghe, hang_ve, vi_tri, trang_thai, may_bay, gia_ghe):
        self.ma_ghe = ma_ghe
        self.hang_ve = hang_ve
        self.vi_tri = vi_tri
        self.trang_thai = trang_thai
        self.may_bay = may_bay
        self.gia_ghe=gia_ghe

class DonHang(db.Model):
    __tablename__ = 'DonHang'
    ma_DH = Column(String(10), primary_key=True, default=lambda: generate_code('DH'))
    khach_hang = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    nhan_vien = Column(Integer, ForeignKey(NhanVien.id), nullable=True)
    ngay_dat_DH = Column(DateTime, nullable=False, default=func.now())
    ma_KM = Column(String(10), ForeignKey(KhuyenMai.ma_KM), nullable=True)
    thanh_toan = relationship('ThanhToan', backref='DonHang')
    ve = relationship('Ve', backref='DonHang')


class Ve(db.Model):
    __tablename__ = 'Ve'
    ma_ve = Column(String(10), primary_key=True, default=lambda: generate_code('VE'))
    ma_don_hang = Column(String(10), ForeignKey(DonHang.ma_DH), nullable=False)
    nguoi_so_huu = Column(String(10), ForeignKey(NguoiDung.id), nullable=False)
    ngay_xuat_ve = Column(DateTime, nullable=True)
    loai_ve = Column(Enum(LoaiVe), default=LoaiVe.MOTCHIEU, nullable=False)
    ma_HL = Column(String(10), ForeignKey(HanhLy.ma_HL), nullable=True)
    gia_ve = Column(Float, nullable=False)
    chi_tiet_cb = relationship('ChiTietVe', backref='Ve')

    ghe = Column(String(10), ForeignKey(Ghe.ma_ghe), nullable=False)

class LichBay(db.Model):
    __tablename__ = 'LichBay'
    ma_LB = Column(String(10), primary_key=True)
    chuyen_bay = relationship('ChuyenBay', backref='LichBay')
    ngay_lap_lich = Column(Date, nullable=True)


class KhuVuc(db.Model):
    __tablename__ = 'KhuVuc'
    ma_khu_vuc = Column(String(10), primary_key=True)
    ten_khu_vuc = Column(String(50), nullable=False)
    san_bay = relationship('SanBay', backref='KhuVuc')

class SanBay(db.Model):
    __tablename__ = 'SanBay'
    ma_san_bay = Column(String(10), primary_key=True)
    ten_san_bay = Column(String(50), nullable=False)
    dia_diem = Column(String(50), nullable=False)
    ma_khu_vuc = Column(String(10), ForeignKey(KhuVuc.ma_khu_vuc), nullable=False)

    # # Các tuyến bay liên kết với sân bay này
    # tuyen_bay = relationship('TuyenBay', backref='SanBay')

    san_bay_trung_gian = relationship('SanBayTrungGian', backref='SanBay')

    def __init__(self, ma_san_bay, ten_san_bay, dia_diem, ma_khu_vuc):
        self.ma_san_bay = ma_san_bay
        self.ten_san_bay = ten_san_bay
        self.dia_diem = dia_diem
        self.ma_khu_vuc = ma_khu_vuc


class TuyenBay(db.Model):
    __tablename__ = 'TuyenBay'
    ma_tuyen_bay = Column(String(10), primary_key=True)

    san_bay_den = Column(String(10), ForeignKey(SanBay.ma_san_bay), nullable=False)
    san_bay_di = Column(String(10), ForeignKey(SanBay.ma_san_bay), nullable=False)
    san_bay_den_ref = db.relationship('SanBay', backref='tuyen_bay_den', uselist=False, foreign_keys=[san_bay_den])
    san_bay_di_ref = db.relationship('SanBay', backref='tuyen_bay_di', uselist=False, foreign_keys=[san_bay_di])

    san_bay_trung_gian = relationship('SanBayTrungGian', backref='TuyenBay')

    def __init__(self, ma_tuyen_bay, san_bay_den, san_bay_di):
        self.ma_tuyen_bay = ma_tuyen_bay
        self.san_bay_den = san_bay_den
        self.san_bay_di = san_bay_di

class SanBayTrungGian(db.Model):
    __tablename__ = 'SanBayTrungGian'
    ma_san_bay = Column(String(10), ForeignKey(SanBay.ma_san_bay), primary_key=True)
    ma_tuyen_bay = Column(String(10), ForeignKey(TuyenBay.ma_tuyen_bay), primary_key=True)
    ma_chuyen_bay = Column(String(10), ForeignKey('ChuyenBay.ma_chuyen_bay'), nullable=False)  # Thêm cột này
    thoi_gian_dung_chan = Column(DateTime, nullable=True)
    thoi_gian_tiep_tuc = Column(DateTime, nullable=True)
    thu_tu = Column(Integer, nullable=False)
    ghi_chu = Column(String(200), nullable=True)

    chuyen_bay = relationship('ChuyenBay', back_populates='san_bay_trung_gian')  # Thiết lập quan hệ



class ChuyenBay(db.Model):
    __tablename__ = 'ChuyenBay'
    ma_chuyen_bay = Column(String(10), primary_key=True)
    may_bay = Column(String(10), ForeignKey(MayBay.so_hieu_mb), nullable=False)
    tuyen_bay = Column(String(10), ForeignKey(TuyenBay.ma_tuyen_bay), nullable=False)
    lich_bay = Column(String(10), ForeignKey(LichBay.ma_LB), nullable=False)
    thoi_gian_di = Column(DateTime, nullable=False)
    thoi_gian_den = Column(DateTime, nullable=False)

    chi_tiet_cb = relationship('ChiTietVe', backref='ChuyenBay')
    san_bay_trung_gian = relationship('SanBayTrungGian', back_populates='chuyen_bay', cascade='all, delete-orphan')  # Thiết lập quan hệ

    def __init__(self, ma_chuyen_bay, may_bay, tuyen_bay, lich_bay, gia_chuyen_bay, thoi_gian_di, thoi_gian_den):
        self.ma_chuyen_bay = ma_chuyen_bay
        self.may_bay = may_bay
        self.tuyen_bay = tuyen_bay
        self.lich_bay = lich_bay
        self.gia_chuyen_bay = gia_chuyen_bay
        self.thoi_gian_di = thoi_gian_di
        self.thoi_gian_den = thoi_gian_den

class ChiTietVe(db.Model):
    __tablename__ = 'ChiTietVe'
    ma_chuyen_bay = Column(String(10), ForeignKey(ChuyenBay.ma_chuyen_bay), primary_key=True)
    ma_ve = Column(String(10), ForeignKey(Ve.ma_ve), primary_key=True)


class ThanhToan(db.Model):
    __tablename__ = 'ThanhToan'
    ma_TT = Column(String(10), primary_key=True)
    ma_DH = Column(String(10), ForeignKey(DonHang.ma_DH), primary_key=True, nullable=False)
    phuong_thuc = Column(String(50))
    so_tien = Column(Float, primary_key=True, nullable=False)
    ngay_TT = Column(DateTime, default=func.now())


if __name__ == '__main__':
    with app.app_context():
        # Xóa tất cả dữ liệu trong cơ sở dữ liệu
        # db.drop_all()
        # Tái tạo các bảng nếu cần
        db.create_all()
