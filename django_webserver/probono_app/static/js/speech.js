if (!("webkitSpeechRecognition" in window)) {
  alert("지원하지 않는 브라우저입니다. 권장 브라우저는 크롬입니다.");
} else {
  const speech = new webkitSpeechRecognition();
  document.querySelector("#start").addEventListener("click", () => {
    speech.start();
  });
  document.querySelector("#end").addEventListener("click", () => {
    speech.stop();
  });
  speech.addEventListener("result", (event) => {
    const { transcript } = event["results"][0][0];
    console.log(transcript);
  });
}
