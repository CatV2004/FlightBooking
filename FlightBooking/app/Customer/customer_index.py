from flask import Blueprint, request, jsonify

# Tạo Blueprint cho customer
customer_bp = Blueprint('customer', __name__)

# Route xử lý tìm kiếm chuyến bay
@customer_bp.route("/search-flights", methods=["POST"])
def search_flights():
    try:
        # Lấy dữ liệu JSON từ request
        data = request.get_json()
        from_code = data.get("from", "").strip()
        to_code = data.get("to", "").strip()

        # Kiểm tra mã sân bay hợp lệ
        if not from_code or not to_code:
            return jsonify({"error": "Vui lòng nhập mã sân bay đi và đến."}), 400

        # Ví dụ: Thực hiện tìm chuyến bay từ database
        # flights = dao.get_flights(from_code, to_code)

        # Trả phản hồi (ví dụ chỉ trả mã sân bay)
        return jsonify({"from": from_code, "to": to_code}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
