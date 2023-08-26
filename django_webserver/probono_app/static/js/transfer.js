document.getElementById("search-bus-btn").addEventListener("click", () => {
  let x1 = sessionStorage.getItem("xCoordinate");
  let y1 = sessionStorage.getItem("yCoordinate");

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
          `${busNum}번 버스가 지나는 가장 가까운 정류장은 ${closestStationInfo.name}입니다.`
        );
      }
    })
    .catch((error) => console.error("Error:", error));
});
