document.addEventListener('DOMContentLoaded', () => {
    //Hiệu ứng click bên ngoài là ẩn menu các thao tác ve
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.custom-dropdown');

    document.addEventListener('click', function (e) {
        if (!dropdownMenu.contains(e.target) && !dropdownToggle.contains(e.target)) {
            dropdownMenu.classList.remove('show'); // Bỏ class 'show'
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {

    // // Hàm lấy dữ liệu khi nhập nơi đi
    // document.querySelectorAll('.dropdown-item').forEach(item => {
    //     item.addEventListener('click', function () {
    //         const input = this.closest('.position-relative').querySelector('input');
    //         input.value = this.textContent; // Set the input value
    //     });
    // });

    // Hàm lấy dữ liệu khi nhập nơi đến
    document.querySelectorAll('.dropdown-menu a').forEach(item => {
        item.addEventListener('click', function () {
            const button = this.closest('.dropdown').querySelector('button');
            button.textContent = this.textContent;
        });
    });


    const adultCount = document.getElementById('adult-count');
    const childCount = document.getElementById('child-count');
    const infantCount = document.getElementById('infant-count');
    const passenger_label = document.querySelector('.passenger-label')

    // Hàm tăng giảm số lượng
    function updateCounter(counter, operation, passenger_type) {
        let currentValue = parseInt(counter.value);
        if (operation === 'increase') {
            if ((passenger_type === 'adult' || passenger_type === 'child') && currentValue < 3) {
                counter.value = currentValue + 1;
            } else if (passenger_type === 'infant' && currentValue < 1) {
                counter.value = currentValue + 1
            }
        } else if (operation === 'decrease' && currentValue > 1 && passenger_type === 'adult') {
            counter.value = currentValue - 1;
        } else if (operation === 'decrease' && currentValue > 0 && (passenger_type === 'child' || passenger_type === 'infant')) {
            counter.value = currentValue - 1;
        }
    }


    document.getElementById('adult-increase').addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định
        checkButtonStatus();
        updateCounter(adultCount, 'increase', 'adult');
    });
    document.getElementById('adult-decrease').addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định
        checkButtonStatus();
        updateCounter(adultCount, 'decrease', 'adult');
    });
    document.getElementById('child-increase').addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định
        checkButtonStatus();
        updateCounter(childCount, 'increase', 'child');
    });
    document.getElementById('child-decrease').addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định
        checkButtonStatus();
        updateCounter(childCount, 'decrease', 'child');
    });
    document.getElementById('infant-increase').addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định
        checkButtonStatus();
        updateCounter(infantCount, 'increase', 'infant');
    });
    document.getElementById('infant-decrease').addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định
        checkButtonStatus();
        updateCounter(infantCount, 'decrease', 'infant');
    });

    // Lấy số lượng hành khách
    document.getElementById('done-btn').addEventListener('click', (event) => {
        event.preventDefault();
        const totalPassengers = parseInt(adultCount.value) + parseInt(childCount.value) + parseInt(infantCount.value);
        passenger_label.textContent = `${totalPassengers} Người`
    });


    //Xu ly khi nhan ngoai hoac nhan done se an dropdown
    const passengers_dropdown = document.querySelector('.passengers-dropdown')
    const done_btn = document.getElementById('done-btn')


    // Hàm ẩn dropdown
    const closeDropdown = () => {
        passengers_dropdown.classList.remove('show'); // Ẩn dropdown bằng cách bỏ class 'show'
    };


    // Sự kiện khi nhấn vào nút Done
    done_btn.addEventListener('click', (event) => {
        event.stopPropagation(); // Ngăn không cho sự kiện lan ra ngoài
        closeDropdown();
    });


    // Ngăn dropdown đóng ngay khi nhấn vào dropdown nội dung
    passengers_dropdown.addEventListener('click', (event) => {
        event.stopPropagation();
    });


    // Ham vo hieu hoa cac button khi toi nguong
    function checkButtonStatus() {
        // Hai nut cua nguoi lon
        if (parseInt(adultCount.value) === 1) {
            document.getElementById('adult-decrease').disabled = true;
        } else {
            document.getElementById('adult-decrease').disabled = false;
        }
        if (parseInt(adultCount.value) === 3) {
            document.getElementById('adult-increase').disabled = true;
        } else {
            document.getElementById('adult-increase').disabled = false;
        }

        // Hai nut cua tre e
        if (parseInt(childCount.value) === 0) {
            document.getElementById('child-decrease').disabled = true;
        } else {
            document.getElementById('child-decrease').disabled = false;
        }
        if (parseInt(childCount.value) === 3) {
            document.getElementById('child-increase').disabled = true;
        } else {
            document.getElementById('child-increase').disabled = false;
        }

        // Hai nut cho tre so sinh
        if (parseInt(infantCount.value) === 1) {
            document.getElementById('infant-increase').disabled = true;
            document.getElementById('infant-decrease').disabled = false;
        } else {
            document.getElementById('infant-increase').disabled = false;
            document.getElementById('infant-decrease').disabled = true;
        }
    }


    //Bat su kien chọn vé khứ hồi hay một chiều tren dropdown
    const type_ticket = document.getElementById('oneWayDropdown')

    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function () {
            if (item.textContent === 'Khứ Hồi') {
                document.getElementById('roundTripToggle').checked = true;
                document.getElementById('returnDate').disabled = false;
                document.getElementById('returnDate').style.color = "black"
            } else {
                document.getElementById('roundTripToggle').checked = false;
                document.getElementById('returnDate').disabled = true;
                document.getElementById('returnDate').style.color = "gray"
            }
        });
    });

    // Bat su kien chon ve khu hoi hay mot chieu tren checkbox
    const check_box_type_ticket = document.getElementById('roundTripToggle')
    check_box_type_ticket.addEventListener('change', (event) => {
        if (check_box_type_ticket.checked === true) {
            document.getElementById('returnDate').disabled = false;
            document.getElementById('oneWayDropdown').textContent = 'Khứ Hồi'
            document.getElementById('returnDate').style.color = "black"
        } else {
            document.getElementById('returnDate').disabled = true;
            document.getElementById('oneWayDropdown').textContent = 'Một Chiều'
            document.getElementById('returnDate').style.color = "gray"
        }
    });

    // Swap chuyen di
    document.getElementById('swapValue').addEventListener('click', (event) => {
        const str = document.getElementById('fromInput').value;
        document.getElementById('fromInput').value = document.getElementById('toInput').value;
        document.getElementById('toInput').value = str;
    });

    // Lay du lieu noi di và đến
    document.querySelectorAll('.btn-outline-secondary').forEach(button => {
        button.addEventListener('click', function () {
            const inputField = this.closest('.position-relative').querySelector('input');
            inputField.value = this.textContent;
        });
    });

    //Xu ly thoi gian di va khu hoi
    document.getElementById('departure-date').addEventListener('change', event =>{
        document.getElementById('returnDate').value = document.getElementById('departure-date').value
    })

});


