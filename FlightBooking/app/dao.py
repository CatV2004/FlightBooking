from datetime import datetime
from app.models import TaiKhoan, NguoiDung, Admin, KhachHang, NhanVien
from app import app, db
import hashlib
import re
import cloudinary.uploader


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
    return db.session.query(TaiKhoan).join(NguoiDung, TaiKhoan.id == NguoiDung.tai_khoan_id) \
        .filter(TaiKhoan.id == user_id).first()


# Kiểm tra username có tồn tại không
def is_username_exists(username):
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first() is not None


def validate_profile_data(data):
    # Kiểm tra họ và tên
    if not data['lname'] or not data['fname']:
        return False, "Họ và tên không được để trống."

    # Kiểm tra ngày sinh
    if data['ngay_sinh']:
        try:
            datetime.strptime(data['ngay_sinh'], '%d/%m/%Y')
        except ValueError:
            return False, "Ngày sinh không đúng định dạng (dd/mm/yyyy)."

    # Kiểm tra số CCCD
    if data['so_CCCD'] and len(data['so_CCCD']) != 12:
        return False, "Số CCCD phải có đúng 12 ký tự."

    # Kiểm tra số điện thoại (bắt đầu từ 0 và 10 chữ số)
    if data.get('so_dien_thoai'):
        if not re.match(r'^0\d{9}$', data['so_dien_thoai']):
            return False, "Số điện thoại không hợp lệ. Phải là 10 chữ số và bắt đầu bằng 0."

    # Kiểm tra email
    if data['email']:
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
            return False, "Email không hợp lệ."

    return True, None


def update_user_profile(user_id, fname, lname, ngay_sinh, dia_chi, so_CCCD, so_dien_thoai, email):
    try:
        # Lấy người dùng thông qua `tai_khoan_id`
        user = NguoiDung.query.filter_by(tai_khoan_id=user_id).first()

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
    except Exception as ex:
        db.session.rollback()
        print(f"Error updating user profile: {ex}")
        raise ex


def check_current_password(user, current_password):
    hashed_password = hashlib.md5(current_password.encode('utf-8')).hexdigest()
    return user.mat_khau == hashed_password


def update_password(user, new_password):
    try:
        hashed_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        user.mat_khau = hashed_password
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(f"Error updating password: {ex}")
        raise ex


