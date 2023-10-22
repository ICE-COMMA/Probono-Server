# 데이터 중심의 사회적 약자 참여형 스마트시티 생활 예보 서비스 개발

<p align="center">
  <br>
  <img src="./images/comma.png">
  <br>
</p>

## 개발기간
- 23.08.14 - 23.11.14

## 프로젝트 개요

<p align="justify">

### 프로젝트 소개

- 도시 거주 사회적 약자들에게 기상 예보를 포함한 외출 관련해서 겪을 수 있는 각종 위험 요소들을 공지하는 서비스
- 대규모 집회, 교통사고 발생구간, 도로 공사 등과 같은 이동 간의 사고를 유발할 수 있는 각종 위험 요소 알림
- 인구 밀집 구역을 분석하고, 안전을 보장할 수 있는 추천 경로를 제공

### 개발 배경

- 지역사회 복지센터 활동을 하면서 사회적 약자들을 가까이서 지켜 보던 중, 중증장애인분들이 도시 생활 속에서 교통사고나 낙상사고에 쉽게 노출되는 것을 관측함
- 정보 소외 계층을 대상으로 정보 격차를 줄이고, 사회적 약자들이 정보를 손쉽게 획득하여 사전에 조치를 취할 수 있도록 돕고자 함
- 도심에서 일어날 수 있는 대규모 집회, 도로 공사 등과 같은 각종 제약 요소를 사전에 공지해주고, 관련 데이터들을 수집해서 AI모델을 바탕으로 위험 요소들을 예측하고자 함


</p>

<p align="center">
</p>

<br>

 ## 개발환경

- **Language**: Python
  
- **Framework**: Django
  
- **Database**: MongoDB
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
