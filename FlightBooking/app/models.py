from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql.operators import truediv

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
class vaiTro(RoleEnum):
    ADMIN = 1
    USER = 2
    EMPLOYEE = 3


class NguoiDung(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    fname = Column(String(50), nullable=False)
    lname = Column(String(50), nullable=False)
    soCCCD = Column(String(12), nullable=True)
    diaChi = Column(String(100), nullable=True)
    email = Column(String(50), nullable=False)
    soDienThoai = Column(String(15), nullable=True)
    ngaySinh = Column(DATETIME, nullable=True)
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), nullable=False, unique=True)
    tai_khoan = relationship('TaiKhoan', back_populates='nguoi_dung')

class TaiKhoan(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenDangNhap = Column(String(50), nullable=False)
    matKhau = Column(String(50), nullable=False)
    trangThai = Column(Boolean, default=True)
    vaiTro = Column(Enum(vaiTro), default=vaiTro.USER)
    nguoi_dung = relationship('NguoiDung', back_populates='tai_khoan', uselist=False)

    def get_id(self):
        return self.id

    def set_ngay_sinh(self, ngay_sinh_str):
        try:
            self.ngaySinh = DATETIME.strptime(ngay_sinh_str, '%d/%m/%Y')  # Tự động gán giờ = 00:00:00
        except ValueError:
            raise ValueError("Ngày sinh phải đúng định dạng dd/mm/yyyy")

    def get_ngay_sinh(self):
        return self.ngaySinh.strftime('%d/%m/%Y') if self.ngaySinh else None


class SanBay(db.Model):
    maSanBay = Column(String(10), primary_key=True)
    diaDiem = Column(String(50), nullable=False)

# class TuyenBay()
# if __name__ == '__main__':
#     with app.app_context():
        # db.create_all()

        # u = User(name="admin", username="admin", password=str(hashlib.md5("cuong2004".encode('utf-8')).hexdigest()),
        #          avatar="https://res.cloudinary.com/dohsfqs6d/image/upload/v1731589856/ewqzzku2a2fcczgumnzf.jpg",
        #          user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        # db_sub.create_all()
        # c1 = CategoryPage(name='Trang chủ')
        # c2 = CategoryPage(name='Giới thiệu')
        # c3 = CategoryPage(name='Dịch vụ')
        # c4 = CategoryPage(name='Khuyến mãi')
        # c5 = CategoryPage(name='Liên hệ')
        #
        # db_sub.session.add_all([c1, c2, c3, c4, c5])
        # db_sub.session.commit()
