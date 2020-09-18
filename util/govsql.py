from psycopg2 import extras as ex
import psycopg2 as pg
import json
import datetime
import os
from functools import reduce

#数据去重
def list_dict_duplicate_removal(data_list):
    run_function = lambda x, y: x if y in x else x + [y]
    reduce(run_function, [[], ] + data_list)
    return reduce(run_function, [[], ] + data_list)

def proFj(fjs):
    result = []
    dicobj = json.loads(fjs) #json字符串转换为对象
    # print(dicobj)
    for k, v in dicobj.items():
        dict_tmp = {}
        dict_tmp["file_name"] = k
        dict_tmp["urls"] = v
        result.append(dict_tmp)
    fjs = json.dumps(result,ensure_ascii=False)#对象转换为字符串 参数免乱码
    return fjs

#读入政府采购网数据
def toDb(filepath,flag ,conn ,cursor):
    tmp = []
    values_list = []
    for line in open(filepath,'r', encoding='UTF-8'):
        tmp.append(json.loads(line))

    #数据去重 9.3有被攻击 数据有的重复21次 数据格式：[{},{}] list json去重
    ids = list_dict_duplicate_removal(tmp)

    if len(ids)>=1:
        print("len of ids:",len(ids))
        for jdata in  ids:
            #处理附件字符串
            fj = ""
            fjs = jdata.get(u"appendix","")
            if fjs !="":
                fj = proFj(fjs)
            tap = (jdata.get(u"projectName",""),jdata.get(u"pingmu",""),jdata.get(u"purUnit",""),jdata.get(u"adminiArea","")
                   ,jdata.get(u"bulletTime",""),jdata.get(u"obtBidTime",""),jdata.get(u"bidDocPrice",""),
                   jdata.get(u"obtBidLoc",""),jdata.get(u"staBidTime",""),jdata.get(u"staLoc",""),jdata.get(u"budget","")
                   ,jdata.get(u"proContact",""),jdata.get(u"proPhone",""),jdata.get(u"purAddress",""),jdata.get(u"purUnitPhone","")
                   ,jdata.get(u"agentName",""),jdata.get(u"agentAddress",""),jdata.get(u"agentPhone",""),flag,fj)
            values_list.append(tap)

        sql = '''insert into ho_sysnc_third_customer_data("purchased_project_name","item_category","purchase_units",
        "administrative_division","notice_time","obt_bid_time","bid_doc_price","obt_bid_address","sta_bid_time",
        "sta_bid_address","budget","contact","project_phone","pur_address","pur_unitphone","agent_name","agent_address",
        "agent_phone","type","fj_json")
                 values %s
         '''
        # 其中函数中的page_size参数默认为100，表示每个statement包含的最大条目数，
        # 如果传过来的argslist长度大于page_size,则该函数最多执行len(argslist)/page_size + 1次。
        ex.execute_values(cursor, sql, values_list, page_size=10000)
        conn.commit()

#导入当日数据，文件名称是今天，内容是按前一天查，因为内容当天是变动的
def prosql():
    # values 后面直接%s
    hostname = '172.18.11.26'
    username = 'postgres'
    password = 'postgres_cnhis@#$'
    database = 'ai'
    conn = pg.connect(database=database, user=username, password=password, host=hostname, port="5432")
    cursor = conn.cursor()
    path = "C:/产品文档/爬虫-我的/"
    today = datetime.date.today().strftime("%Y_%#m_%#d")
    file_list = os.listdir(path)
    file1 = "govBidgk_" + today + ".json"
    file2 = "govBidxj_" + today + ".json"
    flag1 = "1"
    flag2 = "2"

    if file1 in file_list and file2 in file_list:
        file_path1 = path+file1
        toDb(file_path1,flag1,conn ,cursor)
        file_path2 = path + file2
        toDb(file_path2,flag2,conn ,cursor)
    else:
        print("today's file num less than 2")
    conn.close()
    cursor.close()

if __name__ =='__main__':
    prosql()
