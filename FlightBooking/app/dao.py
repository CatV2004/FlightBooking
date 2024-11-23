from datetime import datetime
from app.models import TaiKhoan, NguoiDung, Admin, KhachHang, NhanVien
from app import app, db
import hashlib
from werkzeug.security import check_password_hash
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


# Hàm băm mật khẩu mới
def hash_password(password):
    # Băm mật khẩu sử dụng MD5
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def add_user(first_name, last_name, username, password, email, extra_info=None):
    try:
        # Mã hóa mật khẩu
        # password = hashlib.md5(password.encode('utf-8')).hexdigest()
        password = hash_password(password)

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
    # password = hashlib.md5(password.encode('utf-8')).hexdigest()
    password = hash_password(password)

    # Kiểm tra tài khoản và mật khẩu
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username, TaiKhoan.mat_khau == password).first()


def get_user_by_id(user_id):
    return db.session.query(TaiKhoan).join(NguoiDung, TaiKhoan.id == NguoiDung.tai_khoan_id) \
        .filter(TaiKhoan.id == user_id).first()


# Kiểm tra username có tồn tại không
def is_username_exists(username):
    return TaiKhoan.query.filter(TaiKhoan.ten_dang_nhap == username).first() is not None


# Update profile
def update_user_profile(user_id, fname, lname, ngay_sinh, dia_chi, so_CCCD, so_dien_thoai, email):
    try:
        nguoi_dung = NguoiDung.query.filter_by(tai_khoan_id=user_id).first()
        if not nguoi_dung:
            raise ValueError("Không tìm thấy thông tin người dùng.")

        # Cập nhật thông tin
        nguoi_dung.fname = fname
        nguoi_dung.lname = lname
        nguoi_dung.ngay_sinh = ngay_sinh
        nguoi_dung.dia_chi = dia_chi
        nguoi_dung.so_CCCD = so_CCCD
        nguoi_dung.so_dien_thoai = so_dien_thoai
        nguoi_dung.email = email

        db.session.commit()
        return True  # Trả về True khi thành công
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi khi cập nhật: {e}")  # Log lỗi ra console
        return False  # Trả về False khi có lỗi


# Hàm báo kiểm tra và báo lỗi
def validate_profile_data(data):
    if not data['lname'] or not data['fname']:
        return False, "Họ và tên không được để trống."

    if data['ngay_sinh']:
        try:
            datetime.strptime(data['ngay_sinh'], '%d/%m/%Y')
        except ValueError:
            return False, "Ngày sinh không đúng định dạng (dd/mm/yyyy)."

        # Kiểm tra số điện thoại (giả sử là 10 chữ số, bắt đầu từ 0)
        if data.get('so_dien_thoai'):
            phone_pattern = re.compile(r'^(0\d{9})$')  # Biểu thức chính quy cho số điện thoại
            if not phone_pattern.match(data['so_dien_thoai']):
                return False, "Số điện thoại không hợp lệ. Phải là 10 chữ số và bắt đầu bằng 0."

    if data['so_CCCD'] and len(data['so_CCCD']) != 12:
        return False, "Số CCCD phải có đúng 12 ký tự."

    return True, None

# Hàm kiểm tra mật khẩu hiện tại
def check_current_password(user, current_password):
    # Dùng hashlib để băm mật khẩu
    hashed_password = hashlib.md5(current_password.encode('utf-8')).hexdigest()
    return user.mat_khau == hashed_password

# Hàm cập nhật mật khẩu trong cơ sở dữ liệu
def update_password(user, new_password):
    try:
        # Băm mật khẩu mới
        hashed_new_password = hash_password(new_password)
        user.mat_khau = hashed_new_password
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e