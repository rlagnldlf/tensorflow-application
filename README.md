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
LOSTARK는 2018년 11월 7일 국내에서 정식 출시된 이후, 현재는 북미, 중국, 유럽 등 다양한 지역에서 서비스 중인 국내 MMORPG 게임이다. LOSTARK는 2012년부터 개발을 시작해 출시 전부터 많은 관심을 받았으며, 출시 직후 동시 접속자가 35만 명에 이를 정도로 큰 인기를 끌었다. 그러 얼마 지나지 않아 기대와 달리 특별한 요소가 없는 평범한 RPG로 평가되었고, 그로 인해 많은 유저들이 이탈하며 암흑기를 겪게 되었다. 하지만 2021년 시즌 2 시작을 기점으로 역주행에 성공하며 현재는 국내 MMORPG 1위 자리를 굳건히 지키고 있다.

LOA ON은 LOSTARK의 연 2회 대규모 행사로, 공연, 업데이트 방향 설명, 유저 Q&A 등이 진행된다. LOA ON은 매년 6월과 12월에 개최되며, 6월에 열리는 LOA ON은 주로 'LOA ON SUMMER'로 불리고, 6월부터 9월까지 진행될 대규모 업데이트에 대한 내용을 다룬다. 12월에 열리는 LOA ON은 'LOA ON WINTER'로 불리며, 보통 12월부터 3월까지의 대규모 업데이트에 대해 설명한다.
#### * 로스트아크 인게임 화면 캡처와 로아온 행사 중 촬영된 사진
![combined_image](https://github.com/user-attachments/assets/3082606e-6102-408c-a44b-960aa3cf893e)
## 2. 데이터


### 2.1 데이터 수집
유튜브 댓글을 수집하기 위해 BeautifulSoup와 크롬 드라이버를 활용한 크롤링 방법을 선택했다. 파이참에서 BeautifulSoup 패키지를 설치한 후, 크롬 드라이버를 이용해 유튜브 링크만으로 해당 영상의 댓글들을 크롤링하고, 이를 엑셀 파일로 저장하는 코드를 작성했다. 로스트아크 공식 채널과 로스트아크를 주제로 활동하는 게임 유튜버 4명의 총 8회에 걸친 LOA ON 행사 영상에 업로드된 댓글을 크롤링하여, 총 41개의 페이지에서 12,235개의 댓글을 수집했다.

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
| 기간 | 긍정적 댓글 | 부정적 댓글 |전체 수|긍정 비율 (%)|부정 비율 (%)
|--------|----------|-------------|-------|-|-|
|2021년 상반기|592|89|681|86.9	|13.1
|2021년 하반기|2387|374|2761|86.5	|13.5
|2022년 상반기|1158|205|1363|	85.0	|15.0
|2022년 하반기|428|182|610|70.2	|29.8
|2023년 상반기|451|209|	660|68.3	|31.7
|2023년 하반기|1755|2053|3808|46.1	|53.9
|2024년 상반기|993| 148|1141|87.0	|13.0
|2024년 하반기| 877|319|1196|73.3	|26.7
|전체| 8641|3579|12220|70.7	|29.3

#### * 기간별 분석


2021년과 2022년에는 긍정적 댓글과 부정적 댓글의 비율이 비교적 균형을 이루었으나, 2023년 하반기에는 부정적 댓글 비율이 53.9%로 급격히 증가하며 해당 기간 중 가장 높은 수준을 기록했다. 이는 게임 내 주요 업데이트에 대한 유저들의 불만이 크게 반영된 결과로 보인다.
반면, 2024년 상반기에는 긍정적 댓글 비율이 87%로 크게 상승하며 분위기가 반전된 것을 확인할 수 있었다. 이는 2023년 하반기 이후 이루어진 후속 조치가 유저들에게 긍정적인 반응을 이끌어낸 결과로 해석된다.
#### * 토픽 모델링을 활용한 부정적인 반응의 원인 분석
부정적인 반응의 구체적인 원인을 파악하기 위해, 감정 라벨이 '부정'으로 분류된 댓글만을 선별하여 토픽 모델링을 수행했다. 이를 통해 부정적 반응을 유발한 주요 요인들을 데이터 기반으로 도출하고자 하였다.
분석 결과, 부정적 댓글은 크게 세 가지 주요 주제로 분류되었으며, 각 주제와 관련된 상위 키워드는 다음과 같다.

![토픽모델링표](https://github.com/user-attachments/assets/26cbb212-43fa-4192-ac53-2e8d9ee6b6fe)

첫 번째 주제는 개발과 디렉터의 운영 문제 및 기대 부족으로 '개발', '디렉터', '골드', '기대', '컨텐츠' 등의 키워드가 상위로 도출되었으며, 이는 유저들이 게임 개발 및 디렉터의 운영 방식에 대해 불만을 가지고 있음을 나타낸다. 이는 [[2023년 하반기 LOA-ON 관련 보도](https://www.1conomynews.co.kr/news/articleView.html?idxno=23993)]에서도 언급된 바와 같이, 업데이트 지연 및 명확한 일정 공지 부족으로 인한 유저들의 기대감 저하와 반발과 연결된다. 특히, 연기된 컨텐츠에 대한 불명확한 일정 발표가 유저들의 불만을 증폭시켰던 것으로 보인다.

두 번째 주제는 디렉터의 소통 부족과 레이드 운영 문제로, '디렉터', '소통', '시즌', '레이드', '개발' 등의 키워드가 포함되었다. 이 주제는 디렉터와의 소통 부족이 핵심 문제였음을 시사한다. [[LOA-ON 이후 긴급 라이브](https://www.1conomynews.co.kr/news/articleView.html?idxno=24000)]에 따르면, 긴급 라이브 방송에서도 유저들과의 실시간 소통이 제대로 이루어지지 않았고, 20분 만에 방송이 종료되며 상황이 더욱 악화되었다. 이러한 소통 부족은 레이드 운영 및 시즌 관련 불만과도 깊은 연관이 있는 것으로 분석된다.

세 번째 주제는 컨텐츠 문제와 군단장 관련 발표 부족으로 '컨텐츠', '문제', '레이드', '발표', '군단장' 등이 도출되었으며, 이는 게임 내 컨텐츠의 부족함과 군단장 관련 업데이트나 발표가 유저들의 기대에 미치지 못했음을 나타낸다. 유저들은 컨텐츠 업데이트의 속도와 질적인 면에서 아쉬움을 느끼며 이에 대한 반발을 표출한 것으로 보인다.

## 5. 느낀점 및 개선해야할점

