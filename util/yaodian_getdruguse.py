from util.doseProcess import get_stime_sday
from util.doseProcess import get_stime_jici
from util.doseProcess import get_sday_stime
from util.doseProcess import get_weight_time
from util.doseProcess import get_stime
from util.doseProcess import get_sday
from util.doseProcess import get_stimeday_limit
from util.doseProcess import get_rongye_dose
from util.doseProcess import get_pingci
import os

import re
import json
# 提取需要的字段
# 年龄、体重、给药途径、单次推荐剂量、单日推荐剂量、单次剂量极值、单日剂量极值，推荐给药频次、推荐给药描述、用药推荐天数

#给药方式
admin_route_str = "(涂在溃疡表面|贴用|口腔鼓漱|根管冲洗|冲洗根管|置穿髓孔或根髓断面上|覆盖洞底|封入根管|涂布窝洞|贴在病损处|区域注射|贴敷于病变局部|贴敷于患牙处|贴敷于牙面|贴敷于患区表面" \
                  "|雾化\(超声或蒸汽\)吸入|鼓室内注射|局部涂用|血管瘤内注射及黏膜下注射|黏膜下注射|涂患处|鼻腔内滴入|滴鼻或喷入鼻腔|涂于膜组织表面|涂于下眼睑内|注入前房|前房内注射" \
                  "|伤口冲洗或湿敷|涂药于患处|洗漱|涂于患处|涂于患部|涂于创面|局部外用|放于阴道|注入阴道|推入阴道|放入宫腔|置入宫腔底部|腹壁皮下埋植|局部用药|涂抹外阴" \
                  "|放入阴后穹窿处|放入阴道后穹窿处|阴道后穹窿放置|置于阴道后穹窿处|羊膜腔外宫腔内给药|羊膜腔内给药|阴道内置入|宫颈给药|胸腔注射|颈内动脉注射|吸入气溶胶|“弹丸”吞咽" \
                  "|腹腔内注射和动脉内灌注|静脉“弹丸”式?注入|“弹丸”式注射|“弹丸”式静?脉?注入|静脉注射.口服|穿刺或经导管注入|导管直?接?注入|经鼻腔吸入|冲洗、湿敷患处，冲洗腔道或用于滴耳、滴鼻" \
                  "|洗涤、湿敷，也可口腔含漱、滴鼻|冲洗创伤伤口|灌洗创面|滴患处|含漱|涂搽|外涂|喷洒|外搽|外擦|滴药|涂擦|擦拭皮肤|擦拭|瘤内或瘤周注射|涂入?结膜囊内?|置入下结膜囊内|滴入结膜囊" \
                  "|静脉注射.皮下注射|注射于鞘内|肌内注射.皮下注射.病灶注射|喷洒或涂布|涂布|膀胱保留灌注|皮内针刺|皮肤划痕|瘤内.瘤周注射|皮内注射|静脉.心室腔内注射|塞肛门内" \
                  "|皮下注射.肌内注射.静脉注射|肝动脉给药|胸、腹腔注射|浆膜腔内注射|膀胱腔内灌注|腔内灌注|胸腹腔注射.心包腔内注射|瘤内注射|外敷|创面冲洗|腔内注射|静脉冲入|静脉注射.动脉.注射" \
                  "|置入阴道内|用水送服|整片咽下|膀胱冲洗|湿敷|鞘内或脑室内注射|肌内注射.静脉滴注.静脉注射|肌注.静脉滴注|肌注.静滴|胸腔.注射|心室内注射|局部搽涂|局部涂敷|涂敷" \
                  "|关节腔内.皮下注射|口服.灌肠|口服或舌下含服|口服或皮下注射|舌下含服.舌下喷雾.黏膜给药|口服.静脉注射|口服静脉滴注|静脉滴注.肌内注射|口服.肌内注射.静脉滴注" \
                  "|口服.肌内注射.静脉注射|肌内.静脉注射.静脉滴注|餐?后?口服成?人?|涂敷患?处?|喷于患处|外用|肌内注?射?或缓?慢?静脉缓?慢?注射|静脉注?射?.肌内注射|肌内注射或缓?慢?静脉缓?慢?推注" \
                  "|静脉滴注或缓慢静脉推注|皮下或肌内注射|肌内或皮下注射|皮下.肌内注射.缓慢静脉注射|肌内注射.静脉注射|肌内注射.静脉滴注|心内注射或静脉注射|皮下.静脉注射|静脉注射.静脉滴注" \
                  "|静脉注射或滴注|静脉滴注.静脉注射|皮下注射.肌内注射|皮下注射.静脉注射|静脉缓?慢?注射|动脉插管注?射?|动脉.缓慢注射|动脉.注射|静脉滴注|静滴|球后注射|结膜下注射|关节腔内.肌内注射|深?部?肌内注射" \
                  "|肌注|皮下注射|静脉推注|静脉单?次?输注|静脉.?给药|冲服|嚼服|浸润局麻|浸润麻醉|外用|经眼给药|滴眼|滴鼻|阴道给药|肛门内?给药|舌下含服|含服|阴道用药|瘤体注射|喷雾吸入|雾化吸入" \
                  "|气雾剂?吸入|粉雾吸入|干粉吸入|吸入|阴道冲洗|漱口|关节腔内?注射|注射给药|处方|保留灌肠|灌肠|直肠灌注|直肠给药|贴患处|贴片|外贴|注入脐静脉|静脉注入|涂抹或填塞|涂抹|靶控输注系统给药" \
                  "|使用栓剂|肛门注入|注入|局部注射|放入阴道|阴道.给药|开水冲服|咀嚼服用|鞘内注射或关节腔、软组织等损伤部位内注射|鞘内注射|脑室内注射|冲洗|灌洗|滴耳|肛门灌入|喷药|含化|口含)"


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


