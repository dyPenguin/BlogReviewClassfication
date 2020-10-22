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


options = webdriver.ChromeOptions()
# option.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)


# In[ ]:


lst_keyword = ['블루투스 소정의 받았습니다']

Data = pd.DataFrame()

for keyword in lst_keyword:
    for page in range(1):
        print(f'======================================{page}=====================================')
        error = ''  # error message 출력
        try:
            url = f'https://search.naver.com/search.naver?\
            date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query={keyword}+%2B블루투스&sm=tab_pge&srchby=all&st=sim&where=post&start={page * 10 + 1}'
            driver.get(url)
            time.sleep(3.5)

            lst_title = []
            lst_url = []
            lst_content = []
            lst_comment = []
            lst_image = []
            lst_video = []
            lst_link = []
            lst_hashTag = []
            lst_blogTag = []
            
            df = pd.DataFrame()

            for i in range(1, 11):
                try:
                    title = driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').text
                    print(f'{i}: title: ', title)

                    # 타이틀 클릭
                    driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').click()
                    time.sleep(2.5)

                    # window 탭 이동
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2.5)

                    # 프레임 링크 전환
                    driver.switch_to.frame("mainFrame")
                    time.sleep(1.5)
                    
                    # 블로그 content
                    current_url = driver.current_url
                    url_id = current_url.split('/')[-1]
                    content = contents_cralwing()
                    if content == 'error': raise Exception('contents error')
                        
                    # 댓글 버튼의 유무
                    comment = is_comment(url_id)
                    time.sleep(1.0)
                    # print(comment)
                    
                    # 태그를 list 로 반환
                    hashTags, blogTags = tag_crawling()
                    time.sleep(1.0)
                    
                    try: 
                        # 이미지 갯수
                        image = len(driver.find_elements_by_class_name('se-image-resource'))
                        time.sleep(1.0)
                        # print(image)
                        
                        # 비디오 갯수
                        video = len(driver.find_elements_by_class_name('u_rmcplayer_control_bg'))
                        time.sleep(1.0)
                        # print(video)
                        
                        # 링크 갯수
                        link1 = len(driver.find_elements_by_class_name("se-link"))  
                        link2 = len(driver.find_elements_by_class_name("se-oglink-url"))
                        links = (link1 + link2)
                        # print(links)
                        
                        lst_image.append(image)
                        lst_video.append(video)
                        lst_link.append(links)
                        
                    except Exception as e:
                        print('Len error: ', e)
                        lst_image.append(0)
                        lst_video.append(0)
                        lst_link.append(0)
                        pass

                    lst_title.append(title)
                    lst_url.append(current_url)
                    lst_content.append(content.text)
                    lst_comment.append(comment)
                    lst_hashTag.append(hashTags)
                    lst_blogTag.append(blogTags)

                    df = pd.DataFrame({'title': lst_title, 'content': lst_content, 'comment': lst_comment,
                                       'image_cnt': lst_image, 'video_cnt': lst_video, 'link_cnt': lst_video,
                                       'hash_tag': lst_hashTag, 'blog_tag': lst_blogTag, 'url': lst_url})
                    df.to_csv(f'./datasets/IT_crawling_{keyword}_page{page}.csv')
                    # print(df.info())
                     
                except Exception as e:
                    print('error1: ', e)
                    continue
                
                finally:
                    print('.')
                    driver.close()
                    time.sleep(2.0)
                    driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(e)
            continue
        
        finally:
            print('> 끝!')
            print(df.info())
            Data = pd.concat([Data, df], ignore_index=True)
            Data.to_csv(f'./datasets/IT_crawling_all_{keyword}.csv')
        
driver.close()


# In[ ]:


Data.info()

