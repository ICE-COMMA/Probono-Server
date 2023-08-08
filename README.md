# 사회적 약자 참여형 스마트시티 생활 예보 서비스

<p align="center">
  <br>
  <img src="./images/comma.png">
  <br>
</p>

## 프로젝트 소개

<p align="justify">

### 프로젝트 소개

> 날씨, 미세먼지 외 공공포털 및 기타 개방된 공공 시스템 등에서 다양한 데이터들을 수집하여 분석 후 사회적 약자 맞춤형 생활 예보를 제공해 주고 도시 위험 상황 신고 등의 사용자 참여를 유도하고자 함.

### 개발 배경

> 현재 도시에 거주하는 시민들에게 날씨, 미세먼지 등의 정보를 알려주고는 있지만, 사회적 약자를 위해 안전한 도시 생활을 위한 종합 예보는 거의 없음. 위의 각종 제약 요소들과 관련된 데이터들을 수집해 AI모델을 바탕으로 잠재적인 위험요소들을 예측하는 사회적 약자 맞춤형 서비스를 진행하고자 함.

</p>

<p align="center">
</p>

<br>

<!-- ## 기술 스택 -->

<!-- |  HTML5  |  CSS3  | JavaScript | React    | Figma    | notion    |
| :-----: | :----: | :--------: | -------- | -------- | --------- |
| ![html] | ![css] |   ![js]    | ![react] | ![figma] | ![notion] | -->

<br>

## 구현 기능

### 상세 날씨 정보

### 상세 교통 정보 제공

### 지역 인구 밀집 정보 (혼잡도) 제공

### 각종 시위 정보 및 행사 정보 (생활 안전 정보) 제공

<br>

## 기대 효과

> 사회적 약자의 도시 생활 안전 향상

> 스마트시티를 위한 사용자 참여도 향상

<p align="justify">

</p>

<br>

<!-- ## 라이센스

MIT &copy; [NoHack](mailto:lbjp114@gmail.com) -->

<!-- Stack Icon Refernces -->

<!-- [html]: /images/stack/html.svg
[css]: /images/stack/css.svg
[js]: /images/stack/javascript.svg
[react]: /images/stack/react.svg
[figma]: /images/stack/figma.svg
[notion]: /images/stack/notion.svg

<br> -->

<!-- commit rule (컨벤션) 관련 -->

# 커밋 룰

**git 커밋 룰**을 이용해 **더 나은 로그 가독성, 리뷰 프로세스, 코드 유지 보수**를 하고자 한다.

## 커밋 메세지 구조

커밋 메세지는 **Head, Body, Footer**로 구성한다. 제목을 제외한 나머지는 옵션이다.

### 형식

> Head 타입 : [#이슈 번호 - ]
>
> Body
>
> Footer(옵션)

### 타입

커밋 메세지가 **어떤 의도**를 가진 메세지인지 알린다.
**태그와 제목**으로 구성되어 있고 사용법은 **태그: 제목**의 형태이다. (`: 뒤에 space 주의!`)

**ex) Feat: Infinity Scroll 추가**

#### 태그 종류들

<table style="text-align : center;">
    <th>태그</th>
    <th>의도</th>
    <th>태그</th>
    <th>의도</th>
    <tr>
        <td style="color : red">✔️ Feat</td>
        <td style="color : red">새 기능 추가</td>
        <td style="color : red">✔️ Fix</td>
        <td style="color : red">버그 수정</td>
    </tr>
    <tr>
        <td style="color : red">✔️ Design</td>
        <td style="color : red">CSS, UI 변경</td>
        <td style="color : red">✔️ Style</td>
        <td style="color : red">포맷 변경 등 코드 수정이 없는 경우</td>
    </tr>
        <tr>
        <td style="color : red">✔️ Refactor</td>
        <td style="color : red">코드 리팩토링</td>
        <td style="color : red">✔️ Comment</td>
        <td style="color : red">주석 추가</td>
    </tr>
    </tr>
        <tr>
        <td style="color : red">✔️ Docs</td>
        <td style="color : red">문서 수정</td>
        <td>Test</td>
        <td>테스트 추가, 리팩토링</td>
    </tr>   
    </tr>
    <tr>
        <td style="color : red">✔️ Rename</td>
        <td style="color : red">파일명 수정, 이동</td>
        <td style="color : red">✔️Remove</td>
        <td style="color : red">파일 삭제</td>
    </tr>
    <tr>
        <td>Chore</td>
        <td>패키지 매니저 설정</td>
        <td>!HOTFIX</td>
        <td>급한 버그 수정</td>
    </tr>
    <tr>
        <td>!BREAKING</br>
        CHANGE</td>
        <td>커다란 API 변경</td>
        <td></td>
        <td></td>
    </tr>
</table>

### HEAD

제목은 메세지의 **짧은 요약**입니다. 다음과 같은 규칙을 가진다.

1. "고침", "추가", "변경" 등 **명령조**로 시작한다. ( 영어의 경우 동사 원형 )
2. 총 글자는 **50자** 이내
3. 마지막에 **특수문자 삽입 X**
4. **개조식** 구문 ( 간결, 요점적인 서술 )

### BODY

본문은 다음과 같은 규칙을 가진다.

1. 한 줄 당 **72자 내외**
2. **최대한 상세히 작성**
3. 어떻게보단 **무엇, 왜**에 중점적으로 작성한다.

### FOOTER

1. **이슈 트래커 ID**를 작성한다. `"유형: #이슈 번호"`

> Feat: 추가 Infinity Scroll 기능
>
> - react-intersection-observer 패키지 사용
> - intersection 관측 시 다음 page API 호출
>
> Reslves: #321

<!-- 위와 동일 -->

<!-- # 참고 사이트

#### 🔗[참고 1](https://overcome-the-limits.tistory.com/entry/%ED%98%91%EC%97%85-%ED%98%91%EC%97%85%EC%9D%84-%EC%9C%84%ED%95%9C-%EA%B8%B0%EB%B3%B8%EC%A0%81%EC%9D%B8-git-%EC%BB%A4%EB%B0%8B%EC%BB%A8%EB%B2%A4%EC%85%98-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0)

#### 🔗[참고 2](https://meetup.toast.com/posts/106) -->
