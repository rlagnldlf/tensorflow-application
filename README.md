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

### 2.2 원시데이터
#### * 데이터 구성

| Number | UserID | Comment | ChannelName | UpdateDate | UpdateName | VideoUploadDate |
|--------|----------|-------------|--------------|--------------|--------------|--------------|
|댓글ID | 사용자ID    | 댓글내용       | 유튜브채널  | 로아온날짜 | 업데이트명  | 영상업로드날짜|

크롤링한 데이터를 유튜브 채널, 로아온 날짜, 영상 업로드 날짜별로 분류해 두었다. [[데이터셋 링크](https://www.kaggle.com/datasets/tltydtltbd/loa-on-youtube-reviews)]
#### * 유튜버에 따른 데이터 개수와 로아온 기간별 데이터 비율
![그림판 수정](https://github.com/user-attachments/assets/eb94163c-77c0-4d9f-9e11-e6ee1a544343)
## 3. 학습데이터
원시 데이터 12,235건에서 업데이트 날짜별 비율을 반영해 2,000건을 추출한 뒤, 긍정 데이터를 1로, 부정 데이터를 0으로 라벨링하고 중립 데이터를 제거하여 총 1,862건의 학습 데이터를 생성하였다. 해당 데이터를 활용해 모델을 학습한 결과, 학습 정확도는 54%, 검증 정확도는 57%로 낮아 모델 성능이 부족하다고 판단하였다.

이에 라벨링 오류 가능성을 고려해 ChatGPT를 활용하여 데이터를 재라벨링하는 과정에서 중립 데이터를 제거하고, 최종적으로 1,204건을 추출해 학습을 진행했다. 이 과정에서 ChatGPT가 추출한 1,204건과 직접 라벨링한 1,862건 중 겹치는 1,204건에서 101건의 라벨이 불일치하는 것으로 확인되었다. 그러나 재라벨링된 데이터를 활용한 학습에서도 검증 정확도에는 큰 변화가 없었다.

이를 개선하기 위해 Electra 논문을 참고하여 하이퍼파라미터를 아래 표와 같이 수정한 후 재학습을 수행한 결과, 학습 정확도는 99%, 검증 정확도는 87%로 크게 향상되며 유의미한 모델 성능을 확보할 수 있었다.[[Electra 논문 링크](https://arxiv.org/pdf/2003.10555)]
![스크린샷 2024-11-26 111427](https://github.com/user-attachments/assets/28902182-1efd-4a9a-843d-f9b5b75fe953)

#### * 하이퍼파라메터 값 변경 사항
| 변경전 |  | 변경후 |  |
|--------|----------|-------------|--------------|
|batch_size | 16    | batch_size       | 32  |
|learning rate | 3e-4    | learning rate       | 1e-4  |
|num_warmup_steps | 0    | num_warmup_steps       | 0.1  |

#### * 하이퍼파라메터 변경에 따른 정확도 비교
![정확도 비교](https://github.com/user-attachments/assets/f8c8b60f-55a4-410a-bdb4-6bb2d7a54c47)

## 4. 결과
### 개발환경

<img src="https://img.shields.io/badge/python-%233776AB.svg?&style=for-the-badge&logo=python&logoColor=white" /><img src="https://img.shields.io/badge/pycharm-%23000000.svg?&style=for-the-badge&logo=pycharm&logoColor=white" />

### 패키지

<img src="https://img.shields.io/badge/pandas-%23150458.svg?&style=for-the-badge&logo=pandas&logoColor=white" /><img src="https://img.shields.io/badge/pytorch-%23EE4C2C.svg?&style=for-the-badge&logo=pytorch&logoColor=white" /><img src="https://img.shields.io/badge/tensorflow-%23FF6F00.svg?&style=for-the-badge&logo=tensorflow&logoColor=white" /><img src="https://img.shields.io/badge/numpy-%23013243.svg?&style=for-the-badge&logo=numpy&logoColor=white" />

### KOELECTRA로 학습한 모델을 원시 데이터에 적용한 결과
| 기간 | 긍정적 댓글 | 부정적 댓글 |전체 수|
|--------|----------|-------------|-------|
|2021년 상반기|592|89|681|
|2021년 하반기|2387|374|2761|
|2022년 상반기|1158|205|1363|
|2022년 하반기|428|182|610|
|2023년 상반기|451|209|	660|
|2023년 하반기|1755|2053|3808|
|2024년 상반기|993| 148|1141|
|2024년 하반기| 877|319|1196|
|전체| 8641|3579|12220|

#### * 기간별 분석


2021년과 2022년에는 긍정적 댓글과 부정적 댓글의 비율이 상대적으로 균형을 이루었으나, 2023년 하반기에는 부정적 댓글 비율이 급격히 증가했다. 이는 게임 내 주요 업데이트에 대한 유저들의 불만이 크게 반영된 결과로 보인다.
반면, 2024년 상반기에는 긍정적 댓글이 다시 우위를 점하며 분위기가 반전됐다. 이는 2023년 하반기 이후 이루어진 후속 조치가 유저들의 긍정적인 반응을 이끌어낸 것으로 해석할 수 있다.
#### * 부정적인 반응의 원인 분석
[[2023년 하반기 LOA-ON 관련 보도](https://www.1conomynews.co.kr/news/articleView.html?idxno=23993)]에 따르면, 유저들은 업데이트 지연과 소통 부족에 대해 큰 불만을 표출했다. 특히, LOA-ON 직후 출시될 중국 서버에 집중하기 위해 업데이트가 지연된 것이 아니냐는 의혹이 제기됐고, 연기된 컨텐츠들의 추후 일정을 명확히 밝히지 못한 이유에 대해 "개발자들에게 부담이 될 수 있어 일정을 확정할 수 없다"라고 답하며 유저들의 반발을 샀다. 또한 주요 서버와 지역 이름, 캐릭터 클래스 명칭을 혼동하는 등 기초적인 실수를 저질러 유저들의 실망감을 더욱 키웠다. 이후 긴급 라이브 방송을 통해 사과했으나, [[LOA-ON 이후 긴급 라이브](https://www.1conomynews.co.kr/news/articleView.html?idxno=24000)]에 따르면 라이브 방송임에도 불구하고 유저들과의 실시간 소통이 전혀 이루어지지 않았고, 방송이 20분 만에 종료되면서 상황은 더욱 악화된 것으로 보인다.

#### * 부정적인 반응을 극복한 2024년 상반기 LOA-ON의 개선점
2024년 상반기 LOA-ON에서는 이전 행사에서 제기되었던 총괄 디렉터 부재, 불명확한 출시 일정, 부족한 컨텐츠, 업데이트 지연, 미숙한 진행 등 다양한 문제점들이 개선되었다. [[2024년 상반기 LOA-ON 관련 보도](https://www.e-focus.co.kr/news/articleView.html?idxno=2946208)] 에 따르면, 세 명으로 나뉘어 있던 디렉터 체제가 하나로 통합되어 총괄 디렉터가 선임되었고, 출시 일정이 명확히 공지되었다. 또한, 컨텐츠 양이 약 2배로 증가했으며, 이전 행사에서 1개월가량 지연되었던 업데이트는 이번에는 행사가 끝난 지 일주일 만에 반영되었다. 아울러 매끄러운 진행으로 유저들에게 긍정적인 평가를 받으며 호평을 이끌어냈다.

#### * 토픽모델링 활용 분석

## 5. 느낀점 및 개선해야할점

