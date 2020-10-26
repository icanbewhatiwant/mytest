import re
#服药方式
admin_route_str = "(口服|含服|肌内或(缓慢)?静脉(缓慢)?注射|静脉或肌内注射|静脉注射或肌内注射|肌内注射或(缓慢)?静脉(缓慢)?注射|肌内注射或(缓慢)?静脉(缓慢)?推注|静脉注射|静脉滴注|肌内注射" \
                  "|冲服|嚼服|浸润局麻|浸润麻醉|外用|滴眼|滴鼻|冲洗|阴道给药|肛门给药|舌下含服|阴道用药|瘤体注射|皮下注射|静脉推注|吸入|阴道冲洗|漱口|关节腔注射|处方|灌肠|直肠灌注|贴患处)"

#句中包含序列①的拆分
cir_str = u"（1）口服 成人 ①抗焦虑，一次 2.5〜10 mg,一日2〜4次。②镇静、催眠、急性乙醇戒 断,第一日，一次10 mg。一日3〜4次,以后按需要减少到一次5mg,一日3〜4次。老年或体弱患者应减量。"
def get_circle_str(str):
    circle_patr = re.compile(r'([①②③④⑤⑥⑦⑧⑨⑩]+)')
    f = re.finditer(circle_patr,str)
    indexes = [i.start() for i in f]
    print(indexes)
    start = 0
    result1 = []
    for i,indx in enumerate(indexes):
        sbstr = str[start:indx]
        result1.append(sbstr)
        if i == len(indexes)-1:
            sbstr1 = str[indx:]
            result1.append(sbstr1)
        start = indx

    take_str = result1[0]
    take_patr_b = re.compile("^([（(]\d[）)])*"+admin_route_str)
    if take_patr_b.search(take_str):
        result_left = result1[1:]
        result1 = [take_str+str for str in result_left]

    return result1
#句中包含括号
bracket_str = "（1） 口服成人抗焦虑，一次0.5〜 1 mg,一日2〜3次。镇静催眠。睡前服2〜4 mg。年老体弱 者应减量。12岁以下小儿安全性与剂量尚未确定。&nsp（2）\t肌内注射抗焦虑、镇静催眠,一次按体重 0. 05 mg/kg,总量不超过4 mg。&nsp（3）\t静脉注射 用于癌症化疗止吐，在化疗前30分 钟注射2〜4 mg,与奋乃静合用效果更佳,必要时重复使 用给药；癫痫持续状态,按体重0. 05 mg/kg,一次不超过 4 mg,如10〜15分钟后发作仍继续或再发。可重复注射 0. 05 mg/kg,如再经10〜15分钟仍无效。需采用其他措 施，12小时内用量一般不超过8 mg。"
take_patr = re.compile("^([（(]\d[）)])*"+admin_route_str)
def get_bracket_str(str):
    bracket_patr = re.compile(r"([（(]\d[）)])+?")
    bracket_f = re.finditer(bracket_patr,str)
    indexes = [i.start() for i in bracket_f]
    start = 0
    result1 = []
    for i,indx in enumerate(indexes):
        if indx==0:
            continue
        sbstr = str[start:indx]
        sbstr = sbstr.replace("&nsp","").replace("\t","").replace(" ", "")#去除文本中的空格、指标符、特殊符号
        result1.append(sbstr)
        if i == len(indexes)-1:
            sbstr1 = str[indx:]
            sbstr1 =sbstr1.replace("&nsp","").replace("\t","").replace(" ", "")
            result1.append(sbstr1)
        start = indx
    take_str = result1[0]
    take_patr_b = re.compile("^([（(]\d[）)])+")
    #(1)序号前没有字符串（服药方式）
    if take_patr_b.search(take_str):
        pass
    return result1

result = get_bracket_str(bracket_str)
print(result)

#句内句子的切分  首先匹配分号，再考虑匹配年龄（注意这个先后顺序）
sub_str = "口服 成人 一日3-18 mg,分次服。按反应和病情调整剂量。老年体弱者由一日3 mg 开始,按需调整剂量。"
semicolon_str = "[;|；]"
semiconlon_patr = re.compile(semicolon_str)
age_str = "[，。,.]+?(<1岁|幼儿|小儿|成人|老年.?体弱.?者|年老.?体弱.?者|老年人|儿童)+"
age_patr = re.compile(age_str)
#按分号切分句子
def get_semi_cut(str):
    semi_result = []
    if ";" in str or "；" in str:
        str.replace(";","；")
        if semiconlon_patr.search(str):
            semi_result = str.split("；")
    return semi_result

#按年龄切分句子
def get_age_cut(str):
    age_result= []
    age_match = age_patr.search(str)
    if age_match:
        age_list = age_patr.findall(str)
        print(age_list)
    f = re.finditer(age_patr,str)
    indexes = [i.start() for i in f]
    start = 0
    for i, indx in enumerate(indexes):
        # if i == 0:
        #     continue
        sbstr = str[start:indx+1]
        sbstr = sbstr.replace("&nsp", "").replace("\t", "").replace(" ", "")  # 去除文本中的空格、指标符、特殊符号
        age_result.append(sbstr)
        if i == len(indexes) - 1:
            sbstr1 = str[indx+1:]
            sbstr1 = sbstr1.replace("&nsp", "").replace("\t", "").replace(" ", "")
            age_result.append(sbstr1)
        start = indx+1
    return age_result

result = get_semi_cut(sub_str)







