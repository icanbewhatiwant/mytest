from psycopg2 import extras as ex
import psycopg2 as pg
import json
from functools import reduce
import os
import re

#读取json文件格式 {}，{}，{}……
def getJsondata(filepath):
    tmp = []
    values_list = []
    for line in open(filepath, 'r', encoding='UTF-8'):
        tmp.append(json.loads(line, strict=False))

#读取json文件格式：[{},{},……]
def read_json(filepath):
    # 读取存储于json文件中的列表
    with open(filepath, 'r',encoding='UTF-8') as f_obj:
        jlist = json.load(f_obj)
    return jlist

#获取给药途径
def get_administration_route(use_info,take_patr_b,take_patr_e):
    #下面方式是懒惰匹配和贪婪匹配，python默认贪婪，尽可能匹配多的字符串，非贪婪模式在词量后加？
    #这里分组中的效果就是：肌内注射或静脉注射存在时一定会匹配到，而不会匹配短的如 肌内注射


    take_patr_m = re.compile("静.?脉.?滴注|肌内注射|静脉注射|皮下注射")

    take_patr_mz = re.compile("浸润麻醉|浸润局麻| 黏膜表面局麻|麻醉")

    zw_patr =  re.compile("[\u4e00-\u9fa5]")#中文
    begin_match = take_patr_b.search(use_info)
    end_match = take_patr_e.search(use_info)
    admin_route = ""
    if begin_match:
        admin_route = begin_match.group()
    elif end_match:
        admin_route = end_match.group()

    #处理匹配文字中的数字序列符号、标点符号
    admin_cmatch = zw_patr.findall(admin_route)
    if admin_cmatch:
        admin_route = ''.join(admin_cmatch)
    return admin_route


def extract_info(list1,take_patr_b,take_patr_e):
    if list1:
        len_drug = len(list1)
        print("len_drug:",len_drug)
        for info in list1:
            if "用法与用量" in info.keys():
                drug_use = info["用法与用量"]
                drug_use_list = drug_use.split("&nsp")
                info["给药途径"] = []
                for use_info in drug_use_list:
                    use_info = use_info.replace(" ", "").replace("\t","")#去除文本中的空格
                    admin_route = get_administration_route(use_info,take_patr_b,take_patr_e)
                    info["给药途径"].append((admin_route,use_info))

    if list1:
        with open("C:/产品文档/转换器测试数据/已整理1-200-admin-route.json","w",encoding='utf-8') as fp:
            fp.write(json.dumps(list1, indent=4,ensure_ascii=False))#unicode串转中文传入

filepath = "C:/产品文档/转换器测试数据/已整理1-200.json"
list1 = read_json(filepath)

admin_route_str = "(口服|含服|肌内或(缓慢)?静脉(缓慢)?注射|静脉或肌内注射|静脉注射或肌内注射|肌内注射或(缓慢)?静脉(缓慢)?注射|肌内注射或(缓慢)?静脉(缓慢)?推注|静脉注射|静脉滴注|肌内注射" \
                  "|冲服|嚼服|浸润局麻|浸润麻醉|外用|滴眼|滴鼻|冲洗|阴道给药|肛门给药|舌下含服|阴道用药|瘤体注射|皮下注射|静脉推注|吸入|阴道冲洗|漱口|关节腔注射|处方|灌肠|直肠灌注|贴患处)"

take_patr_b = re.compile("^([（(]\d[）)])*"+admin_route_str)
print("take_patr_b:", take_patr_b)
take_patr_e = re.compile(admin_route_str + "?。*$")

extract_info(list1,take_patr_b,take_patr_e)


