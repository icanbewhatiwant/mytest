from util.doseProcess import get_stime_sday
from util.doseProcess import get_stime_jici
from util.doseProcess import get_sday_stime
from util.doseProcess import get_weight_time
from util.doseProcess import get_stime
from util.doseProcess import get_sday
from util.doseProcess import get_stimeday_limit

import re
# 需要提取字段
# 年龄、体重、给药途径、单次推荐剂量、单日推荐剂量、单次剂量极值、单日剂量极值，推荐给药频次、推荐给药描述、用药推荐天数

test_str = "（2）肌内或静脉注射成人①口服基础麻醉或静脉全麻。10-30mg。"
print("str:",test_str)
admin_route_str = "(口服.灌肠|餐?后?口服成?人?|含服|涂敷患?处?|喷于患处|外用|肌内注?射?或缓?慢?静脉缓?慢?注射|静脉注?射?或肌内注射" \
                  "|肌内注射或缓?慢?静脉缓?慢?推注|皮下或肌内注射|肌内或皮下注射|静脉注射|静脉滴注|深?部?肌内注射|皮下注射|静脉推注|冲服|嚼服|浸润局麻|浸润麻醉|外周神经\(丛\)阻滞|外用" \
                  "|滴眼|滴鼻|冲洗|阴道给药|肛门内?给药|舌下含服|阴道用药|瘤体注射|吸入|阴道冲洗|漱口|关节腔注射|处方|保留灌肠|灌肠|直肠灌注|贴患处" \
                  "|注入脐静脉|涂抹|靶控输注系统给药|注入)"

take_patr = re.compile(admin_route_str+"+")
#返回句中最远的给药方式，即离后面主要句子最近的给药方式
def get_admin_route(str):
    admin_route_str = ""
    admin_search = take_patr.search(str)
    if admin_search:
        admin_route = take_patr.finditer(str)#以列表形式返回全部能匹配的子串
        admin_route_list = [f.group() for f in admin_route]
        admin_route_str = admin_route_list[-1]
    return admin_route_str

print("admin_route:",get_admin_route(test_str))

# age_str = "(成人|肝、肾功能损害者|高龄患者|老年和体弱或肝功能不全患者|老年人?[或及、和]?体弱患?者|老年人?[或及、和]?虚弱的?患?者|老年人|年老[或及、和]?体弱患?者|特殊人群：严重肝损患者|老年、重病和肝功能受损患者" \
#            "|老年患者|重症患者|肝、肾疾病患者|老年、女性、非吸烟、有低血压倾向、严重肾功能损害或中度肝功能损害患者|新生儿|幼儿和儿童|幼儿|儿童青?少年" \
#            "|\d*[-|〜|～|~]?\d+岁小儿|\d+岁以上患?儿?|\d+岁以下|\d+岁或以上者|<\d+岁|>\d+岁|\d*[-|〜|～|~]\d+岁|儿童|小儿|的?患?者)"

#年龄数字+人描述词（有年龄对应的）
person2age_string = "(?:成人|新生儿|婴儿|幼儿|儿童|青少年|小儿|少儿|老年人|老人)"
age_d2d_patr = re.compile("(?:\d+[-|〜|～|~]\d+岁)[^,.;，。；]*?"+person2age_string+"?")
age_lowd_patr = re.compile("(?:\d+岁以上|>\d+岁|\d+岁或以上)[^,.;，。；]*?"+person2age_string+"?")
age_highd_patr = re.compile("(?:\d+岁以下|<\d+岁|\d+岁或以下)[^,.;，。；]*?"+person2age_string+"?")
person_patr = re.compile(person2age_string)


age_priority = re.compile("\d*[-|〜|～|~]?\d+(?:岁|月|天)")
age_num_patr = re.compile("\d+")
age_unit_patr = re.compile("岁|月|天")
# age_patr = re.compile(age_str)
person2age = {"成人":{"low":"16","unit":"岁"},"新生儿":{"low":"0","high":"28","unit":"天"},"婴儿":{"low":"28","high":"12","unit":"天/月"},
              "幼儿":{"low":"1","high":"3","unit":"岁"},"儿童":{"high":"16","unit":"岁"},"青少年":{"high":"18","unit":"岁"},"小儿":{"high":"7","unit":"岁"},
              "少儿":{"high":"12","unit":"岁"},"老年人":{"low":"65","unit":"岁"},"老人":{"low":"65","unit":"岁"}}
