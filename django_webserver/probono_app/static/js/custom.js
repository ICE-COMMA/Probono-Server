const customContainer = document.querySelector("#custom-container");
const customBtn = document.querySelector("#custom-btn");
const customList = document.querySelectorAll(".custom-info");
const customForm = document.querySelector("#custom-form");
let selectCustom = [];

function getCSRFToken() {
  const csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
  if (csrfCookie) {
    return csrfCookie[1];
  }
  return null;
}

customBtn.addEventListener("click", () => {
  if (document.querySelector(".signup-mypage").id === "my-page") {
    customContainer.classList.remove("hidden");
  } else {
    alert("로그인 후 이용해주세요.");
  }
});

customList.forEach((element) => {
  element.addEventListener("click", () => {
    if (element.style.backgroundColor === "red") {
      selectCustom.pop(element.id);
      element.style.backgroundColor = "transparent";
    } else {
      selectCustom.push(element.id);
      element.style.backgroundColor = "red";
    }
  });
});

customForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  console.log(selectCustom);
  const userID = document.querySelector("#greeting-user").dataset.user;

  const requestBody = {
    user_ID: userID,
    custom: selectCustom,
  };
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
      alert("커스터마이징 수정을 완료했습니다.");
      // 원하는 작업 수행
    } else {
      console.log("수정실패");
    }
  } catch (error) {
    console.error("Error:", error);
    // 에러 처리
  }
  selectCustom = [];
  customList.forEach(
    (element) => (element.style.backgroundColor = "transparent")
  );
  customContainer.classList.add("hidden");
});

window.addEventListener("click", (event) => {
  if (event.target === customContainer) {
    customContainer.classList.add("hidden");
  }
});