fanwei_string = "[-|—|〜|～|~]"
#年龄数字+人描述词（有年龄对应的）
person2age_string = "(?:成人|新生儿|婴幼?儿|幼儿|儿童|青少年|小儿|少儿|老年人|老人|患儿|早产儿)"
age_unit_string = "(?:岁|个?月"+person2age_string+"|天"+person2age_string+"|日"+person2age_string+")"
age_dot = "\d*\.?\d+" #有2.5岁的
age_d2d_patr = re.compile("(?:"+age_dot+fanwei_string+age_dot+age_unit_string+")[^,.;，。；]*?"+person2age_string+"?")
age_lowd_patr = re.compile("(?:"+age_dot+age_unit_string+"以上|>"+age_dot+age_unit_string+"|≥"+age_dot+age_unit_string+"|"+age_dot+age_unit_string+"或以上|大于"+age_dot+age_unit_string+")[^,.;，。；]*?"+person2age_string+"?")
age_highd_patr = re.compile("(?:"+age_dot+age_unit_string+"以下|<"+age_dot+age_unit_string+"|≤"+age_dot+age_unit_string+"|"+age_dot+age_unit_string+"或以下|小于"+age_dot+age_unit_string+")[^,.;，。；]*?"+person2age_string+"?")
person_patr = re.compile(person2age_string)


age_num_patr = re.compile("\d+")
age_unit_patr = re.compile("岁|个?月|天|日")
person2age = {"成人":{"low":"16","unit":"岁"},"新生儿":{"low":"0","high":"28","unit":"天"},"婴儿":{"low":"28","high":"12","unit":"天/月"},
              "幼儿":{"low":"1","high":"3","unit":"岁"},"儿童":{"high":"16","unit":"岁"},"青少年":{"high":"18","unit":"岁"},"小儿":{"high":"7","unit":"岁"},
              "少儿":{"high":"12","unit":"岁"},"老年人":{"low":"65","unit":"岁"},"老人":{"low":"65","unit":"岁"}}
#只有岁数+年龄的能匹配到年龄高值、低值、单位，其他：患者……无法匹配
def get_age(str):
    age_result = {}
    age_unit_string = ""

    #数字化的年龄字段 4~20岁
    age_d2d_match=age_d2d_patr.search(str)
    age_lowd_match = age_lowd_patr.search(str)#16>
    age_highd_match = age_highd_patr.search(str)#<16
    person_match = person_patr.search(str)#老人、少儿……

    #字符串中有多个年龄，一般最后一个可能有岁数，但是后面没有数据，所以没有切分，这里应该按第一个匹配到的年龄来计算
    #数字年龄+人物描述
    idx_dict = {}
    sort_string = "" #对应最前的年龄匹配字符串
    if age_d2d_match:# 4~20岁
        d2d_idx = age_d2d_match.start()
        idx_dict["age_d2d_match"] = d2d_idx
    if age_lowd_match:#16>
        lowd_idx = age_lowd_match.start()
        idx_dict["age_lowd_match"] = lowd_idx
    if age_highd_match:
        highd_idx = age_highd_match.start()
        idx_dict["age_highd_match"] = highd_idx
    if person_match:
        person_idx = person_match.start()
        idx_dict["person_match"] = person_idx

    # 对字典按value排序 获得最前的年龄idxd对应的字符串
    if idx_dict:
        idx_dict_sort = sorted(idx_dict.items(), key=lambda x: x[1])
        sort_string = idx_dict_sort[0][0]

    #数字年龄+人物描述
    if sort_string == "age_d2d_match":# 4~20岁 不需考虑后面的人物描述年龄
        age_string = age_d2d_match.group()
        age_low_high = age_num_patr.findall(age_string)
        age_result["age_low"] =age_low_high[0]
        if len(age_low_high)>1:
            age_result["age_high"] = age_low_high[1]
        else:
            age_result["age_high"] = age_low_high[0]
        age_unit_string = age_string

    elif sort_string == "age_lowd_match":#16>
        #指定低值
        age_string = age_lowd_match.group()
        age_low = age_num_patr.search(age_string).group()
        age_result["age_low"] = age_low
        age_unit_string = age_string
        #考虑后面的人物描述年龄，补充年龄字段
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
    elif sort_string == "age_highd_match":#<16
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
    #仅有人物字段  老人、少儿……
    elif sort_string =="person_match":
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


