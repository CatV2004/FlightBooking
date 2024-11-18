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
});
