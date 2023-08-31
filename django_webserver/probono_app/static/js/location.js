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

// 위도(latitude), 경도(longitude)

let locationConatiner = document.querySelector("#location-container");
let locationContent = document.querySelector("#location-content");

let lat = null;
let lon = null;

const csrftoken = getCookie("csrftoken");
const handleLocation = document.getElementById("location");

const gpsLocation = document.querySelector("#gpsLocation");
const mapLocation = document.querySelector("#map-location");

const displayMap = document.querySelector("#display-map");

handleLocation.addEventListener("click", () => {
  locationConatiner.classList.remove("hidden");
  locationContent.classList.remove("hidden");
});

window.addEventListener("click", (e) => {
  if (e.target === locationConatiner) {
    displayMap.classList.add("hidden");
    locationConatiner.classList.add("hidden");
    locationContent.classList.remove("hidden");
  }
});

gpsLocation.addEventListener("click", () => {
  navigator.geolocation.getCurrentPosition(posOk, posError);
});

mapLocation.addEventListener("click", () => {
  let mapOption = {
    center: new kakao.maps.LatLng(37.55803239393497, 126.99830234097189), // 지도의 중심좌표
    level: 4, // 지도의 확대 레벨
  };

  locationContent.classList.add("hidden");
  displayMap.classList.remove("hidden");

  let map = new kakao.maps.Map(displayMap, mapOption); // 지도를 생성합니다

  // 마커가 표시될 위치입니다
  let markerPosition = new kakao.maps.LatLng(37.6519956, 127.3129033);

  // 마커를 생성합니다
  let marker = new kakao.maps.Marker({
    position: markerPosition,
  });

  // 마커가 지도 위에 표시되도록 설정합니다
  marker.setMap(map);

  // 아래 코드는 지도 위의 마커를 제거하는 코드입니다
  // marker.setMap(null);

  kakao.maps.event.addListener(map, "click", function (mouseEvent) {
    // 클릭한 위도, 경도 정보를 가져옵니다
    let locationInfo = mouseEvent.latLng;

    // 마커 위치를 클릭한 위치로 옮깁니다
    marker.setPosition(locationInfo);
    lat = locationInfo.Ma;
    lon = locationInfo.La;
    console.log(map.getCenter());
    alert(`지역 설정을 ${lat}, ${lon}로 완료했습니다`);
    sessionStorage.setItem("latitude", lat);
    sessionStorage.setItem("longitude", lon);
    displayMap.classList.add("hidden");
    locationConatiner.classList.add("hidden");
  });
});

const posOk = (position) => {
  lat = position.coords.latitude;
  lon = position.coords.longitude;

  // Django 서버로 좌표 정보 전송
  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      latitude: lat, //위도
      longitude: lon, //경도
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

  // x와 y 좌표를 localStorage에 저장
  sessionStorage.setItem("latitude", lat);
  sessionStorage.setItem("longitude", lon);
  locationConatiner.classList.add("hidden");
};

const posError = () => console.log("error");
