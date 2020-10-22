#!/usr/bin/env python
# coding: utf-8

# # fake URL review crawling

# In[ ]:


import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
from bs4 import BeautifulSoup


# In[ ]:


options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)


# In[ ]:


# 댓글 버튼 유무
def is_comment(url_id):
    try:
        driver.find_element_by_xpath(f'//*[@id="Comi{url_id}"]')
        return 1
    except:
        return 0


# In[ ]:


# 해시태그 개수
def tag_counts():
    hashtag_cnt = 0
    blogtag_cnt = 0

    try:
        hashtag_cnt = len(driver.find_elements_by_class_name('tag'))

    except Exception as e:
        print(e,'error1!!')

    try:
        blogtag_cnt = len(driver.find_elements_by_class_name('ell'))

    except Exception as e:
        print(e,'error2')
    
    return hashtag_cnt, blogtag_cnt


# In[ ]:


# 블로그 content
def contents_cralwing():
    content = 'error'
    # 기존 블로그
    try:
        content = driver.find_element_by_class_name("se-main-container")
        time.sleep(1.5)
        # print(content)
        # print(current_url)
        return content
    except:
        pass
    
    # 예전 블로그
    try:
        content = driver.find_element_by_id("postViewArea")
        return content
    except:
        pass

    return content


# In[ ]:


fake = pd.read_excel('./datasets/fake_review_all.xlsx') #### 파일명 확인 ####

lst_title = []
lst_url = []
lst_content = []
lst_comment = []
lst_image = []
lst_video = []
lst_link = []
lst_hashTag = []
lst_blogTag = []
cnt = 0

# for url in range(1, 5):
for url in range(0, fake['url'].count()):
    print(f'==========================={url} 번==============================')
    try:
        driver.get(fake['url'][url])
        time.sleep(3.0)
        
        # 프레임 링크 전환
        driver.switch_to.frame("mainFrame")
        
        try:
            # 블로그 content
            current_url = driver.current_url
            url_id = current_url.split('/')[-1]
            title = driver.find_element_by_class_name('pcol1').text
            url_ = fake['url'][url]
            content = contents_cralwing()
            if content == 'error': raise Exception('contents error')
            
            lst_title.append(title)
            lst_content.append(content.text)
            # print(content.text)
            
        except Exception as e:
            print('content error')
            continue
        
        # 댓글 버튼의 유무
        comment = is_comment(url_id)
        time.sleep(1.0)
        # print(comment)

        # 태그 갯수
        hashTags, blogTags = tag_counts()
        time.sleep(1.0)
        
        try: 
            # 이미지 갯수
            image_cnt = len(content.find_elements_by_tag_name('img'))
            # print(image_cnt)

            # 비디오 갯수
            video_cnt = len(driver.find_elements_by_class_name('u_rmcplayer_control_bg'))
            time.sleep(1.0)
            # print(video)

            # 링크 갯수
            link1 = len(driver.find_elements_by_class_name("se-link"))  
            link2 = len(driver.find_elements_by_class_name("se-oglink-url"))
            links_cnt = (link1 + link2)
            time.sleep(1.0)
            # print(links_cnt)

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
        lst_comment.append(comment)
        lst_hashTag.append(hashTags)
        lst_blogTag.append(blogTags)
        cnt += 1

    except Exception as e:
        print('url error: ', e)
        continue
    print('.')

df = pd.DataFrame({'title': lst_title, 'content': lst_content, 'comment': lst_comment,
                   'image_count': lst_image, 'video_count': lst_video, 'link_count': lst_video,
                   'hash_tag_count': lst_hashTag, 'blog_tag_count': lst_blogTag, 'url': lst_url})
df.to_csv(f'./datasets/IT_crawling_fake_review_all_{cnt}.csv')
df.info()
        
driver.close()