#只有岁数+年龄的能匹配到年龄高值、低值、单位，其他：患者……无法匹配
def get_age(str):
    age_result = {}
    age_unit_string = ""

    #数字化的年龄字段 4~20岁
    age_d2d_match=age_d2d_patr.search(str)
    age_lowd_match = age_lowd_patr.search(str)
    age_highd_match = age_highd_patr.search(str)
    person_match = person_patr.search(str)

    #数字年龄+人物描述
    if age_d2d_match:
        age_string = age_d2d_match.group()
        age_low_high = age_num_patr.findall(age_string)
        age_result["age_low"] =age_low_high[0]
        if len(age_low_high)>1:
            age_result["age_high"] = age_low_high[1]
        else:
            age_result["age_high"] = age_low_high[0]
        age_unit_string = age_string

    elif age_lowd_match:
        #指定低值
        age_string = age_lowd_match.group()
        age_low = age_num_patr.search(age_string).group()
        age_result["age_low"] = age_low
        age_unit_string = age_string

        per_match = person_patr.search(age_string)
        if per_match:
            per_age_dict = person2age.get(per_match.group(),{})
            if per_age_dict:
                age_high = per_age_dict.get("high","")
                if age_high !="":
                    age_result["age_high"] = age_high
                age_unit = per_age_dict.get("unit","")
                if age_unit !="":
                    age_result["age_unit"] = age_unit
    elif age_highd_match:
        #指定高值
        age_string = age_highd_match.group()
        age_high = age_num_patr.search(age_string).group()
        age_result["age_high"] = age_high
        age_unit_string = age_string

        per_match = person_patr.search(age_string)
        if per_match:
            per_age_dict = person2age.get(per_match.group(), {})
            if per_age_dict:
                age_low = per_age_dict.get("low", "")
                if age_low != "":
                    age_result["age_low"] = age_low
                age_unit = per_age_dict.get("unit", "")
                if age_unit != "":
                    age_result["age_unit"] = age_unit
    #仅有人物字段
    elif person_match:
        age_string = person_match.group()
        per_age_dict = person2age.get(age_string, {})
        if per_age_dict:
            age_low = per_age_dict.get("low", "")
            if age_low != "":
                age_result["age_low"] = age_low
            age_high = per_age_dict.get("high", "")
            if age_high != "":
                age_result["age_high"] = age_high
            age_unit = per_age_dict.get("unit", "")
            if age_unit != "":
                age_result["age_unit"] = age_unit

    #没有匹配到人的组合时，就没有年龄单位赋值
    if  age_result.get("age_unit","")=="" and age_unit_string !="":
        age_unit_search = age_unit_patr.search(age_unit_string)
        if age_unit_search:
            age_result["age_unit"] = age_unit_search.group()
    return age_result
age_test1 = "口服24-40kg的儿童，早、晚各lOOmg（2袋），或遵医嘱。"
age_test = "2～12岁儿童：体重≤30公斤：一日1次，一次半片(5毫克)。"
print("age:",get_age(age_test))


weight_teststr = "①静脉滴注体重低于70kg（或血压不稳定）者，开始2小时可按每小时7.5μg/kg给药；如耐受性好，2小时后剂量可增至每小时15μg/kg。体重大于70kg者，开始2小时宜按每小时15μg/kg给药；如耐受性好，2小时后剂量可增至每小时30μg/kg。②体重34kg以下小儿,肌内注射2mg。或先静脉注射1mg,如30〜45秒钟无效，再重复静脉注射1mg,直到总量达5mg；③体重34kg以上儿童，肌内注射5mg,或先静脉注射2mg,若30~45秒钟无效，再重复静脉注射1mg,直到总量10mg。"
weight_teststr1 = "口服24-40kg的儿童，早、晚各lOOmg（2袋），或遵医嘱。"
weight_teststr2 = "2～12岁儿童：体重≤30公斤：一日1次，一次半片(5毫克)。"
weight_high_patr = re.compile("低于|小于|≤|<|以下")
weight_low_patr = re.compile("大于|高于|>|≥|以上")
weight_num_patr = re.compile("\d+")
#获取体重高、低值
def get_weight(str):
    weight_result = {}
    weight_str = "(低于|大于|≤|<|>|≥)?\d+[-|〜|~|~]?\d+(kg|公斤)(以下|以上)?"
    weight_patr = re.compile(weight_str)
    weight_str = ""
    weight_search = weight_patr.search(str)
    if weight_search:
        weight_iter = weight_patr.finditer(str)
        weight_str_list = [f.group() for f in weight_iter]
        weight_str = weight_str_list[-1]
        if weight_low_patr.search(weight_str):
            weight_result["weight_low"] =weight_num_patr.search(weight_str).group()
        if weight_high_patr.search(weight_str):
            weight_result["weight_high"] = weight_num_patr.search(weight_str).group()
    return weight_result
