let x1 = sessionStorage.getItem("longitude");
let y1 = sessionStorage.getItem("latitude");

let selectX = x1;
let selectY = y1;

let busMapContainer = document.getElementById("display-bus-map");
// 지도를 표시할 div
busMapContainer.classList.remove("hidden");
let busMapOption = {
  center: new kakao.maps.LatLng(y1, x1), // 지도의 중심좌표
  level: 3, // 지도의 확대 레벨
};

// 지도를 생성합니다
var busMap = new kakao.maps.Map(busMapContainer, busMapOption);

// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

var marker = new kakao.maps.Marker(), // 클릭한 위치를 표시할 마커입니다
  infowindow = new kakao.maps.InfoWindow({ zindex: 1 }); // 클릭한 위치에 대한 주소를 표시할 인포윈도우입니다

// 지도를 클릭했을 때 클릭 위치 좌표에 대한 주소정보를 표시하도록 이벤트를 등록합니다
kakao.maps.event.addListener(busMap, "click", (mouseEvent) => {
  searchDetailAddrFromCoords(mouseEvent.latLng, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      //  !!  값을 불리언(Boolean) 값으로 변환하는 표현식입니다. result[0].road_address가 존재하면 true, 존재하지 않으면 false
      var detailAddr = !!result[0].road_address
        ? result[0].road_address.address_name
        : result[0].address.address_name;
      // 마커를 클릭한 위치에 표시합니다
      marker.setPosition(mouseEvent.latLng);
      marker.setMap(busMap);

      // 인포윈도우에 클릭한 위치에 대한 법정동 상세 주소정보를 표시합니다
      infowindow.setContent(detailAddr);
      infowindow.open(busMap, marker);
    }
  });
});

function searchDetailAddrFromCoords(coords, callback) {
  // 좌표로 법정동 상세 주소 정보를 요청합니다
  geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}

document.getElementById("search-bus-btn").addEventListener("click", () => {
  // 위도(latitude), 경도(longitude)

  let busNum = document.getElementById("bus-input").value;
  fetch(`/get_bus_route/${busNum}`)
    .then((response) => response.json())
    .then((data) => {
      let resultContainer = document.getElementById("bus-result-box");
      if (data.station.length === 0) {
        resultContainer.innerHTML = "<p>No results found.</p>";
      } else {
        document.querySelector("#search-bus-box").classList.add("hidden");

        let closestStationInfo = null;
        let shortestDistance = Number.MAX_VALUE;

        data.station.forEach((station) => {
          // let li = document.createElement("li");
          let x2 = station.x;
          let y2 = station.y;
          let distance = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
          if (distance < shortestDistance) {
            closestStationInfo = station;
            shortestDistance = distance;
          }
        });
        alert(
          `${busNum}번 버스가 지나는 가장 가까운 정류장은 ${closestStationInfo.name}으로 이동합니다.`
        );
        selectX = closestStationInfo.x;
        selectY = closestStationInfo.y;
        marker.setPosition(new kakao.maps.LatLng(selectY, selectX));
        marker.setMap(busMap);
        busMap.setCenter(new kakao.maps.LatLng(selectY, selectX));
      }
    })
    .catch((error) => console.error("Error:", error));
});

// 가까운 정류장 좌표 테스트

// 현재 지도 중심좌표로 주소를 검색해서 지도 좌측 상단에 표시합니다
// searchAddrFromCoords(busMap.getCenter(), displayCenterInfo);

// // 중심 좌표나 확대 수준이 변경됐을 때 지도 중심 좌표에 대한 주소 정보를 표시하도록 이벤트를 등록합니다
// kakao.maps.event.addListener(busMap, "idle", function () {
//   searchAddrFromCoords(busMap.getCenter(), displayCenterInfo);
// });

// function searchAddrFromCoords(coords, callback) {
//   // 좌표로 행정동 주소 정보를 요청합니다
//   geocoder.coord2RegionCode(coords.getLng(), coords.getLat(), callback);
// }

// // 지도 좌측상단에 지도 중심좌표에 대한 주소정보를 표출하는 함수입니다
// function displayCenterInfo(result, status) {
//   if (status === kakao.maps.services.Status.OK) {
//     var infoDiv = document.getElementById("centerAddr");

//     for (var i = 0; i < result.length; i++) {
//       // 행정동의 region_type 값은 'H' 이므로
//       if (result[i].region_type === "H") {
//         infoDiv.innerHTML = result[i].address_name;
//         break;
//       }
//     }
//   }
// }