//Xử lý số lượng hành lý tăng và giảm
document.addEventListener('DOMContentLoaded', () => {
    const input_bagggage = document.getElementById('baggage-count')
    const increaseButton = document.getElementById('baggage-increase');
    const decreaseButton = document.getElementById('baggage-decrease');


    //Xử lý tăng
    increaseButton.addEventListener('click', event => {
        if (parseInt(input_bagggage.value) < 5) {
            input_bagggage.value = parseInt(input_bagggage.value) + 1
        }
    })


    // Xu ly giam
    decreaseButton.addEventListener('click', event => {
        if (parseInt(input_bagggage.value) > 0) {
            input_bagggage.value = parseInt(input_bagggage.value) - 1
        }
    })
});


//Xử lý đổi màu ghế khi click
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.seat').forEach(seat => {
        seat.addEventListener('click', event => {
            event.target.style.backgroundColor = 'mediumseagreen';
            document.getElementById('sitting-position-go').textContent += '  ' + event.target.textContent;
        });
    });
})

//Xử lý thông báo khi hủy vé
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cancelTicket').addEventListener('click', function () {
        const toastElement = document.getElementById('successToast');
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    });
})


//Xử lý tăng giảm số lượng ghế khi lập lịch
document.addEventListener('DOMContentLoaded', () => {
    function quantity_seat(counter, operator, seat_type) {
        let currentValue = parseInt(counter.value);
        if (operator === 'increase') {
            if (currentValue <= 30 && seat_type === 'merchant') {
                counter.value = currentValue + 1
            } else if (currentValue <= 100 && seat_type === 'popular') {
                counter.value = currentValue + 1
            } else {
                //
            }
        } else {
            if (currentValue > 10 && seat_type === 'merchant') {
                counter.value = currentValue - 1
            } else if (currentValue > 70 && seat_type === 'popular') {
                counter.value = currentValue - 1
            } else {
                //
            }
        }
    }

    const seat_class1 = document.getElementById('seatClass1')
    const seat_class2 = document.getElementById('seatClass2')

    document.getElementById('decreaseSeatClass1').addEventListener('click', event => {
        quantity_seat(seat_class1, 'decrease', 'merchant')
    })
    document.getElementById('increaseSeatClass1').addEventListener('click', event => {
        quantity_seat(seat_class1, 'increase', 'merchant')
    })
    document.getElementById('decreaseSeatClass2').addEventListener('click', event => {
        quantity_seat(seat_class2, 'decrease', 'popular')
    })
    document.getElementById('increaseSeatClass2').addEventListener('click', event => {
        quantity_seat(seat_class2, 'increase', 'popular')
    })
})