print("weight:", get_weight(weight_teststr2))



# 一次……mg，一日……mg 单次推荐剂量 单日推荐剂量
dose_str1 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(一日|—日|每日|每天|每晚|晚上|24小时|按体重)\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"

# 一次……mg,一日……次  单次推荐剂量 推荐给药频次
dose_str7 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(隔日|一日|—日|每日|每天|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周))(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次"
# 一次……mg 单次推荐剂量
dose_str2 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*?\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"
#一日……mg，分N次  单日推荐剂量，推荐给药频次
dose_str3 = "(一日|—日|每日|每天|每晚|晚上|24小时|按体重)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).*?(隔日|一日|—日|每日|每天|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周))(\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次"
# 一日……mg 单日推荐剂量
dose_str4 = "(一日|—日|每日|每天|每晚|晚上|24小时|按体重)[^,.;，。；]*?\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"
#0. 4〜0.8mg
dose_str5 = "\d*\.?\d*%?[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)"
# 每1kg体重0.15〜0.2mg。
dose_str6 = "每\d*kg体重\d*\.?\d*[-|〜|～|~]?\d*\.?\d+[μg|mg|ml|g]"

dose_timestr = "(隔日|一日|—日|每日|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周))(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次"
chi_dose_timestr = "[一二三四五六七八九十]次"

dose_stime_sday = re.compile(dose_str1)
dose_stime = re.compile(dose_str2)
dose_sday_stime = re.compile(dose_str3)
dose_sday = re.compile(dose_str4)
dose_sweight = re.compile(dose_str6)
dose_stime_jici = re.compile(dose_str7)

time_patr = re.compile(dose_timestr)
chi_time_patr = re.compile(chi_dose_timestr)
num_patr = re.compile("\d*\.?\d+")
chi_num_patr = re.compile("[一二三四五六七八九十]+")
dose_num_patr = re.compile("\d*\.?\d*%?[-|〜|～|~]?\d*\.?\d+")
dose_unit_patr = re.compile("mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%")
chi2num = {"一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","十":"10"}

pingci = re.compile("隔日|一日|—日|每日|每天|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周)")
cishu = re.compile("(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次")
pingci_geri = re.compile("隔日")
pingci_1day = re.compile("一日|—日|每日|每天|分成|分|晚上|每晚")
pingci_hour = re.compile("(?:\d|[一二三四五六七八九十])小时")
pingci_day = re.compile("(?:\d|[一二三四五六七八九十])日")
pingci_week = re.compile("(?:\d|[一二三四五六七八九十])周")

#获得单次剂量极值、单日剂量极值
#极量关键字
limit_list = ["极量","极最","限量","限最","极限","为限","最大剂量","剂量最大","剂量不超过","剂量不得超过","剂量不宜超过","剂量最大","最大量","最大最","最髙量","最高量","最大日剂量","日剂量不超过","最大每日","最大每次","最大滴定剂量","最高不能超过","一日剂量不得超过","—日剂量不宜超过","24小时不超过"]
#判断句子是否包含极量关键字
def is_limit(str):
    flag = False
    for i in limit_list:
        if i in str:
            flag = True
            break
    return flag

#获取单次推荐剂量、推荐给药频次、单日推荐剂量、剂量单位
def get_single_dose(str):
    dose_result = {}
    single_dose_patr = re.compile(dose_str5)#0. 4〜0.8mg
    single_dose_str = ""
    single_dose_search = single_dose_patr.search(str)
    #获取匹配到的第一个给药剂量，一般是单次给药剂量的概率较大
    if single_dose_search:
        single_dose_iter = single_dose_patr.finditer(str)
        single_dose_str_list = [f.group() for f in single_dose_iter]
        single_dose_str = single_dose_str_list[0]

        # 排除与"极量"同意的句子、最大剂量、最大量,最大最,最髙量,最高量、等关键字
        #匹配用量所在一句话
        dose_1sentence_patr = re.compile("[,，。;；]?[^,，。;；]*"+single_dose_str+"[^,，。;；]*[,，。;；]?")
        dose_1sentence = dose_1sentence_patr.search(str).group()
        #第一句话就包含极值关键字，则后面句子也为极值句子，不用继续判断
        if is_limit(dose_1sentence):
            return dose_result

        #匹配用量所在最多连续两句话
        dose_sentence_patr = re.compile("[,，。;；]?[^,，。;；]*"+single_dose_str+"[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?")
        dose_sentence = dose_sentence_patr.search(str).group()
        #前面一句不包含极值关键字，判断后面一句是否包含极值关键字,包含则只取第一个句子提取推荐剂量，否则两句都可以
        if is_limit(dose_sentence):
            dose_sentence = dose_1sentence

        #用量的各种匹配模式
        stime_sday_search = dose_stime_sday.search(dose_sentence)
        stime_search = dose_stime.search(dose_sentence)
        sday_stime_search = dose_sday_stime.search(dose_sentence)
        sday_search = dose_sday.search(dose_sentence)
        sweight_search = dose_sweight.search(dose_sentence)
        stime_jici_search = dose_stime_jici.search(dose_sentence)

        # 获取给药频次数据，分解 推荐给药频次低值、高值、描述
        #单次推荐剂量和单日推荐剂量
        if stime_sday_search: # 一次……mg，一日……mg
            dose_result = get_stime_sday(single_dose_str, dose_sentence)
        if stime_jici_search:# 一次……mg,一日……次
            dose_result = get_stime_jici(single_dose_str, dose_sentence)
        elif sday_stime_search:#一日……mg，分N次
            dose_result = get_sday_stime(single_dose_str, dose_sentence)
        elif stime_search:# 一次……mg 单次推荐剂量  需要排除一些关键字(所在句子有：最大剂量,最大量,最大最,最髙量,最高量，不得超过，不超过)
            #添加获取总量，即单日推荐低值和高值  总量也能获取
            dose_result = get_stime(single_dose_str,dose_result,dose_sentence)
        elif sday_search:# 一日……mg 单日推荐剂量
            dose_result = get_sday(single_dose_str,dose_result,dose_sentence)
        elif sweight_search:# 每1kg体重0.15〜0.2mg。
            dose_result = get_weight_time(single_dose_str, dose_result)
            single_dose_str+="/kg"
        else:
            #不包含一些关键字的时候，默认选第一个为单次……按单次的方法处理
            dose_result = get_stime(single_dose_str,dose_result)
        #获取剂量单位
        single_dose_unit = dose_unit_patr.search(single_dose_str)
        if single_dose_unit:
            dose_result["single_dose_unit"] = single_dose_unit.group()
    return dose_result

dose1_string = "（1）口服成人①抗焦虑，一次2.5〜10mg,一日2〜4次。"
dose2_string = "（1）口服抗惊厥，一日90~180mg,可在晚上一次顿服，或30〜60mg,一日3次。极量一次250mg,—日500mg。老年人或虚弱患者应减量，常用量即可产生兴奋、精神错乱或抑郁。"
dosestime_sting = "皮下注射或静脉注射成人常用 量一次5〜10mg。极量一日40mg。"
dosestime_stime = "（3）儿童剂量可稍高，每1kg体重0.2mg；用于维持麻醉时，小剂量静脉注射,剂量及注射间隔视患者个体差异而定。"
test_str9 = "（1）镇痛①口服成人常用量：一次50〜100mg,一日200〜400mg。"
dose3_string = "（2）肌内注射抗惊厥一次6〜10mg/kg,必要时4小时后可重复，一次极量不超过0.2g。"

print("single_dose:", get_single_dose(dose3_string))

#获取单次、单日极量极值
limit_1time = re.compile("(?:每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g|%)")
limit_1day = re.compile("(?:一日|—日|每日|每天|每晚|晚上|24小时)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")


# 单次、单日剂量极值关键字（除了极量）
day_limit_str = "(?:限量|限最|极限|最大剂量|剂量最大|最大滴定剂量|最大量|最大最|限量|剂量不超过|最大|剂量不得超过|剂量不宜超过|最高不能超过|不超过)"
day_limit_patr = re.compile("(?:一日|—日|每日|每天|每晚|晚上|日|24小时内|24小时)[^,，。;；]*"+day_limit_str+"[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")
day_limit_patr2 = re.compile("[,，。;；][^,，。;；]*"+day_limit_str+"[^,，。;；]*(?:一日|—日|每日|每天|每晚|晚上|日|24小时内|24小时)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")
#……为限
day_limit_patr3 = re.compile("(?:一日|—日|每日|每天|每晚|晚上|日|24小时内|24小时)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)(?:为限|为极限)")
time_limit_str = "(?:限量|限最|极限|为限|最大剂量|剂量最大|剂量不超过|剂量不得超过|剂量不宜超过|最大量|最大最|最高不能超过|最大每次|最髙量|最高量)"
time_limit_patr = re.compile("(?:每次|一次|初量|开始时|开始|初次量|初始量)[^,，。;；]*"+time_limit_str+"[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")
time_limit_patr2 = re.compile("[,，。;；][^,，。;；]*"+time_limit_str+"[^,，。;；]*(?:每次|一次|初量|开始时|开始|初次量|初始量)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")
time_limit_patr3 = re.compile("(?:每次|一次|初量|开始时|开始|初次量|初始量)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)(?:为限|为极限)")
# 在单次剂量过滤的关键字中，包含以上这些单次、单日极值，保证不会把极值存在单次剂量和单日剂量中，也保证过滤的极值会在单次剂量中获得
# limit_list = ["极量","极最","限量","极限","为限","最大剂量","剂量最大","剂量不超过","剂量不得超过","剂量不宜超过","剂量最大","最大量","最大最","最髙量","最高量","最大日剂量","日剂量不超过","最大每日","最大每次","最大滴定剂量","最高不能超过","一日剂量不得超过","—日剂量不宜超过","24小时不超过"]

def get_limit(str):
    limit_result = {}
    limit_num_patr = re.compile("\d*\.?\d+")
    # (优先级最高)极量所在句，后面有句子时，往后再匹配最多一句
    limit_2sen = "[,，。;；]?[^,，。;；]*(?:极量|极最|最大日剂量|最大滴定剂量|最大剂量).?[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?"
    limit_2patrr = re.compile(limit_2sen)
    limit_2search = limit_2patrr.search(str)
    if limit_2search:
        #极量关键字如果在前一句，则前后都为极量，如果在一日，则一般一日在前。
        limit_sentence = limit_2search.group()
        limit_result = get_stimeday_limit(limit_sentence)
    #其他有极量关键字的，与一次、一日不在同一句的，不要再往前匹配每日、每次，可能是错的
    else:
        time_limit_list = []
        day_limit_list = []
        if time_limit_patr.search(str):
            time_limit_list = time_limit_patr.finditer(str)
        elif time_limit_patr2.search(str):
            time_limit_list = time_limit_patr2.finditer(str)
        elif time_limit_patr3.search(str):
            time_limit_list = time_limit_patr3.finditer(str)
        if time_limit_list:
            time_limit_str_list = [f.group() for f in time_limit_list]
            #以最后一次匹配到的极值数据作为单次剂量极值
            limit_1time_num_list = limit_num_patr.findall(time_limit_str_list[-1])
            if limit_1time_num_list:
                limit_result["limit_1time"] = limit_1time_num_list[-1]
        if day_limit_patr.search(str):
            day_limit_list = day_limit_patr.finditer(str)
        elif day_limit_patr2.search(str):
            day_limit_list = day_limit_patr2.finditer(str)
        elif day_limit_patr3.search(str):
            day_limit_list = day_limit_patr3.finditer(str)
        if day_limit_list:
            day_limit_str_list = [f.group() for f in day_limit_list]
            # 以最后一次匹配到的极值数据作为单日剂量极值
            day_limit_string = day_limit_str_list[-1]
            limit_day_num_list = limit_num_patr.findall(day_limit_string)
            if limit_day_num_list:
                limit_result["limit_1day"] = limit_day_num_list[-1]

            #如果单次剂量为空，此时剂量单位应该也为空，补充为剂量极值的单位
            if limit_result.get("single_dose_unit","") == "":
                single_dose_unit = dose_unit_patr.search(day_limit_string)
                if single_dose_unit:
                    limit_result["single_dose_unit"] = single_dose_unit.group()
    return limit_result

limit_sting = "（2）肌内注射抗惊厥一次6〜10mg/kg,必要时4小时后可重复，一次极量不超过0.2g。"
limit_string1="皮下注射、肌内注射或静脉注射每次10mg,必要时3〜6小时重复。最大剂量每次20mg,每天160mg。"
limit_string2 = "（2）肌内或缓慢静脉注射成人肌内注射0.1g,可每6小时1次，24小时内不超过0.5g。"

print("stime_limit:", get_limit(limit_sting))

liaocheng_str = re.compile("[,，。;；]?[^,，。;；]*\d*\.?\d*(?:天|日|周|月)?[-|〜|～|~]?\d*\.?\d+(?:天|日|周|月)[^,，。;；]*疗程")
liaocheng_after_str = re.compile("[,，。;；]?[^,，。;；]*疗程[^,，。;；]*\d*\.?\d*(?:天|日|周|月)?[-|〜|～|~]?\d*\.?\d+(?:天|日|周|月)")
#用几日停几日这种，可以计算相加
liaocheng_neg = re.compile("[,，。;；]?[^,，。;；]*停\d*\.?\d*(?:天|日|周|月)?[-|〜|～|~]?\d*\.?\d+(?:天|日|周|月)[^,，。;；]*疗程")
liaocheng_patr = re.compile("\d+(?:天|日|周|月)")
low_high_patr = re.compile("\d*\.?\d+[-|〜|～|~]\d*\.?\d+(?:天|日|周|月)")
liaocheng_num = re.compile("\d+")
liaocheng_unit = re.compile("天|日|周|月")
unit2num = {"周":"7","天":"1","日":"1","月":"30"}
def get_recomend_days(str):
    dose_result = {}
    #用几日停几日
    liaocheng_neg_match = liaocheng_neg.search(str)
    liaocheng_match = liaocheng_str.search(str)
    liaocheng_after_match = liaocheng_after_str.search(str)
    tian_list = []
    if liaocheng_neg_match:
        neg_tian_list = []
        liaocheng_list = liaocheng_patr.findall(liaocheng_neg_match.group())
        if liaocheng_list:
            for i in liaocheng_list:
                tian = liaocheng_num.search(i).group()
                num_unit = unit2num.get(liaocheng_unit.search(i).group(),"")
                neg_tian_list.append(int(tian)*int(num_unit))
        if neg_tian_list:
            tian_list.append(sum(neg_tian_list))
    elif liaocheng_match or liaocheng_after_match:
        liaocheng_list = []
        if liaocheng_match:
            liaocheng_list = liaocheng_patr.findall(liaocheng_match.group())
        else:
            liaocheng_list = liaocheng_patr.findall(liaocheng_after_match.group())

        if liaocheng_list:
            #3天~4天
            if len(liaocheng_list)>1:
                for i in liaocheng_list:
                    tian = liaocheng_num.search(i).group()
                    num_unit = unit2num.get(liaocheng_unit.search(i).group(), "")
                    tian_list.append(int(tian) * int(num_unit))
            # 可能包含3~4天这种、或者3天这两种情况
            else:
                unit_string = liaocheng_list[0]
                num_unit = unit2num.get(liaocheng_unit.search(unit_string).group(), "")
                #3~4天
                low_high_match= low_high_patr.search(str)
                if low_high_match:
                    tianshu_list = liaocheng_num.findall(low_high_match.group())
                    if tianshu_list:
                        tian_list = [int(num_unit)*int(i) for i in tianshu_list]
                #4天
                else:
                    tian = liaocheng_num.search(liaocheng_list[0]).group()
                    tian_list.append(int(tian)*int(num_unit))
    if tian_list:
            if len(tian_list)==1:
                dose_result["recommand_days_low"] = tian_list[0]
                dose_result["recommand_days_high"] = tian_list[0]
            else:
                dose_result["recommand_days_low"] = tian_list[0]
                dose_result["recommand_days_high"] = tian_list[1]
    return dose_result

tian_string = "(1)口服成人①一次0.5g，一日3次，连用3日停4日为1个疗程。"
tian_string2 = "静脉滴注急性脑血栓和脑栓塞：一日2万〜4万U,溶于5%葡萄糖氯化钠注射液或右旋糖酊-40注射液500ml中,分1〜2次给药。疗程7天〜3周。可根据病情增减剂量。"
tian_sting3 = "口服一次30万U,一日3次，连用4周为1个疗程。可连服2〜3个疗程，也可连续服用至症状好转。"
tian_no = "静脉滴注首次剂量为10BU,以后维持剂量可减为5BU,隔日1次。先用0.9%氯化钠注射液100〜250ml稀释后，静脉滴注1〜1.5小时。一般治疗急性脑血管病，隔日一次，3次为1个疗程。"

print("recommand days:",get_recomend_days(tian_sting3))









