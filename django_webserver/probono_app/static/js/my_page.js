const cancel = document.querySelector("#profile-cancel");
const edit = document.querySelector("#profile-complete");

cancel.addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "/";
});

document.querySelector("#profile").addEventListener("submit", async (e) => {
  // return 정보 파악 후 ok이면
  e.preventDefault();

  function getCSRFToken() {
    const csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
    if (csrfCookie) {
      return csrfCookie[1];
    }
    return null;
  }

  const userID = document.querySelector("#user-id").value;
  const userHandicap = document.querySelector("#user-handicap").value;
  const previousPw = document.querySelector("#previous-pw").value;
  const nextPw = document.querySelector("#next-pw").value;
  const nextPwCheck = document.querySelector("#next-pw-check").value;

  const requestBody = {
    user_ID: userID,
    user_handicap: userHandicap,
    previous_pw: previousPw,
    next_pw: nextPw,
    next_pw_check: nextPwCheck,
  };
  console.log(requestBody);
  if (
    previousPw === document.querySelector("#previous-pw").name &&
    nextPw === nextPwCheck
  ) {
    try {
      const response = await fetch(`/my_page/${userID}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(), // Replace with the actual CSRF token
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (data.valid) {
        alert("수정 완료됐습니다.");
        // 원하는 작업 수행
      } else {
        alert("수정 실패했습니다.");
        // 원하는 작업 수행
      }
    } catch (error) {
      console.error("Error:", error);
      // 에러 처리
    }
  } else {
    alert("비밀번호를 다시 입력해주세요.");
  }
});
