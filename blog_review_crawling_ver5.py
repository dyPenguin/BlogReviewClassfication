#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# In[2]:


# import sys
# sys.path.insert(0, 'usr/lib/chromium-browser/chromedriver')


# In[3]:


options = webdriver.ChromeOptions()
# option.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)


# In[4]:


# 댓글 버튼 유무
def is_comment(url_id):
    try:
        driver.find_element_by_xpath(f'//*[@id="Comi{url_id}"]')
        return 0
    except:
        return 1


# In[5]:


# 해시태그 갯수
def tag_counts():
    hash_tags = []
    blog_tags = []
    try:
        tags = []
        for i in range(len(driver.find_elements_by_class_name('tag'))):
            tag = driver.find_elements_by_class_name('tag')[i].text
            tags.append(tag.replace('#',''))
            join_tags = ', '.join(tags)
        
        if tags == []:
            hash_tags = np.NaN
        else:
            hash_tags = join_tags
            
    except Exception as e:
        print(e,'!!error1!!')
        return 0

    try:
        blogtags = []
        for j in range(len(driver.find_elements_by_class_name('ell'))):
            blogtag = driver.find_elements_by_class_name('ell')[j].text
            blogtags.append(blogtag.replace('#',''))
            join_blogtags = ','.join(blogtags)
        
        if blogtags == []:
            blog_tags = np.NaN
        else:
            blog_tags = join_blogtags
    
    except Exception as e:
        print(e,'error2')
        return 0
    
    return hash_tags, blog_tags


# In[6]:


def writeDate():
    pass


# In[7]:


lst_keyword = ['블루투스 마우스','블루투스 키보드']


Data = pd.DataFrame()


for keyword in lst_keyword:
    for page in range(2):
        print(f'======================================{page}=====================================')
        try:
            url = f'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=            &query={keyword}&sm=tab_pge&srchby=all&st=sim&where=post&start={page*10 + 1}'
            driver.get(url)
            time.sleep(2.5)
            
            lst_title = []
            lst_content = []
            lst_comment = []
            lst_image = []
            lst_video = []
            lst_link = []
            lst_date = []
            lst_category = []
            lst_hashTag = []
            lst_blogTag = []
            
            df = pd.DataFrame()
            
            for i in range(1, 5):
                try:
                    title = driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').text
                    lst_title.append(title)
                    print('title: ', title)
                    
                    # 타이틀 클릭
                    driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').click()
                    time.sleep(2.5)
                    
                    #window 탭 이동
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2.5)
                    
                    # 프레임 링크 전환
                    driver.switch_to.frame("mainFrame")
                    
                    # 블로그 content
                    current_url = driver.current_url
                    url_id = current_url.split('/')[-1]
                    # content = driver.find_element_by_xpath('//*[@id="post-view{0}"]/div'.format(current_url)).text
                    content = driver.find_element_by_class_name("se-main-container").text
                    # print(content)
                    # print(current_url)
                    
                    # 댓글 버튼의 유무
                    comment = is_comment(url_id)
                    # print(comment)
                    
                    # 태그 갯수 -> list로 반환
                    hashTags, blogTags = tag_counts()
                    
                    #블로그 날짜
                    date=driver.find_element_by_class_name("blog2_container").text
                    date=re.sub('[^0-9|.]', '', date)
                    date=date[:-5]
                    print(date)
                    
                    try: 
                        # 이미지 갯수
                        image = len(driver.find_elements_by_class_name('se-image-resource'))  
                        # print(image)
                        
                        # 비디오 갯수
                        video = len(driver.find_elements_by_class_name('u_rmcplayer_control_bg'))  
                        # print(video)
                        
                        # 링크 갯수
                        link1 = len(driver.find_elements_by_class_name("se-link"))  
                        link2 = len(driver.find_elements_by_class_name("se-oglink-url"))
                        links = (link1 + link2)
                        # print(links)
                        
                        # 카테고리 갯수
                        category = driver.find_element_by_class_name('bcc').text 
                        category = re.sub('[^0-9]', '', category)
                        
                        
                        lst_image.append(image)
                        lst_video.append(video)
                        lst_link.append(links)
                        lst_category.append(category)
                        
                    except:
                        lst_image.append(0)
                        lst_video.append(0)
                        lst_link.append(0)
                        lst_category.append(0)

                    lst_content.append(content)
                    lst_comment.append(comment)
                    lst_hashTag.append(hashTags)
                    lst_blogTag.append(blogTags)
                    lst_date.append(date)
                     
                except:
                    continue
                
                finally:
                    print('.')
                    driver.close()
                    time.sleep(2.0)
                    driver.switch_to.window(driver.window_handles[0])

                    df = pd.DataFrame({'title':lst_title, 'content':lst_content, 'comment': lst_comment,
                                       'image_cnt':lst_image, 'video_cnt':lst_video, 'link_cnt':lst_video,
                                       'hash_tag':lst_hashTag, 'blog_tag':lst_blogTag, 'categort_cnt':lst_category,
                                       'date': lst_date})
                    df.to_csv(f'./crawling/IT_crawling_{keyword}_page{page+1}.csv')
                    # print(df.head())
        
        except Exception as e:
            print(e)
            continue
        
        finally:
            print('> 끝!')
            Data = pd.concat([Data, df], ignore_index=True)
            Data.to_csv(f'./crawling/IT_crawling_{keyword}.csv')
        
driver.close()

Data.head()


# **전처리 시 고려해야할 사항**
# 
# """
# 네이버 동영상 플레이어
# 키보드와 마우스 터치펜으로 아이패드 7세대 활용하기
# 3
# 1,708
# 01
# :
# 45
# 재생시간, 이 동영상의 길이는 1분 45초 입니다.
# 화질 선택 옵션
# 270p 360p 480p 720p
# 화질 선택 옵션
# 접기/펴기 """ ---> 처리

# In[8]:


Data.head()


# In[9]:


Data.info() 

