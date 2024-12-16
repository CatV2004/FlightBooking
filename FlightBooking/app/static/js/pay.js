
document.addEventListener('DOMContentLoaded', function() {
    // Lấy phần tử cần thay đổi
    const containerRight = document.querySelector('.container-right');
    const header = document.querySelector('.header');
    const footer = document.querySelector('.footer');


    // Hàm cập nhật vị trí top của phần tử khi cuộn trang
    function updatePosition() {
        // Lấy chiều cao của cửa sổ trình duyệt
        const viewportHeight = window.innerHeight;

        // Lấy chiều cao của header và footer từ JavaScript
        const headerHeight = header.offsetHeight; // Lấy chiều cao thực tế của header
        const footerHeight = footer.offsetHeight; // Lấy chiều cao thực tế của footer

        // Lấy chiều cao của body
        const bodyHeight = document.body.scrollHeight;
        // Lấy vị trí cuộn trang theo trục dọc (vertical)
        const scrollPosition = window.scrollY;

        // Tính toán chiều cao của container-left
        const containerHeight = viewportHeight - headerHeight - footerHeight + 150;

        // Cập nhật giá trị top của phần tử (có thể thay đổi giá trị ở đây theo yêu cầu)
        containerRight.style.top = `${Math.max(scrollPosition, 0)}px`;

        // Lấy vị trí bottom của footer (vị trí cuối cùng của footer trên trang)
        const footerBottom = footer.getBoundingClientRect().bottom;

        containerRight.style.height = `${Math.max(footerBottom - headerHeight - 300, 0)}px`;  // Dừng lại trước footer

    }
    // Lắng nghe sự kiện cuộn
    window.addEventListener('scroll', updatePosition);



    // Lấy tất cả các nút "Chi tiết"
    const detailButtons = document.querySelectorAll(".btn-detail");

    detailButtons.forEach(button => {
        button.addEventListener("click", function () {
            const flightType = button.getAttribute("data-flight-type");

            // Đóng tất cả các modal
            const modals = document.querySelectorAll(".modal");
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });

            // Hiển thị modal được chọn
            const modalToShow = document.getElementById(`flightDetailModal-${flightType}`);
            if (modalToShow) {
                const modalInstance = new bootstrap.Modal(modalToShow);
                modalInstance.show();

            }
        });
    });




    const toggleButton = document.querySelector(".toggle-detail");
    const detailBill = document.querySelector(".detail-bill");
    const icon = toggleButton.querySelector("i");

    toggleButton.addEventListener("click", function () {
        // Toggle mở/đóng
        detailBill.classList.toggle("open");

        // Thêm hoặc gỡ bỏ class `p-3` và `mt-3` dựa trên trạng thái của `.open`
        if (detailBill.classList.contains("open")) {
            detailBill.classList.add("p-3", "mt-3");
            detailBill.style.maxHeight = detailBill.scrollHeight + "px"; // Mở với chiều cao thực
        } else {
            detailBill.classList.remove("p-3", "mt-3");
            detailBill.style.maxHeight = "0"; // Thu nhỏ lại
        }

        // Đổi icon xoay
        icon.classList.toggle("rotate");
    });


    const selectLuggageButton = document.querySelector(".add-code a");
    const luggageModal = new bootstrap.Modal(document.getElementById("discountModal"));

    selectLuggageButton.addEventListener("click", function (e) {
        e.preventDefault(); // Ngăn chặn hành động mặc định của thẻ <a>
        luggageModal.show(); // Hiển thị modal
    });







});


