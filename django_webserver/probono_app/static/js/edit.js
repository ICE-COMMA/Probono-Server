const edit = document.querySelector("#profile_complete");

edit.addEventListener("submit", async (e) => {
  e.preventDefault();

  const userHandicap = document.querySelector("#user_handicap").value;
  const previousPw = document.querySelector("#previous_pw").value;
  const nextPw = document.querySelector("#next_pw").value;
  const nextPwCheck = document.querySelector("#next_pw_check").value;

  console.log(userHandicap);

  const requestBody = {
    user_handicap: userHandicap,
    previous_pw: previousPw,
    next_pw: nextPw,
    next_pw_check: nextPwCheck,
  };

  try {
    const response = await fetch("/my_page/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token, // Replace with the actual CSRF token
      },
      body: JSON.stringify(requestBody),
    });

    const data = await response.json();

    if (data.valid === "ok") {
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
});
