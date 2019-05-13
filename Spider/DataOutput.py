# encoding:utf-8

# @Author: Rilzob
# @Time: 2019/4/2 下午10:59

import json


class DataOutput(object):
    def __init__(self):
        super(DataOutput, self).__init__()

    @staticmethod
    def output(file, dict):
        with open(file, "w", encoding="utf-8") as f:
            output = json.dumps(dict, ensure_ascii=False, indent=1)
            f.write(output)
        return