import pandas as pd
import pandas.io.formats.excel
import datetime
import os
import json


def pre_process():
    #json文件数据入库
    data_df = pd.DataFrame()
    drug_names = []
    dose_info = []
    erke_dose_info = []
    sentences = []
    #切分字段
    age_low = []
    age_high = []
    age_unit = []
    weight_low = []
    weight_high = []
    admin_route = []
    sdose_low = []
    sdose_high = []
    dose_time_low = []
    dose_time_high = []
    dose_time_low_des = []
    dose_time_high_des = []
    sday_dose_low = []
    sday_dose_high = []
    single_dose_unit = []
    limit_1time = []
    limit_1day = []
    recommand_days_low = []
    recommand_days_high = []

    data_df["药品名称"] = drug_names
    data_df["用药用量"] = dose_info
    data_df["儿科用药用量"] = erke_dose_info
    data_df["审查结果"] = sentences

    #字段
    data_df["年龄低值"] = age_low
    data_df["年龄高值"] = age_high
    data_df["年龄单位（岁；月；天）"] = age_unit
    data_df["体重低值"] = weight_low
    data_df["体重高值"] = weight_high
    data_df["给药途径"] = admin_route
    data_df["单次推荐剂量低值"] = sdose_low
    data_df["单次推荐剂量高值"] = sdose_high
    data_df["单次剂量极值"] = limit_1time
    data_df["单日推荐剂量低值"] = sday_dose_low
    data_df["单日推荐剂量高值"] = sday_dose_high
    data_df["单日剂量极值"] = limit_1day
    data_df["剂量单位"] = single_dose_unit
    data_df["推荐给药频次低值"] = dose_time_low
    data_df["推荐给药频次低值描述"] = dose_time_low_des
    data_df["推荐给药频次高值"] = dose_time_high
    data_df["推荐给药频次高值描述"] = dose_time_high_des
    data_df["用药推荐天数低值"] = recommand_days_low
    data_df["用药推荐天数高值"] = recommand_days_high


    #创建excel文件
    writer = pd.ExcelWriter('C:/产品文档/转换器测试数据/shenme.xlsx')
    # result2.to_excel(writer, float_format='%.5f')
    data_df.to_excel(writer,index = False,encoding='UTF-8')#不保存索引
    writer.save()
    writer.close()


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False