weight_high_patr = re.compile("低于|小于|≤|<|以下")
weight_low_patr = re.compile("大于|高于|>|≥|以上")
weight_num_patr = re.compile("\d+")
weight_scope_patr = re.compile("\d+"+fanwei_string+"\d+(?:kg|公斤)")
#获取体重高、低值
def get_weight(str):
    weight_result = {}
    weight_str = "(?:低于|大于|≤|<|>|≥)?\d*"+fanwei_string+"?\d+(?:kg|公斤)(?:以下|以上)?"
    weight_patr = re.compile(weight_str)
    weight_string = ""
    weight_search = weight_patr.search(str)
    if weight_search:
        weight_iter = weight_patr.finditer(str)
        weight_str_list = [f.group() for f in weight_iter]
        weight_string = weight_str_list[-1]
        #匹配体重低值
        weight_low_match = weight_low_patr.search(weight_string)
        if weight_low_match:
            weight_lownum_match =weight_num_patr.search(weight_string)
            if weight_lownum_match:
                weight_result["weight_low"] =weight_lownum_match.group()
        #匹配体重高值
        weight_high_match = weight_high_patr.search(weight_string)
        if weight_high_match:
            weight_highnum_match = weight_num_patr.search(weight_string)
            if weight_highnum_match:
                weight_result["weight_high"] = weight_highnum_match.group()

        #匹配体重范围值
        weight_scope_match = weight_scope_patr.search(weight_string)
        if weight_scope_match:
            weight_scopenum_list = weight_num_patr.findall(weight_scope_match.group())
            weight_result["weight_low"] = weight_scopenum_list[0]
            weight_result["weight_high"] = weight_scopenum_list[1]
    return weight_result


# fanwei_string = "[-|—|〜|～|~]" 修改第一个方法前的fanwei_string
#1-1539的所有剂量单位组合
unit_string = "(?:ug|μg|ug|mg元素铁|mg|Mg|ng|g氮|g（甘油三酯）|g脂质|g脂肪|g|BU|kU|万IU|IU|万U|U|MBq|MBq（\d*\.\d*mCi）|kBq|mCi|J|昭|ml|mmol|kcal|丸|片|袋|粒|枚|支|揿|喷|包|滴|瓶|枚|套)(?:\/[（(]kg.min[）)]|\/[（(]kg.d[）)]|\/[（(]kg.h[）)]|\/kg|\/mL|\/ml|\/h|\/d|\/L|\/min|\/m2|\/cm2)?"
#中文单位组合
percent_unit_string = "(?:ug|μg|ug|mg元素铁|mg|Mg|ng|g氮|g（甘油三酯）|g脂质|g脂肪|g|BU|kU|万IU|IU|万U|U|MBq|MBq（\d*\.\d*mCi）|kBq|mCi|J|昭|ml|mmol|kcal|%|丸|片|袋|粒|枚|支|揿|喷|包|滴|瓶|枚|套)(?:\/[（(]kg.min[）)]|\/[（(]kg.d[）)]|\/[（(]kg.h[）)]|\/kg|\/mL|\/ml|\/h|\/d|\/L|\/min|\/m2|\/cm2)?"
yici_string = "(?:每次|一次|单次|单剂|首次|初量|开始时|开始|初次量|初始量|最大滴定剂量|按体重)"
yiri_string = "(?:一日|—日|一天|首日|单日|每日|日|日服|每天|每晚|晚上|24小时.*|按体重)"

# cishu_string =  "(?:隔日|一日|—日|一天|每日|单日|日|每天|分成|分|晚上|每晚|每?(?:\d*"+fanwei_string+"?\d*|[一二三四五六七八九十])(?:小时|日|周|月|年))[^,.;，。；]*(?:\d*\.?\d*"+fanwei_string+"?\d*\.?\d+|[一二三四五六七八九十/])次"
cishu_string_before =  "(?:隔日|一日|—日|一天|单日|日|分成|晚上|每小时|每[天日周月年晚]|每?(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十])(?:小时|日|周|月|年))+[^,.;，。；]*(?:\d*\.?\d*"+fanwei_string+"?\d*\.?\d+|[一二三四五六七八九十/])次"
cishu_string_after =  "|分(?:\d*\.?\d*[-|—|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十/])次"
cishu_string = cishu_string_before+cishu_string_after

#加入片袋粒这些单位的话 范围前的数字  0.3mg|6袋|1/4包  范围后的数字 0.3mg|6袋|1/4包|半包|二袋  范围数字一般都是数字 不会用中文所以前面没有中文
before_num_string = "(?:\d+\/\d+|\d*\.?\d*万?)"
after_num_string = "(?:\d+\/\d+|\d*\.?\d+|[半两一二三四五六七八九十])"

# 一次……mg，一日……mg 单次推荐剂量 单日推荐剂量
# dose_str1 = yici_string+"[^,.;，。；]*\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string+".+?"+yiri_string+"\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string
dose_str1 = yici_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+".+?"+yiri_string+before_num_string+fanwei_string+"?"+after_num_string+unit_string
dose_str1_after =  "[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/次"+".+?"+yiri_string+before_num_string+fanwei_string+"?"+after_num_string+unit_string


