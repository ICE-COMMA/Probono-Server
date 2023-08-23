const reportContainer = document.querySelector("#report-container");
const reportBtn = document.querySelector("#report-btn");

reportBtn.addEventListener("click", () => {
  reportContainer.classList.remove("hidden");
});

window.addEventListener("click", (event) => {
  if (event.target === reportContainer) {
    reportContainer.classList.add("hidden");
  }
});
