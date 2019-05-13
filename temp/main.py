from HtmlDownload import *
from HtmlParser import *
import json
import time

def output_dict(file, data):
    with open(file, "w", encoding="utf-8") as f:
        jsonDumpsIndentStr = json.dumps(data, ensure_ascii=False, indent=1)
        f.write(jsonDumpsIndentStr)
    return

# def output_table(file, table):
#     with open(file, "w", encoding="utf-8") as f:
#         jsonDumpsIndentStr = json.dumps(list(table), indent=1, ensure_ascii=False)
#         f.write(jsonDumpsIndentStr)
#     return

def main():
    #浙江大学
    # school = "浙江大学"
    # url = 'https://baike.baidu.com/item/%E6%B5%99%E6%B1%9F%E5%A4%A7%E5%AD%A6'
    #东北大学
    # school = "东北大学"
    # url = 'https://baike.baidu.com/item/%E4%B8%9C%E5%8C%97%E5%A4%A7%E5%AD%A6/18014'

    # 高玉堂
    # name = "高玉堂"
    # url = 'http://xueshu.baidu.com/scholarID/CN-BT73WSNJ'

    name = "scholar"
    i = 0
    # url_list
    url_list = []
    url_list.append('http://xueshu.baidu.com/scholarID/CN-BT73WSNJ')
    url_list.append('http://xueshu.baidu.com/scholarID/CN-B3742FWJ')
    url_list.append('http://xueshu.baidu.com/scholarID/CN-B0746Q8J')
    url_list.append('http://xueshu.baidu.com/scholarID/CN-B97472MJ')
    url_list.append('http://xueshu.baidu.com/scholarID/CN-BN733MNJ')

    download = HtmlDownloader()
    parser = HtmlParser()

    for item in url_list:

        url = item
        # download = HtmlDownloader()
        # parser = HtmlParser()
        html_cont = download.download(url)
        # data, table = parser.parser(url, html_cont)
        data = parser.parser(url, html_cont, url_list)

        # output_dict(school + "out_dict.txt", data)
        # output_table(school + "out_table.txt", table)
        # return

        output_dict(name + str(i) + "out_dict.txt", data)
        # output_table(name + "out_table.txt", table)
        i += 1
        # time.sleep(1)

    return

    # download = HtmlDownloader()
    # parser = HtmlParser()
    # html_cont = download.download(url)
    # # data, table = parser.parser(url, html_cont)
    # data = parser.parser(url, html_cont)
    #
    # # output_dict(school + "out_dict.txt", data)
    # # output_table(school + "out_table.txt", table)
    # # return
    #
    # output_dict(name + "out_dict.txt", data)
    # # output_table(name + "out_table.txt", table)
    #
    # return


if __name__ == '__main__':
    main()



