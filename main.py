# encoding:utf-8

# @Author: Rilzob
# @Time: 2019/3/31 下午10:16

from Spider.HtmlParser import HtmlParser
from Spider.DataOutput import DataOutput
from EventTriplesExtraction.triple_extraction import TripleExtractor

if __name__ == "__main__":
    # url = 'https://baike.baidu.com/item/%E4%B8%9C%E5%8C%97%E5%A4%A7%E5%AD%A6/18014'

    # whole_info = HtmlParser().main_parse()
    whole_info = HtmlParser().new_main_parse()
    DataOutput().output('output2.json', whole_info)

    # 将school_introduce生成三元组并将生成后的结果添加到whole_info中
    extractor = TripleExtractor()
    for school_name, item in whole_info.items():
        introduce_tripe = extractor.triples_main(item['school_introduce'])
        school_introduce_triple = {}
        school_introduce_triple['school_introduce_triple'] = introduce_tripe
        whole_info[school_name].update(school_introduce_triple)

    DataOutput().output('data.json', whole_info)
