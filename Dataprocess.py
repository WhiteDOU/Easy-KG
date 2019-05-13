# encoding:utf-8

# @Author: Rilzob
# @Time: 2019/5/12 下午3:06

import json


def dataprocess(file):
    with open(file, "r", encoding="utf-8") as f:
        dict = json.load(f)
        print(dict)
    for school_name, values in dict.items():
        for key, value in values.items():
            if key == 'school_introduce_triple':
                school_introduce_triple = value
                for item in school_introduce_triple:
                    string = item[0] + ' ' + item[1] + ' ' + item[2]
                    with open('new_data_attribution.txt', 'a+', encoding='utf-8') as new_data:
                        new_data.write(string + '\n')
            else:
                if key == 'school_introduce':
                    value = value.strip()
                string = school_name + ' ' + key + ' ' + value
                with open('new_data.txt', 'a', encoding='utf-8') as new_data:
                    new_data.write(string + '\n')
        with open('new_data.txt', 'a+', encoding='utf-8') as new_data:
            new_data.write('\n')


if __name__ == '__main__':
    dataprocess('Spider/data.json')
