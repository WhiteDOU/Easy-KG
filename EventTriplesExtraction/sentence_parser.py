#!/usr/bin/env python3
# coding: utf-8
# File: sentence_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-10

import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
class LtpParser:
    def __init__(self):
        LTP_DIR = "/Users/rilzob/PycharmProjects/SubjectKG/ltp_data_v3.4.0"
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl.model'))

    '''语义角色标注'''
    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        # 打印结果
        for role in roles:
            print(role.index, "".join(
                ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
        # self.labeller.release()  # 释放模型
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name:[arg.name,arg.range.start, arg.range.end] for arg in role.arguments}
        return roles_dict

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def build_parse_child_dict(self, words, postags, arcs):
        child_dict_list = []
        format_parse_list = []
        # print('words:', words)
        # print('postags:', postags)
        # print('arcs:', arcs)
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                # print('arc_index:', arc_index)
                if arcs[arc_index].head == index+1:   #arcs的索引从1开始
                    # print('arc_index.relation:', arcs[arc_index].relation)
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            # print('child_dict:', child_dict)
            child_dict_list.append(child_dict)
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i]-1, postags[rely_id[i]-1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list

    '''parser主函数'''
    def parser_main(self, sentence):
        words = list(self.segmentor.segment(sentence))
        # segment是将句子分词后的返回值并且使用list转换为Python的列表类型，原类型为native的VectorOfString
        postags = list(self.postagger.postag(words))
        # postag是将words进行词性标注的返回结果
        arcs = self.parser.parse(words, postags)
        # parse是进行依存句法分析
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        # # 较原来的版本修改的部分
        # old_child_dict_list, old_format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        # # print('child_dict_list:', child_dict_list)
        # # print('format_parse_list:', format_parse_list)
        # new_format_parse_list = old_format_parse_list
        #
        # # 找到中心词在old_format_parse_list的index
        # hed_num = 0  # 中心词的index
        # for format_parse in old_format_parse_list:
        #     if old_format_parse_list[0] == 'HED':
        #         hed_num = format_parse[2]
        #     else:
        #         continue
        #
        # # 找到被中心词所支配的主语
        # subject = ''  # 中心词的从属词
        # for format_parse in old_format_parse_list:
        #     if format_parse[0] == 'SBV' and format_parse[5] == hed_num:
        #         subject = old_format_parse_list[1]
        #     else:
        #         continue
        #
        # # 对原文进行修改，增加主语
        # for format_parse in old_format_parse_list:
        #     if format_parse[0] == 'ADV':
        #         if old_format_parse_list[format_parse[5]][0] == 'COO':
        #             new_format_parse_list.insert(format_parse[2], list(subject))
        #     else:
        #         continue
        #
        # #
        # for

        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list

    def supply_subject(self, old_format_parse_list):
        # 较原来的版本修改的部分
        # print('child_dict_list:', child_dict_list)
        # print('format_parse_list:', format_parse_list)
        new_format_parse_list = old_format_parse_list

        # 找到中心词在old_format_parse_list的index
        hed_num = 0  # 中心词的index
        for old_format_parse in old_format_parse_list:
            if old_format_parse[0] == 'HED':
                hed_num = old_format_parse[2]
            else:
                continue

        # 找到被中心词所支配的主语
        subject = ''  # 中心词的从属词
        for old_format_parse in old_format_parse_list:
            if old_format_parse[0] == 'SBV' and old_format_parse[5] == hed_num:
                subject = old_format_parse[1]
            else:
                continue

        # 对原文进行修改，增加主语
        for old_format_parse in old_format_parse_list:
            if old_format_parse[0] == 'ADV':
                if old_format_parse_list[old_format_parse[5]][0] == 'COO':
                    new_format_parse_list.insert(old_format_parse[2], list(('', subject)))
            else:
                continue

        # 生成补充主语后的新句子
        string = ''
        for new_format_parse in new_format_parse_list:
            string = string + new_format_parse[1]

        return string


if __name__ == '__main__':
    parse = LtpParser()
    # old_sentence = '北京大学（Peking University），简称“北大”，由中华人民共和国教育部直属'
    old_sentence = '北京大学（Peking University），简称“北大”，由中华人民共和国教育部直属'
    old_words, old_postags, old_child_dict_list, old_roles_dict, old_format_parse_list = parse.parser_main(old_sentence)
    # print('old_word: ', old_words, len(old_words))
    # print('old_postags: ', old_postags, len(old_postags))
    print('old_child_dict_list: ', old_child_dict_list, len(old_child_dict_list))
    print('old_role_dict: ', old_roles_dict)
    print('old_format_parse_list: ', old_format_parse_list, len(old_format_parse_list))
    new_sentence = parse.supply_subject(old_format_parse_list)
    print('new_sentence: ', new_sentence)
    new_words, new_postags, new_child_dict_list, new_roles_dict, new_format_parse_list = parse.parser_main(new_sentence)
    # print('new_words', new_words, len(new_words))
    # print('new_postags', new_postags, len(new_postags))
    print('new_child_dict_list', new_child_dict_list, len(new_child_dict_list))
    print('new_roles_dict', new_roles_dict)
    print('new_format_parse_list', new_format_parse_list, len(new_format_parse_list))