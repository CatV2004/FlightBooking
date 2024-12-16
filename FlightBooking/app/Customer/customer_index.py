import json
from datetime import datetime

from flask_login import current_user

from .info_passenger import PassengerInfo, Luggage

from flask import Flask, request, jsonify, Blueprint, session, Blueprint, render_template, redirect, url_for, flash, \
    abort
from .customer_dao import find_flights, get_full_flight_info_v2, find_airport_name, find_airport_location, \
    convert_to_datetime, find_route_by_airport_codes, get_airlines_by_flights, format_vietnamese_date, create_passenger
from .customer__init__ import cost_map
from app import app

from ..models import KhuyenMai, KhachHang, HangThanhVien, Ve

# Định nghĩa Blueprint
customer_bp = Blueprint('customer', __name__, template_folder='../templates')


# Định nghĩa filter format_currency
@app.template_filter('format_currency')
def format_currency(value):
    if isinstance(value, (int, float)):
        return f"{value:,.0f}".replace(",", ".") + " VND"
    return value

@app.route('/customer/submit-airport-codes', methods=['POST'])
def submit_airport_codes():
    # Sử dụng từ khóa global để sửa biến toàn cục
    # global from_code, to_code, departure_date_str, return_date, seat_class, ticket_quantity

    # Lấy dữ liệu từ request
    data = request.get_json()

    # Trích xuất mã sân bay và các thông tin cần thiết
    session['from_code'] = data.get('from')
    session['to_code'] = data.get('to')
    session['departure_date_str'] = data.get('departure_date')
    session['round_trip'] = data.get('round_trip')
    session['return_date_str'] = data.get('return_date')
    session['seat_class'] = data.get('seat_class')
    session['ticket_quantity'] = data.get('ticket_quantity')
    session['round_trip'] = data.get('round_trip')

    # Trả về phản hồi cho client
    return jsonify({'success': True, 'message': 'Dữ liệu đã được xử lý thành công'})


@customer_bp.route('/flights_normal', methods=['GET', 'POST'])
def flights_normal():

    # Lấy dữ liệu từ session
    from_code = session.get('from_code')
    to_code = session.get('to_code')
    departure_date_str = session.get('departure_date_str')
    seat_class = session.get('seat_class')
    ticket_quantity = session.get('ticket_quantity')
    round_trip = session.get('round_trip')

    # Lấy danh sách hãng hàng không được chọn từ query parameters
    selected_airlines = request.args.getlist('selected_airlines')

    # Chuyển đổi departure_date_str thành datetime nếu cần
    departure_date = convert_to_datetime(departure_date_str)
    departure_date_format = format_vietnamese_date(departure_date)

    # Tìm mã tuyến bay đi
    route_code = find_route_by_airport_codes(from_code, to_code)

    # Tìm thông tin sân bay
    start = find_airport_location(from_code)
    destination = find_airport_location(to_code)
    departure_airport_location = find_airport_name(from_code)
    arrival_airport_location = find_airport_name(to_code)

    # Tìm tất cả chuyến bay không bị lọc
    list_flights = find_flights(departure_date_str, route_code, seat_class, ticket_quantity)
    flight_info_list = get_full_flight_info_v2(list_flights, seat_class)

    # Nếu không có tham số lọc 'selected_airlines' thì hiển thị tất cả chuyến bay
    if selected_airlines:
        flight_info_list = [flight for flight in flight_info_list if flight['airline_code'] in selected_airlines]

    # Tìm danh sách hãng hàng không
    airlines = get_airlines_by_flights(list_flights, seat_class)

    return render_template('flights_normal.html',
                           from_code=from_code,
                           to_code=to_code,
                           start=start,
                           destination=destination,
                           departure_date=departure_date_format,
                           seat_class=seat_class,
                           ticket_quantity=ticket_quantity,
                           flights=flight_info_list,
                           airlines=airlines,
                           departure_airport_location=departure_airport_location,
                           arrival_airport_location=arrival_airport_location,
                           selected_airlines=selected_airlines,
                           round_trip=round_trip
                           )