# 一次……mg,一日……次  单次推荐剂量 推荐给药频次
# dose_str7 = yici_string+"[^,.;，。；]*\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string+".+?"+cishu_string
dose_str7 = yici_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+".+?"+cishu_string
dose_str7_after = "[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/次"+".+?"+cishu_string

#一日……次，一次……mg 与上面顺序相反
dose_str_8 =  cishu_string+".+?"+yici_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string

# 一次……mg 单次推荐剂量
# dose_str2 = yici_string+"[^,.;，。；]*?\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string
dose_str2 = yici_string+"[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string
dose_str2_after = "[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/次"

#一日……mg，分N次  单日推荐剂量，推荐给药频次
# dose_str3 = yiri_string+"[^,.;，。；]*\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string+".*?"+cishu_string
dose_str3 = yiri_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+".*?"+cishu_string

# 一日……mg 单日推荐剂量
# dose_str4 = yiri_string+"[^,.;，。；]*?\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string
dose_str4 = yiri_string+"[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string
dose_str4_after = "[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/[天日]"

#0. 4〜0.8mg
# dose_str5 = "\d*\.?\d*%?"+fanwei_string+"?\d*\.?\d+"+percent_unit_string
dose_str5 = before_num_string+"%?"+fanwei_string+"?"+after_num_string+percent_unit_string

#没有用量，只有频次
dose_pinci_patr = re.compile(cishu_string)

# 每1kg体重0.15〜0.2mg。
dose_str6 = "(?:每\d*kg体重|按体表面积)[^,.;，。；]*\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string


dose_stime_sday = re.compile(dose_str1)
dose_stime = re.compile(dose_str2)
dose_sday_stime = re.compile(dose_str3)
dose_sday = re.compile(dose_str4)
dose_sweight = re.compile(dose_str6)
dose_stime_jici = re.compile(dose_str7)

#添加 /次
dose_stime_sday_after = re.compile(dose_str1_after)
dose_stime_jici_after = re.compile(dose_str7_after)
dose_stime_after = re.compile(dose_str2_after)
dose_sday_after = re.compile(dose_str4_after)

#一日几次，一次8mg
dose_jici_stime = re.compile(dose_str_8)

num_patr = re.compile("\d*\.?\d+")#只有溶液用到了 而溶液好像没有包，袋这样的单位
dose_unit_patr = re.compile(percent_unit_string)

#溶液所在句子
rongye_sentence_patr = re.compile("[,，。;；]?[^,，。;；]*\d*\.?\d*%?"+fanwei_string+"?\d*\.?\d+%[^,，。;；]*溶液[^,，。;；]*[,，。;；]?")
rongye_num_patr = re.compile("\d*\.?\d*?"+fanwei_string+"?\d*\.?\d+"+unit_string)

#获得单次剂量极值、单日剂量极值
#极量关键字
limit_list = ["极量","极最","限量","限最","极限","为限","最大剂量","剂量最大","最高剂量","剂量最高","剂量不超过","剂量不得超过","剂量不宜超过","剂量不应超过","剂量应当不超过",
              "剂量不能超过","剂量最大","最大量","最大最","最髙量","最高量","最大日剂量","日剂量不超过","最大每日","最大每次","最大单次","最大滴定剂量","最高不能超过",
              "一次不得超过","一次不超过","一日剂量不得超过","—日剂量不宜超过","24小时不超过","最大用量","最大给药量","最大推荐剂量"]

#判断句子是否包含极量关键字
def is_limit(str):
    flag = False
    for i in limit_list:
        if i in str:
            flag = True
            break
    return flag

#获取剂量所在的句子
def get_dose_sentence(single_dose_str,str):
    # 排除与"极量"同意的句子、最大剂量、最大量,最大最,最髙量,最高量、等关键字
    dose_1sentence_before_string = "" #用量及其前一句话
    # 匹配用量所在一句话
    dose_1sentence = ""
    dose_sentence = ""
    dose_1sentence_patr = re.compile("[,，。;；]?[^,，。;；]*" + single_dose_str + "[^,，。;；]*[,，。;；]?")
    dose_1sentence_match = dose_1sentence_patr.search(str)
    if dose_1sentence_match:
        dose_1sentence = dose_1sentence_match.group()
    # 第一句话就包含极值关键字，则后面句子也为极值句子，不用继续判断
    if dose_1sentence!="":
        dose_1sentence = dose_1sentence.replace("(","\(").replace(")","\)")
        if is_limit(dose_1sentence):
            return dose_sentence,dose_1sentence_before_string

        # 匹配用量所在最多连续两句话
        dose_sentence_patr = re.compile("[,，。;；]?[^,，。;；]*" + single_dose_str + "[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?")
        dose_sentence_match = dose_sentence_patr.search(str)
        if dose_sentence_match:
            dose_sentence = dose_sentence_match.group()
        # 前面一句不包含极值关键字，判断后面一句是否包含极值关键字,包含则只取第一个句子提取推荐剂量，否则两句都可以
        if is_limit(dose_sentence):
            dose_sentence = dose_1sentence

        # 如果匹配到第二句话为纯中文，dose_sentence 匹配连续三句话(从第二句开始不包含极量关键字时才会作为一整句话来进行字段提取),如下例子
        # "一次100〜200mg,必要时重复，24小时内总量可达400mg"
        zhongwen_match = zhongwen.search(dose_sentence)
        if zhongwen_match:
            dose_3sentence_patr = re.compile(
                "[,，。;；]?[^,，。;；]*" + single_dose_str + "[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?")
            dose_3sentence = dose_3sentence_patr.search(str).group()
            # 前面一句不包含极值关键字，判断后面一句是否包含极值关键字,包含则只取第一个句子提取推荐剂量，否则两句都可以
            if not is_limit(dose_3sentence):
                dose_sentence = dose_3sentence

        #匹配剂量所在句子以及前一句
        dose1sentence_before_patr  = re.compile("[,，。;；]?[^,，。;；]*"+dose_1sentence)
        dose_1sentence_before_match = dose1sentence_before_patr.search(str)
        if dose_1sentence_before_match:
            dose_1sentence_before_string = dose_1sentence_before_match.group()
    return dose_sentence,dose_1sentence_before_string

