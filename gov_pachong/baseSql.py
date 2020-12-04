from psycopg2 import extras as ex
import psycopg2 as pg
import json
import datetime
import os
from functools import reduce


data_list = [{'projectName': '伊犁哈萨克自治州友谊医院开发区分院保洁服务项目', 'pingmu': '服务', 'purUnit': '新疆伊犁哈萨克自治州友谊医院', 'adminiArea': '新疆维吾尔自治区', 'bulletTime': '2020年09月02日  19:20', 'obtBidTime': '2020年09月02日至2020年09月09日每日上午:00:00 至 12:00\xa0\xa0下午:12:00 至 23:59（北京时间，法定节假日除外）', 'bidDocPrice': '￥500', 'obtBidLoc': '伊宁市经济合作区福安·西城国际1416室', 'staBidTime': '', 'staLoc': '伊宁市海棠路3号州财政局办公楼附楼1层州政府采购中心 一楼招标厅', 'budget': '￥807.000000万元（人民币）', 'proContact': '胡川', 'proPhone': '18690293446', 'purAddress': '伊宁市斯大林街92号', 'purUnitPhone': '0999-8024023', 'agentName': '新疆诚成工程项目管理有限公司', 'agentAddress': '详见公告正文', 'agentPhone': '18690293446'}
    , {'projectName': '旅顺口医疗区医用氧气管道检修采购项目', 'pingmu': '服务/维修和保养服务/其他维修和保养服务', 'purUnit': '中国人民解放军联勤保障部队第九六七医院', 'adminiArea': '大连市', 'bulletTime': '2020年09月02日  19:52', 'obtBidTime': '2020年09月02日至2020年09月07日每日上午:8:30 至 11:30\xa0\xa0下午:13:00 至 16:30（北京时间，法定节假日除外）', 'budget': '￥0.000000万元（人民币）', 'proContact': '廖大成，尹辉', 'proPhone': '0411-80841295  0411-80841296', 'purAddress': '辽宁省大连市西岗区胜利路80号', 'purUnitPhone': '廖大成，尹辉 0411-80841295  0411-80841296', 'agentName': '中国人民解放军联勤保障部队第九六七医院', 'agentAddress': '辽宁省大连市西岗区胜利路80号', 'agentPhone': '廖大成，尹辉 0411-80841295  0411-80841296', 'appendix': '{"2.报价书氧气管道检修.docx": "http://www.ccgp.gov.cn/oss/download?uuid=88FCEC822374C5002F6DD48B15DC44", "3.货物指标及要求氧气管道检修.docx": "http://www.ccgp.gov.cn/oss/download?uuid=2773DFCD00839B5E034DA43339EDF1"}'}
    ]


dict_tmp={}
values_list = []
result = []
def processJson(dic):
    dicobj = json.loads(dic)
    print(dicobj)
    for k,v in dicobj.items():
        dict_tmp = {}
        dict_tmp["file_name"] = k
        dict_tmp["urls"] =v
        print(k)
        print(v)
        result.append(dict_tmp)
        # dict_tmp.clear()
    return result

def procesV():
    for i in data_list:
        if "appendix" in i.keys():
            appendix = i["appendix"]
            if appendix != "":
                fj = processJson(i["appendix"])
                print(fj)
                fjs = json.dumps(fj,ensure_ascii=False)
                values_list.append(("testtest",fjs))

def prosql():
    # values 后面直接%s
    hostname = '172.18.11.26'
    username = 'postgres'
    password = 'postgres_cnhis@#$'
    database = 'ai'
    conn = pg.connect(database=database, user=username, password=password, host=hostname, port="5432")
    cursor = conn.cursor()
    procesV()
    sql = '''insert into ho_sysnc_third_customer_data("purchased_project_name","fj_json")
                     values %s
             '''
    # 其中函数中的page_size参数默认为100，表示每个statement包含的最大条目数，
    # 如果传过来的argslist长度大于page_size,则该函数最多执行len(argslist)/page_size + 1次。
    ex.execute_values(cursor, sql, values_list, page_size=10000)
    conn.commit()

    conn.close()
    cursor.close()




if __name__ =='__main__':
    prosql()
    # procesV()
