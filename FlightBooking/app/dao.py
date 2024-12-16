from datetime import datetime, timedelta
from itertools import groupby

from app.models import TaiKhoan, NguoiDung, Admin, KhachHang, NhanVien, KhuVuc, SanBay, Ghe, HangMayBay, TuyenBay, ChuyenBay, SanBayTrungGian, MayBay
from app import app, db
import hashlib
import cloudinary.uploader
from sqlalchemy.sql import func, or_, and_
from sqlalchemy.orm import aliased


def add_or_get_user_from_google(first_name, last_name, username, email):
    user = TaiKhoan.query.filter_by(ten_dang_nhap=username).first()
    if not user:
        try:
            # Tạo tài khoản người dùng mới
            user_account = TaiKhoan(ten_dang_nhap=username, mat_khau='', trang_thai=True)
            db.session.add(user_account)
            db.session.commit()

            # Thêm người dùng vào bảng KhachHang
            customer = KhachHang(
                fname=first_name,
                lname=last_name,
                email=email,
                tai_khoan_id=user_account.id
            )
            db.session.add(customer)
            db.session.commit()

            # Gán lại `user` với tài khoản vừa tạo
            user = user_account
        except Exception as ex:
            db.session.rollback()
            print(f"Error while adding user: {ex}")
            raise ex

    return user


def add_user(first_name, last_name, username, password, email, extra_info=None):
    try:
        # Mã hóa mật khẩu
        password = hashlib.md5(password.encode('utf-8')).hexdigest()

        # # Tạo đối tượng NguoiDung
        # user = NguoiDung(fname=first_name, lname=last_name, email=email)
        # db.session.add(user)
        # db.session.commit()

        # Sau đó, Tạo tài khoản người dùng liên kết với người dùng
        account = TaiKhoan(ten_dang_nhap=username, mat_khau=password)
        db.session.add(account)
        db.session.commit()

        # Sau đó, tạo bảng KhachHang
        customer = KhachHang(fname=first_name, lname=last_name, email=email, tai_khoan_id=account.id)
        db.session.add(customer)
        db.session.commit()

    except Exception as ex:
        db.session.rollback()
        print(f"Error: {ex}")
        raise ex


def auth_user(username, password):
    # Mã hóa mật khẩu
    password = hashlib.md5(password.encode('utf-8')).hexdigest()

    # Kiểm tra tài khoản và mật khẩu
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username, TaiKhoan.mat_khau == password).first()


def get_user_by_id(user_id):
    return db.session.query(NguoiDung).join(TaiKhoan, TaiKhoan.nguoi_dung_id == NguoiDung.id) \
        .filter(TaiKhoan.id == user_id).first()


# Kiểm tra username có tồn tại không
def is_username_exists(username):
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first() is not None


# load khu vuc
def load_area():
    return KhuVuc.query.all()


# load san bay
def load_airport():
    return SanBay.query.order_by('ma_khu_vuc').all()


# load hang may bay
def load_airline():
    return HangMayBay.query.all()


# Load chuyen bay ban dau de chon
def load_flight(noi_di, noi_den, ngay_bay, so_luong_hanh_khach, hang_ve):
    SanBayDi = aliased(SanBay)
    SanBayDen = aliased(SanBay)
    return (db.session.query(
        HangMayBay.ten_hang,
        SanBayDi.dia_diem.label("noi_di"),
        SanBayDen.dia_diem.label("noi_den"),
        ChuyenBay.thoi_gian_di,
        ChuyenBay.thoi_gian_den,
        ChuyenBay.gia_chuyen_bay,
        func.count(func.distinct(SanBayTrungGian.ma_tuyen_bay)).label("diem_dung"),
        ChuyenBay.ma_chuyen_bay
    ).join(
        MayBay, MayBay.hang_may_bay_ID == HangMayBay.so_hieu_hangmb
    ).join(
        ChuyenBay, ChuyenBay.may_bay == MayBay.so_hieu_mb
    ).join(
        TuyenBay, TuyenBay.ma_tuyen_bay == ChuyenBay.tuyen_bay
    ).join(
        SanBayDi, SanBayDi.ma_san_bay == TuyenBay.san_bay_di
    ).join(
        SanBayDen, SanBayDen.ma_san_bay == TuyenBay.san_bay_den
    ).join(
        Ghe, MayBay.so_hieu_mb == Ghe.may_bay
    ).outerjoin(
        SanBayTrungGian, SanBayTrungGian.ma_chuyen_bay == ChuyenBay.ma_chuyen_bay
    ).filter(SanBayDi.dia_diem == noi_di,
        SanBayDen.dia_diem == noi_den,
        func.date(ChuyenBay.thoi_gian_di) == ngay_bay,
        ChuyenBay.thoi_gian_di >= app.config["TIME_NOW"] + timedelta(hours=4),
        Ghe.trang_thai == 0,
        Ghe.hang_ve == hang_ve
    ).group_by(
        HangMayBay.ten_hang, SanBayDi.dia_diem,
        SanBayDen.dia_diem, ChuyenBay.thoi_gian_di,
        ChuyenBay.thoi_gian_den, ChuyenBay.gia_chuyen_bay,ChuyenBay.ma_chuyen_bay
    ).having(func.count(Ghe.ma_ghe) >= so_luong_hanh_khach).all())


