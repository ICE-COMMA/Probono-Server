const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const csrftoken = getCookie("csrftoken");
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

  // Django 서버로 좌표 정보 전송
  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      latitude: lat,
      longitude: lon,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      // 응답 처리
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  alert(`지역 설정을 ${lat}, ${lon}로 완료했습니다`);
  locationConatiner.classList.add("hidden");
};

const posError = () => console.log("error");
