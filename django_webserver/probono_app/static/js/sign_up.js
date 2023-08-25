let idFlag = false;
let pwFlag = false;
const signupContainer = document.querySelector("#signup-container");
const signupBtn = document.querySelector(".signup-mypage");

signupBtn.addEventListener("click", () => {
  if (signupBtn.id === "sign-up") {
    signupContainer.classList.remove("hidden");
  } else {
    window.location.href = "/my_page";
  }
});

window.addEventListener("click", (e) => {
  e.target === signupContainer
    ? signupContainer.classList.add("hidden")
    : false;
});

function getCSRFToken() {
  var csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
  if (csrfCookie) {
    return csrfCookie[1];
  }
  return null;
}

document.getElementById("check-id").addEventListener("click", (event) => {
  event.preventDefault();
  const userID = document.getElementById("ID").value;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/id_check", true); // 실제 서버 주소로 수정
  xhr.setRequestHeader("Content-Type", "application/json"); // json으로 바꿔서 전송
  xhr.setRequestHeader("X-CSRFToken", getCSRFToken()); // CSRF 토큰 추가
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 201) {
        let response = JSON.parse(xhr.responseText);
        if (response.valid) {
          alert("사용 가능한 아이디입니다.");
          idFlag = true;
        } else {
          alert("사용 중인 아이디입니다.");
          idFlag = false;
        }
      } else {
        console.error("Error:", xhr.statusText);
      }
    }
  };
  var data = JSON.stringify({ check_id: userID });
  xhr.send(data);
});

// HTML에서 비밀번호 입력 필드와 비밀번호 확인 입력 필드의 id를 사용해야 합니다.
let passwordInput = document.getElementById("PW");
let confirmPasswordInput = document.getElementById("check-pw");
let messageElement = document.getElementById("message");

// 비밀번호 입력 필드나 비밀번호 확인 입력 필드가 변경될 때 실행되는 함수
function checkPasswords() {
  let password = passwordInput.value;
  let confirmPassword = confirmPasswordInput.value;
  messageElement.classList.remove("hidden");
  if (password === confirmPassword) {
    messageElement.textContent = "비밀번호가 일치합니다.";
    messageElement.style.color = "green";
  } else {
    messageElement.textContent = "비밀번호가 일치하지 않습니다.";
    messageElement.style.color = "red";
  }
}

passwordInput.addEventListener("input", checkPasswords);
confirmPasswordInput.addEventListener("input", checkPasswords);

// 비밀번호 입력 필드나 비밀번호 확인 입력 필드가 변경될 때 checkPasswords 함수 호출

document.querySelector("#sign-up-form").addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);
  if (messageElement.style.color === "green") pwFlag = true;
  if (idFlag && pwFlag) {
    fetch("/sign_up/", {
      method: "POST",
      headers: {
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.message) {
          alert("회원가입이 완료되었습니다.");
        } else {
          console.log(data.message);
          alert("회원가입에 실패했습니다. 다시 시도해주세요.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    if (!idFlag) {
      alert("사용하지 않는 아이디로 가입해주세요");
    } else alert("비밀번호 재확인");
  }
});

//
