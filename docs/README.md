# 블로그 광고 리뷰 분류
## **데이터저장소: [Datasets][drivelink]**

[drivelink]: https://drive.google.com/drive/folders/1PRSHKNPuE6AGbU_cZJdeU9crbP1xsiMK?usp=sharing

<p align="center"><메인 UI>
<p align="center"><img src="/img/main화면.PNG" width="450px" height="600px"></>
  

## 개요
오늘날 많은 사람들이 SNS를 통해 정보를 얻고 있습니다. 그중 하나인 블로그를 통해서도 리뷰 관련 글을 많이 찾아볼 수 있는데요. 언제부턴가 대가성 리뷰가 많아지면서 비대가성 리뷰를 찾기가 어려워졌습니다.

이에 **광고가 아닌 실제 리뷰만을 보고 싶은 취지**에서 프로젝트 주제를 선정하게 되었습니다.

  ## 프로젝트 목표 
  협찬 및 원고료를 제공 받은 대가성 리뷰와 비대가성 리뷰를 구별할 수 있는 모델 설계 및 어플리케이션 개발
  
## 조사 대상
네이버 블로그 중 ‘블루투스’ 관련 포스팅 리뷰
  
## 진행 기간
2020.10.06 ~ 2020.10.23
  
## 작업 환경
 - **Platform : Anaconda Python 3.7**
 - **Tools : Colab, Jupyter Notebook, Pycharm, Anaconda3**
 - **Package : pandas, re, selenium, numpy, konlpy, okt, matplotlib, seaborn, pickle, Pyqt5, tensorflow.keras, sklearn, time**
  
# 프로젝트 진행 과정
### 1. 데이터 수집
  (1) 입
 다음과 같은 기준에 해당하는 경우, **실제 리뷰**로 판단
 
|임시 분류 기준 표|
|------|
|구매 후기 포스팅 중 비슷한 제품이 3개 이하 인 경우
 구매 후기 포스팅 개수가 20개 미만인 경우
 댓글이 20개 미만인 경우
 하루에 작성한 게시글 수가 4개 미만인 경우|


### (2) 광고 및 실제 리뷰 데이터 표본 수집
  블로그에서 광고 리뷰 및 실제 리뷰로 간주될 수 있는 리뷰를 각각 수집
  
  - 광고 리뷰의 경우 '소정의 원고료를 받았습니다' 와 같은 문장이 포함되어 있으면 광고 글로 간주
  - 실제 리뷰의 경우 '내돈내산', '내돈주고', '솔직 리뷰' 와 같은 키워드가 포함되어 있으면 실제 리뷰로 간주
 
 <p align="center">각 리뷰 데이터 150 개 Word2Vec 비교
  
광고 리뷰의 Word2Vec        |  실제 리뷰의 Word2Vec
:-------------------------:|:-------------------------:
<img src="/img/5.fake_data_cleaned_content.png" width="450px" height="300px">  | <img src="/img/5.real_data_cleaned_content.png" width="450px" height="300px"><figcaption>
 
### (3) 전처리 및 상관 관계 분석
<p align="center"><리뷰에 사용된 글자 수 비교>  
<img src="/img/3.본문글자수_상관관계.PNG" width="1000px" height="300px">
 
 <p align="center"><블로그 하단 태그 개수 비교>  
<img src="/img/3.블로그태그_상관관계.PNG" width="1000px" height="300px">
  
### (4) 모델 설계
  - LSTM 모델과 DNN 모델을 결합.
  - LSTM 모델에 형태소 단위로 구성된 문장을 input 값으로 주고, 나온 출력값을 DNN 모델에 input 값으로 줌
  
  

 ## 4. 결론 및 한계
 ### (1) 모델 accuracy
 
| LSTM 모델 | DNN 모델  |
|:-------------------------:|:-------------------------: |
|<p align="center"><img src="/img/7.Model_LSTM_Result.png" width="450px" height="300px" />|<p align="center"><img src="/img/8.Model_DNN_Result.png" width="450px" height="300px" /> |
| 약 98 %의 정확도를 나타냄                              ||
  
### (2) 의의 및 한계점

- 해당 모델은 약 98.5%라는 높은 정확도를 기록
- 모델을 어플리케이션 형태로 구현하여 키워드 검색을 통한 모델의 실제 리뷰 추정 링크 출력기능을 통해 모델의 편의성을 향상시켰다는 점에서 의의가 있음.
- 수집한 데이터 개수의 표본이 1,000개로 적은 편에 해당. 그러나 이는 실제 리뷰와 광고를 구별할 수 있는 명확한 기준이 부재한 것에 기인함.
- 해당 모델을 구동하는 데 많은 GPU가 사용된다는 점 역시 한계점 -> 이에 좀 더 경량화 된 모델이 개발될 필요가 있음

### (3) 향후 계획

본 프로젝트는 데이터 범위를 블루투스 관련 제품으로 한정해서 진행하였음. 이에 블루투스 제품 외에도 다른 상품 리뷰 및 맛집 리뷰 등 데이터 범위를 확장해서 진행한다면 상용화도 가능하다고 생각. 이는 본 프로젝트가 앞으로 나아가야 할 방향이며 향후에 많은 소비자들이 SNS 상에서 투명한 정보를 수집하는 데 있어 본 프로젝트가 도움이 되었으면 하는 바람
