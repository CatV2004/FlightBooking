from datetime import datetime

from app.models import TaiKhoan, NguoiDung, Admin, KhachHang, NhanVien
from app import app, db
import hashlib
import cloudinary.uploader


def add_or_get_user_from_google(first_name, last_name, username, email):
    # Kiểm tra nếu user đã tồn tại
    user = TaiKhoan.query.filter_by(ten_dang_nhap=username).first()
    if not user:
        try:

            # Tạo đối tượng NguoiDung liên kết với tài khoản
            # user = NguoiDung(fname=first_name, lname=last_name)
            # # Sau đó, Tạo mới tài khoản người dùng nếu không tồn tại
            # account = TaiKhoan(ten_dang_nhap=username, mat_khau="", trang_thai=True, nguoi_dung_id=user.id)
            #
            # db.session.add(user)
            # db.session.add(account)
            # db.session.commit()
            # Nếu tài khoản không tồn tại, tạo mới người dùng và tài khoản
            user = NguoiDung(fname=first_name, lname=last_name, email=email)
            db.session.add(user)
            db.session.commit()

            # # Tạo tài khoản người dùng
            # user_account = TaiKhoan(ten_dang_nhap=username, mat_khau='', nguoi_dung_id=user.id)
            # db.session.add(user_account)
            # db.session.commit()

            # Thêm người dùng vào bảng KhachHang nếu cần
            customer = KhachHang(ten_dang_nhap=username, mat_khau='', nguoi_dung_id=user.id)
            db.session.add(customer)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(f"Error while adding user: {ex}")
            raise ex
    return user


def add_user(first_name, last_name, username, password, email, extra_info=None):
    try:
        # Mã hóa mật khẩu
        password = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Tạo đối tượng NguoiDung
        user = NguoiDung(fname=first_name, lname=last_name, email=email)
        db.session.add(user)
        db.session.commit()

        # # Sau đó, Tạo tài khoản người dùng liên kết với người dùng
        # account = TaiKhoan(ten_dang_nhap=username, mat_khau=password, nguoi_dung_id=user.id)
        # db.session.add(account)
        # db.session.commit()

        # Sau đó, tạo bảng KhachHang
        customer = KhachHang(ten_dang_nhap=username, mat_khau=password, nguoi_dung_id=user.id)
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


def get_user_by_id(id):
    return TaiKhoan.query.get(id)


# Kiểm tra username có tồn tại không
def is_username_exists(username):
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first() is not None
