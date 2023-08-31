getdatas = []
m_infos = []
positions = []

$.ajax({
    type: 'get',
    url: "/safety_info/data",
    success: function (response) {
        getdatas = response.ret;

        console.log(getdatas);
        for (i = 0; i < getdatas.length; i++) {
            let name = getdatas[i]['name']
            let x = getdatas[i]['x']
            let y = getdatas[i]['y']
            let m_info = { 'name': name, 'x': x, 'y': y }
            m_infos.push(m_info)
        }

        //  아래는 마커와 인포윈도우 여러개 표시
        for (var i = 0; i < m_infos.length; i++) {
            var m_i_name = m_infos[i]['name']
            var m_i_x = m_infos[i]['x']
            var m_i_y = m_infos[i]['y']
            var gb_position = { content: `<div class="ifw"><h5>${m_i_name}</h5></div>`, latlng: new kakao.maps.LatLng(m_i_y, m_i_x) }
            positions.push(gb_position)
        }

        for (var i = 0; i < positions.length; i++) {
            var m_i_name2 = m_infos[i]['name']
            var marker = new kakao.maps.Marker({
                map: map,
                position: positions[i].latlng,
                clickable: true
            })
            var iwContent = `<div id="iw_con_info"><h5>${m_i_name2}</h5></div>`, // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
                iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

            var infowindow = new kakao.maps.InfoWindow({
                content: iwContent,
                removable: iwRemoveable
            });
            kakao.maps.event.addListener(marker, 'click', makeOverListener(map, marker, infowindow));
        }
    },
    error: function (error) {
        console.error("Error fetching data:", error);
    }
})

// 인포윈도우를 표시하는 클로저를 만드는 함수
function makeOverListener(map, marker, infowindow) {
    return function () {
        infowindow.open(map, marker);
    };
}
// 인포윈도우를 닫는 클로저를 만드는 함수
function makeOutListener(infowindow) {
    return function () {
        infowindow.close();
    };
}