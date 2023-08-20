document.addEventListener("DOMContentLoaded", () => {
  // DOMContentLoaded => JavaScript 이벤트의 하나로, 웹 페이지의 모든 HTML 콘텐츠가 로드되고 파싱된 후에 발생하는 이벤트

  const logButton = document.getElementById("login-logout");
  const modal = document.getElementById("login-container");
  const loginForm = document.getElementById("loginForm");
  const statusBtn = document.querySelector("#signup-mypage");

  logButton.addEventListener("click", () => {
    if (logButton.classList[0] === "login") {
      modal.classList.remove("hidden");
    } else {
      logButton.classList.remove("logout");
      logButton.classList.add("login");
      logButton.querySelector("a").innerHTML = "login";
      statusBtn.classList.add("sign_up");
      statusBtn.classList.remove("mypage");
      statusBtn.querySelector("a").innerHTML = "회원가입";
    }
  });

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.classList.add("hidden");
    }
  });

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    logButton.classList.remove("login");
    logButton.classList.add("logout");
    logButton.querySelector("a").innerHTML = "logout";
    statusBtn.classList.remove("sign_up");
    statusBtn.classList.add("mypage");
    statusBtn.querySelector("a").innerHTML = "마이페이지";
    const formData = new FormData(loginForm);
    fetch("/login/", {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest", // AJAX 요청 헤더 추가
        "X-CSRFToken": getCSRFToken(), // CSRF 토큰 추가
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("로그인 성공!");
          window.location.reload(); // 페이지 리로드
        } else {
          // 로그인 실패 시 처리할 코드 작성
          alert("아이디 또는 비밀번호가 일치하지 않습니다.");
          const errorContainer = document.getElementById("login-error");
          errorContainer.textContent = "로그인 실패: " + data.error;
          console.log(errorContainer);
        }
      })
      .catch((error) => {
        alert(error);
      });
  });

  // CSRF 토큰을 가져오는 함수
  function getCSRFToken() {
    const csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
    if (csrfCookie) {
      return csrfCookie[1];
    }
    return null;
  }
});
