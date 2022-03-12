const menuButton = document.querySelector(".menu-button");
const menuClose = document.querySelector("#menuClose");
const main = document.querySelector("main");
const navbar = document.querySelector(".navbar");

const navToggle = function () {
  main.classList.toggle("hidden");
  navbar.classList.toggle("hidden");
  navbar.classList.toggle("navbar--active");
  menuButton.classList.toggle("hidden");
  menuClose.classList.toggle("hidden");
  menuClose.classList.toggle("menu-close");
};

menuButton.addEventListener("click", navToggle);
menuClose.addEventListener("click", navToggle);
