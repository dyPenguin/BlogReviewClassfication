#!/usr/bin/env python
# coding: utf-8

# # real review crawling

# In[1]:


import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
from bs4 import BeautifulSoup


# In[2]:


options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)


# In[3]:


# 댓글 버튼 유무
def is_comment(url_id):
    try:
        driver.find_element_by_xpath(f'//*[@id="Comi{url_id}"]')
        return 1
    except:
        return 0


# In[4]:


# 해시태그 크롤링
def tag_crawling():
    hash_tags = []
    blog_tags = []
    try:
        tags = []
        for i in range(len(driver.find_elements_by_class_name('tag'))):
            tag = driver.find_elements_by_class_name('tag')[i].text
            tags.append(tag.replace('#', ''))
            join_tags = ', '.join(tags)

        if tags == []:
            hash_tags = np.NaN
        else:
            hash_tags = join_tags

    except Exception as e:
        print(e, '!!error1!!')
        return 0

    try:
        blogtags = []
        for j in range(len(driver.find_elements_by_class_name('ell'))):
            blogtag = driver.find_elements_by_class_name('ell')[j].text
            blogtags.append(blogtag.replace('#', ''))
            join_blogtags = ','.join(blogtags)

        if blogtags == []:
            blog_tags = np.NaN
        else:
            blog_tags = join_blogtags

    except Exception as e:
        print(e, 'error2')
        return 0

    return hash_tags, blog_tags


# In[5]:


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


# In[6]:


real = pd.read_excel('./test/fake_review_all.xlsx')

lst_title = []
lst_url = []
lst_content = []
lst_comment = []
lst_image = []
lst_video = []
lst_link = []
lst_hashTag = []
lst_blogTag = []

# for url in range(1, 3):
for url in range(0, real['url'].count()):
    print(f'======================================{url}=====================================')
    try:
        print(url,' 번')
        driver.get(real['url'][url])
        time.sleep(3.5)
        
        # 프레임 링크 전환
        driver.switch_to.frame("mainFrame")
        
        try:
            # 블로그 content
            current_url = driver.current_url
            url_id = current_url.split('/')[-1]
            title = driver.find_element_by_class_name('pcol1').text
            url_ = real['url'][url]
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
        time.sleep(1.5)
        # print(comment)

        # 태그를 list 로 반환
        hashTags, blogTags = tag_crawling()
        time.sleep(1.5)
        
        try: 
            # 이미지 갯수
            image_cnt = len(content.find_elements_by_tag_name('img'))
            print(image_cnt)

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

    except Exception as e:
        print('url error: ', e)
        continue
    
df = pd.DataFrame({'title': lst_title, 'content': lst_content, 'comment': lst_comment,
                   'image_cnt': lst_image, 'video_cnt': lst_video, 'link_cnt': lst_video,
                   'hash_tag': lst_hashTag, 'blog_tag': lst_blogTag, 'url': lst_url})
df.to_csv('./datasets/IT_crawling_real_review_all.csv')
        
driver.close()


# In[8]:


df.info()


# In[9]:


df.head()

