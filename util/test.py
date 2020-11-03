
# from util.yaodianRe import get_bracket_str #引入同一包下的模块，文件夹下创建__init__文件()，代表目录是一个包，模块名就是util

import re
admin_route_str = "(口服|含服|肌内或(缓慢)?静脉(缓慢)?注射|静脉或肌内注射|静脉注射或肌内注射|肌内注射或(缓慢)?静脉(缓慢)?注射|肌内注射或(缓慢)?静脉(缓慢)?推注|静脉注射|静脉滴注|肌内注射" \
                  "|皮下或肌内注射|肌内或皮下注射|冲服|嚼服|浸润局麻|浸润麻醉|硬膜外麻醉|外用|滴眼|滴鼻|冲洗|阴道给药|肛门给药|舌下含服|阴道用药|瘤体注射|皮下注射|静脉推注|吸入|阴道冲洗|漱口|关节腔注射|处方|灌肠|直肠灌注|贴患处)"

bracket_str = "测试（1） 口服成人抗焦虑，一次0.5〜 1 mg,一日2〜3次。镇静催眠。睡前服2〜4 mg。年老体弱 者应减量。12岁以下小儿安全性与剂量尚未确定。&nsp（2）\t肌内注射抗焦虑、镇静催眠,一次按体重 0. 05 mg/kg,总量不超过4 mg。&nsp（3）\t静脉注射 用于癌症化疗止吐，在化疗前30分 钟注射2〜4 mg,与奋乃静合用效果更佳,必要时重复使 用给药；癫痫持续状态,按体重0. 05 mg/kg,一次不超过 4 mg,如10〜15分钟后发作仍继续或再发。可重复注射 0. 05 mg/kg,如再经10〜15分钟仍无效。需采用其他措 施，12小时内用量一般不超过8 mg。"
#效果：[test(1)……,test(2)……，……]
# take_patr = re.compile("^([（(]\d[）)])*"+admin_route_str)
def get_bracket_str(str):
    # str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    result = []
    result1 = re.split(r"([（(]\d[）)])+", str)
    if result1:
        str0 = result1[0]
        if str0 !="":
            result.append(str0)
        result1 = ["".join(i) for i in zip(result1[1::2], result1[2::2])]
        result.extend(result1)

    # bracket_patr = re.compile(r"([（(]\d[）)])+?")
    # bracket_f = re.finditer(bracket_patr,str)
    # indexes = [i.start() for i in bracket_f]
    # start = 0
    # result1 = []
    # for i,indx in enumerate(indexes):
    #     if indx==0:
    #         continue
    #     sbstr = str[start:indx]
    #     result1.append(sbstr)
    #     if i == len(indexes)-1:
    #         sbstr1 = str[indx:]
    #         result1.append(sbstr1)
    #     start = indx
    take_str = result[0]
    take_patr_b = re.compile("^([（(]\d[）)])+")
    # (1)序号前有字符串（服药方式）,拼接
    if not take_patr_b.search(take_str):
        result = ["".join(i) for i in zip([take_str]*(len(result)-1),result[1::1])]
    return result

result = get_bracket_str(bracket_str)
print("get_bracket_str",result)

import re
cir_str = u"(1)口服 成人 ①抗焦虑，开始一次 0.4〜1.2mg,一日2次，用量按需递增。最大限量一日 可达4 mg。"
# 结果效果：['（1）给药方式 ①……', '（1）给药方式 ②……']

def get_circle_str(str):
    result = []
    result1 = re.split(r'([①②③④⑤⑥⑦⑧⑨⑩]+)',str)
    if result1:
        str0 = result1[0]
        if str0 != "":
            result.append(str0)
        result1 = ["".join(i) for i in zip(result1[1::2], result1[2::2])]
        result.extend(result1)
    #①前匹配到给药方式时，拼接。序列前的文字一般是汇总，应该进行拼接
    take_str = result[0]
    take_patr_b = re.compile("^([①②③④⑤⑥⑦⑧⑨⑩]+)+")
    if not take_patr_b.search(take_str):
        result = ["".join(i) for i in zip([take_str] * (len(result) - 1), result[1::1])]

    return result

result1 = get_circle_str("（2）肌内或静脉注射成人①催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；②抗惊厥（常 用于治疗癫痫持续状态），缓慢静脉注射300〜500 mg。 成人极量一次0. 25 g,—日0. 5g。")
print("circle_cut:",result1)


