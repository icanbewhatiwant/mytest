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
           "|老年患者|重症患者|肝、肾疾病患者|老年、女性、非吸烟、有低血压倾向、严重肾功能损害或中度肝功能损害患者|新生儿|幼儿和儿童|幼儿|儿童青?少年|儿童" \
           "|<?\d*岁|\d*[-|〜|~|~]?\d*岁小儿|\d*岁以上患?儿?|\d*[-|〜|~|~]\d*岁|\d*岁以下|d*岁或以上者|>\d*岁|小儿|的?患?者)"

age_patr = re.compile(age_str+"+")
def get_age(str):
    age_str = ""
    age_search = age_patr.search(str)
    if age_search:
        age_list = age_patr.finditer(str)#以列表形式返回全部能匹配的子串
        age_str_list = [f.group() for f in age_list]
        age_str = age_str_list[-1]
    return age_str
print("age:",get_age(test_str))

weight_teststr = "①静脉滴注体重低于70kg（或血压不稳定）者，开始2小时可按每小时7.5μg/kg给药；如耐受性好，2小时后剂量可增至每小时15μg/kg。体重大于70kg者，开始2小时宜按每小时15μg/kg给药；如耐受性好，2小时后剂量可增至每小时30μg/kg。②体重34kg以下小儿,肌内注射2mg。或先静脉注射1mg,如30〜45秒钟无效，再重复静脉注射1mg,直到总量达5mg；③体重34kg以上儿童，肌内注射5mg,或先静脉注射2mg,若30~45秒钟无效，再重复静脉注射1mg,直到总量10mg。"
weight_teststr1 = "口服24-40kg的儿童，早、晚各lOOmg（2袋），或遵医嘱。"
weight_teststr2 = "2～12岁儿童：体重≤30公斤：一日1次，一次半片(5毫克)。"


def get_weight(str):
    weight_str = "(低于|大于|≤|<|>≥)?\d+[-|〜|~|~]?\d+(kg|公斤)(以下|以上)?"
    weight_patr = re.compile(weight_str)
    weight_str = ""
    weight_search = weight_patr.search(str)
    if weight_search:
        weight_iter = weight_patr.finditer(str)
        weight_str_list = [f.group() for f in weight_iter]
        weight_str = weight_str_list[-1]
    return weight_str
print("weight:", get_weight(weight_teststr2))


#单次推荐剂量
# 一次……，一日……
dose_str1 = "(一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|~|~]?\d*\.?\d*(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(一日|—日|每晚)\d*\.?\d*[-|〜|~|~]?\d*\.?\d*(次|ml)?"
# 一次……mg
dose_str2 = "(一次)[^,.;，。；(不超过)]*\d*\.?\d*[-|〜|~|~]?\d*\.?\d*(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"
#一日，分N次
dose_str3 = "(一日|—日|按体重)[^,.;，。；]*\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).?(分成|分)\d*\.?\d*[-|〜|~]?\d*\.?\d*(次)?"
# 一日……一日……
dose_str4 = "(一日|—日)[^,.;，。；]*\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).?(一日|—日)\d*\.?\d*[-|〜|~]?\d*\.?\d*(次)?"
#0. 4〜0.8mg
dose_str5 = "\d*\.?\d*%?[-|〜|~]?\d*\.?\d*(mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)"
# 每1kg体重0.15〜0.2mg。
dose_str6 = "每\d*kg体重\d*\.?\d*[-|〜|~]?\d*\.?\d*[μg|mg|ml|g]"

dose_patr = re.compile(dose_str5)
def get_single_dose(str):
    single_dose = "(低于|大于|≤|<|>≥)?\d+[-|〜|~|~]?\d+(kg|公斤)(以下|以上)?"
    single_dose_patr = re.compile(single_dose)
    single_dose_str = ""
    single_dose_search = single_dose_patr.search(str)
    if single_dose_search:
        single_dose_iter = single_dose_patr.finditer(str)
        single_dose_str_list = [f.group() for f in single_dose_iter]
        single_dose_str = single_dose_str_list[-1]
    return single_dose_str
print("single_dose:", get_single_dose(weight_teststr2))






