# from __future__ import unicode_literals
import datetime
from dateutil.relativedelta import relativedelta
#
# today = datetime.date.today()
# end_time = today.strftime('%Y:%m:%d')
# start_time = (today - relativedelta(months=+3)).strftime('%Y:%m:%d')
# baseUrl = "http://search.ccgp.gov.cn/bxsearch?"
# paraS = "searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=3&bidType="
# paraE = "&displayZone=&zoneId=&pppStatus=0&agentName="
# paraM  = "&dbselect=bidx&kw=医院"
#
#
# seTime = "&start_time="+start_time+"&end_time="+end_time+"&timeType=4"
# eeTime = "&start_time="+end_time+"&end_time="+end_time+"&timeType=0"
#
# url_gk3 = baseUrl+paraS+"1"+paraM+seTime+paraE
# url_xj3 = baseUrl+paraS+"2"+paraM+seTime+paraE
# url_gk_today = baseUrl +paraS+"1"+paraM+eeTime+paraE
# url_xj_today = baseUrl +paraS+"2"+paraM+eeTime+paraE
#
# print(url_gk3)
# print(url_xj_today)
# print(url_gk_today)
# print(url_xj_today)
#
# next_url = "gopage(2)"
# page_num = next_url[next_url.index("(")+1:next_url.index(")")]
# print(page_num)
# print(type(page_num))


# from selenium import webdriver
# import requests
# browser = webdriver.Chrome(r"C:\软件\chromedriver_win32\chromedriver.exe")
#
#
# driver = webdriver.Chrome(r"C:\软件\chromedriver_win32\chromedriver.exe")
# driver.get("http://www.ccgp.gov.cn/")
# browser.set_page_load_timeout(30)
# cookies = driver.get_cookies()
# print("get cookies")
# driver.close()
# print("开始会话")
#
# for  cookie  in cookies:
#     print(cookie['name']+" : "+cookie["value"])

# import pandas as pd
# import pandas.io.formats.excel
# import datetime
# import os
#
# to_time = datetime.datetime.now()
# today = to_time.strftime('%Y-%m-%d')
# path = "C:\\产品文档\\爬虫-我的\\数据\\"
# exl_list= os.listdir(path)
#
# frames=[]
# def pre_process(exl_list):
#     for el in exl_list:
#         df = pd.read_excel(io=path+el)
#         data_df = pd.DataFrame(df)
#         frames.append(data_df)
#     if len(frames)>=2:
#         result = pd.concat(frames)
#         print(result.describe())
#         writer = pd.ExcelWriter(path + today + '_tianyancha.xlsx')
#         result.to_excel(writer,index = False)#不保存索引
#         writer.save()
#         writer.close()
#     else:
#         print("数据未下载完全")
#
# pre_process(exl_list)


base = "http://www.ccgp.gov.cn"
# 标题过滤列表
filter_list = ["信息", "医疗", "系统", "软件", "绩效", "数字", "电子", "技术", "维护", "管理", "项目", "服务", "接口"]

# today = datetime.date.today()
# end_time = today.strftime('%Y:%m:%d')
# start_time = (today - relativedelta(months=+3)).strftime('%Y:%m:%d')
# # 指定时间  日更用昨天日期
# end_time = (today - relativedelta(days=+1)).strftime('%Y:%m:%d')
# start_time = (today - relativedelta(days=+4)).strftime('%Y:%m:%d')
#
# baseUrl = "http://search.ccgp.gov.cn/bxsearch?"
# paraS = "searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=3&bidType="
# paraE = "&displayZone=&zoneId=&pppStatus=0&agentName="
# paraM = "&dbselect=bidx&kw=医院"
# seTime = "&start_time=" + start_time + "&end_time=" + end_time + "&timeType=4"
# eeTime = "&start_time=" + end_time + "&end_time=" + end_time + "&timeType=6"
# zdTime = "&start_time=" + start_time + "&end_time=" + end_time + "&timeType=6"
#
#
# # url_gk3 公开招标三个月 url_xj3询价三个月 url_gk_today公开今日  url_xj_today询价今日
# url_gk_today = baseUrl + paraS + "1" + paraM + eeTime + paraE
# # url_xj3 = baseUrl + paraS + "2" + paraM + seTime + paraE
# # url_xj_today = baseUrl + paraS + "2" + paraM + eeTime + paraE
# print(url_gk_today)

# today = datetime.date.today().strftime("%Y_%#m_%#d")
# print(today)

# par_str = "【用法与用量】 滴入结膜囊.一次1〜2滴.按需要 滴1次。"
# begin_idx = par_str.find("【")
# end_idx = par_str.find("】")
# label = par_str[begin_idx+1: end_idx ]
# print(label)

# str = unicode(u"用法用量"，"gb2312")

import re

sub_str = "口服 成人 一日3-18 mg,分次服。按反应和病情调整剂量。老年体弱者由一日3 mg 开始,按需调整剂量。"
semicolon_str = "[;|；]"
semiconlon_patr = re.compile(semicolon_str)
age_str = "[，。,.]+?(<1岁|幼儿|小儿|成人|老年.?体弱.?者|年老.?体弱.?者|老年人|儿童)+"
age_patr = re.compile(age_str)
#按分号切分句子
def get_semi_cut(str):
    semi_result = []
    if ";" in str or "；" in str:
        str.replace(";","；")
        if semiconlon_patr.search(str):
            semi_result = str.split("；")
    return semi_result

#按年龄切分句子
def get_age_cut(str):
    age_result= []
    age_match = age_patr.search(str)
    if age_match:
        age_list = age_patr.findall(str)
        print(age_list)
    f = re.finditer(age_patr,str)
    indexes = [i.start() for i in f]
    start = 0
    for i, indx in enumerate(indexes):
        # if i == 0:
        #     continue
        sbstr = str[start:indx+1]
        sbstr = sbstr.replace("&nsp", "").replace("\t", "").replace(" ", "")  # 去除文本中的空格、指标符、特殊符号
        age_result.append(sbstr)
        if i == len(indexes) - 1:
            sbstr1 = str[indx+1:]
            sbstr1 = sbstr1.replace("&nsp", "").replace("\t", "").replace(" ", "")
            age_result.append(sbstr1)
        start = indx+1
    return age_result

result = get_semi_cut(sub_str)
print(result)