if __name__=="__main__":
    # json文件数据入库
    data_df = pd.DataFrame()

    drug_names = []
    dose_info = []
    erke_dose_info = []
    sentences = []
    # 切分字段
    age_low = []
    age_high = []
    age_unit = []
    weight_low = []
    weight_high = []
    admin_route = []
    sdose_low = []
    sdose_high = []
    dose_time_low = []
    dose_time_high = []
    dose_time_low_des = []
    dose_time_high_des = []
    sday_dose_low = []
    sday_dose_high = []
    single_dose_unit = []
    limit_1time = []
    limit_1day = []
    recommand_days_low = []
    recommand_days_high = []
    cut_senteces = []

    #读取切分结果，excel保存
    def data_process(filepath):
        tmp = []
        json_str = ""
        for line in open(filepath, 'r', encoding='UTF-8'):
            json_str += line.replace("\n", "").replace("'", " ")
            if check_json_format(json_str):
                tmp.append(json.loads(json_str))
                json_str = ""
        if tmp:
            for drug_info in tmp:
                s_result_list = []
                e_s_result_list =[]
                drugName = drug_info.get("drugName", "").replace("@", "")
                if drugName !="":

                    drug_names.append(drugName)
                    dose_info.append(drug_info.get("用法与用量","").replace("&nsp", "").replace("\t", "").replace(" ", ""))

                    #用药用量分句和结果list[{"1":……,"2":……},{},……] 1：分句 2：对应字段
                    s_result_list = drug_info.get("s_result",[])
                    # 儿科用药用量分句和结果list[{"1":……,"2":……},{},……] 1：分句 2：对应字段
                    e_s_result_list = drug_info.get("e_s_result",[])
                    #获取药品名称、用药用量、儿科用药用量需要扩展的长度（dateframe需要列的list长度一致）
                    sentence_length = 0
                    s_result_len = 0
                    e_s_result_len = 0
                    if s_result_list:
                        s_result_len = len(s_result_list)
                        sentence_length += s_result_len
                    if e_s_result_list:
                        e_s_result_len = len(e_s_result_list)
                        sentence_length += e_s_result_len

                    if sentence_length >1:
                        drug_names.extend([""]*(sentence_length - 1))

                    #拼接用法用量下的空字符串 用法……
                    if sentence_length >1:
                        dose_info.extend([""]*(sentence_length-1))
                    #拼接儿科用法用量的空字符串 ……儿科……
                    if s_result_len > 0:
                        erke_dose_info.extend([""]*s_result_len)
                    if e_s_result_len >0:
                        erke_dose_info.append(drug_info.get("儿科用法与用量", "").replace("&nsp", "").replace("\t", "").replace(" ", ""))
                        erke_dose_info.extend([""]*(e_s_result_len-1))


                    #审查结果：断句切分
                    if s_result_list:
                        for sen_ziduan in s_result_list:
                            sent_string = sen_ziduan.get("1","")
                            if sent_string != "":
                                cut_senteces.append(sent_string)
                                sen_result = sen_ziduan.get("2",{})
                                # if sen_result:
                                age_low.append(sen_result.get("age_low",""))
                                age_high.append(sen_result.get("age_high",""))
                                age_unit.append(sen_result.get("age_unit",""))
                                weight_low.append(sen_result.get("weight_low",""))
                                weight_high.append(sen_result.get("weight_high",""))
                                admin_route.append(sen_result.get("admin_route",""))
                                sdose_low.append(sen_result.get("sdose_low",""))
                                sdose_high.append(sen_result.get("sdose_high",""))
                                dose_time_low.append(sen_result.get("dose_time_low",""))
                                dose_time_high.append(sen_result.get("dose_time_high",""))
                                dose_time_low_des.append(sen_result.get("dose_time_low_des",""))
                                dose_time_high_des.append(sen_result.get("dose_time_high_des",""))
                                sday_dose_low.append(sen_result.get("sday_dose_low",""))
                                sday_dose_high.append(sen_result.get("sday_dose_high",""))
                                single_dose_unit.append(sen_result.get("single_dose_unit",""))
                                limit_1time.append(sen_result.get("limit_1time",""))
                                limit_1day.append(sen_result.get("limit_1day",""))
                                recommand_days_low.append(sen_result.get("recommand_days_low",""))
                                recommand_days_high.append(sen_result.get("recommand_days_high",""))
                    if e_s_result_list:
                        for erke_sen_ziduan in e_s_result_list:
                            #儿科数据解析
                            ek_sent_string = erke_sen_ziduan.get("1", "")
                            if ek_sent_string != "":
                                cut_senteces.append(ek_sent_string)
                                sen_result = erke_sen_ziduan.get("2", {})
                                # if sen_result:
                                age_low.append(sen_result.get("age_low", ""))
                                age_high.append(sen_result.get("age_high", ""))
                                age_unit.append(sen_result.get("age_unit", ""))
                                weight_low.append(sen_result.get("weight_low", ""))
                                weight_high.append(sen_result.get("weight_high", ""))
                                admin_route.append(sen_result.get("admin_route", ""))
                                sdose_low.append(sen_result.get("sdose_low", ""))
                                sdose_high.append(sen_result.get("sdose_high", ""))
                                dose_time_low.append(sen_result.get("dose_time_low", ""))
                                dose_time_high.append(sen_result.get("dose_time_high", ""))
                                dose_time_low_des.append(sen_result.get("dose_time_low_des", ""))
                                dose_time_high_des.append(sen_result.get("dose_time_high_des", ""))
                                sday_dose_low.append(sen_result.get("sday_dose_low", ""))
                                sday_dose_high.append(sen_result.get("sday_dose_high", ""))
                                single_dose_unit.append(sen_result.get("single_dose_unit", ""))
                                limit_1time.append(sen_result.get("limit_1time", ""))
                                limit_1day.append(sen_result.get("limit_1day", ""))
                                recommand_days_low.append(sen_result.get("recommand_days_low", ""))
                                recommand_days_high.append(sen_result.get("recommand_days_high", ""))

        data_df["药品名称"] = drug_names
        data_df["用药用量"] = dose_info
        data_df["儿科用药用量"] = erke_dose_info
        data_df["审查结果"] = cut_senteces

        # 字段
        data_df["年龄低值"] = age_low
        data_df["年龄高值"] = age_high
        data_df["年龄单位（岁；月；天）"] = age_unit
        data_df["体重低值"] = weight_low
        data_df["体重高值"] = weight_high
        data_df["给药途径"] = admin_route
        data_df["单次推荐剂量低值"] = sdose_low
        data_df["单次推荐剂量高值"] = sdose_high
        data_df["单次剂量极值"] = limit_1time
        data_df["单日推荐剂量低值"] = sday_dose_low
        data_df["单日推荐剂量高值"] = sday_dose_high
        data_df["单日剂量极值"] = limit_1day
        data_df["剂量单位"] = single_dose_unit
        data_df["推荐给药频次低值"] = dose_time_low
        data_df["推荐给药频次低值描述"] = dose_time_low_des
        data_df["推荐给药频次高值"] = dose_time_high
        data_df["推荐给药频次高值描述"] = dose_time_high_des
        data_df["用药推荐天数低值"] = recommand_days_low
        data_df["用药推荐天数高值"] = recommand_days_high

        # 创建excel文件
        writer = pd.ExcelWriter('C:/产品文档/转换器测试数据/100-200-1.xlsx')
        # result2.to_excel(writer, float_format='%.5f')
        data_df.to_excel(writer, index=False, encoding='UTF-8')  # 不保存索引
        writer.save()
        writer.close()


    filepath = "C:/产品文档/转换器测试数据/1-200_20201120_ziduan.json"
    data_process(filepath)