#处理溶液所在句子
def process_rongye(rongye_search,dose_result,single_dose_str,str,dose_1sentence_before_string):
    rongye_string = rongye_search.group()
    # x%溶液，结尾,溶液后面没有剂量单位的，多匹配后面两句 ，因为可能用量、频次都有 成人用1%溶 液，一日3次，一次3〜4滴
    rongye_end_patr = re.compile("溶液[,，。;；]")
    rongye_end_match = rongye_end_patr.search(rongye_string)
    if rongye_end_match:
        rongye_2sen_patr = re.compile(rongye_string + "[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?")
        rongye_2sen_match = rongye_2sen_patr.search(str)
        if rongye_2sen_match:
            rongye_2sentence = rongye_2sen_match.group()
            rongye_string = rongye_2sentence
    # 一次 一日 的各种组合，同上面的if else
    # 溶液的单位已处理每分钟，不用赋值single_dose_str
    dose_result = get_rongye_dose(str, dose_result,single_dose_str,dose_1sentence_before_string)
    if not dose_result:
        # ……溶液\dml  ……ml……溶液 100mg(5%〜7.5%溶液)
        # 匹配除了%以外的其他的用量单位
        rongye_single_search = rongye_num_patr.search(rongye_string)
        if rongye_single_search:
            # 0.4-0.4mg
            rongye_dose_string = rongye_single_search.group()
            rongye_num_list = num_patr.findall(rongye_dose_string)
            dose_result["sdose_low"] = rongye_num_list[0]
            if len(rongye_num_list) > 1:
                dose_result["sdose_high"] = rongye_num_list[1]
            else:
                dose_result["sdose_high"] = rongye_num_list[0]
            single_dose_str = rongye_dose_string
    # 3、直接使用溶液的百分号数据
    if not dose_result:  # 不包含一些关键字的时候，默认选第一个为单次……按单次的方法处理
        dose_result = get_stime(single_dose_str, dose_result, rongye_string)
        # single_dose_str = dose_1sentence
    return dose_result,single_dose_str


