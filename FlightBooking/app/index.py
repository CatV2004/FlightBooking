import math

from flask import render_template, request, redirect, jsonify, url_for, session
from numpy.f2py.symbolic import ewarn

import dao
from app import app, login, google
from flask_login import login_user, logout_user

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['get', 'post'])
def register_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
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
            del data['email']
            dao.add_user(**data)

            return redirect('/login')

    return render_template('register.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def login_view():
    err_msg =''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        # Sử dụng hàm auth_user để xác thực
        user = dao.auth_user(username, password)
        if user:
            login_user(user=user)
            return redirect('/')
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
        token = google.authorize_access_token()
        user_info = google.get('userinfo').json()

        # Lấy thông tin người dùng từ Google
        email = user_info['email']
        name = user_info.get('name', email)

        # Thêm hoặc lấy người dùng từ cơ sở dữ liệu
        user = dao.add_or_get_user_from_google(name=name, username=email)

        # Đăng nhập người dùng
        login_user(user=user)
        return redirect('/')
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





if __name__ == '__main__':
    app.run(debug=True)
