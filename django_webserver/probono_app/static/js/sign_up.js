function getCSRFToken() {
  var csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
  if (csrfCookie) {
    return csrfCookie[1];
  }
  return null;
}

document.getElementById("checkID").addEventListener("click", (event) => {
  //   event.preventDefault();
  const userID = document.getElementById("ID").value;

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/id_check", true); // 실제 서버 주소로 수정
  xhr.setRequestHeader("Content-Type", "application/json"); // json으로 바꿔서 전송
  xhr.setRequestHeader("X-CSRFToken", getCSRFToken()); // CSRF 토큰 추가
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      console.log('dasdf')
      if (xhr.status === 201) {
        let response = JSON.parse(xhr.responseText);
        let resultMessage = document.getElementById("id-valid");
        console.log(response)
        if (response.valid) {
          resultMessage.textContent = "사용 가능한 아이디입니다.";
        } else {
          resultMessage.textContent = "사용중인 아이디입니다.";
        }
      } else {
        console.error("Error:", xhr.statusText);
        alert(userID);
      }
    }
  };
  var data = JSON.stringify({ check_id: userID });
  xhr.send(data);
});
