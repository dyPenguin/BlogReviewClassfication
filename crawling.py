import time
import pandas as pd
from selenium import webdriver

def driver_options():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome('./chromedriver', options=options)

    return driver

# 댓글 버튼의 유무
def is_comment(driver, post_id):
    try:
        driver.find_element_by_xpath(f'//*[@id="Comi{post_id}"]')
        return 1
    except:
        return 0


# 블로그 content
def get_contents(driver):
    # 유형1) 기존 블로그
    try:
        content = driver.find_element_by_class_name("se-main-container")
        return content
    except:
        pass

    # 유형2) 예전 블로그
    try:
        content = driver.find_element_by_id("postViewArea")
        return content
    except:
        pass

    return 0


# 태그 갯수
def tag_counts(driver):
    hashtag_cnt = 0
    blogtag_cnt = 0
    # 해시태그 갯수
    try:
        hashtag_cnt = len(driver.find_elements_by_class_name('tag'))
    except Exception as e:
        print(e, 'hashtagError')

    # 블로그 태그 갯수
    try:
        blogtag_cnt = len(driver.find_elements_by_class_name('ell'))
    except Exception as e:
        print(e, 'error2')

    return hashtag_cnt, blogtag_cnt


# 키워드 검색으로 크롤링
def search_crawling(keyword, start=0, end=1):
    """Returns blog review data
    Args:
        web : Chrome driver
        keyword : Search Keyword
        start (int): Start page
        end (int): End page
    Returns:
        DataFrame (pandas.core.frame.DataFrame): Blog review data
   """
    driver = driver_options()
    review_data = pd.DataFrame()

    # 페이지 설정
    for page in range(start, end + 1):
        print(f'======================================{page}=====================================')
        try:
            url = f'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=\
                    &query={keyword}+%2B블루투스&sm=tab_pge&srchby=all&st=sim&where=\
                    post&start={page * 10 + 1}'
            driver.get(url)
            time.sleep(3.0)

            lst_title = []
            lst_url = []
            lst_content = []
            lst_comment = []
            lst_image = []
            lst_video = []
            lst_link = []
            lst_hashtag = []
            lst_blogtag = []

            data = pd.DataFrame()

            for i in range(1, 11):
                try:
                    title = driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').text
                    print(f'{i}: title: ', title)

                    # 타이틀 클릭
                    driver.find_element_by_xpath(f'//*[@id="sp_blog_{i}"]/dl/dt/a').click()
                    time.sleep(2.5)

                    # window 탭 이동
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(2.0)

                    # 프레임 링크 전환
                    driver.switch_to.frame("mainFrame")
                    time.sleep(1.0)

                    # 블로그 contents
                    contents = get_contents(driver)
                    if not contents:
                        raise Exception('contentsError')
                    # print(contents.text)

                    # 현재 블로그의 URL
                    current_url = driver.current_url
                    post_id = current_url.split('/')[-1]

                    # 댓글 버튼의 유무
                    comment = is_comment(driver, post_id)
                    # print(comment)

                    # 태그 개수
                    hashtags, blogtags = tag_counts(driver)
                    # print(hashtags, blogtags)

                    # 이미지 개수
                    try:
                        image = len(contents.find_elements_by_tag_name('img'))
                        # print(image)
                    except Exception as e:
                        image = 0
                        print(e, 'imageError')

                    # 비디오 개수
                    try:
                        video = len(driver.find_elements_by_class_name('u_rmcplayer_control_bg'))
                        print(video)
                    except Exception as e:
                        video = 0
                        print(e, 'videoError')

                    # 링크 개수
                    try:
                        link1 = len(driver.find_elements_by_class_name("se-link"))
                        link2 = len(driver.find_elements_by_class_name("se-oglink-url"))
                        links = (link1 + link2)
                        # print(links)
                    except Exception as e:
                        links = 0
                        print(e, 'linkError')

                    lst_title.append(title)
                    lst_content.append(contents.text)
                    lst_url.append(current_url)
                    lst_comment.append(comment)
                    lst_hashtag.append(hashtags)
                    lst_blogtag.append(blogtags)
                    lst_image.append(image)
                    lst_video.append(video)
                    lst_link.append(links)

                    data = pd.DataFrame({'title': lst_title, 'content': lst_content, 'comment': lst_comment,
                                         'image_count': lst_image, 'video_count': lst_video,
                                         'link_count': lst_link, 'hash_tag_count': lst_hashtag,
                                         'blog_tag_count': lst_blogtag, 'url': lst_url})

                except Exception as e:
                    print('blogError', e)
                    continue

                finally:
                    print('.')
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print('pageError: ', e)
            continue

        finally:
            print(data.info())
            data.to_csv(f'./datasets/IT_crawling_{keyword}_page{page}.csv')
            review_data = pd.concat([review_data, data], ignore_index=True)
            print('> 끝!')
    driver.close()

    return review_data


