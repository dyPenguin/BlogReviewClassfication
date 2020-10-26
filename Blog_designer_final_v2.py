import sys
from PyQt5. QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from selenium import webdriver
import time
import re
import pandas as pd
import numpy as np
import pickle
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

form_window = uic.loadUiType('./naver_basic.ui')[0]

class Worker(QThread):
    def __init__(self,parent):
        super(Worker,self).__init__(parent)
        self.parent = parent
        self.working = False

    def run(self):
        self.parent.check_df_flag = False
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('lang=ko_KR')
        self.driver = webdriver.Chrome('./chromedriver', options=options)
        self.driver.implicitly_wait(0.01)
        #파일 import
        self.stopwords = pd.read_csv('./datasets/stopwords_for_blog.csv', index_col=0)
        self.okt = Okt()

        self.crawling()
        print('crawling 끝')
        self.preprocessing()
        print('preprocessing 끝')
        self.modeling()
        print('modeling 끝')
        self.parent.check()
        print('스레드 종료')

    def crawling(self):
        print('안녕하세요 저는 쓰레드의 크롤링입니당')
        '''
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome('./chromedriver', options=options)
        driver.implicitly_wait(0.01)
        '''
        # 해시태그
        def tag_counts():
            hashtag_cnt = 0
            blogtag_cnt = 0
            try:
                hashtag_cnt = len(self.driver.find_elements_by_class_name('tag'))
            except Exception as e:
                print(e, 'error1!!')
            try:
                blogtag_cnt = len(self.driver.find_elements_by_class_name('ell'))
            except Exception as e:
                print(e, 'error2')
            return hashtag_cnt, blogtag_cnt
        # 블로그 content
        def contents_cralwing():
            content = 'error'
            # 기존 블로그
            try:
                content = self.driver.find_element_by_class_name("se-main-container")
                return content
            except:
                pass
            # 예전 블로그
            try:
                content = self.driver.find_element_by_id("postViewArea")
                return content
            except:
                pass
            return content
        lst_title = []
        lst_url = []
        lst_content = []
        lst_image = []
        lst_video = []
        lst_link = []
        lst_hashTag = []
        lst_blogTag = []
        df_url = self.parent.df_url
        for url in range(0, df_url['url'].count()):
            if self.working:
                print('check')
                break
            print(f'==========================={url} 번==============================')
            try:
                self.driver.get(df_url['url'][url])
                time.sleep(0.05)
                # 프레임 링크 전환
                self.driver.switch_to.frame("mainFrame")
                try:
                    # 블로그 content
                    current_url = self.driver.current_url
                    url_id = current_url.split('/')[-1]
                    title = self.driver.find_element_by_class_name('pcol1').text
                    url_ = df_url['url'][url]
                    content = contents_cralwing()
                    if content == 'error': raise Exception('contents error')
                    lst_title.append(title)
                    lst_content.append(content.text)
                except Exception as e:
                    print('content error')
                    continue
                # 태그 갯수
                hashTags, blogTags = tag_counts()
                try:
                    # 이미지 갯수
                    image_cnt = len(content.find_elements_by_tag_name('img'))
                    # 비디오 갯수
                    video_cnt = len(self.driver.find_elements_by_class_name('u_rmcplayer_control_bg'))
                    # 링크 갯수
                    link1 = len(self.driver.find_elements_by_class_name("se-link"))
                    link2 = len(self.driver.find_elements_by_class_name("se-oglink-url"))
                    links_cnt = (link1 + link2)
                    lst_image.append(image_cnt)
                    lst_video.append(video_cnt)
                    lst_link.append(links_cnt)
                except Exception as e:
                    print('Len error: ', e)
                    lst_image.append(0)
                    lst_video.append(0)
                    lst_link.append(0)
                    pass
                lst_url.append(current_url)
                lst_hashTag.append(hashTags)
                lst_blogTag.append(blogTags)
            except Exception as e:
                print('url error: ', e)
                continue
        df = pd.DataFrame({'title': lst_title, 'content': lst_content,
                           'image_count': lst_image, 'video_count': lst_video, 'link_count': lst_video,
                           'hash_tag_count': lst_hashTag, 'blog_tag_count': lst_blogTag, 'url': lst_url})
        self.df = df
        self.driver.close()
        self.parent.working = False

    def preprocessing(self):
        print('안녕하세요 저는 쓰레드의 전처리 입니당')
        for i in range(len(self.df['content'])):
            self.df['content'][i] = self.df['content'][i].replace('\n', ' ')
        self.df['content_count'] = 0
        for i in range(len(self.df['content'])):
            self.df['content_count'][i] = len(self.df['content'][i])

        clean_content = []
        for sentence in self.df['content']:
            sentence = re.sub('[^가-힣|A-Z|+|-]', ' ', sentence)
            token = self.okt.pos(sentence, norm=True, stem=True)  # 전에는 mos를 써는데 pos를 쓰면 튜플로(쌍으로) ('','noun')형태로 만들어 준다.
            df_token = pd.DataFrame(token, columns=['word', 'class'])
            cleaned_df_token = df_token[(df_token['class'] == 'Noun') | (df_token['class'] == 'Verb') | (df_token['class'] == 'Adjective')]
            cleaned_sentences = cleaned_df_token['word']
            cleaned_sentences = ' '.join(cleaned_sentences)
            clean_content.append(cleaned_sentences)

        self.df['cleaned_content'] = clean_content
        #cleaned_count 글자수
        self.df['cleaned_content_count'] = 0
        for i in range(len(self.df['cleaned_content'])):
            self.df['cleaned_content_count'][i] = len(self.df['cleaned_content'][i])
        cleaned_token_review = list(self.df['cleaned_content'])
        cleaned_sentences = []


        for sentence in cleaned_token_review:
            token = sentence.split(' ')
            cleaned_sentences.append(token)

        self.df['cleaned_content'] = cleaned_sentences
        self.df['bluetooth_word_count'] = 0

        for j in range(len(self.df['cleaned_content'])):
            for i in self.df['cleaned_content'][j]:
                if i == '블루투스':
                    self.df['bluetooth_word_count'][j] += 1
        cleaned_words = []

        for i in range(len(self.df['cleaned_content'])):
            words = []
            for word in self.df['cleaned_content'][i]:
                if i >= 0:
                    if word not in (list(self.stopwords['stopword'])):
                        words.append(word)

            cleaned_word = ' '.join(words)
            cleaned_words.append(cleaned_word)
        self.df['very_cleaned_content'] = cleaned_words
        print('전처리 끝이에용')
        self.df.info()
        self.df.head()

    def modeling(self):
        print('모델링 들어갑니다')
        with open('./datasets/tokenizer.pickle', 'rb') as f:
            token = pickle.load(f)
        X = self.df['very_cleaned_content']
        Xtoken = token.texts_to_sequences(X)
        max = 2684
        Xpad = pad_sequences(Xtoken, max)
        path = './datasets/LSTM_MODEL_new.h5'
        model = load_model(path)
        self.df['LSTM_data'] = 0
        predict = model.predict(Xpad)
        self.df['LSTM_data'] = predict
        data_input = self.df[
            ['image_count', 'video_count', 'link_count', 'content_count', 'hash_tag_count', 'blog_tag_count',
             'bluetooth_word_count', 'cleaned_content_count', 'LSTM_data']]
        with open('./datasets/MinMax.pickle', 'rb') as f:
            minmaxscaler = pickle.load(f)
        scaled_input_data = minmaxscaler.transform(data_input)
        path = './datasets/DNN_MODEL.h5'
        model = load_model(path)
        predict = model.predict(scaled_input_data)
        #self.df['predict'] = 0
        self.df['predict'] = np.around(predict)
        self.df['predict'] = self.df['predict'].astype('int64')
        print(self.df.info())
        self.parent.df = self.df
        self.parent.check_df_flag = True

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.rb_len_flag = False
        self.setupUi(self)
        self.setWindowTitle('NAVER BLOG')
        self.initUI()
        self.working = False
 
    def initUI(self):
        self.ds = pd.read_csv('./datasets/final_1000.csv')
        self.setStyleSheet("background-color: #ffffff")
        self.setFixedSize(750, 960)
        self.btn_search.setStyleSheet("image:url(search_icon.png); border:0px")
        self.le_search.setStyleSheet("border-color: #ebebeb")
        #길이: 라디오 버튼 연결
        self.rb_20.setChecked(1)
        self.rb_20.clicked.connect(self.rb_len)
        self.rb_30.clicked.connect(self.rb_len)
        self.rb_40.clicked.connect(self.rb_len)
        #추가 키워드: 체크박스 연결
        self.str_keyword = ''
        self.cb_keyword1.stateChanged.connect(self.cb_keyword)
        self.cb_keyword2.stateChanged.connect(self.cb_keyword)
        self.cb_keyword3.stateChanged.connect(self.cb_keyword)
        #검색 버튼 눌렀을 때
        self.btn_search.clicked.connect(self.btn_search_slot)
        #scroll
        self.scrollbar_real = self.tb_real_window.verticalScrollBar()
        self.scrollbar_real.setStyleSheet("background-color: #ebebeb")
        self.scrollbar_model = self.tb_model_window.verticalScrollBar()
        self.scrollbar_model.setStyleSheet("background-color: #ebebeb")
        self.check_df_flag = False
        self.check()

    def rb_len(self):
        self.url_len = 1
        if self.rb_20.isChecked():
            print("url 20개")
            self.url_len = 1 #2p
        elif self.rb_30.isChecked():
            print("url 30개")
            self.url_len = 2 #3p
        elif self.rb_40.isChecked():
            print("url 40개")
            self.url_len = 3 #4p
        else:
            self.url_len = 1
        self.rb_len_flag = True

    def cb_keyword(self): #키워드 추가
        if self.cb_keyword1.isChecked():
            self.str_keyword = self.str_keyword + '+%2B내돈내산'
            print("! '내돈내산' 키워드가 추가되었습니다!")
        if self.cb_keyword2.isChecked():
            self.str_keyword = self.str_keyword + '+%2B내돈주고'
            print("! '내돈주고' 키워드가 추가되었습니다!")
        if self.cb_keyword3.isChecked():
            self.str_keyword = self.str_keyword + '+%2B솔직'
            print("! '솔직' 키워드가 추가되었습니다!")
        print(self.str_keyword)

    def url_compared(self):
        # 크롤링 1차 시작
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome('./chromedriver', options=options)
        driver.implicitly_wait(0.01)

        # len 설정
        if not self.rb_len_flag:
            self.url_len = 1
        elif self.rb_len_flag:
            self.url_len = self.url_len

        # url 비교하는 코드 : 있으면 DataFrame에서 출력, 없으면 crawling
        url_list = []
        title_list = []
        for page in range(0, self.url_len + 1):
            try:
                error = ''  # error message 출력
                url = f'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query={self.search}+%2B블루투스{self.str_keyword}&sm=tab_pge&srchby=all&st=sim&where=post&start={page * 10 + 1}'
                driver.get(url)

                for i in range(1, 11):
                    try:
                        time.sleep(0.02)
                        title = driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').text
                        url_data = driver.find_element_by_xpath(
                            f'// *[ @ id = "sp_blog_{i}"] / dl / dd[3] / span / a[2]').text
                        # print(url_data)
                        url_data = 'https://' + url_data
                        url_list.append(url_data)
                        title_list.append(title)

                    except Exception as e:
                        print('비비디바비디부', e)
                        # 검색어가 없습니다 다른 검색어를 입력해주세요 알림창! 넣어야 함
                        continue

            except Exception as e:
                print(e)
                pass

        df_url = pd.DataFrame({'url': url_list, 'title': title_list})
        # '이어폰 솔직 후기'로 접근 url 5개 겹침 > 출력은 4개
        for i in range(len(df_url.title)):
            if df_url.title[i] in list(self.ds['title']):
                idx = self.ds[self.ds['title'] == df_url.title[i]].index[0]
                # print('ds 인덱스 번호 입니다. :', idx)
                if self.ds['answer'][idx] == 1:
                    str_url = str(self.ds['url'][idx])
                    # 라벨에 어펜드 되는 형식으로 짜기
                    self.tb_real_window.append('<a href="' + str_url + '"target="_blank">' + df_url.title[i] + '</a>')
                    self.tb_real_window.setOpenExternalLinks(True)
                    # print('겹치는 내용 :',df_url.title[i])
                df_url = df_url[df_url.title != df_url.title[i]]  # 겹치는 내용 drop

        df_url.reset_index(inplace=True, drop=True)
        print('df_url 돌릴 데이터')
        df_url.info()
        self.df_url = df_url
        driver.close()

        text = self.tb_real_window.toPlainText().split('\n')
        if text == ['']:
            text = []
        self.lbl_result.setText(f'총 {len(text)}개의 자료가 검색되었습니다.')


    def btn_search_slot(self): #네이버에서 검색하여 블로그로 접속하는 창
        self.check_df_flag = False
        msg = QMessageBox()
        self.search = self.le_search.text() #검색어
        print('검색어',self.search)
        # 검색어가 없을 때 메세지 창 오픈
        if self.search == '':
            msg.setWindowTitle('MessageBox')
            msg.setText('검색어를 입력해주세요.')
            msg.exec()
            return 0
        self.tb_real_window.clear()
        self.tb_model_window.clear()


        '''
        df_url = pd.DataFrame({'url': url_list, 'title':title_list})
        for i in range(len(df_url.title)):
            if df_url.title[i] in list(self.ds['title']):
                idx = self.ds[self.ds['title'] == df_url.title[i]].index[0]
                #print('ds 인덱스 번호 입니다. :', idx)
                if self.ds['answer'][idx] == 1:
                    str_url = str(self.ds['url'][idx])
                    # 라벨에 어펜드 되는 형식으로 짜기
                    self.tb_real_window.append('<a href="' + str_url + '"target="_blank">' + df_url.title[i] + '</a>')
                self.tb_real_window.setOpenExternalLinks(True)
                df_url = df_url[df_url.title != df_url.title[i]]  # 겹치는 내용 drop
        df_url.reset_index(inplace=True, drop=True)
        print('df_url 돌릴 데이터')
        df_url.info()
        self.df_url = df_url
        driver.close()

        text = self.tb_real_window.toPlainText().split('\n')
        if text == ['']:
            text = []
        self.lbl_result.setText(f'총 {len(text)}개의 자료가 검색되었습니다.')
        '''

        # url 비교 메소드
        self.url_compared()

        # thread 작업
        if not self.working:
            self.working = True
        else:
            ans = msg.warning(self, 'Crawling', '진행중인 크롤링을 중단합니다.',QMessageBox.Ok)
            if ans == QMessageBox.Ok:
                self.worker.working = True
        self.worker = Worker(self)
        self.worker.start()
        print('본체에서는 뭐하는지 쓰레드 확인중입니당')
    def check(self):
        if self.check_df_flag == True:
            self.df_predict = self.df[self.df['predict'] == 1]
            print(len(self.df_predict.title))
            self.df_predict.reset_index(inplace=True, drop=True)
            self.lbl_result_2.setText(f'총 {len(self.df_predict.title)}개의 자료가 검색되었습니다.')
            for i in range(len(self.df_predict.title)):
                predict_text = '<a href="' + self.df_predict.url[i] + '"target="_blank">' + self.df_predict.title[i] + '</a>'
                self.tb_model_window.append(predict_text)
            self.tb_model_window.setOpenExternalLinks(True)
        self.check_df_flag == False

    # 창 닫기
    def closeEvent(self, QCloseEvent) :
        ans = QMessageBox.question(self, '종료하기', '종료하시겠습니까?',QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())
