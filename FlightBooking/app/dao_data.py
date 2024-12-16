from app import db
from app.models import ChiTietVe, HanhLy, Ve, DonHang, NguoiDung
from datetime import datetime

# Hàm thêm Chi Tiết Chuyến Bay vào database
def add_chi_tiet_chuyen_bay(ma_chuyen_bay, ma_san_bay, thoi_gian_dung, san_bay_den, chi_phi):
    try:
        chi_tiet_chuyen_bay = ChiTietVe(
            ma_chuyen_bay=ma_chuyen_bay,
            ma_san_bay=ma_san_bay,
            thoi_gian_dung=thoi_gian_dung,
            san_bay_den=san_bay_den,
            chi_phi=chi_phi
        )
        db.session.add(chi_tiet_chuyen_bay)
        db.session.commit()
        return chi_tiet_chuyen_bay
    except Exception as e:
        db.session.rollback()
        print(f"Error adding ChiTietChuyenBay: {e}")
        return None

# Hàm thêm Hành Lý vào database
def add_hanh_ly(ma_ve, loai_hanh_ly, trong_luong):
    try:
        hanh_ly = HanhLy(
            ma_ve=ma_ve,
            loai_hanh_ly=loai_hanh_ly,
            trong_luong=trong_luong
        )
        db.session.add(hanh_ly)
        db.session.commit()
        return hanh_ly
    except Exception as e:
        db.session.rollback()
        print(f"Error adding HanhLy: {e}")
        return None

# Hàm thêm Vé vào database
def add_ve(ma_ve, ma_chuyen_bay, ma_ghe, gia_ve, loai_ve, hạng_ve):
    try:
        ve = Ve(
            ma_ve=ma_ve,
            ma_chuyen_bay=ma_chuyen_bay,
            ma_ghe=ma_ghe,
            gia_ve=gia_ve,
            loai_ve=loai_ve,
            hang_ve=hạng_ve
        )
        db.session.add(ve)
        db.session.commit()
        return ve
    except Exception as e:
        db.session.rollback()
        print(f"Error adding Ve: {e}")
        return None

# Hàm thêm Đơn Hàng vào database
def add_don_hang(ma_don_hang, ma_khuyen_mai, ma_nhan_vien, so_luong_ve, tong_tien, ngay_dat, trang_thai):
    try:
        don_hang = DonHang(
            ma_don_hang=ma_don_hang,
            ma_khuyen_mai=ma_khuyen_mai,
            ma_nhan_vien=ma_nhan_vien,
            so_luong_ve=so_luong_ve,
            tong_tien=tong_tien,
            ngay_dat=ngay_dat,
            trang_thai=trang_thai
        )
        db.session.add(don_hang)
        db.session.commit()
        return don_hang
    except Exception as e:
        db.session.rollback()
        print(f"Error adding DonHang: {e}")
        return None

# Hàm thêm Người Dùng vào database
def add_nguoi_dung(ho, ten, dia_chi, email, so_dien_thoai, ngay_sinh, so_cccd, loai_nguoi_dung):
    try:
        nguoi_dung = NguoiDung(
            ho=ho,
            ten=ten,
            dia_chi=dia_chi,
            email=email,
            so_dien_thoai=so_dien_thoai,
            ngay_sinh=ngay_sinh,
            so_cccd=so_cccd,
            loai_nguoi_dung=loai_nguoi_dung
        )
        db.session.add(nguoi_dung)
        db.session.commit()
        return nguoi_dung
    except Exception as e:
        db.session.rollback()
        print(f"Error adding NguoiDung: {e}")
        return None
