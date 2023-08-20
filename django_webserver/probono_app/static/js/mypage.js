const cancel = document.querySelector("#profile_cancel");
const edit = document.querySelector("#profile_complete");

cancel.addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "/";
});

edit.addEventListener("submit", (e) => {
  // return 정보 파악 후 ok이면
  e.preventDefault();
  fetch("/my_page/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: "test" }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.valid === "ok") {
        alert("수정 완료됐습니다.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
