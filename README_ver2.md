# 진짜 리뷰를 보여줘!

<p align="center"><img src="/img/main화면.PNG" width="450px" height="600px"></>

## 1. 개요
오늘날 많은 사람들이 SNS를 통해 리뷰 관련 정보를 얻고 있습니다. 그중 하나인 블로그를 통해서도 많이 찾아볼 수 있는데요. 언제부터인가 협찬 및 원고료를 제공받은 대가성 리뷰가 많아지면서 솔직한 리뷰를 찾는 것이 어려워졌습니다. 이에 대가성 리뷰가 아닌 솔직한 리뷰만을 보고 싶은 취지에서 프로젝트를 진행하게 되었습니다.

  ### 팀명 / 참여 인원 / 진행 기간 
  Team 'I DEER' / 4인 / 2020.10.06~2020.10.23
  
  ### 작업 환경
  - Platform : Anaconda Python 3.7   
  - Tools : Jupyter Notebook, Pycharm, Colab 등   
  - Package : Pandas, numpy, re, selenum, konlpy, pickle, Tensroflow, Keras 등
  
  ### **데이터 저장소 : [Datasets][drivelink]**
  
  [drivelink]: https://drive.google.com/drive/folders/1PRSHKNPuE6AGbU_cZJdeU9crbP1xsiMK?usp=sharing
  
## 2. 주요 기능
작성중

## 3. 데이터 수집
  #### (1) 수집 대상 선정 : 네이버 포스팅 리뷰 중 '블루투스' 관련 데이터
  #### (2) 임시 분류 기준표 작성
  #### (3) XPath 를 사용하여 데이터 수집
  
## 4. 데이터 전처리 및 데이터 분석
  #### (1) WordCloud 분석 및 결과
  
  광고 리뷰의 WordCloud        |  실제 리뷰의 WordCloud
  :-------------------------:|:-------------------------:
  <img src="/img/5.fake_data_cleaned_content.png" width="450px" height="300px">  | <img src="/img/5.real_data_cleaned_content.png" width="450px" height="300px"><figcaption>
   
  - '있다', '하다' 등 보편적인 키워드들은 불용어 사전에 추가
  - 분석 결과, '블루투스' 키워드가 비대가성 리뷰보다 대가성 리뷰에 빈번하게 사용 된다고 판단

  #### (2) 불용어 처리
  #### (3) 분포도 작성을 통한 상관 관계 분석 및 결과
  - 총 8개 데이터 비교
  - 그 중에서 가장 뚜렷한 결과를 보였던 데이터의 상관 관계 분석 결과
     
    <p align="center"><리뷰에 사용된 글자 수>
    <img src="/img/3.본문글자수_상관관계.PNG" width="1000px" height="300px">
    
    <p align="center"><블로그 하단 태그 개수>
    <img src="/img/3.블로그태그_상관관계.PNG" width="1000px" height="300px">
  
## 5. 모델 설계
  - LSTM 모델과 DNN 모델을 결합
  
  #### (1) 학습 결과
  | LSTM 모델 | DNN 모델  |
|:-------------------------:|:-------------------------: |
|<p align="center"><img src="/img/7.Model_LSTM_Result.png" width="450px" height="300px" />|<p align="center"><img src="/img/8.Model_DNN_Result.png" width="450px" height="300px" /> |
| 약 98 %의 정확도를 나타냄                              ||
