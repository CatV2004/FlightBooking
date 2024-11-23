from datetime import timedelta
from multiprocessing.reduction import duplicate

from cloudinary.utils import unique
from pycparser import CParser
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, Date, column, nullsfirst, DateTime
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


class LoaiVe(RoleEnum):
    MOTCHIEU = 1
    KHUHOI = 2

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'TaiKhoan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_dang_nhap = Column(String(50), nullable=False, unique=True)
    mat_khau = Column(String(100), nullable=False)
    trang_thai = Column(db.Boolean, default=True)
    vai_tro = Column(Enum(VaiTro), default=VaiTro.USER, nullable=False)
    nguoi_dung = relationship("NguoiDung", backref='TaiKhoan', uselist=False)

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
    tai_khoan_id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=True)

    def __str__(self):
        return self.lname

class Admin(NguoiDung, UserMixin):
    __tablename__ = 'Admin'
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    ngay_vao_lam = Column(Date)
    kinh_nghiem = Column(String(200))

    __mapper_args__ = {
        'inherit_condition': id == TaiKhoan.id
    }


class KhachHang(NguoiDung, UserMixin):
    __tablename__ = 'KhachHang'
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    hang_thanh_vien = Column(Enum(HangThanhVien), default=HangThanhVien.BAC, nullable=False)
    don_hang = relationship('DonHang', backref='KhachHang')

    __mapper_args__ = {
        'inherit_condition': id == TaiKhoan.id
    }


class NhanVien(NguoiDung, UserMixin):
    __tablename__ = 'NhanVien'
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    luong = Column(Float, nullable=False)
    ngay_vao_lam = Column(Date, nullable=False)
    ghi_chu = Column(String(200))
    don_hang = relationship('DonHang', backref='NhanVien')

    __mapper_args__ = {
        'inherit_condition': id == TaiKhoan.id
    }


class HangMayBay(db.Model):
    __tablename__ = 'HangMayBay'
    so_hieu_hangmb = Column(String(10), primary_key=True)
    ten_hang = Column(String(50), nullable=False)
    may_bay = relationship("MayBay", backref='HangMayBay')

    def __str__(self):
        return self.ten_hang


class MayBay(db.Model):
    __tablename__ = 'MayBay'
    so_hieu_mb = Column(String(10), primary_key=True)
    so_ghe_trong = Column(Integer, nullable=True)  # Số ghế trống
    hang_may_bay_ID = Column(String(10), ForeignKey(HangMayBay.so_hieu_hangmb), nullable=False)
    ghe = relationship('Ghe', backref='MayBay')
    chuyen_bay = relationship('ChuyenBay', backref='MayBay')


class HanhLy(db.Model):
    __tablename__ = 'HanhLy'
    ma_HL = Column(String(10), primary_key=True)
    loai_HL = Column(String(20), nullable=True)
    trong_luong = Column(Integer, nullable=False)
    chi_phi = Column(Float, nullable=False)
    ve = relationship("Ve", backref='HanhLy', uselist=False)


class KhuyenMai(db.Model):
    __tablename__ = 'KhuyenMai'
    ma_KM = Column(String(10), primary_key=True)
    mo_ta = Column(String(50), nullable=True)
    ty_le_giam = Column(Float, nullable=False)
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)
    ve = relationship('Ve', backref='KhuyenMai')
    dieu_kien_KM = relationship('DieuKienKM', backref='KhuyenMai')


class DieuKienKM(db.Model):
    __tablename__ = 'DieuKienKM'
    ma_DK = Column(String(10), primary_key=True)
    noi_dung = Column(String(200), nullable=True)
    ghi_chu = Column(String(200), nullable=True)
    khuyen_mai_id = Column(String(10), ForeignKey(KhuyenMai.ma_KM), nullable=False)


# class ChiTietKM(db.Model):

class Ghe(db.Model):
    __tablename__ = 'Ghe'
    ma_ghe = Column(String(10), primary_key=True)
    hang_ve = Column(Enum(HangVe), default=HangVe.PHOTHONG, nullable=False)
    may_bay = Column(String(10), ForeignKey(MayBay.so_hieu_mb), nullable=False)
    ve = relationship('Ve', backref='Ghe')


class DonHang(db.Model):
    __tablename__ = 'DonHang'
    ma_DH = Column(String(10), primary_key=True)
    khach_hang = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    nhan_vien = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    ngay_dat_DH = Column(DateTime, nullable=False, default=func.now())
    ve = relationship('Ve', backref='DonHang')
    thanh_toan = relationship('ThanhToan', backref='DonHang')


