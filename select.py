import json


def process():
    with open("./temp/test1.json", "r", encoding="utf-8", errors="ignore") as f:
        dictFinal = json.load(f)

    for i in range(4804):
        pre = './temp/test'
        mid = str(i + 1)
        post = '.json'
        file_name = pre + mid + post
        with open(file_name, "r", encoding="utf-8", errors="ignore") as f1:
            temp = json.load(f1)
            print(temp)
            with open("./ouput.txt", "a+") as f2:
                str_temp = str(temp["主题"]).strip(']').strip('[').strip('\'') + "\t"
                listtemp = temp["合作单位"]
                # for i in listtemp:
                #     output = str_temp +"\t合作（单位）\t"+ i +"\n"
                #     f2.write(output)
                # for i in temp["合作者"]:
                #     output = str_temp + "\t合作（学者）\t"+i + '\n'
                #     f2.write(output)
                # for i in temp["论文"]:
                #         output = str_temp + "\t撰写\t" + i + "\n"
                #         f2.write(output)
                output = str_temp + "\tID\t" + temp["id"] + "\n"
                f2.write(output)


if __name__ == "__main__":
    process()
