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
  console.log(`현재 위치는 ${lat}, ${lon}입니다`);
};

const posError = () => console.log("error");
