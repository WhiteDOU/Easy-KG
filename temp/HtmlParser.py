from bs4 import BeautifulSoup, element

class HtmlParser(object):

    # 返回爬虫结果
    def parser(self, page_url, html_cont, ulist):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        # new_data, new_table = self._get_new_data(page_url, soup)
        new_data = self._get_new_data(page_url, soup, ulist)
        # return new_data, new_table
        return new_data

    # 从给定的url和html数据中，按格式获取需要的数据
    def _get_new_data(self, page_url, soup, ulist):
        data = {}
        # table = []
        # title
        # data['主题'] = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1').get_text()
        # summary
        # summary_list = soup.find('div', class_="lemma-summary").find_all('div', class_="para")
        # data['概述'] = []
        # for para in summary_list:
        #     data['概述'].append(para.get_text())

        data['url'] = page_url
        # title
        data['主题'] = []
        try:
            # data['主题'] = soup.find('div', class_="p_name").get_text()
            theme = soup.find('div', class_="p_name")
        except AttributeError:
            print(str(print(theme)))
        else:
            data['主题'].append(theme.get_text())
        # ID
        data['id'] = soup.find('span', class_="p_scholarID_id").get_text()
        # 工作单位
        data['工作单位'] = soup.find('div', class_="p_affiliate").get_text()
        # oth_list
        data['被引次数'] = []
        data['成果数'] = []
        data['H指数'] = []
        data['G指数'] = []
        oth_list = soup.find_all('p', class_="p_ach_num")
        # for oth in oth_list:
        data['被引次数'].append(oth_list[0].get_text())
        data['成果数'].append(oth_list[1].get_text())
        data['H指数'].append(oth_list[2].get_text())
        data['G指数'].append(oth_list[3].get_text())
        # 领域
        data['领域'] = []
        #     data['领域'] = soup.find('span', class_="person_domain person_text").get_text()
        task = soup.find('span', class_="person_domain person_text")
        if task is not None:
            data['领域'].append(task.get_text())
        # 合作者
        data['合作者'] = []
        # colla_list = soup.find('div', class_="co_authorlist").find_all('div', class_="co_author_item")
        colla_list = soup.find_all('a', class_="au_name")
        for colla in colla_list:
            # colla_name = soup.find('span', class_="au_info").find('a', class_="au_name")
            # data['合作者'].append(colla_name.get_text())
            data['合作者'].append(colla.get_text())
        # 合作者链接
        # data['合作者链接'] = []
        co_list = soup.find_all('a', class_="au_name")
        for sts in co_list:
            flag = 1
            plink = str('http://xueshu.baidu.com') + sts.get("href")
            for item in ulist:
                if item == plink:
                    flag = 0
                    break
            if flag == 1:
                ulist.append(plink)
            # ulist.append(str('http://xueshu.baidu.com') + sts.get("href"))
        # 合作单位
        data['合作单位'] = []
        set_list = soup.find_all('span', class_="au_label")
        for sts in set_list:
            data['合作单位'].append(sts.get_text())
        #合作机构
        data['合作机构'] = []
        # collacom_list = soup.find('ul', class_="co_affiliate_list").find_all('span', class_="co_paper_name")
        collacom_list = soup.find_all('span', class_="co_paper_name")
        for com in collacom_list:
            data['合作机构'].append(com.get_text())
        # 论文
        data['论文'] = []
        # paper_list = soup.find('div', class_="in_conternt_reslist").find_all('div', class_="result")
        paper_list = soup.find_all('h3', class_="res_t")
        for res in paper_list:
            # pname = soup.find('h3', class_="res_t").get_text()
            # data['论文'].append(pname)
            data['论文'].append(res.get_text())



        # maincontent = soup.find('div', class_="in_conternt_reslist")
        # tmp = maincontent.contents
        # curh3 = ""
        # curh2 = ""
        #
        # for tag in tmp:
        #     if not isinstance(tag, element.Tag): # 去掉contents换行等字符串
        #         continue
        #     if tag.has_attr('id') and tag['id'] == "open-tag": #去掉最后的标签列
        #         continue
        #
        #     if tag.name == "table":
        #         curta = []
        #         for row in tag:
        #             # print(row)
        #             if row.name == "caption":
        #                 curta.append(["caption", row.get_text()])
        #             elif row.name == "tr":
        #                 curta.append([cell.get_text() for cell in row])
        #         table.append(curta)
        #
        #
        #     elif tag['class'] == ['para-title', 'level-2']:
        #         # print("L2      ", curh2,  curh3)
        #         if curh2 != "" and curh3 != "":
        #             data[curh2][curh3] = data[curh3]
        #             data.pop(curh3)
        #             curh3 = ""
        #
        #         content = tag.contents[1]
        #         curh2 = content.contents[1].string
        #         data[curh2] = {}
        #         # print("h2", curh2)
        #
        #     elif tag['class'] == ['para-title', 'level-3']:
        #         # 把上一部分存到h2中
        #         if curh2 != "" and curh3 != "":
        #             data[curh2][curh3] = data[curh3]
        #             data.pop(curh3)
        #             curh3 = ""
        #
        #         content = tag.contents[1]
        #         curh3 = content.contents[1].string
        #         data[curh3] = ""
        #         # print("h3", curh3)
        #
        #     elif tag['class'] == ['custom_dot',  'para-list', 'list-paddingleft-1']:
        #         if curh2 != "" and curh3 != "":
        #             data[curh2][curh3] = data[curh3]
        #             data.pop(curh3)
        #             curh3 = ""
        #
        #         curh3 = tag.get_text()
        #         data[curh3] = ""
        #         # print("h3", curh3)
        #
        #     elif tag['class'] == ['para']:
        #         contents = tag.contents
        #         for item in contents:
        #             # print(item.name)
        #             if isinstance(item, element.NavigableString):
        #                 # print(item.string, end="")
        #                 if curh3 == "":
        #                     curh3 = "具体内容"
        #                     data[curh3] = ""
        #                 data[curh3] += item.string
        #             elif isinstance(item, element.Tag) and item.name != "sup":
        #                 str = item.string
        #                 if str != None:
        #                     # print(str, end="")
        #                     data[curh3] += item.string
        #
        # return data, table
        return data

