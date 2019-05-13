# encoding:utf-8

# @Author: Rilzob
# @Time: 2019/3/31 下午7:19

import requests


class HtmlDownloader(object):
    def __init__(self):
        super(HtmlDownloader, self).__init__()

    @staticmethod
    def download(url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            # print(r.text)
            return r.text
        else:
            print("下载网页内容失败")
            return None