//Xử lý session lấy dữ liệu từ /page/sellticket qua /page/choiceticket
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search-info').addEventListener('click', event => {
        const loai_ve = document.getElementById('oneWayDropdown').textContent
        const so_luong_hanh_khach = document.querySelector('.passenger-label').innerText
        const hang_ve = document.getElementById('classDropdown').textContent
        const noi_di = document.getElementById('fromInput').value
        const noi_den = document.getElementById('toInput').value
        const ngay_di = document.getElementById('departure-date').value
        const ngay_ve = document.getElementById('returnDate').value
        fetch('/api/sellticket', {
            method: 'POST',
            body: JSON.stringify({
                "loai_ve": loai_ve,
                "so_luong_hanh_khach": so_luong_hanh_khach,
                "hang_ve": hang_ve,
                "noi_di": noi_di,
                "noi_den": noi_den,
                "ngay_di": ngay_di,
                "ngay_ve": ngay_ve
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        })
    })
})


//Xử lý session lấy dữ liệu từ /page/choiceticket
document.addEventListener('DOMContentLoaded', () => {
    const thoi_gian_bay = document.querySelector('.flight-time')
    const hang_bay = document.querySelector('.airlines')
    const so_diem_dung = document.querySelector('.stop-point')
    document.querySelectorAll('.aircraft-company').forEach(item => {
        item.addEventListener('click', event => {
            hang_bay.innerText = item.textContent
            document.querySelector('.icon-airplane').style.display = 'none'
        })
    })

    document.querySelectorAll('.time-flight').forEach(item => {
        item.addEventListener('click', event => {
            thoi_gian_bay.innerText = item.textContent
            document.querySelector('.icon-clock').style.display = 'none'
        })
    })

    document.querySelectorAll('.point-stop').forEach(item => {
        item.addEventListener('click', event => {
            so_diem_dung.innerText = item.textContent
            document.querySelector('.icon-geo').style.display = 'none'
        })
    })
    document.getElementById('search-flight').addEventListener('click', event => {
        event.preventDefault() //Ngăn  sự kiện load lại trang
        fetch('/api/searchflights', {
            method: "POST",
            body: JSON.stringify({
                'so_diem_dung': so_diem_dung.innerText,
                'thoi_gian_bay': thoi_gian_bay.innerText,
                'hang_bay': hang_bay.innerText
            }),
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => response.json()).then(data => {
            const cac_chuyen_bay = document.getElementById("flights")
            cac_chuyen_bay.innerHTML = ''

            if (data.flights_data && data.flights_data.length > 0) {

                for (let i = 0; i < data.flights_data.length; i = i+1) {
                    cac_chuyen_bay.innerHTML += `
                        <div class="container p-5 my-3 bg-light bg-gradient text-dark"
                                                     style="width: 100%; border-radius: 5px; font-family: Arial, sans-serif; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); position: relative">
                                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                                        <!-- Thông tin hãng bay -->
                                                        <div style="flex: 2;">
                                                            <div style="font-weight: bold; color: #333; position: absolute; top: 3px; left: 15px; font-size: 18px">
                                                                ${data.flights_data[i]['ten_hang']}
                                                            </div>
                                                            <div style="margin-top: 0; text-align: center; display: flex; align-items: center; gap: 20px; width: 300px; margin-left: 150px">
                                                                <div class="d-flex flex-column align-items-center"
                                                                     style="width: 70px; margin-right: 10px">
                                                                    <div style="width: 100px; margin-right: 10px">
                                                                        <p style="margin-bottom: 2px;">
                                                                            ${data.flights_data[i]['noi_di']}</p>
                                                                    </div>
                                                                    <div>
                                                                        <span class="font-bold"
                                                                              style="font-weight: bold;">${data.list_time_flight[i]['thoi_gian_di']}</span>
                                                                    </div>
                                                                </div>
                                                                <!-- điểm dừng -->
                                                                <div class="d-flex flex-column align-items-center"
                                                                     style="width: 120px">
                                                                    <p class="text-muted mb-2"
                                                                       style="margin-top: -11px">
                                                                        ${data.flights_data[i]['diem_dung']} điểm dừng</p>
                                                                    <!-- Mũi tên -->
                                                                    <div class="arrow-c ontainer d-flex align-items-center"
                                                                         style="display: flex; align-items: center; position: absolute">
                                                                    <span class="dot"
                                                                          style="height: 8px; width: 8px; background-color: gray; border-radius: 50%;"></span>
                                                                        <div class="line"
                                                                             style=" flex-grow: 2; height: 2px; background-color: gray; margin: 0; width: 80px;"></div>
                                                                        <div style="font-size: 19px; color: gray; margin-left: -15px; margin-top: -4px">
                                                                            &rarr;
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="d-flex flex-column align-items-center"
                                                                     style="width: 70px; margin-left: 10px">
                                                                    <div style="width: 100px; margin-right: 10px">
                                                                        <p style="margin-bottom: 2px;">
                                                                            ${data.flights_data[i]['noi_den']}</p>
                                                                    </div>
                                                                    <div class="">
                                                                        <span class="font-bold"
                                                                              style="font-weight: bold;">${data.list_time_flight[i]['thoi_gian_den']}</span>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div style="position: absolute; bottom: 3px; left: 15px; ">
                                                            <div style="margin-top: 5px;">Giá tiền: <span
                                                                    style="font-weight: bold; color: #d9534f; font-size: 18px">${data.flights_data[i]['gia_chuyen_bay']} VND</span>
                                                            </div>
                                                        </div>
                                                        <!-- Nút lựa chọn -->
                                                         <div style="flex: 1; text-align: right;">
                                                            <button type="submit" name="flight" value="('${data.flights_data[i]['ten_hang']}', '${data.flights_data[i]['noi_di']}', '${data.flights_data[i]['noi_den']}', ${data.list_date_flight[i]['thoi_gian_di']}, ${data.list_date_flight[i]['thoi_gian_den']}, ${data.flights_data[i]['gia_chuyen_bay']}, ${data.flights_data[i]['diem_dung']}, '${data.flights_data[i]['ma_chuyen_bay']}')" style="background-color: #d9534f; color: white; border:none; border-radius: 5px; padding: 10px 20px; font-weight:bold; cursor: pointer; position: absolute; bottom: 10px;right: 20px;">Lựa chọn</button>
                                                        </div>
                                                    </div>
                                                </div>
                    `
                }
            }
            else{
                cac_chuyen_bay.innerHTML= `
                    <div style="background: blue">
                        <p>Không tìm thấy chuyến bay nào phù hợp</p>
                    </div>
                `
            }
        })
    })
})
