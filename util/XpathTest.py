import psycopg2 as pg
from io import StringIO
import json

f = StringIO()  # StringIO 结构类似文件，但是内容都在内存里面

# 循环写入数据到内存里面， 里面每个字段用制表符\t 隔开，每一行用换行符\n 隔开
str =""
tmp = []
values_list = []
for line in open('C:/Users/admin/Desktop/数据/test.json','r', encoding='UTF-8'):
    tmp.append(json.loads(line))
for jdata in  tmp:
    tap = (jdata.get(u"companyName",""), jdata.get(u'introduction',""), jdata.get(u'label',""), jdata.get(u'scale',""), jdata.get(u'comLabel',""), jdata.get(u'registerTime',""),
           jdata.get(u'contact',""), jdata.get(u'telephone',""), jdata.get(u'phone',""),jdata.get(u'website',""),jdata.get(u'address',""))
    values_list.append('\t'.join(tap))

s = ''
for value in values_list:
    s += value + '\n'
    # str = (jdata["companyName"]+"\t"+jdata["introduction"]+"\t"+jdata["label"]+"\t"+jdata["scale"]+"\t"+jdata["comLabel"]
    # +"\t"+jdata["registerTime"]+"\t"+jdata["contact"]+"\t"+jdata["telephone"]+"\t"+jdata["phone"]
    # +"\t" + jdata["website"] + "\t" + jdata["address"]+"\n")
# f.write(str)

# 最重要的一步，要把f 的游标移到第一位，write 方法后，游标会变成最尾，StringIO(**) 就不会
# f.seek(0)

hostname = '172.18.11.26'
username = 'postgres'
password = 'postgres_cnhis@#$'
database = 'ai'
# 创建连接
conn =pg.connect(database=database, user=username, password=password, host=hostname, port="5432")
cursor = conn.cursor()

# cursor.copy_from(f, '"tc_compete"',
#                  columns=("company_name","introduction","label","scale","company_label","register_time","contact","telephone","phone","website","address"),
#                  sep='\t', null='\\N', size=16384)  # 默认sep和null 都是none

cursor.copy_from(StringIO(s), "tc_compete",
                 columns=("company_name","introduction","label","scale","company_label","register_time","contact","telephone","phone","website","address"),
                  )  # 默认sep和null 都是none

conn.commit()