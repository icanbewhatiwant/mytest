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

    data_df["药品名称"] = drug_names
    data_df["用药用量"] = dose_info
    data_df["儿科用药用量"] = erke_dose_info
    data_df["审查结果"] = sentences

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
                drugName = drug_info.get("drugName", "")
                if drugName !="":

                    drug_names.append(drugName)
                    dose_info.append(drug_info.get("用法与用量",""))
                    erke_dose_info.append(drug_info.get("儿科用法与用量",""))

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
                    if e_s_result_len >0:
                        s_result_list.extend([{}]*e_s_result_len)
                    if s_result_len > 0:



                    erke_take_way = drug_info.get("erke_sentence_cut", "")
                    erke_take_result_list = []
                    if take_way != "":
                        for take_string in take_way:
                            take_result = {}
                            take_way_dict = get_gruguse_result(take_string)
                            take_result["1"] = take_string
                            take_result["2"] = take_way_dict
                            take_result_list.append(take_result)
                        del drug_info["sentence_cut"]
                        if take_result_list:
                            drug_info["s_result"] = take_result_list

                    if erke_take_way != "":
                        for erke_take_string in erke_take_way:
                            erke_take_result = {}
                            erke_take_way_dict = get_gruguse_result(erke_take_string)
                            erke_take_result["1"] = erke_take_string
                            erke_take_result["2"] = erke_take_way_dict
                            erke_take_result_list.append(erke_take_result)
                        del drug_info["erke_sentence_cut"]
                        if erke_take_result_list:
                            drug_info["e_s_result"] = erke_take_result_list

            with open("C:/产品文档/转换器测试数据/1-200_20201120_ziduan.json", "w", encoding='utf-8') as fp:
                for drug in tmp:
                    fp.write(json.dumps(drug, indent=4, ensure_ascii=False))
                    fp.write('\n')


    filepath = "C:/产品文档/转换器测试数据/1-200_20201120_cutsentence.json"
    pre_process()


