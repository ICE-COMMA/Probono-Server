document.addEventListener("DOMContentLoaded", function () {
  const logButton = document.querySelector(".login-logout");
  const modal = document.getElementById("login-container");
  logButton.addEventListener("click", () => {
    if (logButton.id === "login") {
      modal.classList.remove("hidden");
    }
  });

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.classList.add("hidden");
    }
  });

  const loginForm = document.getElementById("login-form"); // 로그인 폼의 ID를 사용
  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    function getCSRFToken() {
      const csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
      if (csrfCookie) {
        return csrfCookie[1];
      }
      return null;
    }

    const formData = new FormData(loginForm);
    const response = await fetch("/login/", {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest", // AJAX 요청 헤더 추가
        "X-CSRFToken": getCSRFToken(), // CSRF 토큰 추가
      },
    });

    const responseData = await response.json();
    if (response.ok) {
      console.log(response);
      if (responseData.success) {
        console.log(responseData);

        modal.classList.add("hidden");
      } else {
        console.log("로그인 실패");
        // 실패 시에 대한 처리
      }
    } else {
      console.log("네트워크 오류");
      // 네트워크 오류 처리
    }
    window.location.href = "/";
  });
});