@customer_bp.route('/flights_roundtrip', methods=['GET', 'POST'])
def flights_roundtrip():


    # Lấy thông tin chuyến bay từ session
    outbound_flight = session.get('outbound_flight', None)  # Chuyến bay lượt đi
    return_flight = session.get('return_flight', None)  # Chuyến bay khứ hồi (nếu đã chọn)

    print('outbound_flight: ',outbound_flight)
    print('return_flight: ', return_flight)

    # Lấy dữ liệu từ session
    return_date_str = session.get('return_date_str')  # Ngày khứ hồi
    from_code = session.get('from_code')
    to_code = session.get('to_code')
    departure_date_str = session.get('departure_date_str')
    seat_class = session.get('seat_class')
    ticket_quantity = session.get('ticket_quantity')
    round_trip = session.get('round_trip')


    # Chuyển đổi departure_date_str, return_date_str thành datetime nếu cần
    departure_date = convert_to_datetime(departure_date_str)
    departure_date_format = format_vietnamese_date(departure_date)
    return_date = convert_to_datetime(return_date_str)
    return_date_format = format_vietnamese_date(return_date)

    # Tìm mã tuyến bay đi
    route_code = find_route_by_airport_codes(from_code, to_code)
    # Tìm mã tuyến bay về
    route_code_return = find_route_by_airport_codes(to_code, from_code)

    # Tìm thông tin sân bay
    start = find_airport_location(from_code)
    destination = find_airport_location(to_code)
    departure_airport_location = find_airport_name(from_code)
    arrival_airport_location = find_airport_name(to_code)

    # Tìm tất cả chuyến bay ĐI không bị lọc
    list_flights = find_flights(departure_date_str, route_code, seat_class, ticket_quantity)
    flight_info_list = get_full_flight_info_v2(list_flights, seat_class)
    # Tìm tất cả chuyến bay VỀ không bị lọc
    list_flights_return = find_flights(return_date_str, route_code_return, seat_class, ticket_quantity)
    flight_info_list_return = get_full_flight_info_v2(list_flights_return, seat_class)



    # Lấy danh sách hãng hàng không được chọn từ query parameters
    selected_airlines = request.args.getlist('selected_airlines')
    # Nếu không có tham số lọc 'selected_airlines' thì hiển thị tất cả chuyến bay
    # if selected_airlines:
    #     flight_info_list = [flight for flight in flight_info_list if flight['airline_code'] in selected_airlines]
    #     flight_info_list_return = [flight for flight in flight_info_list if flight['airline_code'] in selected_airlines]
    if selected_airlines:
        if 'flight_info_list' in locals() and flight_info_list:
            # Nếu flight_info_list có trong phạm vi hiện tại và không rỗng
            flight_info_list = [flight for flight in flight_info_list if flight['airline_code'] in selected_airlines]

        if 'flight_info_list_return' in locals() and flight_info_list_return:
            # Nếu flight_info_list_return có trong phạm vi hiện tại và không rỗng
            flight_info_list_return = [flight for flight in flight_info_list_return if
                                       flight['airline_code'] in selected_airlines]

    # Tìm danh sách hãng hàng không
    airlines = get_airlines_by_flights(list_flights, seat_class)
    airlines_return = get_airlines_by_flights(list_flights_return, seat_class)
    return render_template('flights_normal.html',
                               from_code=from_code,
                               to_code=to_code,
                               start=start,
                               destination=destination,
                               departure_date=departure_date_format,
                               seat_class=seat_class,
                               ticket_quantity=ticket_quantity,

                               flights=flight_info_list,
                               flights_return=flight_info_list_return,

                               airlines=airlines,
                               airlines_return=airlines_return,

                               departure_airport_location=departure_airport_location,
                               arrival_airport_location=arrival_airport_location,
                               selected_airlines=selected_airlines,
                               round_trip=round_trip,
                               return_date_str = return_date_format,

                               outbound_flight=outbound_flight,
                               return_flight=return_flight
                                )

@customer_bp.route('/info_flight', methods=['POST'])
def info_flight():
    flight_data = request.get_json()  # Lấy dữ liệu chuyến bay từ client
    if flight_data is None:
        print("Không nhận được dữ liệu JSON!")
        return jsonify({"error": "Invalid JSON"}), 400  # Trả về lỗi nếu không nhận được JSON


    # Lưu thông tin chuyến bay đi vào session
    if 'outbound_flight' not in session:
        session['outbound_flight'] = flight_data
        return jsonify({"success": True, "next_step": "return_flight"})
    else:
        session['return_flight'] = flight_data  # Lưu chuyến bay khứ hồi nếu có
        print(f"Chuyến bay đi: {session.get('outbound_flight')}")
        print(f"Chuyến bay khứ hồi: {session.get('return_flight')}")
        return jsonify({"success": True, "next_step": "info_customer"})


