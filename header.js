fetch("header.html")
  .then(response => response.text())
  .then(data => {
    document.getElementById("header-placeholder").innerHTML = data;

    // Activate menu toggle after header loads
    const hamburger = document.getElementById("hamburger");
    const mobileMenu = document.getElementById("mobileMenu");
    const overlay = document.getElementById("overlay");

    function toggleMenu() {
      hamburger.classList.toggle("active");
      mobileMenu.classList.toggle("active");
      overlay.classList.toggle("active");
    }

    hamburger.addEventListener("click", toggleMenu);
    overlay.addEventListener("click", toggleMenu);

    // Close when clicking a link
    document.querySelectorAll(".mobile-menu a").forEach(link => {
      link.addEventListener("click", toggleMenu);
    });
  });