class Ve(db.Model):
    __tablename__ = 'Ve'
    ma_ve = Column(String(10), primary_key=True)
    ma_don_hang = Column(String(10), ForeignKey(DonHang.ma_DH), nullable=False)
    ngay_xuat_ve = Column(DateTime, nullable=True)
    loai_ve = Column(Enum(LoaiVe), default=LoaiVe.MOTCHIEU, nullable=False)
    ma_KM = Column(String(10), ForeignKey(KhuyenMai.ma_KM), nullable=True)
    ma_HL = Column(String(10), ForeignKey(HanhLy.ma_HL), nullable=True)
    gia_ve = Column(Float, nullable=False)
    chi_tiet_cb = relationship('ChiTietChuyenBay', backref='Ve')
    ghe = Column(String(10), ForeignKey(Ghe.ma_ghe), nullable=False)


class LichBay(db.Model):
    __tablename__ = 'LichBay'
    ma_LB = Column(String(10), primary_key=True)
    chuyen_bay = relationship('ChuyenBay', backref='LichBay')
    ngay_lap_lich = Column(Date, nullable=True)


class SanBay(db.Model):
    __tablename__ = 'SanBay'
    ma_san_bay = Column(String(10), primary_key=True)
    dia_diem = Column(String(50), nullable=False)

    # # Các tuyến bay liên kết với sân bay này
    # tuyen_bay = relationship('TuyenBay', backref='SanBay')

    san_bay_trung_gian = relationship('SanBayTrungGian', backref='SanBay')


class TuyenBay(db.Model):
    __tablename__ = 'TuyenBay'
    ma_tuyen_bay = Column(String(10), primary_key=True)

    san_bay_den = Column(String(10), ForeignKey(SanBay.ma_san_bay), nullable=False)
    san_bay_di = Column(String(10), ForeignKey(SanBay.ma_san_bay), nullable=False)
    san_bay_den_ref = db.relationship('SanBay', backref='tuyen_bay_den', uselist=False, foreign_keys=[san_bay_den])
    san_bay_di_ref = db.relationship('SanBay', backref='tuyen_bay_di', uselist=False, foreign_keys=[san_bay_di])

    san_bay_trung_gian = relationship('SanBayTrungGian', backref='TuyenBay')


class SanBayTrungGian(db.Model):
    __tablename__ = 'SanBayTrungGian'
    ma_san_bay = Column(String(10), ForeignKey(SanBay.ma_san_bay), primary_key=True)
    ma_tuyen_bay = Column(String(10), ForeignKey(TuyenBay.ma_tuyen_bay), primary_key=True)
    thoi_gian_su_dung = Column(Float, nullable=True)
    ghi_chu = Column(String(200), nullable=True)


class BaoCao(db.Model):
    __tablename__ = 'BaoCao'
    ma_bao_cao = Column(String(10), primary_key=True)
    ngay_bao_cao = Column(Date, nullable=True)
    tong_doanh_thu = Column(Float, nullable=False)


class ChiTietBaoCao(db.Model):
    __tablename__ = 'ChiTietBaoCao'
    ma_bao_cao = Column(String(10), ForeignKey(BaoCao.ma_bao_cao), primary_key=True)
    ma_tuyen_bay = Column(String(10), ForeignKey(TuyenBay.ma_tuyen_bay), primary_key=True)
    ty_le = Column(String(10))


class ChuyenBay(db.Model):
    __tablename__ = 'ChuyenBay'
    ma_chuyen_bay = Column(String(10), primary_key=True)
    may_bay = Column(String(10), ForeignKey(MayBay.so_hieu_mb), nullable=False)
    tuyen_bay = Column(String(10), ForeignKey(TuyenBay.ma_tuyen_bay), nullable=False)
    lich_bay = Column(String(10), ForeignKey(LichBay.ma_LB), nullable=False)
    gia_chuyen_bay = Column(Float, nullable=False)
    thoi_gian_di = Column(DateTime, nullable=False)
    thoi_gian_den = Column(DateTime, nullable=False)
    chi_tiet_cb = relationship('ChiTietChuyenBay', backref='ChuyenBay')


class ChiTietChuyenBay(db.Model):
    __tablename__ = 'ChiTietChuyenBay'
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
        db.drop_all()
        # Tái tạo các bảng nếu cần
        db.create_all()

