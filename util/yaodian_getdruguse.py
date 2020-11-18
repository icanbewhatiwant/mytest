from util.doseProcess import get_stime_sday
from util.doseProcess import get_stime_jici
from util.doseProcess import get_sday_stime
from util.doseProcess import get_weight_time
from util.doseProcess import get_stime

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

age_str = "(成人|肝、肾功能损害者|高龄患者|老年和体弱或肝功能不全患者|老年人?[或及、和]?体弱患?者|老年人?[或及、和]?虚弱的?患?者|老年人|年老[或及、和]?体弱患?者|特殊人群：严重肝损患者|老年、重病和肝功能受损患者" \
           "|老年患者|重症患者|肝、肾疾病患者|老年、女性、非吸烟、有低血压倾向、严重肾功能损害或中度肝功能损害患者|新生儿|幼儿和儿童|幼儿|儿童青?少年" \
           "|\d*[-|〜|～|~]?\d+岁小儿|\d+岁以上患?儿?|\d+岁以下|d+岁或以上者|<\d+岁|>\d+岁|\d*[-|〜|～|~]\d+岁|儿童|小儿|的?患?者)"

age_priority = re.compile("\d*[-|〜|～|~]\d+岁")
age_num_patr = re.compile("\d+")
age_unit_patr = re.compile("岁|月|天")
age_patr = re.compile(age_str)
person2age = {"成人":"16岁","新生儿":"","幼儿":"","儿童":"4岁","青少年":"14岁","小儿":"","老年人":""}
def get_age(str):
    age_result = {}
    age_str = ""
    age_unit_string = ""
    age_search = age_patr.search(str)
    if age_search:
        age_string = age_search.group()
        #匹配年龄所在的一句话
        age_sentence_patr = re.compile("[,，。;；]?[^,，。;；]*" + age_string + "[^,，。;；]*[,，。;；]")
        age_sentence = age_sentence_patr.search(str).group()

        age_priority_match=age_priority.search(age_sentence)
        #年龄所在句子优先匹配
        if age_priority_match:
            age_string = age_priority_match.group()
            age_low_high = age_num_patr.findall(age_string)
            age_result["age_low"] =age_low_high[0]
            if len(age_low_high)>1:
                age_result["age_high"] = age_low_high[1]
            else:
                age_result["age_high"] = age_low_high[0]
            age_unit_string = age_string
        else:
            age_list = age_patr.finditer(age_sentence)#以列表形式返回全部能匹配的子串
            age_str_list = [f.group() for f in age_list]
            age_str = age_str_list[-1]
            if age_str in person2age.keys():
                age_result_str = person2age[age_str]
                age_low_high = age_num_patr.findall(age_result_str)
                age_result["age_low"] = age_low_high[0]
                age_unit_string =age_result_str
        #年龄单位
        age_unit_search = age_unit_patr.search(age_unit_string)
        if age_unit_search:
            age_result["age_unit"] = age_unit_search.group()

    return age_result
age_test1 = "口服24-40kg的儿童，早、晚各lOOmg（2袋），或遵医嘱。"
age_test = "2～12岁儿童：体重≤30公斤：一日1次，一次半片(5毫克)。"
print("age:",get_age(age_test1))


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
dose_str1 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(一日|—日|每日|每晚|晚上|按体重)\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"