#获取单次推荐剂量、推荐给药频次、单日推荐剂量、剂量单位
#匹配纯中文的一句话
zhongwen = re.compile("[,，。;；][\u4e00-\u9fa5]*[,，。;；]")
sentence_patr = re.compile("[^，。,;；]+[，。,;；]?")
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
        #ml/min的单位匹配到的时候，需要做一下排除
        sentence_patr = re.compile("[，。,;；]?[^，。,;；]*肌酐清除率[^，。,;；]*"+single_dose_str+"[^，。,;；]*[，。,;；]?")
        sentence_exclude_match = sentence_patr.search(str)
        if sentence_exclude_match:
            if len(single_dose_str_list)>1:
                single_dose_str = single_dose_str_list[1]
        if single_dose_str !="":
            dose_sentence,dose_1sentence_before_string = get_dose_sentence(single_dose_str,str)

            #用量的各种匹配模式
            stime_sday_search = dose_stime_sday.search(dose_sentence)
            stime_search = dose_stime.search(dose_sentence)
            sday_stime_search = dose_sday_stime.search(dose_sentence)
            sday_search = dose_sday.search(dose_sentence)
            sweight_search = dose_sweight.search(dose_sentence)
            stime_jici_search = dose_stime_jici.search(dose_sentence)

            #/次的模式
            stime_sday_after_search = dose_stime_sday_after.search(dose_sentence)
            stime_jici_after_search = dose_stime_jici_after.search(dose_sentence)
            stime_after_search = dose_stime_after.search(dose_sentence)
            sday_after_search = dose_sday_after.search(dose_sentence)

            #一日几次，一次9mg
            dose_jici_match = dose_jici_stime.search(dose_1sentence_before_string)

            #溶液数据单独处理，匹配是否是溶液句子(上面是按第一次出现的用量进行匹配，对溶液来说并不适用，在默认处理前进行溶液处理)
            rongye_search = rongye_sentence_patr.search(str)
            # 溶液所在的句子
            if rongye_search:
                dose_result, single_dose_str = process_rongye(rongye_search, dose_result, single_dose_str,str,dose_1sentence_before_string)
            else:

                # 获取给药频次数据，分解 推荐给药频次低值、高值、描述
                #单次推荐剂量和单日推荐剂量
                if dose_jici_match:
                    dose_result = get_stime_jici(single_dose_str, dose_1sentence_before_string)
                elif stime_sday_search or stime_sday_after_search: # 一次……mg，一日……mg
                    dose_result = get_stime_sday(single_dose_str, dose_sentence)
                elif stime_jici_search or stime_jici_after_search:# 一次……mg,一日……次
                    dose_result = get_stime_jici(single_dose_str, dose_sentence)
                elif sday_stime_search:#一日……mg，分N次
                    dose_result = get_sday_stime(single_dose_str, dose_sentence)
                elif stime_search or stime_after_search:# 一次……mg 单次推荐剂量  需要排除一些关键字(所在句子有：最大剂量,最大量,最大最,最髙量,最高量，不得超过，不超过)
                    #添加获取总量，即单日推荐低值和高值  总量也能获取
                    dose_result = get_stime(single_dose_str,dose_result,dose_sentence)
                elif sday_search or sday_after_search:# 一日……mg 单日推荐剂量
                    dose_result = get_sday(single_dose_str,dose_result,dose_sentence)
                elif sweight_search:# 每1kg体重0.15〜0.2mg。
                    dose_result = get_weight_time(single_dose_str, dose_result)
                    if "kg体重" in sweight_search.group():
                        single_dose_str+="/kg"
                else:
                    #不包含一些关键字的时候，默认选第一个为单次……按单次的方法处理  最后在一句话中判断频率和用量
                    dose_result = get_stime(single_dose_str,dose_result,dose_sentence)
                #获取剂量单位,溶液的剂量单位已经处理过了，溶液以外的没有，判断
            if dose_result.get("single_dose_unit","")=="":
                single_dose_unit = dose_unit_patr.search(single_dose_str)
                if single_dose_unit:
                    dose_result["single_dose_unit"] = single_dose_unit.group()
            #判断是否要在单位后面添加"/min /h"
            if dose_result.get("single_dose_unit", "") != "":
                per_minute = False
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+single_dose_str)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "/min" not in dose_result["single_dose_unit"]:
                        if "每分钟" in per_minute_match.group():
                            per_minute = True
                            dose_result["single_dose_unit"] += "/min"
                    if  per_minute ==False and "/h" not in dose_result["single_dose_unit"]:
                        if "每小时" in per_minute_match.group():
                            dose_result["single_dose_unit"] += "/h"
             #获取给药频次
            if dose_result.get("dose_time_low","") =="" and dose_result.get("dose_time_high","") =="":
                dose_result = get_pingci(dose_result, dose_sentence)
    elif dose_pinci_patr.search(str):
        dose_result = get_pingci(dose_result,str)
    return dose_result

