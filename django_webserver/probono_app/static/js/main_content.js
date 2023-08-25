let slideIndex = 0;
const contentImg = document.querySelector("#content-img");
const contentInfo = document.querySelectorAll(".content-info");
const slideInfo = document.querySelectorAll(".slide");

const showContent = () => {
  const len = contentInfo.length;
  contentInfo[slideIndex].classList.add("hidden");
  slideInfo[slideIndex].innerHTML = "○";
  slideIndex++;
  if (slideIndex === len) slideIndex = 0;
  contentImg.style.backgroundImage = `url("static/images/${slideIndex}.svg")`;
  contentInfo[slideIndex].classList.remove("hidden");
  slideInfo[slideIndex].innerHTML = "●";
  setTimeout(showContent, 3000);
};

showContent();

// 손으로 넘기거나 x,y 좌표 반영해서 넘기는 로직 추가하기
