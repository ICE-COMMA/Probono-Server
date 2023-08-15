const modalOpenLogin = document.getElementById("login");
const modalCloseButton = document.getElementById("modalCloseButton");
const modal = document.getElementById("modalContainer");

modalOpenLogin.addEventListener("click", () => {
  modal.classList.remove("hidden");
});

modalCloseButton.addEventListener("click", () => {
  modal.classList.add("hidden");
});