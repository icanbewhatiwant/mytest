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

#出现“第几节”的时候，药品数据是横跨页面两栏的，这个识别有没有问题
#整个文本是纯数据吗 后面好像还有索引、等等其他数据，1429页有部分药品给药方式,这些数据可能要人工处理,如看下是否可以去掉1423页后的数据
useType =["滴入","注射","口服","静脉滴注","口服给药","直肠给药","	肌内或皮下注射","静脉给药"]
#数据分析：用法用量，一日几次前面一般是给药途径
before_useType = ["周","日","次"]
yfyl_dict={}
grugStr=""
pattern = re.compile(u'[^\u4e00-\u9fa5]') #匹配药物名称，只有中文，其他段落有标点符号，基本可以区分
enpattern = re.compile(u'^[a-zA-Z\s]+$') #匹配药物英文名称，只有英文，没有标点符号
yfyl_patr = re.compile(r".*用法用量.*")
str = u"【用法与用量】 滴入结膜囊 ①轻、中度感染：一 次1〜2滴，每4小时1次。②重度感染：一次2滴，一小 时1次。"


print(str)
