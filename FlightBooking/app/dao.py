from datetime import datetime, timedelta
from itertools import groupby

from app.models import TaiKhoan, NguoiDung, Admin, KhachHang, NhanVien, KhuVuc, SanBay, Ghe, HangMayBay, TuyenBay, ChuyenBay, SanBayTrungGian, MayBay

from app import app, db
import hashlib
import cloudinary.uploader
from sqlalchemy.sql import func, or_, and_
from sqlalchemy.orm import aliased


def add_or_get_user_from_google(first_name, last_name, username, email):
    user_account = TaiKhoan.query.filter_by(ten_dang_nhap=username).first()
    if not user_account:
        try:
            # Tạo đối tượng NguoiDung
            customer = KhachHang(fname=first_name, lname=last_name, email=email)
            db.session.add(customer)
            db.session.commit()

            # Sau đó, Tạo đối tượng tài khoản người dùng liên kết với người dùng
            account = TaiKhoan(ten_dang_nhap=username, mat_khau="", nguoi_dung_id=customer.id, trang_thai=True)
            db.session.add(account)
            db.session.commit()

            # Gán lại `user` với tài khoản vừa tạo
            user_account = customer

        except Exception as ex:
            db.session.rollback()
            print(f"Error while adding user: {ex}")
            raise ex
    else:
        # Nếu tài khoản đã tồn tại, lấy đối tượng NguoiDung từ TaiKhoan
        user_account = NguoiDung.query.get(user_account.nguoi_dung_id)

    return user_account



def add_user(first_name, last_name, username, password, email):
    try:
        # Mã hóa mật khẩu
        password = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Tạo đối tượng NguoiDung
        customer = KhachHang(fname=first_name, lname=last_name, email=email)
        db.session.add(customer)
        db.session.commit()

        # Sau đó, Tạo đối tượng tài khoản người dùng liên kết với người dùng
        account = TaiKhoan(ten_dang_nhap=username, mat_khau=password, nguoi_dung_id = customer.id)
        db.session.add(account)
        db.session.commit()

        # # Sau đó, tạo đối tượng KhachHang
        # customer = KhachHang(id=user.id, hang_thanh_vien=HangThanhVien.BAC)
        # db.session.add(customer)
        # db.session.commit()

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
        .filter(NguoiDung.id == user_id).first()


# Kiểm tra username có tồn tại không
def is_username_exists(username):
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first() is not None


# load khu vuc
def load_area():
    return KhuVuc.query.all()



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
def update_user_profile(user_id, fname, lname, ngay_sinh, dia_chi, so_CCCD, so_dien_thoai, email):
    try:
        # Lấy người dùng thông qua `nguoi_dung_id` trong bảng TaiKhoan
        user_account = TaiKhoan.query.filter_by(id=user_id).first()

        if user_account and user_account.nguoi_dung_id:
            # Lấy thông tin người dùng từ bảng NguoiDung
            user = NguoiDung.query.filter_by(id=user_account.nguoi_dung_id).first()

            if user:
                # Cập nhật thông tin cá nhân
                user.fname = fname
                user.lname = lname
                user.ngay_sinh = ngay_sinh
                user.dia_chi = dia_chi
                user.so_CCCD = so_CCCD
                user.so_dien_thoai = so_dien_thoai
                user.email = email

                # Lưu thay đổi vào database
                db.session.commit()
                return True
            else:
                print("Người dùng không tồn tại.")
                return False
        else:
            print("Tài khoản không tồn tại hoặc không liên kết với người dùng.")
            return False
    except Exception as ex:
        db.session.rollback()
        print(f"Error updating user profile: {ex}")
        raise ex



def check_current_password(user, current_password):
    hashed_password = hashlib.md5(current_password.encode('utf-8')).hexdigest()
    return user.tai_khoan.mat_khau == hashed_password


def update_password(user, new_password):
    try:
        hashed_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        user.tai_khoan.mat_khau = hashed_password
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(f"Error updating password: {ex}")
        raise ex

