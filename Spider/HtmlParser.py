# encoding:utf-8

# @Author: Rilzob
# @Time: 2019/3/31 下午7:23

import re
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
import time

from Spider.HtmlDownloader import HtmlDownloader


class HtmlParser(object):
    def __init__(self):
        super(HtmlParser, self).__init__()
        self.browser = webdriver.Chrome(
            executable_path='/Users/rilzob/PycharmProjects/SubjectKG/chromedriver'
        )
        self.dropdown_num = 1  # 自动下滚次数

    @staticmethod
    def parser(url):
        if url is None:
            return None
        content = HtmlDownloader().download(url)
        soup = BeautifulSoup(content, 'html.parser')
        # school_name = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1').get_text()  # 学校名称
        # en_school_name = soup.find('dd', class_='lemmaWgt-lemmaTitle-subTitle').find('h3').get_text()  # 学校英文名
        # school_tag = soup.find('dd', class_="lemmaWgt-lemmaTitle-keyInfo lemmaWgt-lemmaTitle-keyInfo-with-link").get_text().strip()  # 学校标签
        old_school_introduce = soup.find('div', class_='lemma-summary').get_text().strip('\n')  # 学校简介
        pattern = re.compile(r'\[[0-9-]*\]')
        new_school_introduce = re.sub(pattern, '', old_school_introduce)
        # for i in r
        # # base_info1 = soup.find_all('div', class_='dl-baseinfo')[0]
        # # base_info2 = soup.find_all('div', class_='dl-baseinfo')[1]
        # # infoset1 = []
        # # for info in base_info1.select('dd'):
        # #     if isinstance(info, Tag):
        # #         infoset1.append(info.get_text())
        # #     else:
        # #         continue
        # # creation_time = infoset1[0]  # 创办时间
        # # property = infoset1[1]  # 属性
        # # Administration = infoset1[2]  # 主管部门
        #
        # # infoset2 = []
        # # for info in base_info2.select('dd'):
        # #     if isinstance(info, Tag):
        # #         infoset1.append(info.get_text())
        # #     else:
        # #         continue
        # # category = infoset2[0]  # 类别
        # # famous_alumni = infoset2[1]  # 知名校友
        # # official_website = infoset2[2]  # 官网
        #
        # # property_test = soup.select('body > div.body-wrapper.feature.feature_small.collegeSmall > div.feature_poster > div > div.poster-left > div.poster-bottom > div > div:nth-child(1) > dl:nth-child(2) > dd')
        #
        # # html = etree.HTML(content)
        # # property = html.xpath("//html/body/div[4]/div[3]/div/div[1]/div[3]/div/div[1]/dl[2]/text()")  # 属性
        # # print("属性：", property)
        # # Administration = html.xpath('//html/body/div[4]/div[3]/div/div[1]/div[3]/div/div[1]/dl[3]/dd/a/text()')  # 主管部门
        #
        # # property = soup.find('div', class_)

        basic_info_dict = {}  # 所有信息所存放的dict

        dict_school_url = {}
        dict_school_url['baike_url'] = url
        basic_info_dict.update(dict_school_url)
        # dict_school_tag = {}
        # dict_school_tag['school_tag'] = school_tag
        # basic_info_dict.update(dict_school_tag)
        dict_school_introduce = {}
        dict_school_introduce['school_introduce'] = new_school_introduce
        basic_info_dict.update(dict_school_introduce)

        basic_info = soup.find('div', class_='basic-info cmn-clearfix')
        dt_list = []
        for dt in basic_info.find_all('dt'):
            if isinstance(dt, Tag):
                dt_list.append(dt.get_text().strip('\n').replace('\xa0', '').replace('\n', '|'))
            else:
                continue
        dd_list = []
        for dd in basic_info.find_all('dd'):
            if isinstance(dd, Tag):
                dd_list.append(dd.get_text().strip('\n').replace('\xa0', '').replace('\n', '|'))
            else:
                continue

        for i in range(len(dt_list)):
            dict = {}
            dict[dt_list[i]] = dd_list[i]
            basic_info_dict.update(dict)

        return basic_info_dict

    def main_parse(self):
        # 985工程url
        url = 'https://baike.baidu.com/item/985%E5%B7%A5%E7%A8%8B/1077915?fromtitle=985&fromid=7809859&fr=aladdin'

        # url = 'https://baike.baidu.com/item/%E6%9C%AC%E7%A7%91%E9%99%A2%E6%A0%A1/17606093'
        if url is None:
            return None
        # self.browser.get(url)
        # for i in range(self.dropdown_num):  # 下滚次数
        #     self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);"
        #                                   "var lenOfPage=document.body.scrollHeight;"
        #                                   "return lenOfPage")  # 执行下拉操作刷新页面
        content = HtmlDownloader().download(url)
        # print(content)
        # content1 = self.browser.page_source
        # print(content1)
        # self.browser.quit()
        soup = BeautifulSoup(content, 'html.parser')
        school_set = soup.find_all('td', align='center')
        school_url_list = []
        school_name_list = []
        for school in school_set:
            # school.find('a')['href'])
            # print(str(school.find('a')['href']))
            # school_url = 'https://baike.baidu.com' + str(school.find_all('a')['href'])
            if school.find('a') is not None:
                school_url_list.append('https://baike.baidu.com' + school.find('a')['href'])
                school_name_list.append(school.find('a').get_text())
            else:
                continue
            # print("school_url", school_url)

        whole_info = {}
        for i in range(len(school_url_list)):
            school_dict = {}
            school_dict[school_name_list[i]] = HtmlParser().parser(school_url_list[i])
            whole_info.update(school_dict)
            time.sleep(1)
        return whole_info

    def new_main_parse(self):
        url = 'https://baike.baidu.com/wikitag/taglist?tagId=37678&fromLemma=true'
        if url is None:
            return None
        content = ''
        self.browser.get(url)
        for i in range(1, 38):  # 下滚次数
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                                          "var lenOfPage=document.body.scrollHeight;"
                                          "return lenOfPage")  # 执行下拉操作刷新页面
            time.sleep(3)
            content = content + self.browser.page_source
            self.browser.find_element_by_css_selector('#waterfall-horPagerBox > div > a.pTag.next').click()
            print('i: ', i)
            # time.sleep(3)
        soup = BeautifulSoup(content, 'html.parser')
        school_set = soup.find_all('div', class_='waterFall_item fromLemma')
        school_url_list = []
        school_name_list = []
        for school in school_set:
            if school.find('a') is not None:
                school_url_list.append(school.find('a')['href'])
                school_name_list.append(school.find('div', class_='waterFall_content_title').get_text())
            else:
                continue
            # print("school_url", school_url)

        whole_info = {}
        for i in range(len(school_url_list)):
            school_dict = {}
            school_dict[school_name_list[i]] = self.parser(school_url_list[i])
            whole_info.update(school_dict)
            time.sleep(1)
        return whole_info

