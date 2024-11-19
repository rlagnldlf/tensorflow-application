## KOELECTRA를 활용한 LOA ON 유튜브 댓글 분석
<!--
badge icon 참고 사이트
https://github.com/danmadeira/simple-icon-badges
-->
<p align="center"><img src="https://img.shields.io/badge/python-%233776AB.svg?&style=for-the-badge&logo=python&logoColor=white" /><img src="https://img.shields.io/badge/pytorch-%23EE4C2C.svg?&style=for-the-badge&logo=pytorch&logoColor=white" /><img src="https://img.shields.io/badge/pycharm-%23000000.svg?&style=for-the-badge&logo=pycharm&logoColor=white" /><p>

## 1. 개 요

### 1.1 문제정의
이번 프로젝트에서는 게임 업데이트 방향성을 결정하는 데 중요한 유저 반응을 분석하고자, LOSTARK의 연 2회 업데이트 방향을 설명하는 "LOA ON" 행사 유튜브 라이브 방송 댓글을 수집하여, 긍정과 부정 반응을 예측하는 모델을 개발한다. 이를 통해 어떤 업데이트가 유저들에게 긍정적인 평가를 받았는지 또는 부정적인 평가를 받았는지 파악하고자 한다.
### 1.2 LOSTARK와 LOA ON
LOSTARK는 2018년 11월 7일 국내에서 정식 출시된 이후, 현재는 북미, 중국, 유럽 등 다양한 지역에서 서비스 중인 국내 MMORPG 게임이다. LOSTARK는 2012년부터 개발을 시작해 출시 전부터 많은 관심을 받았으며, 출시 직후 동시 접속자가 35만 명에 이를 정도로 큰 인기를 끌었다. 그러나 기대와는 달리 특별한 요소가 없는 평범한 RPG로 평가되며 유저들이 대거 이탈, 암흑기를 맞이했다. 하지만 2021년 시즌 2 시작을 기점으로 역주행에 성공하며 현재는 국내 MMORPG 1위 자리를 굳건히 지키고 있다.
LOA ON은 LOSTARK의 연 2회 대규모 행사로, 공연, 업데이트 방향 설명, 유저 Q&A 등이 진행된다. LOA ON은 매년 6월과 12월에 개최되며, 6월에 열리는 LOA ON은 주로 'LOA ON SUMMER'로 불리며, 6월부터 9월까지 진행될 대규모 업데이트에 대한 내용을 다룬다. 12월에 열리는 LOA ON은 'LOA ON WINTER'로 불리며, 보통 12월부터 3월까지의 대규모 업데이트에 대해 설명한다.
#### * 로스트아크 인게임 화면 캡처와 로아온 행사 중 촬영된 사진
![combined_image](https://github.com/user-attachments/assets/3082606e-6102-408c-a44b-960aa3cf893e)
## 2. 데이터


### 2.1 데이터 수집
유튜브 댓글을 수집하기 위해 BeautifulSoup와 크롬 드라이버를 활용한 크롤링 방법을 선택했다. 파이참에서 BeautifulSoup 패키지를 설치한 후, 크롬 드라이버를 이용해 유튜브 링크만으로 해당 영상의 댓글들을 크롤링하고, 이를 엑셀 파일로 저장하는 코드를 작성했다. 로스트아크 공식 채널과 로스트아크를 주제로 활동하는 게임 유튜버 4명의 8번의 LOA ON 행사 영상에 업로드된 댓글을 크롤링하여, 총 41개의 페이지에서 12,235개의 댓글을 수집했다.
#### * 크롤링 코드와 엑셀 파일 형식의 데이터
![combined_image_side_by_side](https://github.com/user-attachments/assets/dd449f86-ff60-44b8-a115-004908d2213f)
### 2.2 원시데이터
#### * 데이터 구성

| Number | UserID | Comment | ChannelName | UpdateDate | UpdateName | VideoUploadDate |
|--------|----------|-------------|--------------|--------------|--------------|--------------|
|댓글ID | 사용자ID    | 댓글내용       | 유튜브채널  | 로아온날짜 | 업데이트명  | 영상업로드날짜|

크롤링한 데이터를 유튜브 채널, 로아온 날짜, 영상 업로드 날짜별로 분류해 두었다.
#### * 유튜버 별 크롤링한 영상 개수와 로아온기간별 데이터 비율
| 유튜버 이름 | 크롤링한 영상 개수 | 
|--------|----------|
|2021년 상반기 | 681|
|2021년 하반기 | 2763|
|2022년 상반기 | 1365|
|2022년 하반기 | 610|
|2023년 상반기 | 664|
|2023년 하반기 | 3809|
|2024년 상반기 | 1143|
|2024년 하반기 | 1199|
![원그래프](https://github.com/user-attachments/assets/f7a736aa-0347-400f-acce-939bb6836586)
## 3. 학습데이터
전체 데이터 12,235건 중 업데이트 날짜별 비율에 따라 2,000건을 추출한 후, 긍정은 1, 부정은 0으로 라벨링하고, 중립 데이터는 제거하여 총 1,205건의 학습 데이터를 생성했다. 이 데이터를 기반으로 모델을 학습한 결과, 검증 정확도가 58%로 낮게 나타나 모델 성능이 부족하다고 판단했다. 이에 다음과 같은 변경을 적용하여 재학습을 진행했다: batch_size를 16에서 32로, **learning rate (lr)**를 3e-4에서 1e-4로 조정하고, scheduler에서 num_warmup_steps를 0에서 0.1로 변경했다. 이러한 수정 후 재학습한 결과, 최종 검증 정확도가 87%로 크게 향상되며 유의미한 모델 성능을 얻을 수 있었다.
