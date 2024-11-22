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

  // Function to swap values between "Từ" and "Đến"
  window.swapValues = function () {
        const fromInput = document.querySelector('input[placeholder="City"][name="from"]');
        const toInput = document.querySelector('input[placeholder="City"][name="to"]');

        if (fromInput && toInput) {
              // Swap the values
              const temp = fromInput.value;
              fromInput.value = toInput.value;
              toInput.value = temp;
        } else {
              console.error('Cannot find input fields for "Từ" and "Đến".');
        }
  };
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
});