# fanwei_string = "[-|—|〜|～|~]"
# unit_string = "(?:mg\/kg|μg\/kg|IU\/kg|ml\/kg|IU|μg|mg|ml|g)"
# percent_unit_string = "(?:mg\/kg|μg\/kg|IU\/kg|ml\/kg|IU|μg|mg|ml|g|%)"
# yici_string = "(?:每次|一次|初量|开始时|开始|初次量|初始量|最大滴定剂量)"
# yiri_string = "(?:一日|—日|每日|每天|每晚|晚上|24小时|按体重)"
#获取单次、单日极量极值
limit_1time = re.compile(yici_string+"[^,.;，。；]*\d*\.?\d+"+percent_unit_string)
limit_1day = re.compile(yiri_string+"[^,，。;；]*\d*\.?\d+"+percent_unit_string)
limit_number = "(?:\d+\/\d+|\d*\.?\d+|[半两一二三四五六七八九十])"
# 单次、单日剂量极值关键字（除了极量）
day_limit_str = "(?:限量|限最|极限|最大剂量|剂量最大|最高剂量|剂量最高|最大滴定剂量|最大量|最大最|剂量不超过|最大|剂量不得超过|剂量不宜超过|剂量不应超过|剂量不能超过|最高不能超过|不能超过|不超过|最大用量|最大给药量|最大推荐剂量|剂量<)"
day_limit_patr = re.compile(yiri_string+"[^,，。;；]*"+day_limit_str+"[^,，。;；]*"+limit_number+percent_unit_string)
day_limit_patr2 = re.compile("[,，。;；][^,，。;；]*"+day_limit_str+"[^,，。;；]*"+yiri_string+"[^,，。;；]*"+limit_number+percent_unit_string)
#……为限
day_limit_patr3 = re.compile(yiri_string+"[^,，。;；]*"+limit_number+percent_unit_string+"(?:为限|为极限)")
time_limit_str = "(?:限量|限最|极限|为限|最大剂量|剂量最大|最高剂量|剂量最高|剂量不超过|剂量不得超过|不得超过|剂量不宜超过|剂量不应超过|剂量不能超过|最大量|最大最|最高不能超过|不能超过|不超过|最大|最髙量|最高量|最大用量|最大给药量|最大推荐剂量|剂量<)"
time_limit_patr = re.compile(yici_string+"[^,，。;；]*"+time_limit_str+"[^,，。;；]*"+limit_number+percent_unit_string)
time_limit_patr2 = re.compile("[,，。;；][^,，。;；]*"+time_limit_str+"[^,，。;；]*"+yici_string+"[^,，。;；]*"+limit_number+percent_unit_string)
time_limit_patr3 = re.compile(yici_string+"[^,，。;；]*"+limit_number+percent_unit_string+"(?:为限|为极限)")
# 在单次剂量过滤的关键字中，包含以上这些单次、单日极值，保证不会把极值存在单次剂量和单日剂量中，也保证过滤的极值会在单次剂量中获得
# limit_list = ["极量","极最","限量","极限","为限","最大剂量","剂量最大","剂量不超过","剂量不得超过","剂量不宜超过","剂量最大","最大量","最大最","最髙量","最高量","最大日剂量","日剂量不超过","最大每日","最大每次","最大滴定剂量","最高不能超过","一日剂量不得超过","—日剂量不宜超过","24小时不超过"]
#获得单次、单日极量极值，1、极量……2、其他关键字
chi2num = {"半":"0.5","两":"2","每":"1","一":"1","/":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","十":"10"}
def get_limit(str,yaodian_result):
    limit_result = {}
    # limit_num_patr = re.compile("\d*\.?\d+")
    limit_num_patr = re.compile("(?:\d+\/\d+|\d*\.?\d+|[半两一二三四五六七八九十])")
    zhong_num_patr = re.compile("[半两一二三四五六七八九十]+")

    # (优先级最高)极量所在句，后面有句子时，往后再匹配最多一句
    limit_2sen = "[,，。;；]?[^,，。;；]*(?:极量|极最|最大日剂量|最大单次剂量|最大滴定剂量|最大剂量).?[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?"
    limit_2patrr = re.compile(limit_2sen)
    limit_2search = limit_2patrr.search(str)
    if limit_2search:
        #极量关键字如果在前一句，则前后都为极量，如果在一日，则一般一日在前。
        limit_sentence = limit_2search.group()
        #yaodian_result判断是否已经在单次用药中保存了用药单位
        limit_result = get_stimeday_limit(limit_sentence,yaodian_result)
    #其他有极量关键字的，与一次、一日不在同一句的，不要再往前匹配每日、每次，可能是错的
    else:
        time_limit_list = []
        day_limit_list = []
        unit_string = ""
        if time_limit_patr.search(str):
            time_limit_list = time_limit_patr.finditer(str)
        elif time_limit_patr2.search(str):
            time_limit_list = time_limit_patr2.finditer(str)
        elif time_limit_patr3.search(str):
            time_limit_list = time_limit_patr3.finditer(str)
        if time_limit_list:
            time_limit_str_list = [f.group() for f in time_limit_list]
            #以最后一次匹配到的极值数据作为单次剂量极值
            time_limit_string =time_limit_str_list[-1]
            limit_1time_num_list = limit_num_patr.findall(time_limit_string)
            if limit_1time_num_list:
                limit_num_string = limit_1time_num_list[-1]
                zhong_num_match = zhong_num_patr.search(limit_num_string)
                if zhong_num_match:
                    limit_num_string = chi2num.get(zhong_num_match.group(),"")
                limit_result["limit_1time"] = limit_num_string
            unit_string = time_limit_string

         #单日极量极值
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
                limit_day_num_string = limit_day_num_list[-1]
                zhong_num_match = zhong_num_patr.search(limit_day_num_string)
                if zhong_num_match:
                    limit_day_num_string = chi2num.get(zhong_num_match.group(), "")
                limit_result["limit_1day"] = limit_day_num_string
            if  unit_string =="":
                unit_string = day_limit_string

        #如果单次剂量为空，此时剂量单位应该也为空，补充为剂量极值的单位
        if yaodian_result.get("single_dose_unit","") == "":
            per_minute = False
            single_dose_unit = dose_unit_patr.search(unit_string)
            if single_dose_unit:
                limit_result["single_dose_unit"] = single_dose_unit.group()
                # 判断是否要在单位后面添加"/min"
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*" + unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True
                    if per_minute:
                        limit_result["single_dose_unit"] += "/min"
    return limit_result

days_type = "(?:天|日|周|个?月|年)"
liaocheng_str = re.compile("[,，。;；]?[^,，。;；]*\d*\.?\d*"+days_type+"?"+fanwei_string+"?\d*\.?\d+"+days_type+"[^,，。;；]*疗程")
liaocheng_after_str = re.compile("[,，。;；]?[^,，。;；]*疗程[^,，。;；]*\d*\.?\d*"+days_type+"?"+fanwei_string+"?\d*\.?\d+"+days_type)
#用几日停几日这种，可以计算相加
liaocheng_neg = re.compile("[,，。;；]?[^,，。;；]*停\d*\.?\d*"+days_type+"?"+fanwei_string+"?\d*\.?\d+"+days_type+"[^,，。;；]*疗程")
liaocheng_patr = re.compile("\d+"+days_type)
low_high_patr = re.compile("\d*\.?\d+"+fanwei_string+"\d*\.?\d+"+days_type)
liaocheng_num = re.compile("\d+")
liaocheng_unit = re.compile(days_type)
unit2num = {"周":"7","天":"1","日":"1","月":"30","个月":"30","年":"365"}
def get_recomend_days(str):
    dose_result = {}
    #用几日停几日
    liaocheng_neg_match = liaocheng_neg.search(str)
    liaocheng_match = liaocheng_str.search(str)
    liaocheng_after_match = liaocheng_after_str.search(str)
    tian_list = []
    #用几日停几日 疗程为天数相加
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
     #  3天~4天 疗程
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
                    if num_unit!= "":
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

# tian_string = "(1)口服成人①一次0.5g，一日3次，连用3日停4日为1个疗程。"
# tian_string2 = "静脉滴注急性脑血栓和脑栓塞：一日2万〜4万U,溶于5%葡萄糖氯化钠注射液或右旋糖酊-40注射液500ml中,分1〜2次给药。疗程7天〜3周。可根据病情增减剂量。"
# tian_sting3 = "口服一次30万U,一日3次，连用4周为1个疗程。可连服2〜3个疗程，也可连续服用至症状好转。"
# tian_no = "静脉滴注首次剂量为10BU,以后维持剂量可减为5BU,隔日1次。先用0.9%氯化钠注射液100〜250ml稀释后，静脉滴注1〜1.5小时。一般治疗急性脑血管病，隔日一次，3次为1个疗程。"
# print("recommand days:",get_recomend_days(tian_sting3))

#完整处理一个句子中的字段
if __name__=="__main__":
    # yao_string = "（3）静脉注射癫痫持续状态,按体重0.05mg/kg,一次不超过4mg,如10〜15分钟后发作仍继续或再发。可重复注射0.05mg/kg,如再经10〜15分钟仍无效。需采用其他措施，12小时内用量一般不超过8mg。"
    # print(yao_string)
    # print(get_single_dose("（1）头癣和手癣、足癣，每日3次。"))
    # print(get_age("6〜12个月"))
    # print(get_single_dose("②镇静，一次5〜10mg,一日15〜40mg；"))
    # print("成人①臂丛神经阻滞,0.375%溶液，20ml。")
    # print(get_single_dose("(1)精神分裂症②肌内注射：一次100mg,一日2次。"))
    # print(get_recomend_days("每8小时10mg/kg或500mg/m²"))
    print(get_limit("（2）肌内或静脉注射成人②镇静、催眠或急性乙醇戒断，开始10mg,成人用药一日最大限量一般为9g。",{}))


    #调用方法
    #获取句子中的字段值
    def get_gruguse_result(str):
        yaodian_result = {}
        #给药方式
        admin_route_way = get_admin_route(str)
        if admin_route_way != "":
            yaodian_result["admin_route"] = admin_route_way

        #年龄
        age_result = get_age(str)
        if age_result:
            yaodian_result.update(**age_result)

        #体重
        weight_result = get_weight(str)
        if weight_result:
            yaodian_result.update(**weight_result)

        #获取单次推荐剂量、推荐给药频次、单日推荐剂量、剂量单位
        dose_result = get_single_dose(str)
        if dose_result:
            yaodian_result.update(**dose_result)

        #获得单次、单日极量极值：单日极量极值中会判断单位是否存在，带入药典数据，判断单位是否已经存在
        limit_result = get_limit(str,yaodian_result)
        if limit_result:
            yaodian_result.update(**limit_result)

        #获得推荐给药天数
        recommand_result= get_recomend_days(str)
        if recommand_result:
            yaodian_result.update(**recommand_result)
        return yaodian_result


    # 将多层list展平
    def sum_brackets(a):
        return sum(a, [])

        # print(sum_brackets(result))


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

    def data2excel(result_dict):
        pass


    def data_process(filepath,file_name):
        tmp = []
        json_str = ""
        for line in open(filepath, 'r', encoding='UTF-8'):
            json_str += line.replace("\n", "").replace("'", " ")
            if check_json_format(json_str):
                tmp.append(json.loads(json_str))
                json_str = ""

        if tmp:
            for drug_info in tmp:
                take_way = drug_info.get("sentence_cut", "")
                take_result_list=[]
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




            with open("C:/产品文档/转换器测试数据/excel_result/"+file_name+"_ziduan.json", "w", encoding='utf-8') as fp:
                for drug in tmp:
                    fp.write(json.dumps(drug, indent=4, ensure_ascii=False))
                    fp.write('\n')

    # 获取字段方法
    def get_druguse_ziduan():
        file_name_list = ["1-200","201-400","401-600","601-800","801-1000","1001-1200","1201-1400","1401-1539"]
        # file_name_list = ["1401-1539"]
        for file_name in file_name_list:
            doc_path =  "C:/产品文档/转换器测试数据/cutsentence/"+file_name+".json"
            if os.path.exists(doc_path):
                data_process(doc_path, file_name)
                print("file {} sent2ziduan finished!".format(file_name + ".json"))


    # get_druguse_ziduan()






