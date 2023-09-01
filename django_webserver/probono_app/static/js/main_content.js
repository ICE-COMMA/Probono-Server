let slideIndex = 2;
const contentImg = document.querySelector("#content-img");
const contentInfo = document.querySelectorAll(".content-info");
const slideInfo = document.querySelectorAll(".slide");
const userBox = document.getElementById("user");
const initContent = document.getElementById("init-content");
const regex = new RegExp("Hello ([^\n]+)!");

const showContent = () => {
  // 만약에 다른 사진들만 나오면 해당 정보들에 대한 자료가 없어서 임의로 넣어 둔것
  const len = contentInfo.length;
  contentInfo[slideIndex].classList.add("hidden");
  slideInfo[slideIndex].innerHTML = "○";
  slideIndex++;
  let url = null;
  if (slideIndex === len) slideIndex = 0;
  if (contentInfo[slideIndex].id === "custom-demo") {
    contentInfo[slideIndex].querySelector("span").innerText =
      "오늘의 시위 정보";
    const siteNum = "00232765";
    // 시위 사진은 백에서 00232600 부분만 알아오면 수정 가능
    url = `https://www.smpa.go.kr/common/attachfile/attachfileView.do?attachNo=${siteNum}&imgType=L`;
  } else if (contentInfo[slideIndex].id === "custom-population") {
    url = "static/images/seoulStation.jpg";
    contentInfo[slideIndex].querySelector("span").innerText = "서울역 혼잡";
    // 추후 해당 부분에서 처리
  } else {
    url = `https://kacpe.or.kr/en/images/content/content_ready_img.png`;
    contentInfo[slideIndex].querySelector(
      "span"
    ).innerText = `해당 서비스는 준비 중입니다 (${contentInfo[
      slideIndex
    ].id.replace(/custom-(.+)/, "$1")})`;
  }
  contentImg.style.backgroundImage = `url(${url})`;
  contentInfo[slideIndex].classList.remove("hidden");
  slideInfo[slideIndex].innerHTML = "●";
  setTimeout(showContent, 3000);
};
const initImg = "static/images/custom.png";
if (userBox.children.length === 3) {
  const greeting = document.querySelector("#greeting > a").innerHTML;
  const userID = greeting.match(regex)[1];

  let customItem = null;
  if (!sessionStorage.getItem(userID)) {
    initContent.classList.remove("hidden");
    contentImg.style.backgroundImage = `url("${initImg}")`;
    document.querySelector(".content-slide").classList.add("hidden");
  } else {
    customItem = [sessionStorage.getItem(userID).split(",")];
    for (let i = 0; i < 4; i++) contentInfo[i].id = customItem[0][i];
    showContent();
  }
} else {
  initContent.classList.remove("hidden");
  contentImg.style.backgroundImage = `url("${initImg}")`;
  document.querySelector(".content-slide").classList.add("hidden");
}

// 손으로 넘기거나 x,y 좌표 반영해서 넘기는 로직 추가하기
