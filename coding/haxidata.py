#!/usr/bin/env python# -*- coding: utf-8 -*-# @Time    : 2018/6/11 下午10:19# @Author  : ziyi# @File    : haxidata.py# @Software: PyCharm# -*- coding: utf-8 -*-#爬取投资界：http://www.pedaily.cn/；# 巴比特：http://www.8btc.com/；# 36氪:http://36kr.com/newsflashes;# 雷锋网：https://www.leiphone.com/category/aijuejinzhi；https://www.leiphone.com/category/sponsor；# 人工智能产业新闻：http://ai.ofweek.com/CATList-201700-8100-ai.html# QQtoplist：http://news.qq.com/# 钛媒体：http://www.tmtpost.com/tag/299106# 科技资讯：http://www.ailab.cn/news/tech/# 界面新闻：http://www.jiemian.com/# 澎湃新闻：http://www.thepaper.cn/# 界面新闻：http://www.jiemian.com/# http://www.kejixun.com/tags/dashuju_659大数据网站# http://www.kejixun.com/tags/rengongzhineng_772人工智能标签# http://www.kejixun.com/tags/ai_64787标签aiimport copyimport datetimefrom urllib.parse import urlencodeimport osimport pandas as pdimport reimport requestsfrom selenium import webdriverfrom selenium.common.exceptions import TimeoutExceptionfrom selenium.webdriver.common.by import Byfrom selenium.webdriver.support.ui import WebDriverWaitfrom selenium.webdriver.support import expected_conditions as ECimport timefrom pyquery import PyQuery as pqfrom requests.exceptions import RequestExceptionfrom faker import Factory #它可以生成很多模拟的数据，如user-agentf = Factory.create()headers = {'User-Agent': f.user_agent()}def get_html(url):    try:        response = requests.get(url, headers=headers)        if response.status_code == 200:            html = response.text            doc = pq(html)  # 设置解析器为“lxml”            return doc        else:            print('获取不到', url, response.status_code)            return None    except RequestException as e:        print('获取不到', url, e)        return Nonedef get_btc():    url = 'http://www.8btc.com/sitemap'    df = pd.DataFrame({})    doc = get_html(url)    # print(doc)    title_list = doc('li.itm.itm_new').items()    contents = {}    n = 1    for title in title_list:        if n > 20:            break        contents['header'] = title('a').attr('title')        contents['url'] = 'http://www.8btc.com' + title('a').attr('href')        # print(title('p span:nth-child(3)').text())        contents['pub_time'] = title('p span:nth-child(3)').text()        if contents['url']:            time.sleep(5)            detail_doc = get_html(contents['url'])            contents['views'] = detail_doc('.single-crumbs.clearfix span.pull-right.fa-eye-span').text()        print(contents)        df = df.append(contents, ignore_index=True)        n = n + 1    return dfdef get_pedaily():    url = 'http://www.pedaily.cn/first/'    df = pd.DataFrame({})    doc = get_html(url)    title_list = doc('#firstnews-list ul').items()    contents = {}    for title in title_list:        if title('span.time.date').text() == "0:00":            break        contents['header'] = title('a').attr('title')        contents['url'] = title('a').attr('href')        # print(title('p span:nth-child(3)').text())        contents['pub_time'] = title('span.time.date').text()        print(contents)        df = df.append(contents, ignore_index=True)    return dfdef get_leiphone():    urls = ['https://www.leiphone.com/category/aijuejinzhi', 'https://www.leiphone.com/category/sponsor']    df = pd.DataFrame({})    for url in urls:        doc = get_html(url)        # print(doc)        contents_div = doc('ul.clr li').items()        contents = {}        for content in contents_div:            if '昨天' in content('.word .time').text():                break            contents['header'] = content('.word h3 a').attr('title').encode('gbk', 'ignore').decode('gbk')            contents['url'] = content('.word h3 a').attr('href')            contents['brief'] = content('.word .des').text().encode('gbk', 'ignore').decode('gbk')            # print(title('p span:nth-child(3)').text())            contents['pub_time'] = content('.word .time').text()            contents['type'] = doc('body div.lph-pageList.list-pageList h1').text().encode('gbk', 'ignore').decode('gbk')            print(contents)            df = df.append(contents, ignore_index=True)    return dfdef get_ofweek():    url = 'http://ai.ofweek.com/CATList-201700-8100-ai.html'    df = pd.DataFrame({})    doc = get_html(url)    contents_div = doc('.main-cont-left.w640 .content').items()    contents = {}    for content in contents_div:        if '小时前' not in content('span:eq(4)').text():            break        contents['header'] = content('.top-title a').text()        contents['url'] = content('.top-title a').attr('href')        # contents['content'] = content('.word .des').text()        # print(title('p span:nth-child(3)').text())        contents['pub_time'] = content('span:eq(4)').text()        # contents['type'] = doc('body div.lph-pageList.list-pageList h1').text()        print(contents)        df = df.append(contents, ignore_index=True)    return dfdef get_tmtpost(now):    url = 'http://www.tmtpost.com/tag/299106'    df = pd.DataFrame({})    doc = get_html(url)    contents_div = doc('.mod-article-list.clear ul li').items()    contents = {}    for content in contents_div:        pub_time = re.search(r'\d{4}-\d{2}-\d{2}', content('span.author').text().strip()).group()        print(now)        print(pub_time)        if pub_time != now:            break        contents['header'] = content('.cont a').attr('title').encode('gbk', 'ignore').decode('gbk')        contents['url'] = 'http://www.tmtpost.com' + content('.cont a').attr('href')        contents['brief'] = content('p.intro').text()        # print(title('p span:nth-child(3)').text())        contents['pub_time'] = pub_time        # contents['type'] = doc('body div.lph-pageList.list-pageList h1').text()        print(contents)        df = df.append(contents, ignore_index=True)    return df# 启动浏览器，executable_path路径要根据自己chromedriver.exe的位置更改# driver = webdriver.Chrome(executable_path=r'/Users/lvzeqin/Applications/chromedriver')driver = webdriver.Chrome()# 设置浏览器窗口位置及大小# driver.set_window_rect(x=0, y=0, width=667, height=748)# 设定页面加载限制时间driver.set_page_load_timeout(30)# 设置锁定标签等待时长wait = WebDriverWait(driver, 20)# 打开登陆网址def get_36k():    url = 'http://36kr.com/newsflashes'    driver.get(url)    # 模拟js操作向下滑动窗口到最底部    driver.execute_script('window.scrollTo(0, 0.8*document.body.scrollHeight)')    time.sleep(3)    driver.execute_script('window.scrollTo(0, 0.8*document.body.scrollHeight)')    time.sleep(3)    driver.execute_script('window.scrollTo(0, 0.8*document.body.scrollHeight)')    time.sleep(5)    df = pd.DataFrame({})    title_list = driver.find_elements_by_css_selector('.conter-wrapper .fast_section_list .sameday_list li')    contents = {}    for title in title_list:        # print(title)        contents['header'] = title.find_element_by_css_selector('h2 span').text.encode('gbk','ignore').decode('gbk')        contents['brief'] = title.find_element_by_css_selector('.fast_news_content span').text.encode('gbk', 'ignore').decode('gbk')        contents['url'] = title.find_element_by_css_selector('.fast_news_content a').get_attribute('href')        # print(title('p span:nth-child(3)').text())        contents['pub_time'] = title.find_element_by_css_selector('div.publish-datetime span').get_attribute('title')        print(contents)        df = df.append(contents, ignore_index=True)    return dfdef get_jiemian():    content = {}    df = pd.DataFrame({})    url = 'http://www.jiemian.com/'    driver.get(url)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(5)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(3)    driver.execute_script('window.scrollTo(document.body.scrollHeight,0)')    time.sleep(5)    # 依次获取每个新闻分类的数据列表集    tianxia_list = driver.find_elements_by_xpath('//*[@id="centerAjax"]/div[2]/div[@class="news-view "]/div[@class="news-header"]/h3/a')    china_list = driver.find_elements_by_xpath('//*[@id="centerAjax"]/div[4]/div[@class="news-view "]/div[@class="news-header"]/h3/a')    hongguan_list = driver.find_elements_by_xpath ('//*[@id="centerAjax"]/div[6]/div[@class="news-view "]/div[@class="news-header"]/h3/a')    most_popular = driver.find_elements_by_xpath ('//*[@id="centerAjax"]/div[8]/ul/li/a')    jmedia = driver.find_elements_by_xpath ('//*[@id="jmediaAjax"]/div[@class="media-news"]/div[@class="media-header"]/h3/a')    # jmedia_introduction = driver.find_elements_by_xpath('//*[@id="jmediaAjax"]/div[class="media-news"]/div[@class="media-main"]/p')    classes_name = ['天下', '中国', '宏观', '最热', '媒体']    news_list = [tianxia_list, china_list, hongguan_list,most_popular,jmedia]    for i,news_classes in enumerate(news_list):        print (i, classes_name[i])        for news in news_classes:            content['header'] = news.text.encode('gbk', 'ignore').decode('gbk')            content['news_url'] = news.get_attribute('href')            content['classes_name'] = classes_name[i]            content['pubtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))            print(content)            df = df.append(content, ignore_index=True)    return dfdef get_aibot():    content = {}    df = pd.DataFrame({})    url = 'http://www.aihot.net/index.html'    driver.get(url)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep (3)    driver.execute_script('window.scrollTo(document.body.scrollHeight,200)')    time.sleep (5)    headers_list = driver.find_elements_by_xpath('//*[@id="main-wrap-left"]/div[1]/article[@class="home-blog-entry col span_1 clr"]/div[1]/h3/a')    for i,news in enumerate(headers_list):        content['header'] = news.text.encode('gbk', 'ignore').decode('gbk')        content['news_url'] = news.get_attribute('href')        content['brief'] = driver.find_element_by_xpath('//*[@id="main-wrap-left"]/div[1]/article[{}]/div[1]/p'.format(i+1)).text.encode('gbk', 'ignore').decode('gbk')        content['classes_name'] = '人工智能'        content['pubtime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))        print (content)        df = df.append(content, ignore_index=True)    return dfdef get_pengpai():    content = {}    df = pd.DataFrame({})    url = 'https://www.thepaper.cn/'    driver.get (url)    for i in range(7):        driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')        time.sleep (1)    time.sleep (3)    # driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')    # time.sleep (5)    headers_list = driver.find_elements_by_xpath('//*[@id="masonryContent"]/div[@class="news_li"]/h2/a')    print(len(headers_list))    print(headers_list)    for i,news in enumerate(headers_list):        try:            content['header'] = news.text.encode('gbk','ignore').decode('gbk')            content['news_url'] = news.get_attribute('href')            content['brief'] = driver.find_element_by_xpath('//*[@id="masonryContent"]/div[{}]/p'.format(i+1)).text.encode('gbk','ignore').decode('gbk')            content['classes_name'] = '澎湃新闻'            content['pubtime'] = driver.find_element_by_xpath('//*[@id="masonryContent"]/div[{}]/div[@class="pdtt_trbs"]/span[1]'.format(i+1)).text.encode('gbk','ignore').decode('gbk')            content['savetime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime(time.time ()))            print(content)            df = df.append(content, ignore_index=True)        except Exception as e:            print(e)    return dfdef get_iyiou():    content = {}    df = pd.DataFrame ({})    url = 'https://www.iyiou.com/breaking/'    driver.get (url)    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')    time.sleep (3)    driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')    time.sleep (2)    # driver.find_element_by_xpath('/html/body/div[1]/div[5]/div/div[1]/div/div/div/div[2]/ul/li[3]/a').click()    # time.sleep(3)    headers_list = driver.find_elements_by_xpath('//ul[@class="list_box_zx"]/li/div/a/h2')    # headers = driver.find_element_by_xpath('//*[@id="root101"]/li[1]/div/div[2]/h3/a').text    # print(headers)    for i,news in enumerate(headers_list):        if i != 0:            content['header'] = news.text.encode('gbk','ignore').decode('gbk')            content['news_url'] = news.find_element_by_xpath('//ul[@class="list_box_zx"]/li[{}]/div/a'.format(i+1)).get_attribute ('href')            content['classes_name'] = '每日资讯'            content['savetime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))            if i == 15:                break            print (content)            df = df.append (content, ignore_index=True)    return dfdef get_qqnews():    content = {}    df = pd.DataFrame ({})    url = 'http://news.qq.com/articleList/rolls/'    driver.get (url)    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')    time.sleep (5)    driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')    time.sleep (5)    headers_list = driver.find_elements_by_xpath('//*[@id="listInfo"]/ul[@class="titMode"]/li/a')    for i,news in enumerate(headers_list):        print(i)        content['header'] = news.find_element_by_xpath ('//*[@id="listInfo"]/ul[@class="titMode"]/li[{}]/a/span[@class="txt"]'.format(i + 1)).text.encode ('gbk','ignore').decode ('gbk')        content['news_url'] = news.get_attribute ('href')        content['pubtime'] = news.find_element_by_xpath ('//*[@id="listInfo"]/ul[@class="titMode"]/li[{}]/a/span[@class="time"]'.format (i + 1)).text.encode ('gbk','ignore').decode('gbk')        content['classes_name'] = news.find_element_by_xpath ('//*[@id="listInfo"]/ul[@class="titMode"]/li[{}]/a/strong'.format (i + 1)).text.encode ('gbk','ignore').decode('gbk')        content['savetime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))        print (content)        df = df.append (content, ignore_index=True)    return dfdef get_iresearch():    content = {}    df = pd.DataFrame ({})    url = 'http://news.iresearch.cn/'    driver.get (url)    driver.execute_script ('window.scrollTo(0, document.body.scrollHeight)')    time.sleep (3)    driver.execute_script ('window.scrollTo(document.body.scrollHeight,200)')    time.sleep (5)    headers_list = driver.find_elements_by_xpath('//*[@id="root101"]/li/div/div[2]/h3/a')    for i,news in enumerate(headers_list):        content['header'] = news.text.encode('gbk','ignore').decode('gbk')        content['news_url'] = news.get_attribute ('href')        try:            content['brief'] = driver.find_element_by_xpath('//*[@id="root101"]/li[{}]/div/div[2]/p'.format(i+1)).text.encode('gbk','ignore').decode('gbk')            content['pubtime'] = driver.find_element_by_xpath ('//*[@id="root101"]/li[{}]/div/div[2]/div/div[2]/span'.format (i + 1)).text.encode ('gbk','ignore').decode('gbk')        except Exception as e:            print('没有简介')        content['classes_name'] = '移动资讯'        content['savetime'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))        if i == 15:            break        print (content)        df = df.append (content, ignore_index=True)    return dfdef get_sina():    content = {}    url = 'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%E5%A4%A7%E6%95%B0%E6%8D%AE&from=home&ie=utf-8'    df = pd.DataFrame({})    driver.get(url)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(3)    headers_list = driver.find_elements_by_xpath('//*[@id="result"]//div[@class="r-info r-info2"]')    print(len(headers_list))    for i, news in enumerate(headers_list):        content['header'] = news.find_element_by_css_selector('h2 a').text.encode('gbk','ignore').decode('gbk')        content['news_url'] = news.find_element_by_css_selector('h2 a').get_attribute('href')        content['brief'] = news.find_element_by_css_selector('p.content').text.encode('gbk','ignore').decode('gbk')        content['pubtime'] = news.find_element_by_css_selector('h2 span').text.encode('gbk','ignore').decode('gbk')        content['savetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))        print(content)        df = df.append(content, ignore_index=True)    return dfdef get_tmtpost_data(now):    index = False    df = pd.DataFrame({})    for i in range(1,10):        num = 0        url = 'http://www.tmtpost.com/nictation/{0}'.format(i)        print(url)        doc = get_html(url)        try:            divs = doc('.word_list .day_part div.date time').items()        except Exception:            break        for div in divs:            num = num + 1            print(div.text().strip()[-3:-1])            print(now.split('-')[2])            if div.text().strip()[-3:-1] != now.split('-')[2]:                print('true')                index = True        if num == 1 and index:            break        contents_divs = doc('.word_list .day_part ul li').items()        contents = {}        contents_list = []        for content in contents_divs:            contents['header'] = content('h2.w_tit a').text().encode('gbk', 'ignore').decode('gbk')            contents['url'] = content('h2.w_tit a').attr('href')            contents['brief'] = content('p').text().encode('gbk','ignore').decode('gbk')            # print(title('p span:nth-child(3)').text())            contents['pub_time'] = content('time.source').text().strip()            # contents['type'] = doc('body div.lph-pageList.list-pageList h1').text()            if not contents['header']:                break            print(contents)            contents_list.append(copy.deepcopy(contents))        df = df.append(copy.deepcopy(contents_list), ignore_index=True)        if num > 1:            break        print(i)        time.sleep(5)    return dfdef get_chinanews():    url = 'http://www.chinanews.com/world.shtml'    df = pd.DataFrame({})    doc = get_html(url)    title_list = doc('div.content_list ul li').items()    contents = {}    i = 0    for title in title_list:        i += 1        if i > 50:            break        elif i % 6 == 0:            print(i)            continue        contents['header'] = title('a').text()        contents['url'] = 'http://www.chinanews.com'+title('a').attr('href')        # print(title('p span:nth-child(3)').text())        contents['pub_time'] = title('.dd_time').text()        print(contents)        df = df.append(contents, ignore_index=True)    return dfdef get_chainnews():    content = {}    url = 'https://www.chainnews.com/news/'    df = pd.DataFrame({})    driver.get(url)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(3)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(3)    headers_list = driver.find_elements_by_css_selector('#news_list div.entry.news-list-item')    print(len(headers_list))    for i, news in enumerate(headers_list):        content['header'] = news.find_element_by_css_selector('h2.news-title').text.encode('gbk','ignore').decode('gbk')        content['brief'] = news.find_element_by_css_selector('li.news-content').text.encode('gbk','ignore').decode('gbk')        content['pubtime'] = news.find_element_by_css_selector('.publish-time').text.encode('gbk','ignore').decode('gbk')        content['savetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))        print(content)        df = df.append(content, ignore_index=True)    return dfdef get_btcside():    content = {}    url = 'https://www.btcside.com/posts/'    df = pd.DataFrame({})    driver.get(url)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(3)    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')    time.sleep(3)    headers_list = driver.find_elements_by_css_selector('#scroll section ul li')    print(len(headers_list))    for i, news in enumerate(headers_list):        content['header'] = news.find_element_by_css_selector('h2 a').get_attribute('title').encode('gbk', 'ignore').decode('gbk')        #content['brief'] = news.find_element_by_css_selector('li.news-content').text.encode('gbk', 'ignore').decode('gbk')        content['pubtime'] = news.find_element_by_css_selector('div.left span.date b').text.encode('gbk', 'ignore').decode('gbk')        content['savetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))        print(content)        df = df.append(content, ignore_index=True)    return dfdef save_info(now, contents, name):    df = pd.DataFrame()    df = df.append(contents.copy())    df.to_csv(r'../data/haxinews/{0}/{1}_{0}.csv'.format(now, name), encoding='gbk')def main():    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))    delDir = r'../data/haxinews/'    delList = os.listdir(delDir)    print(delList)    if now not in delList:        os.mkdir(r'../data/haxinews/{}'.format(now))    try:        ofweek = get_ofweek()        save_info(now, ofweek, 'ofweek')    except:        pass    try:        tmtpost = get_tmtpost(now)        save_info(now, tmtpost, 'tmtpost')    except:        pass    try:        aibot = get_aibot()        save_info(now, aibot, 'aibot')    except:        pass    try:        btc = get_btc()        save_info(now, btc, 'btc')    except:        pass    try:        ped = get_pedaily()        save_info(now, ped, 'ped')    except:        pass    try:        tsk = get_36k()        save_info(now, tsk, '36k')    except:        pass    try:        leiphone = get_leiphone()        save_info(now, leiphone, 'leiphone')    except:        pass    try:        jm = get_jiemian()        save_info(now, jm, 'jiemian')    except:        pass    try:        yiou = get_iyiou()        save_info(now, yiou, 'yiou')    except:        pass    try:        qqnews = get_qqnews()        save_info(now, qqnews, 'qqnews')    except:        pass    try:        pengpai = get_pengpai()        save_info(now, pengpai, 'pengpai')    except:        pass    try:        irsearch = get_iresearch()        save_info(now, irsearch, 'irsearch')    except:        pass    try:        sina = get_sina()        save_info(now, sina, 'sina')    except:        pass    try:        tmtpost = get_tmtpost_data(now)        save_info(now, tmtpost, 'tmtpost_data')    except:        pass    try:        chinanews = get_chinanews()        save_info(now, chinanews, 'chinanews_data')    except:        pass    try:        chainnews = get_chainnews()        save_info(now, chainnews, 'chainnews_data')    except:        pass    try:        btcside = get_btcside()        save_info(now, btcside, 'btcside_data')    except:        passif __name__ == '__main__':    main()    driver.quit()