# 一次……mg,一日……次  单次推荐剂量 推荐给药频次
dose_str7 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(隔日|一日|—日|每日|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周))(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次"
# 一次……mg 单次推荐剂量
dose_str2 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*?\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"
#一日……mg，分N次  单日推荐剂量，推荐给药频次
dose_str3 = "(一日|—日|每日|每晚|晚上|按体重)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).*?(隔日|一日|—日|每日|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周))(\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次"
# 一日……mg 单日推荐剂量
dose_str4 = "(一日|—日|每日|每晚|晚上)[^,.;，。；]*?\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"
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

pingci = re.compile("隔日|一日|—日|每日|分成|分|晚上|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周)")
cishu = re.compile("(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次")
pingci_geri = re.compile("隔日")
pingci_1day = re.compile("一日|—日|每日|分成|分|晚上|每晚")
pingci_hour = re.compile("(?:\d|[一二三四五六七八九十])小时")
pingci_day = re.compile("(?:\d|[一二三四五六七八九十])日")
pingci_week = re.compile("(?:\d|[一二三四五六七八九十])周")

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

        #匹配用量所在最多连续两句话
        dose_sentence_patr = re.compile("[,，。;；]?[^,，。;；]*"+single_dose_str+"[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?")
        dose_sentence = dose_sentence_patr.search(str).group()

        #用量的各种匹配模式
        stime_sday_search = dose_stime_sday.search(dose_sentence)
        stime_search = dose_stime.search(dose_sentence)
        sday_stime_search = dose_sday_stime.search(dose_sentence)
        sday_search = dose_sday.search(dose_sentence)
        sweight_search = dose_sweight.search(dose_sentence)
        stime_jici_search = dose_stime_jici.search(dose_sentence)

        # 获取给药频次数据，分解 推荐给药频次低值、高值、描述
        #单次推荐剂量和单日推荐剂量
        if stime_sday_search:
            dose_result = get_stime_sday(single_dose_str, dose_sentence)
        elif stime_jici_search:
            dose_result = get_stime_jici(single_dose_str, dose_sentence)
        elif sday_stime_search:
            dose_result = get_sday_stime(single_dose_str, dose_sentence)
        elif sweight_search:
            dose_result = get_weight_time(single_dose_str, dose_result)
            single_dose_str+="/kg"
        elif  stime_search:
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
test_str9 = "皮下注射或静脉注射成人常用量一次5〜10mg。极量一日40mg。"
dose3_string = "（1）口服成人①抗焦虑，一次2.5〜10mg"

print("single_dose:", get_single_dose(dosestime_sting))

#获得单次剂量极值、单日剂量极值
limit_list = ["极量","极最"]
def get_limit(str):
    limit_result = {}
    limit_num_patr = re.compile("\d*\.?\d+")
    # 极量所在句，后面有句子时，往后再匹配最多一句
    limit_2sen = "[,，。;；]?[^,，。;；]*极量.?[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?"
    limit_1day = re.compile("(?:一日|—日|每日|每晚)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")
    #
    limit_2patrr = re.compile(limit_2sen)
    limit_2search = limit_2patrr.search(str)
    #极量所在句子+后面一句

    #单次剂量极值匹配时按极量所在句子匹配第一个用量，提高匹配度（一次这种匹配度比较低）单日的则一般是后面一个句子，用"一日"匹配，准确率高一些
    # 也有一日极量的，这里还是需要修改，排除每日关键字
    if limit_2search:
        limit_sentence = limit_2search.group()
        dose_patr = re.compile(dose_str5)
        dose_str = ""
        dose_search = dose_patr.search(limit_sentence)
        if dose_search:
            dose_iter = dose_patr.finditer(limit_sentence)
            dose_str_list = [f.group() for f in dose_iter]
            dose_str = dose_str_list[0]
            limit_result["limit_1time"] = limit_num_patr.search(dose_str).group()

        day_search = limit_1day.search(limit_sentence)
        if day_search:
            limit_1daystr = limit_num_patr.search(day_search.group())
            if limit_1daystr:
                limit_result["limit_1day"] = limit_1daystr.group()

    return limit_result

limit_sting = "（1）口服抗惊厥，一日90~180mg,可在晚上一次顿服，或30〜60mg,一日3次。极量250mg,—日500mg。老年人或虚弱患者应减量，常用量即可产生兴奋、精神错乱或抑郁。"

limit_string1="（1）癫痫口服成人每日按体重15mg/kg"
limit_string2 = "（3）阿片全碱皮下注射②极量，一次30mg。"

print("stime_limit:", get_limit(limit_string2))

