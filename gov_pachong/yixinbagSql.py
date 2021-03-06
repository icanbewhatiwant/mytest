from psycopg2 import extras as ex
import psycopg2 as pg
from io import StringIO
import json


# values 后面直接%s
#test
hostname = '172.18.11.26'
username = 'postgres'
password = 'postgres_cnhis@#$'
database = 'ai'
# local
# hostname = '127.0.0.1'
# username = 'postgres'
# password = 'qj123456'
# database = 'myai'

conn =pg.connect(database=database, user=username, password=password, host=hostname, port="5432")
cursor = conn.cursor()

tmp = []
values_list = []
for line in open('C:/产品文档/爬虫-我的/euser_2020_10_9.json','r', encoding='UTF-8'):
    tmp.append(json.loads(line))
for jdata in  tmp:
    tap = (jdata.get(u"companyName",""), jdata.get(u'introduction',""), jdata.get(u'label',""), jdata.get(u'scale',""), jdata.get(u'comLabel',""), jdata.get(u'registerTime',""),
           jdata.get(u'contact',""), jdata.get(u'telephone',""), jdata.get(u'phone',""),jdata.get(u'website',""),jdata.get(u'address',""))
    values_list.append(tap)

sql = '''insert into tc_compete("company_name","introduction","label","scale","company_label","register_time","contact","telephone","phone","website","address")
         values %s
 '''

ex.execute_values(cursor, sql, values_list, page_size=10000)

conn.commit()