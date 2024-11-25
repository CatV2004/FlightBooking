document.addEventListener('DOMContentLoaded', function () {
  // Smooth scrolling for all links with 'navbar' class and footer links
      document.querySelectorAll('.navbar a, footer a[href="#myPage"]').forEach(anchor => {
            anchor.addEventListener('click', function (event) {
              // Make sure hash is present
                  if (this.hash !== "") {
                        event.preventDefault();

                        // Get the hash value
                        const hash = this.hash;

                        // Scroll smoothly to the target section
                        document.querySelector(hash).scrollIntoView({
                            behavior: 'smooth',
                        });

                        // Update the URL hash
                        history.pushState(null, null, hash);
                  }
        });
  });

  // Scroll-triggered animations
  window.addEventListener('scroll', function () {
        document.querySelectorAll('.slideanim').forEach(function (element) {
              const pos = element.getBoundingClientRect().top + window.pageYOffset;
              const winTop = window.scrollY;
              if (pos < winTop + 600) {
                    element.classList.add('slide');
              }
        });
  });

  // Toggle visibility of return date based on checkbox state
    const roundTripToggle = document.getElementById('roundTripToggle');
    const returnDate = document.getElementById('returnDate');

    roundTripToggle.addEventListener('change', function () {
            if (this.checked) {
                    returnDate.disabled = false; // Enable return date input
            } else {
                    returnDate.disabled = true; // Disable return date input
                    returnDate.value = ''; // Clear value if unchecked
            }
    });


     // Tăng/giảm số lượng vé
    const increaseBtn = document.getElementById("increaseBtn");
    const decreaseBtn = document.getElementById("decreaseBtn");
    const quantityInput = document.getElementById("ticketQuantity");
    function increaseQuantity() {
        const quantityInput = document.getElementById("ticketQuantity");
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    }

    function decreaseQuantity() {
        const quantityInput = document.getElementById("ticketQuantity");
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) { // Không giảm xuống dưới 1
            quantityInput.value = currentValue - 1;
        }
    }
    // Gắn sự kiện click cho nút tăng và giảm
    if (increaseBtn && decreaseBtn && quantityInput) {
        increaseBtn.addEventListener("click", increaseQuantity);
        decreaseBtn.addEventListener("click", decreaseQuantity);
    } else {
        console.error("Cannot find increase, decrease buttons or quantity input.");
    }


    // Fetch data from API and populate dropdown
    fetch('/api/sanbay')
    .then(response => response.json())
    .then(data => {
        const fromDropdown = document.getElementById('from-options');
        const toDropdown = document.getElementById('to-options');

        if (data && Array.isArray(data)) {
            // Lưu danh sách sân bay để có thể tìm kiếm
            window.airports = data;

            // Đặt data vào dropdown
            data.forEach(sanBay => {
                const displayText = `${sanBay.ten_san_bay} (${sanBay.dia_diem}) - ${sanBay.ma_san_bay}`;

                // Tạo option cho dropdown "Sân bay đi"
                const fromOption = document.createElement('div');
                fromOption.classList.add('dropdown-option');
                fromOption.textContent = displayText;
                fromOption.dataset.value = sanBay.ma_san_bay;
                fromOption.onclick = function () {
                    document.getElementById('from').value = displayText;
                    fromDropdown.style.display = 'none'; // Ẩn dropdown sau khi chọn
                };
                fromDropdown.appendChild(fromOption);

                // Tạo option cho dropdown "Sân bay đến"
                const toOption = document.createElement('div');
                toOption.classList.add('dropdown-option');
                toOption.textContent = displayText;
                toOption.dataset.value = sanBay.ma_san_bay;
                toOption.onclick = function () {
                    document.getElementById('to').value = displayText;
                    toDropdown.style.display = 'none'; // Ẩn dropdown sau khi chọn
                };
                toDropdown.appendChild(toOption);
            });
        }
    })
    .catch(err => console.error('Error fetching airport data:', err));

    // Hàm filter dữ liệu khi gõ vào input (tìm kiếm sân bay)
    function filterAirports(changedField, otherField) {
        const changedInput = document.getElementById(changedField);
        const otherInput = document.getElementById(otherField);
        const dropdown = document.getElementById(`${changedField}-options`);

        const searchTerm = changedInput.value.toLowerCase();

        // Lọc danh sách sân bay theo từ khóa tìm kiếm
        const filteredAirports = window.airports.filter(sanBay => {
            const displayText = `${sanBay.ten_san_bay} (${sanBay.dia_diem}) - ${sanBay.ma_san_bay}`;
            return displayText.toLowerCase().includes(searchTerm);
        });

        // Xóa tất cả các option hiện tại trong dropdown
        dropdown.innerHTML = '';

        // Thêm các sân bay đã lọc vào dropdown
        filteredAirports.forEach(sanBay => {
            const displayText = `${sanBay.ten_san_bay} (${sanBay.dia_diem}) - ${sanBay.ma_san_bay}`;

            const option = document.createElement('div');
            option.classList.add('dropdown-option');
            option.textContent = displayText;
            option.dataset.value = sanBay.ma_san_bay;
            option.onclick = function () {
                changedInput.value = displayText;
                dropdown.style.display = 'none'; // Ẩn dropdown sau khi chọn
            };
            dropdown.appendChild(option);
        });

        // Nếu không có kết quả, hiển thị thông báo "Không tìm thấy"
        if (filteredAirports.length === 0) {
            const noResults = document.createElement('div');
            noResults.classList.add('dropdown-option');
            noResults.textContent = 'Không tìm thấy sân bay';
            dropdown.appendChild(noResults);
        }

        // Nếu cả hai input giống nhau, xóa giá trị của input "other"
        if (changedInput.value === otherInput.value) {
            otherInput.value = '';
        }
    }

    // Hàm hiển thị danh sách khi nhấp vào input (sân bay đi hoặc đến)
    function showDropdown(changedField) {
        const fromDropdown = document.getElementById('from-options');
        const toDropdown = document.getElementById('to-options');

        // Ẩn tất cả các dropdown trước khi hiển thị dropdown của input đang được nhấp
        fromDropdown.style.display = 'none';
        toDropdown.style.display = 'none';

        // Hiển thị dropdown của input đang được nhấp
        const dropdown = document.getElementById(`${changedField}-options`);
        dropdown.style.display = 'block'; // Hiển thị dropdown
        changedInput.value = ''; // Có thể để trống input khi nhấp vào

        // Đảm bảo rằng input không bị lọc (để hiển thị tất cả các sân bay)
        const changedInput = document.getElementById(changedField);
        changedInput.value = ''; // Có thể để trống input khi nhấp vào
    }


    // Hàm hoán đổi giá trị giữa "Sân bay đi" và "Sân bay đến"
    function swapValues() {
        const fromInput = document.getElementById('from');
        const toInput = document.getElementById('to');

        const fromValue = fromInput.value;
        fromInput.value = toInput.value;
        toInput.value = fromValue;
    }

    // Đóng dropdown khi nhấp bên ngoài input hoặc dropdown
    document.addEventListener('click', function(event) {
        const fromDropdown = document.getElementById('from-options');
        const toDropdown = document.getElementById('to-options');
        const fromInput = document.getElementById('from');
        const toInput = document.getElementById('to');

        // Nếu nhấp vào ngoài các dropdown và input, ẩn dropdown
        if (!fromDropdown.contains(event.target) && !fromInput.contains(event.target)) {
            fromDropdown.style.display = 'none';
        }

        if (!toDropdown.contains(event.target) && !toInput.contains(event.target)) {
            toDropdown.style.display = 'none';
        }
    });

    // Hiển thị dropdown khi nhấp vào input
    document.getElementById('from').addEventListener('focus', function() {
        showDropdown('from');
    });
    document.getElementById('to').addEventListener('focus', function() {
        showDropdown('to');
    });
    // Lắng nghe sự kiện input để lọc sân bay
    document.getElementById('from').addEventListener('input', function() {
        filterAirports('from', 'to');
    });
    document.getElementById('to').addEventListener('input', function() {
        filterAirports('to', 'from');
    });

    // Hàm tách mã sân bay từ chuỗi
    function extractAirportCode(inputValue) {
        const parts = inputValue.split(" - "); // Tách chuỗi dựa trên " - "
        return parts.length > 1 ? parts[1] : ""; // Nếu có mã sân bay, trả về mã; nếu không, trả về chuỗi rỗng
    }

    function submitAirportCodes() {
        // Lấy giá trị từ các input
        const fromInput = document.getElementById("from").value.trim();
        const toInput = document.getElementById("to").value.trim();

        // Tách mã sân bay từ chuỗi hiển thị (dựa vào dấu '-')
        const fromCode = extractAirportCode(fromInput);
        const toCode = extractAirportCode(toInput);

        if (fromCode && toCode) {
            // Gửi dữ liệu đến Flask backend
            fetch("/customer/search-flights", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ from: fromCode, to: toCode }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log("Server response:", data); // Xử lý phản hồi từ server
                    if (data.error) {
                        alert(data.error); // Hiển thị lỗi nếu có
                    } else {
                        alert(`Tìm chuyến bay từ ${data.from} đến ${data.to}`);
                    }
                })
                .catch((error) => console.error("Error:", error));
        } else {
            alert("Vui lòng nhập cả mã sân bay đi và đến đúng định dạng.");
        }
    }

});