# URL 로 크롤링
def url_crawling(url_data, count=None):
    if not count:
        count = url_data['url'].count()
    lst_title = []
    lst_url = []
    lst_content = []
    lst_comment = []
    lst_image = []
    lst_video = []
    lst_link = []
    lst_hashtag = []
    lst_blogtag = []

    driver = driver_options()
    review_data = pd.DataFrame()

    for url in range(1, count + 1):
        try:
            driver.get(url_data['url'][url])
            time.sleep(3.0)

            # 프레임 링크 전환
            driver.switch_to.frame("mainFrame")

            # 현재 블로그의 URL
            current_url = driver.current_url
            post_id = current_url.split('/')[-1]

            # 리뷰 제목
            title = driver.find_element_by_class_name('pcol1').text
            print(f'{url}. \n', title)

            # 블로그 contents
            contents = get_contents(driver)
            if not contents:
                raise Exception('contentsError')
            # print(contents.text)

            # 댓글 버튼의 유무
            comment = is_comment(driver, post_id)
            # print(comment)

            # 태그 개수
            hashtags, blogtags = tag_counts(driver)
            # print(hashtags, blogtags)

            # 이미지 개수
            try:
                image = len(contents.find_elements_by_tag_name('img'))
                # print(image)
            except Exception as e:
                image = 0
                print(e, 'imageError')

            # 비디오 개수
            try:
                video = len(driver.find_elements_by_class_name('u_rmcplayer_control_bg'))
                # print(video)
            except Exception as e:
                video = 0
                print(e, 'videoError')

            # 링크 개수
            try:
                link1 = len(driver.find_elements_by_class_name("se-link"))
                link2 = len(driver.find_elements_by_class_name("se-oglink-url"))
                links = (link1 + link2)
                # print(links)
            except Exception as e:
                links = 0
                print(e, 'linkError')

            lst_title.append(title)
            lst_content.append(contents.text)
            lst_url.append(current_url)
            lst_comment.append(comment)
            lst_hashtag.append(hashtags)
            lst_blogtag.append(blogtags)
            lst_image.append(image)
            lst_video.append(video)
            lst_link.append(links)

            data = pd.DataFrame({'title': lst_title, 'content': lst_content, 'comment': lst_comment,
                                 'image_count': lst_image, 'video_count': lst_video,
                                 'link_count': lst_link, 'hash_tag_count': lst_hashtag,
                                 'blog_tag_count': lst_blogtag, 'url': lst_url})
        except Exception as e:
            print(e)
            if WindowsError:
                break
            continue

        finally:
            print('> 끝')
    driver.close()

    review_data = pd.concat([review_data, data], ignore_index=True)
    cnt = len(review_data)
    review_data.to_csv(f'./datasets/IT_url_crawling_review_all_{cnt}.csv')
    print(review_data.info())


if __name__ == '__main__':
    # 여기만 변경 #
    lst_keyword = ['블루투스 이어폰 내돈내산']
    start, end = 1, 4

    for keyword in lst_keyword:
        review_data = search_crawling(keyword, start, end)
        print(review_data.info())
        review_data.to_csv(f'./datasets/IT_crawling_{keyword}_total.csv')

    """url crawling
    # 파일명 확인 #
    start = time.time()
    real = pd.read_excel('./datasets/real_review_all.xlsx')
    url_crawling(real, 10)

    print("time :", time.time() - start)
    """