#句内按指定分号切分
# sub_str = "②镇静催眠，0. 4〜0.8mg,睡前服。老年和 体弱患者开始用小量，一次0. 2 mg, 一日3次，逐渐递增 至最大耐受量。"
# 结果效果：result = ['②镇静催眠，0.4〜0.8mg,睡前服。', '②镇静催眠，老年和体弱患者开始用小量，一次0.2mg,一日3次，逐渐递增至最大耐受量。']
semicolon_str = "[;|；](用于|或|用作|硬膜外麻醉|臂丛神经阻滞麻醉|各种神经阻滞或硬膜外麻醉|镇静|催眠|抗惊厥)"
#100-200页内分号切分个例
semicolon_12_zd = "[;|；](快速气管插管|癫痫持续状态|麻醉前用药|术后应用|拮抗东芨着碱中毒|癫痫持续状态|牙科|肋间神经|宫颈旁浸润|椎旁脊神经阻滞|阴部神经)"
#100-200页内无分号切分个例
semicolon_12_str = "用作胶原酶合成抑制剂时"
semiconlon_patr = re.compile(semicolon_str)

#按分号切分句子
import re
def get_semi_cut(str):
    # str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    semi_result = []
    if semiconlon_patr.search(str):
        semi_result = re.split(r'('+semicolon_str+')+',str)


    return semi_result
semi_str = "（2）肌内或静脉注射成人①催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；"
semi_str1="（1） 口服 成人 抗癫痫一般一次 0.03g，一日3次；或 0. 09 g睡前顿服。极量一次0. 25 g。一日 0. 5g。"
print(get_semi_cut(semi_str1))



test_sub_list =['口服 成人 ①抗焦虑，开始一次 0.4〜1.2mg,一日2次，用量按需递增。最大限量一日 可达4 mg。', '口服 成人 ②镇静催眠，0. 4〜0.8mg,睡前服。老年和 体弱患者开始用小量，一次0. 2 mg, 一日3次，逐渐递增 至最大耐受量。', '口服 成人 ③抗恐惧，一次0.4 mg,一日3次，需要 时逐渐增加剂量，一日最大量可达10 mg。']
# 考虑匹配年龄和用药方式
#按年龄切分句子
age_patr = re.compile("[，。,.]+?(<1岁|幼儿|小儿|\d+〜\d+岁小儿|\d+岁以上患儿|成人|老年.?体弱.?者|年老.?体弱.?者|老年人|儿童)+")
circle_sub_patr = re.compile("([①②③④⑤⑥⑦⑧⑨⑩]+)[^，。,]+[，。,]+?")#匹配序列标号后第一个句子

#最后一句匹配到年龄不进行切分
def get_age_cut(str):
    str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    age_result= []
    f = re.finditer(age_patr,str)#获取匹配年龄字段的indx
    if f:
        indexes = [i.start() for i in f]
        start = 0
        for i, indx in enumerate(indexes):
            sbstr = str[start:indx+1]
            age_result.append(sbstr)
            if i == len(indexes) - 1:
                sbstr1 = str[indx+1:]
                age_result.append(sbstr1)
            start = indx+1
    if age_result:
        b_str = ""
        circle_match = circle_sub_patr.search(age_result[0])
        if circle_match:
            b_str = circle_match.group()
        if b_str !="":
            rlen = len(age_result)
            for i in range(1,rlen):
                age_result[i] = b_str+age_result[i]
    else:
        age_result.append(str)

    return age_result

#从头开始完整处理一个句子
bracket_patr = re.compile("([（(]\d[）)]){1}")
def get_sentence_cut(str):
    str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    circle_patr = re.compile(r'([①②③④⑤⑥⑦⑧⑨⑩]+)')
    bracket_list=[]
    circle_list=[]
    semiconlon_list = []

    #str有括号（）
    if bracket_patr.search(str):
        bracket_list1 = get_bracket_str(str)
        b1 = bracket_list1[0]
        if not bracket_patr.search(b1):
            bracket_list = ["".join(i) for i in zip([b1]*(len(bracket_list1)-1),bracket_list1[1::1])]
    else:
        bracket_list.append(str)

    #str中没有（），判断是否有①圆括号
    if bracket_list:
        for ci in bracket_list:
            yuan_list = circle_patr.findall(ci)
            if len(yuan_list)>1:
                cir_list = get_circle_str(ci)
                circle_list.extend(cir_list)
            else:
                circle_list.append(ci)

     #句内切分
    # if circle_list:










    #
    # for i, con in enumerate(str):
    #     len_list = len(test_sub_list)
    #     if i !=  (len_list-1):
    #         result = get_age_cut(con)
    #         print("句内年龄切分：",result)


