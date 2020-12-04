import pandas as pd
import pandas.io.formats.excel
import datetime
import os
path = "C:/产品文档/天眼查数据备份/天眼查数据9.12/"
exl_list= os.listdir(path)

to_time = datetime.datetime.now()
today = to_time.strftime('%Y-%m-%d')

pandas.io.formats.excel.header_style = None

str=["妇科","产科","儿科","骨科","皮肤科","眼科","美容","体检","康复","养老","口腔","肿瘤"]
def label_fun(a):
    label=[]
    labelStr=""
    for s in str:
        if s in a:
            label.append(s)
    if len(label) >= 1:
        labelStr = ','.join(label)
    return labelStr

# df1 = pd.read_excel(io='C:\产品文档\天眼查\code\sheet1.xlsx',skiprows = 2)
# data_df1 = pd.DataFrame(df1)
#
# df2 = pd.read_excel(io='C:\产品文档\天眼查\code\sheet2.xlsx',skiprows = 2)
# data_df2= pd.DataFrame(df2)
#
# df3 = pd.read_excel(io='C:\产品文档\天眼查\code\sheet3.xlsx',skiprows = 2)
# data_df3= pd.DataFrame(df3)
#
# data_df1.drop(['注册号','组织机构代码','企业公示的联系电话（更多号码）','参保人数','纳税人识别号'],axis=1,inplace=True)
# data_df2.drop(['注册号','组织机构代码','企业公示的联系电话（更多号码）','参保人数','纳税人识别号'],axis=1,inplace=True)
# data_df3.drop(['注册号','组织机构代码','企业公示的联系电话（更多号码）','参保人数','纳税人识别号'],axis=1,inplace=True)

# print(data_df1.columns)


# exl_list= ['C:\产品文档\天眼查\code\sheet1.xlsx','C:\产品文档\天眼查\code\sheet2.xlsx','C:\产品文档\天眼查\code\sheet3.xlsx']
frames=[]
def pre_process(exl_list):
    for el in exl_list:
        df = pd.read_excel(io=path+el, skiprows=2)
        data_df = pd.DataFrame(df)
        data_df.drop(['注册号', '组织机构代码', '企业公示的联系电话（更多号码）', '参保人数', '纳税人识别号'], axis=1, inplace=True)
        frames.append(data_df)
    if len(frames)>=2:
        result = pd.concat(frames)
        print(result.describe())
        # 去重并保存文件
        result2 = result.drop_duplicates(keep='last')
        print(result2.describe())
        result2['标签'] = result2.apply(lambda x: label_fun(x.公司名称), axis=1)

        #创建excel文件

        writer = pd.ExcelWriter('C:/产品文档/天眼查数据备份/code/' + today + '_tianyancha.xlsx')
        # result2.to_excel(writer, float_format='%.5f')
        result2.to_excel(writer,index = False)#不保存索引
        writer.save()
        writer.close()
    else:
        print("数据未下载完全")


pre_process(exl_list)

#数据入库
# def process_item(self, item, spider)
#     # sql_desc="INSERT INTO postgresql_1(fullname, username, organization, mail, joined,followers,starred,following,popular_repos,popular_repos_download,popular_repos_star,popular_repos_info,home_page)values(item['fullname'], item['username'], item['organization'], item['mail'],item['joined'],item['followers'],item['starred'],item['following'],item['popular_repos'],item['popular_repos_download'],item['popular_repos_star'],item['popular_repos_info'], item['home_page'])"
#     conn = psycopg2.connect(database="mypg", user="postgres", password="student", host="127.0.0.1", port="5432")
#     try:
#         cur = conn.cursor()
#         # self.conn.query(sql_desc)
#         # cur.execute("INSERT INTO ewrrw values(dict(item));")
#         cur.execute(
#             """INSERT INTO postgresql_1 (fullname, username, organization, mail, joined, followers, starred, following, popular_repos, popular_repos_download, popular_repos_star, popular_repos_info, home_page) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
#             (item['fullname'],
#              item['username'],
#              item['organization'],
#              item['mail'],
#              item['joined'],
#              item['followers'],
#              item['starred'],
#              item['following'],
#              item['popular_repos'],
#              item['popular_repos_download'],
#              item['popular_repos_star'],
#              item['popular_repos_info'],
#              item['home_page']), )
#
#         conn.commit()
#         log.msg("Data added to PostgreSQL database!",
#                 level=log.DEBUG, spider=spider)
#
#     except Exception, e:
#         print
#         'insert record into table failed'
#         print
#         e
#
#     finally:
#         if cur:
#             cur.close()
#     conn.close()
#     return item
