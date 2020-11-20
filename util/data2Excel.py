import pandas as pd
import pandas.io.formats.excel
import datetime
import os


def pre_process():
    # for el in exl_list:
    #     df = pd.read_excel(io=path+el, skiprows=2)
    #     data_df = pd.DataFrame(df)
    #     data_df.drop(['注册号', '组织机构代码', '企业公示的联系电话（更多号码）', '参保人数', '纳税人识别号'], axis=1, inplace=True)
    #     frames.append(data_df)
    data_df = pd.DataFrame()
    numbers = [1,2,3,4,5,6]
    names = ["1","2","3","4","5","6"]
    '药理', '不良反应', '禁忌证', '注意事项', '用法与用量', '儿科用法与用量', '制剂与规格', '适应证', '儿科注意事项'
    data_df["药品名称"] = numbers
    data_df["药品英文名称"] = names

    data_df["适应证"] = names
    data_df["药理"] = names
    data_df["不良反应"] = names
    data_df["禁忌证"] = names
    data_df["注意事项"] = names
    data_df["用法与用量"] = names
    data_df["儿科用法与用量"] = names
    data_df["制剂与规格"] = names
    data_df["儿科注意事项"] = names
    data_df["药物相互作用"] = names


    #创建excel文件
    writer = pd.ExcelWriter('C:/产品文档/转换器测试数据/shenme.xlsx')
    # result2.to_excel(writer, float_format='%.5f')
    data_df.to_excel(writer,index = False,encoding='UTF-8')#不保存索引
    writer.save()
    writer.close()

# pre_process()

#针对每个备份文件都要进行：
#遍历去重得到文件中的label名称作为列名称
#赋值的时候找到对应列名进行赋值

#删除每个备份文件中不符合格式处理的数据
#修改label中不对的数据
#数据存储到json文件中，最后得到keys进行最终的列名list，最后再存入excel数据
if __name__=="__main__":
    dict = {"年龄低值":"","年龄高值":""}
    df = pd.DataFrame(columns=['年龄低值','年龄高值'])
    df.iloc[0,0] = "1111"
    print(df)


