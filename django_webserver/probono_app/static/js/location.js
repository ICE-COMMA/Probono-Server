const handleLocation = document.getElementById("location");
const locationConatiner = document.querySelector("#locationContainer");
const locationContent = document.querySelector("#locationContent");
const gpsLocation = document.querySelector("#gpsLocation");

handleLocation.addEventListener("click", () => {
  locationConatiner.classList.remove("hidden");
});

window.addEventListener("click", (e) => {
  e.target === locationConatiner
    ? locationConatiner.classList.add("hidden")
    : false;
});

gpsLocation.addEventListener("click", () => {
  navigator.geolocation.getCurrentPosition(posOk, posError);
});

const posOk = (position) => {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  alert(`지역 설정을 ${lat}, ${lon}로 완료했습니다`);
  locationConatiner.classList.add("hidden");
};

const posError = () => console.log("error");
