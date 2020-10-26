# 블로그 리뷰 광고 분류 모델

<p align="center"><메인 UI>
<p align="center"><img src="/img/main화면.PNG" width="450px" height="600px"></>
  

## 1. 개요
### 프로젝트 목표 : 광고와 실제 리뷰룰 구별할 수 있는 모델 개발
### 조사 대상 : 네이버 블로그 중 ‘블루투스’ 내용을 포함한 포스팅
### 프로젝트 진행 기간 : 2020. 10. 06 ~ 2020. 10. 23
### 작업 환경
  - 개발 언어 : **Python 3.X**
  - 개발 도구 : **Colab, Jupyter Notebook, Pycharm, Anaconda3**
  - 사용 패키지 : **pandas, re, selenium, numpy, konlpy, okt, matplotlib, seaborn, pickle, Pyqt5, tensorflow.keras, sklearn, time**

## 2. 주제 선정 이유
  오늘날 다수의 사람들이 SNS를 이용하는 만큼 SNS 광고도 증가하는 추세. SNS 매체 중 하나인 블로그의 경우 주로 리뷰 형식을 통해 소통함
  그러나 블로그 역시 언제부턴가 실제 리뷰가 아닌 리뷰 형식의 광고 글이 많아졌음.
  이에 광고가 아닌 실제 리뷰만을 보고 싶은 취지에서 본 프로젝트의 주제를 ‘블로그 리뷰 광고 분류 모델 생성’으로 선정
  
## 3. 프로젝트 진행 과정
### (1) 임시 분류 기준 선정
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
|            | 약 98.5%의 정확도를 나타냄  |
  
### (2) 의의 및 개선점

