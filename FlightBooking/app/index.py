import math
#from crypt import methods

from passlib.hash import md5_crypt as md5

from flask import render_template, request, redirect, jsonify, url_for, session, flash
from numpy.f2py.symbolic import ewarn
from datetime import datetime
import dao
from app import app, login, google, db
from flask_login import login_user, login_required, logout_user, current_user
from app.models import TaiKhoan, VaiTro, SanBay


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['get', 'post'])
def register_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if dao.is_username_exists(username):
            err_msg = 'Tài khoản này đã được tạo. Vui lòng tạo tài khoản khác.'
        elif not password.__eq__(confirm):
            err_msg = 'Mật khẩu không khớp!'
        else:
            data = request.form.copy()
            del data['confirm']
            dao.add_user(**data)

            return redirect('/login')

    return render_template('register.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def login_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        # Sử dụng hàm auth_user để xác thực
        user = dao.auth_user(username, password)
        if user:
            login_user(user=user)
            if user.vai_tro == VaiTro.USER:
                return redirect('/')
            elif user.vai_tro == VaiTro.EMPLOYEE:
                return redirect('/page/sellticket')
            else:
                pass
        else:
            # Kiểm tra nếu tài khoản tồn tại
            if dao.is_username_exists(username):
                err_msg = 'Mật khẩu không đúng. Vui lòng thử lại.'
            else:
                err_msg = 'Tài khoản không tồn tại.'

    return render_template('login.html', err_msg=err_msg)




# Gọi đăng nhập Google
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/callback')
def google_callback():
    try:
        # Lấy token từ Google
        token = google.authorize_access_token()

        # Lấy thông tin người dùng từ Google

        user_info = google.get('userinfo').json()

        # Trích xuất thông tin cần thiết
        email = user_info.get('email')
        name = user_info.get('name', email)  # Nếu 'name' không có, dùng email làm mặc định

        # first_name hoặc last_name tách từ name
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Thêm hoặc lấy người dùng từ cơ sở dữ liệu
        user = dao.add_or_get_user_from_google(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email
        )

        if user:
            login_user(user=user)  # Đăng nhập người dùng
            return redirect('/')  # Chuyển hướng về trang chủ
        else:
            raise Exception("Người dùng không hợp lệ hoặc không được tạo thành công.")
    except Exception as e:
        print(f"Lỗi khi xử lý đăng nhập Google: {e}")
        return redirect('/login')


@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


# Gọi page profile
@app.route('/profile')
def profile():
    return render_template('profile.html')  # Chỉ định template `profile.html`


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    form_data = {
        'lname': request.form.get('lname'),
        'fname': request.form.get('fname'),
        'ngay_sinh': request.form.get('ngay_sinh'),
        'dia_chi': request.form.get('dia_chi'),
        'so_CCCD': request.form.get('so_CCCD'),
        'so_dien_thoai': request.form.get('so_dien_thoai'),
        'email': request.form.get('email')
    }


    # Xác thực dữ liệu
    valid, error_message = dao.validate_profile_data(form_data)
    if not valid:
        flash(error_message, 'danger')  # Flash thông báo lỗi
        return redirect(url_for('profile'))

    try:
        ngay_sinh_date = datetime.strptime(form_data['ngay_sinh'], '%d/%m/%Y') if form_data['ngay_sinh'] else None
        success = dao.update_user_profile(
            user_id=current_user.id,
            fname=form_data['fname'],
            lname=form_data['lname'],
            ngay_sinh=ngay_sinh_date,
            dia_chi=form_data['dia_chi'],
            so_CCCD=form_data['so_CCCD'],
            so_dien_thoai=form_data['so_dien_thoai'],
            email=form_data['email']
        )
        if success:
            flash("Cập nhật thông tin thành công!", "success")
        else:
            flash("Cập nhật thất bại.", "danger")

    except Exception as e:
        flash(f"Có lỗi xảy ra: {e}", "danger")

    return redirect(url_for('profile'))


@app.route('/update-password', methods=['POST'])
@login_required
def update_password_route():
    # Lấy thông tin từ form
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Kiểm tra mật khẩu hiện tại
    if not dao.check_current_password(current_user, current_password):
        flash("Mật khẩu hiện tại không đúng.", "danger")
        return redirect(url_for('profile'))  # Redirect về trang profile sau khi lỗi

    # Kiểm tra mật khẩu mới và xác nhận mật khẩu mới
    if new_password != confirm_password:
        flash("Mật khẩu mới và xác nhận mật khẩu không khớp.", "danger")
        return redirect(url_for('profile'))  # Redirect về trang profile nếu có lỗi

    # Kiểm tra độ dài mật khẩu mới (ví dụ tối thiểu 6 ký tự)
    if len(new_password) < 6:
        flash("Mật khẩu mới phải có ít nhất 6 ký tự.", "danger")
        return redirect(url_for('profile'))  # Redirect về trang profile nếu có lỗi

    # Cập nhật mật khẩu mới trong cơ sở dữ liệu
    try:
        dao.update_password(current_user, new_password)
        flash("Cập nhật mật khẩu thành công!", "success")
    except Exception as e:
        flash(f"Có lỗi xảy ra: {e}", "danger")

    return redirect(url_for('profile'))  # Redirect về trang profile sau khi thành công


#Ham luu du lieu chuyen bay tam thoi
def save_data_flight_temp(flight, name):
    info_flight = session.get(name)
    cleaned_data = flight.replace("datetime.datetime", "datetime")
    flight_update = eval(cleaned_data)  # chuyen chuoi thanh tuple
    if not info_flight:
        info_flight= {}
    info_flight.update({
        "hang_bay": flight_update[0],
        "noi_di": flight_update[1],
        "noi_den": flight_update[2],
        "ngay_di": flight_update[3],
        "ngay_ve": flight_update[4],
        "gia_tien": flight_update[5],
        "so_luong_diem_dung": flight_update[6],
        "ma_chuyen_bay": flight_update[7]
    })
    return info_flight

@app.route('/page/chooseticket', methods=['get','post'])
def choose_ticket():
    app.config["CHOOSE_TICKET_RETURN"] = False
    airlines = dao.load_airline()
    flights = dao.load_flight(session['info']['noi_di'], session['info']['noi_den'], session['info']['ngay_di'], session['info']['so_luong_hanh_khach'][0], app.config["TICKET_CATEGORY"][session['info']['hang_ve']])
    if request.method == "POST":
        flight = request.form.get('flight')
        info_flight_one = save_data_flight_temp(flight, 'info_flight_one')
        session['info_flight_one'] = info_flight_one
        if session['info']['loai_ve'] == "Khứ Hồi":
            return redirect('/page/chooseticketreturn')
        return redirect('/page/booktickets')
    return render_template('Employees/choose_ticket.html', airlines=airlines, flights=flights)



@app.route('/api/searchflights', methods=['get','post'])
def searchflights():
    so_diem_dung = thoi_gian_bay = hang_bay = ''
    if request.method == 'POST':
        so_diem_dung = request.json.get('so_diem_dung')
        thoi_gian_bay = request.json.get('thoi_gian_bay')
        hang_bay = request.json.get('hang_bay')

    flight = session.get('flight')
    if not flight:
        flight = {}
    flight.update({
        "so_diem_dung": so_diem_dung,
        "thoi_gian_bay": thoi_gian_bay,
        "hang_bay": hang_bay
    })
    session["flight"] = flight

    temp_time_flight = 12 if thoi_gian_bay == "Chuyến Bay Sáng" else 6 # Bien de tinh thoi gian

    temp_number_stop = 4 if so_diem_dung == "Số điểm dừng" else app.config["NUMBER_STOP"][so_diem_dung]

    noi_di = session['info']['noi_di'] if app.config["CHOOSE_TICKET_RETURN"] == False else session['info']['noi_den']
    noi_den = session['info']['noi_den'] if app.config["CHOOSE_TICKET_RETURN"] == False else session['info']['noi_di']
    ngay_bay = session['info']['ngay_di'] if app.config["CHOOSE_TICKET_RETURN"] == False else session['info']['ngay_ve']

    flights1 = dao.load_flight_click_search(noi_di, noi_den, ngay_bay,
                                            temp_number_stop, 35 if thoi_gian_bay == "Thời gian bay" else app.config["TIME_FLIGHT"][thoi_gian_bay],
                                            hang_bay, temp_time_flight,app.config["TICKET_CATEGORY"][session['info']['hang_ve']],
                                            session['info']['so_luong_hanh_khach'][0])
    flights = [dict(flight._mapping) for flight in flights1] # mapping là thuôcj tính của đôi tượng row của sqlalchema cho phép chuyển row thành dic
    list_time_flight = []
    list_date_flight = []
    for i in range(0, len(flights)):
        time ={
            "thoi_gian_di": flights[i]['thoi_gian_di'].strftime('%H:%M'),
            'thoi_gian_den': flights[i]['thoi_gian_den'].strftime('%H:%M')
        }
        date = {
            "thoi_gian_di": repr(flights[i]['thoi_gian_di']), # chuyen doi tuong thanh chuoi
            'thoi_gian_den': repr(flights[i]['thoi_gian_den'])
        }
        list_date_flight.append(date)
        list_time_flight.append(time)

    return jsonify({'flights_data': flights, 'list_time_flight': list_time_flight, 'list_date_flight':list_date_flight})

@app.route('/page/chooseticketreturn', methods=['get','post'])
def choose_ticket_return():
    app.config["CHOOSE_TICKET_RETURN"] = True
    airlines = dao.load_airline()
    flights = dao.load_flight(session['info']['noi_den'], session['info']['noi_di'], session['info']['ngay_ve'],
                              session['info']['so_luong_hanh_khach'][0],
                              app.config["TICKET_CATEGORY"][session['info']['hang_ve']])

    if request.method == "POST":
        flight = request.form.get('flight')
        info_flight_two = save_data_flight_temp(flight, 'info_flight_two')
        session['info_flight_two'] = info_flight_two
        return redirect('/page/booktickets')

    return render_template('Employees/choose_ticket_return.html', airlines=airlines, flights=flights)


@app.route('/page/booktickets', methods=['get'])
def book_tickets():
    list_alphabet = app.config["LIST_ALPHABET"]
    print(session['info_flight_one']['ma_chuyen_bay'])
    quantity_chair = dao.load_quantity_chair(session['info_flight_one']['ma_chuyen_bay'])
    print(quantity_chair)
    return render_template('Employees/book_tickets.html',  list_alphabet=list_alphabet, quantity = int(session['info']['so_luong_hanh_khach'][0]))

#Hủy vé
@app.route('/page/cancelticket', methods=['get'])
def cancel_tickets():

    return render_template('Employees/cancel_tickets.html')


#Đổi vé
@app.route('/page/changeticket', methods=['get'])
def change_tickets():

    return render_template('Employees/change_ticket.html')


# Lập lịch
@app.route('/page/schedule', methods=['get'])
def schedule_flight():

    return render_template('Employees/schedule.html')


#Xuất vé
@app.route('/page/printticket', methods=['get'])
def print_ticket():

    return render_template('Employees/print_ticket.html')


#Bán vé
@app.route('/page/sellticket', methods=['get', 'post'])
def sell_ticket():
    time_now = datetime.today()
    airports = dao.load_airport()
    areas = dao.load_area()
    err_msg = ''
    if request.method == 'POST':
        fromInput = request.form.get('fromInput')
        toInput = request.form.get('toInput')
        if fromInput != toInput and fromInput != '' and toInput != '':
            return redirect('/page/chooseticket')
        else:
            err_msg = 'Dữ liệu không đúng'
    return render_template('Employees/sell_ticket.html', time_now=time_now.strftime('%Y-%m-%d'), airports=airports, areas=areas, err_msg=err_msg)


#Lấy dữ liệu trang sell_ticket lưu tạm thời
@app.route('/api/sellticket', methods=['post'])
def sell_ticket_session():
    info = session.get('info')
    if not info:
        info = {}

    loai_ve = request.json.get('loai_ve')
    so_luong_hanh_khach = request.json.get('so_luong_hanh_khach')
    hang_ve = request.json.get('hang_ve')
    noi_di = request.json.get('noi_di')
    noi_den = request.json.get('noi_den')
    ngay_di = request.json.get('ngay_di')
    ngay_ve = request.json.get('ngay_ve')

    info.update({
        "loai_ve": loai_ve,
        "so_luong_hanh_khach": so_luong_hanh_khach,
        "hang_ve": hang_ve,
        "noi_di": noi_di,
        "noi_den": noi_den,
        "ngay_di": ngay_di,
        "ngay_ve": ngay_ve
    })
    session['info'] = info
    return jsonify(info)


#Thanh Toán
@app.route('/page/paytickets', methods=['get'])
def pay_ticket():

    return render_template('Employees/pay_tickets.html')

if __name__ == '__main__':
    app.run(debug=True)