@customer_bp.route('/info_customer', methods=['GET', 'POST'])
def info_customer():
    current_year = datetime.now().year  # Lấy năm hiện tại
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        passengers = []
        ticket_quantity = int(session.get('ticket_quantity', 0))
        has_return_flight = session.get('return_flight') is not None  # Kiểm tra có chuyến khứ hồi hay không

        for i in range(ticket_quantity):
            passenger_id = i + 1


            # Nếu có chuyến khứ hồi, tạo PassengerInfo cho chuyến về
            if has_return_flight:
                return_passenger = create_passenger(passenger_id, request.form, cost_map, is_return=True)
                passengers.append(return_passenger)
            else:
                # Tạo PassengerInfo cho chuyến đi
                trip_passenger = create_passenger(passenger_id, request.form, cost_map, is_return=False)
                passengers.append(trip_passenger)

        # Lưu vào session hoặc cơ sở dữ liệu
        session['passengers'] = [p.get_info() for p in passengers]

        flash("Thông tin hành khách và hành lý đã được lưu thành công!", "success")

    # Xử lý GET
    flight_data = session.get('outbound_flight', None)
    flight_data_return = session.get('return_flight', None)
    ticket_quantity = session.get('ticket_quantity')
    seat_class = session.get('seat_class')

    return_date_str = session.get('return_date_str')
    departure_date_str = session.get('departure_date_str')
    departure_date = convert_to_datetime(departure_date_str).strftime('%d/%m/%Y')

    if return_date_str:
        return_date = convert_to_datetime(return_date_str).strftime('%d/%m/%Y')
    else:
        return_date = None

    # Kiểm tra xem có dữ liệu hành khách trong session không
    passengers = session.get('passengers', [])
    if not passengers:
        # Nếu không có hành khách trong session, tạo lại đối tượng PassengerInfo
        passengers = [PassengerInfo(passenger_id=i + 1) for i in range(int(ticket_quantity))]
        session['passengers'] = [p.get_info() for p in passengers]  # Lưu thông tin hành khách vào session

    print("Thông tin hành khách từ session info_passenger:")
    for passenger in passengers:
        print(passenger)

    return render_template('info_customer.html',
                           flight_data=flight_data,
                           flight_data_return=flight_data_return,
                           ticket_quantity=ticket_quantity,
                           seat_class=seat_class,
                           departure_date=departure_date,
                           return_date=return_date,
                           passengers=passengers,
                           current_year=current_year)


@customer_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    # Xử lý GET
    flight_data = session.get('outbound_flight', None)
    flight_data_return = session.get('return_flight', None)
    ticket_quantity = session.get('ticket_quantity')
    seat_class = session.get('seat_class')

    return_date_str = session.get('return_date_str')
    departure_date_str = session.get('departure_date_str')
    departure_date = convert_to_datetime(departure_date_str).strftime('%d/%m/%Y')

    if return_date_str:
        return_date = convert_to_datetime(return_date_str).strftime('%d/%m/%Y')
    else:
        return_date = None

    # Kiểm tra xem có dữ liệu hành khách trong session không
    passengers = session.get('passengers', [])
    if not passengers:
        # Nếu không có hành khách trong session, tạo lại đối tượng PassengerInfo
        passengers = [PassengerInfo(passenger_id=i + 1) for i in range(int(ticket_quantity))]
        session['passengers'] = [p.get_info() for p in passengers]  # Lưu thông tin hành khách vào session

    for ticket in int(ticket_quantity):
        ve = Ve()


    return render_template('pay.html',
                           flight_data=flight_data,
                           flight_data_return=flight_data_return,
                           ticket_quantity=ticket_quantity,
                           seat_class=seat_class,
                           departure_date=departure_date,
                           return_date=return_date,
                           passengers=passengers,
                           )


@app.route('/search-discount', methods=['POST'])
def search_discount():
    data = request.json
    discount_code = data.get('code')

    khuyen_mai = KhuyenMai.query.filter_by(ma_KM=discount_code).first()
    if khuyen_mai:
        return jsonify({
            "status": "success",
            "discount_code": khuyen_mai.ma_KM,
            "discount_percentage": int(khuyen_mai.ty_le_giam * 100),
            "start_date": khuyen_mai.ngay_bat_dau.strftime('%d/%m/%Y'),
            "end_date": khuyen_mai.ngay_ket_thuc.strftime('%d/%m/%Y')
        })
    return jsonify({"status": "error", "message": "Mã khuyến mãi không tồn tại."}), 404


@app.route('/apply-discount', methods=['POST'])
def apply_discount():
    data = request.json
    discount_code = data.get('code')

    print(discount_code)
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Vui lòng đăng nhập."}), 401

    khuyen_mai = KhuyenMai.query.filter_by(ma_KM=discount_code).first()
    if not khuyen_mai:
        return jsonify({"status": "error", "message": "Mã khuyến mãi không tồn tại."}), 404

    # Kiểm tra hạng thành viên
    khach_hang = KhachHang.query.filter_by(id=current_user.id).first()
    if not khach_hang or khach_hang.hang_thanh_vien.value < HangThanhVien.BAC.value:
        return jsonify({"status": "error", "message": "Bạn không đủ điều kiện sử dụng mã khuyến mãi này."}), 403

    # Lưu vào session
    session['applied_discount'] = discount_code
    return jsonify({"status": "success", "message": f"Mã khuyến mãi '{discount_code}' đã được áp dụng."})