# Load chuyen bay sau khi nhan nut tim de chon
def load_flight_click_search(noi_di, noi_den, ngay_bay, so_diem_dung, thoi_gian_bay, hang_bay, temp_time_flight, hang_ve, so_luong_hanh_khach):
    SanBayDi = aliased(SanBay)
    SanBayDen = aliased(SanBay)
    return (db.session.query(
        HangMayBay.ten_hang,
        SanBayDi.dia_diem.label("noi_di"),
        SanBayDen.dia_diem.label("noi_den"),
        ChuyenBay.thoi_gian_di,
        ChuyenBay.thoi_gian_den,
        ChuyenBay.gia_chuyen_bay,
        func.count(func.distinct(SanBayTrungGian.ma_tuyen_bay)).label("diem_dung"),
        ChuyenBay.ma_chuyen_bay
    ).join(
        MayBay, MayBay.hang_may_bay_ID == HangMayBay.so_hieu_hangmb
    ).join(
        ChuyenBay, ChuyenBay.may_bay == MayBay.so_hieu_mb
    ).join(
        TuyenBay, TuyenBay.ma_tuyen_bay == ChuyenBay.tuyen_bay
    ).join(
        SanBayDi, SanBayDi.ma_san_bay == TuyenBay.san_bay_di
    ).join(
        SanBayDen, SanBayDen.ma_san_bay == TuyenBay.san_bay_den
    ).join(
        Ghe, MayBay.so_hieu_mb == Ghe.may_bay
    ).outerjoin(
        SanBayTrungGian, SanBayTrungGian.ma_chuyen_bay == ChuyenBay.ma_chuyen_bay
    ).filter(SanBayDi.dia_diem == noi_di,
             SanBayDen.dia_diem == noi_den,
             func.date(ChuyenBay.thoi_gian_di) == ngay_bay,
             or_(hang_bay == "Hãng Bay", HangMayBay.ten_hang == hang_bay),
             or_(thoi_gian_bay == 35, and_(func.hour(ChuyenBay.thoi_gian_di) < thoi_gian_bay, func.hour(ChuyenBay.thoi_gian_di) >= thoi_gian_bay - temp_time_flight)),
             ChuyenBay.thoi_gian_di >= app.config["TIME_NOW"] + timedelta(hours=4),
             Ghe.trang_thai == 0,
             Ghe.hang_ve == hang_ve
    ).group_by(HangMayBay.ten_hang, ChuyenBay.thoi_gian_di, ChuyenBay.thoi_gian_den,
               ChuyenBay.gia_chuyen_bay, SanBayDi.dia_diem, SanBayDen.dia_diem, ChuyenBay.ma_chuyen_bay
    ).having(and_(so_diem_dung == 0, func.count(SanBayTrungGian.ma_chuyen_bay) == 0
        ) if so_diem_dung == 0 else or_(
            func.count(func.distinct(SanBayTrungGian.ma_tuyen_bay)) == so_diem_dung,
            and_(
                so_diem_dung == 4,
                func.count(SanBayTrungGian.ma_chuyen_bay) != so_diem_dung
            )
        ),
        func.count(Ghe.ma_ghe) >= so_luong_hanh_khach
    ).all())


#Ham load so luong ghe cua mot chuyen
def load_quantity_chair(chuyen_bay):
    return db.session.query(
        func.count(Ghe.ma_ghe).label('so_luong_ghe')
    ).select_from(ChuyenBay  # Xác định bảng gốc là ChuyenBay
    ).join(
        MayBay, ChuyenBay.may_bay == MayBay.so_hieu_mb
    ).join(
        Ghe, Ghe.may_bay == MayBay.so_hieu_mb
    ).filter(
        ChuyenBay.ma_chuyen_bay == chuyen_bay
    )


#Ham load ghế
def load_chair(chuyen_bay):
    return db.session.query(
        func.sum(Ghe.ma_ghe),

    )