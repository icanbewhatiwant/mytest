from psycopg2 import extras as ex
import psycopg2 as pg
import json
from functools import reduce
import os

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
        tmp.append(json.loads(line,strict=False))

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

#指定文档导入数据
def prosql():
    file_path = "C:/产品文档/爬虫-我的/gvzd_file/"
    file_list= os.listdir(file_path)

    # values 后面直接%s
    hostname = '172.18.11.26'
    username = 'postgres'
    password = 'postgres_cnhis@#$'
    database = 'ai'
    #本地测试环境
    # hostname = '127.0.0.1'
    # username = 'postgres'
    # password = 'qj123456'
    # database = 'myai'
    conn = pg.connect(database=database, user=username, password=password, host=hostname, port="5432")
    cursor = conn.cursor()

    flag1 = "1"
    flag2 = "2"

    for file_name in file_list:
        if "gk" in file_name:
            file_path1 = file_path + file_name
            toDb(file_path1, flag1, conn, cursor)
        elif "xj" in file_name:
            file_path2 = file_path + file_name
            toDb(file_path2, flag2, conn, cursor)

    conn.close()
    cursor.close()

if __name__ =='__main__':
    prosql()
