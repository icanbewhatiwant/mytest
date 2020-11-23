#获得单次推荐剂量和单日推荐剂量
import re

# 一次……mg，一日……mg 单次推荐剂量 单日推荐剂量
dose_str1 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(一日|—日|每日|每晚|晚上|按体重)\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)"

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

pingci = re.compile("隔日|一日|—日|每日|分成|分|晚上|每晚|(?:\d+|[一二三四五六七八九十])(?:小时|日|周)")
cishu = re.compile("(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次")
pingci_geri = re.compile("隔日")
pingci_1day = re.compile("一日|—日|每日|分成|分|晚上|每晚")
pingci_hour = re.compile("(?:\d+|[一二三四五六七八九十])小时")
pingci_day = re.compile("(?:\d+|[一二三四五六七八九十])日")
pingci_week = re.compile("(?:\d+|[一二三四五六七八九十])周")


#获取给药频次
def get_pingci(dose_result,stime_string):
    # 获取给药频次及其分解
    pingci_match = pingci.search(stime_string)
    pingci_string = pingci_match.group()#每天/每周
    hour_match = pingci_hour.search(pingci_string)
    week_match = pingci_week.search(pingci_string)
    desc_list =[]#给药频次描述里面的高低值保存 6,8

    cishu_match = cishu.search(stime_string)
    if cishu_match:
        cishu_num = "0"
        cishu_list = []
        cishu_string = cishu_match.group()#6~8次
        cishu_num_match = num_patr.search(cishu_string) #数字\d
        if cishu_num_match:
            cishu_list = num_patr.findall(cishu_string)
        else:#中文数字转换：一：1
            chi_cishu_match = chi_num_patr.search(cishu_string)
            if chi_cishu_match:
                chi_cishu_num = chi_cishu_match.group()
                cishu_num = chi2num.get(chi_cishu_num, "")
                if cishu_num != "0":
                    cishu_list.append(cishu_num)
        desc_list = cishu_list
    if pingci_match:#每天/每周 频次转换 天、周、小时、转换为日单位
        if pingci_1day.search(pingci_string):
            pingci_str = "/1"
        elif pingci_geri.search(pingci_string):
            pingci_str = "/2"
        elif hour_match:
            hour_num_match = num_patr.search(pingci_string)
            hour_num = "0"
            if hour_num_match:
                hour_num = hour_num_match.group()
            else:
                chi_hour_match = chi_num_patr.search(pingci_string)
                if chi_hour_match:
                    chi_num = chi_hour_match.group()
                hour_num = chi2num.get(chi_num, "")
            if hour_num != 0:
                hour_mul_num = 24 // int(hour_num)
                pingci_str = "/1"
                if cishu_list:
                    cishu_list = [int(i)*int(hour_mul_num) for i in cishu_list]
        elif week_match:
            week_num_match = num_patr.search(pingci_string)
            week_num = "0"
            if week_num_match: #数字
                week_num = week_num_match.group()
            else:#中文数字转换
                chi_week_match = chi_num_patr.search(pingci_string)
                if chi_week_match:
                    chi_week_num = chi_week_match.group()
                    week_num = chi2num.get(chi_week_num, "")
            if week_num != "0":
                pingci_str = "/" + str(int(week_num) * 7)

    if cishu_list:
        dose_result["dose_time_low"] = str(cishu_list[0]) + pingci_str
        if len(cishu_list) > 1:
            dose_result["dose_time_high"] = str(cishu_list[1]) + pingci_str
        else:
            dose_result["dose_time_high"] = str(cishu_list[0]) + pingci_str

    if desc_list:
        dose_result["dose_time_low_des"] = pingci_string + str(desc_list[0]) + "次"
        if len(desc_list) > 1:
            dose_result["dose_time_high_des"] = pingci_string + str(desc_list[1]) + "次"
        else:
            dose_result["dose_time_high_des"] = pingci_string + str(desc_list[0]) + "次"

    return dose_result


#获取单次、单日给药剂量
def get_stime_sday(single_dose_str,dose_sentence):
    dose_result = {}
    # 获取单次给药剂量，分解 单次给药低、高值，以及剂量单位
    # 单次剂量
    single_dose = dose_num_patr.search(single_dose_str)
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]
    #单日剂量
    sday_match = dose_sday.search(dose_sentence)
    if sday_match:
        sday_low_high = num_patr.findall(sday_match.group())
        dose_result["sday_dose_low"] = sday_low_high[0]
        if len(sday_low_high) > 1:
            dose_result["sday_dose_high"] = sday_low_high[1]
        else:
            dose_result["sday_dose_high"] = sday_low_high[0]
    return dose_result


#获取单次给药剂量和频次
def get_stime_jici(single_dose_str, dose_sentence):
    dose_result = {}
    # 单次剂量
    single_dose = dose_num_patr.search(single_dose_str)
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]

    stime_search = time_patr.search(dose_sentence)
    if stime_search:
        stime_string = stime_search.group()
        dose_result = get_pingci(dose_result,stime_string)
    return dose_result

#获取单日给药剂量和频次
def get_sday_stime(single_dose_str, dose_sentence):
    dose_result = {}
    # 单次剂量
    day_dose = dose_num_patr.search(single_dose_str)
    if day_dose:
        day_low_high = num_patr.findall(day_dose.group())
        dose_result["sday_dose_low"] = day_low_high[0]
        if len(day_low_high) > 1:
            dose_result["sday_dose_high"] = day_low_high[1]
        else:
            dose_result["sday_dose_high"] = day_low_high[0]

    stime_search = time_patr.search(dose_sentence)
    if stime_search:
        stime_string = stime_search.group()
        dose_result = get_pingci(dose_result,stime_string)
    return dose_result


def get_weight_time(single_dose_str,dose_result):
    # 获取单次给药剂量，分解 单次给药低、高值，以及剂量单位
    single_dose = dose_num_patr.search(single_dose_str)
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]
    return dose_result

pingci_repeat_time = re.compile("(?:每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*?\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)[,.;，。；][^,.;，。；]*可重复")
pingci_repeat_day = re.compile("(?:一日|—日|每日|每天|每晚|晚上|24小时|按体重)[^,.;，。；]*?\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)[,.;，。；][^,.;，。；]*可重复")
def get_stime(single_dose_str,dose_result,dose_sentence):
    # 获取单次给药剂量，分解 单次给药低、高值，以及剂量单位
    single_dose = dose_num_patr.search(single_dose_str)
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]

    if pingci_repeat_time.search(dose_sentence):
        dose_result["dose_time_low_des"] = "需要时"
        dose_result["dose_time_high_des"] = "需要时"
        dose_result["dose_time_low"] = "1/1"
        dose_result["dose_time_high"] = "1/1"
    return dose_result

def get_sday(single_dose_str,dose_result,dose_sentence):
    # 获取单日给药剂量，分解 单次给药低、高值，以及剂量单位
    day_dose = dose_num_patr.search(single_dose_str)
    if day_dose:
        day_low_high = num_patr.findall(day_dose.group())
        dose_result["sday_dose_low"] = day_low_high[0]
        if len(day_low_high) > 1:
            dose_result["sday_dose_high"] = day_low_high[1]
        else:
            dose_result["sday_dose_high"] = day_low_high[0]
    if pingci_repeat_day.search(dose_sentence):
        dose_result["dose_time_low_des"] = "需要时"
        dose_result["dose_time_high_des"] = "需要时"
        dose_result["dose_time_low"] = "1/1"
        dose_result["dose_time_high"] = "1/1"
    return dose_result

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

def is_rongye_limit(str):
    flag = False
    is_limit_string = re.compile("[,，。;；]?[^,，。;；]*" + str + "[^,，。;；]*[,，。;；]?")
    limit_sentence_match = is_limit_string.search(str)
    if limit_sentence_match:
        limit_sentence = limit_sentence_match.group()
        flag = is_limit(limit_sentence)
        return flag

def  get_rongye_dose(str,dose_result):
    single_dose_patr = re.compile(dose_str5)  #0. 4〜0.8mg
    unit_string = ""

    rongye_stime_sday_search = dose_stime_sday.search(str)
    rongye_stime_search = dose_stime.search(str)
    rongye_sday_stime_search = dose_sday_stime.search(str)
    rongye_sday_search = dose_sday.search(str)
    rongye_sweight_search = dose_sweight.search(str)
    rongye_stime_jici_search = dose_stime_jici.search(str)


    #直接搜索句子中第一次匹配到的单次用法用量数据
    if rongye_stime_sday_search:# 一次……mg，一日……mg
        #获得单次、单日用量
        stime_sday_string = rongye_stime_sday_search.group()
        stime_string = dose_stime.search(stime_sday_string).group()
        sday_string = dose_sday.search(stime_sday_string).group()
        #判断用药单位后是否要添加“/min”
        per_minute = False

        #判断句子是否为极量句子：

        is_time_limit= is_rongye_limit(stime_string)
        is_day_limit = is_rongye_limit(sday_string)
        if not is_time_limit:
            dose_result = get_stime(stime_string,dose_result,stime_sday_string)
        if not is_day_limit:
            dose_result = get_sday(sday_string,dose_result,stime_sday_string)
        #获取用药字符串，用来获取用药单位
        if not is_time_limit or not is_day_limit:
            single_dose_search = single_dose_patr.search(stime_string)
            if single_dose_search:
                unit_string = single_dose_search.group()
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True

    elif rongye_stime_jici_search:  # 一次……mg,一日……次
        stime_jici_string = rongye_stime_jici_search.group()
        stime_string = dose_stime.search(stime_jici_string).group()

        is_time_jici_limit = is_rongye_limit(stime_string)
        if not is_time_jici_limit:
            dose_result = get_stime_jici(stime_string,stime_jici_string)
            #用药单位
            single_dose_search = single_dose_patr.search(stime_string)
            if single_dose_search:
                unit_string = single_dose_search.group()
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True
    elif rongye_sday_stime_search:#一日……mg，分N次
        sday_stime_string = rongye_sday_stime_search.group()
        sday_string = dose_sday.search(sday_stime_string).group()
        is_day_limit = is_rongye_limit(sday_string)
        if not is_day_limit:
            dose_result = get_sday_stime(sday_string,sday_stime_string)

            single_dose_search = single_dose_patr.search(sday_string)
            if single_dose_search:
                unit_string = single_dose_search.group()
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True
    elif rongye_stime_search:# 一次……mg 单次推荐剂量  需要排除一些关键字(所在句子有：最大剂量,最大量,最大最,最髙量,最高量，不得超过，不超过)
        stime_search_string = rongye_stime_search.group()
        is_stime_limit = is_rongye_limit(stime_search_string)
        if not is_stime_limit:
            dose_result = get_stime(stime_search_string, dose_result, stime_search_string)

            single_dose_search = single_dose_patr.search(stime_search_string)
            if single_dose_search:
                unit_string = single_dose_search.group()
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True
    elif rongye_sday_search:# 一日……mg 单日推荐剂量
        sday_search_string = rongye_sday_search.group()
        is_sday_limit = is_rongye_limit(sday_search_string)
        if not is_sday_limit:
            dose_result = get_sday(sday_search_string,dose_result,sday_search_string)

            single_dose_search = single_dose_patr.search(sday_search_string)
            if single_dose_search:
                unit_string = single_dose_search.group()
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True
    elif rongye_sweight_search:# 每1kg体重0.15〜0.2mg。
        sweight_string =rongye_sweight_search.group()
        is_weight_limit = is_rongye_limit(sweight_string)
        if not is_weight_limit:
            dose_result = get_weight_time(sweight_string, dose_result)

            single_dose_search = single_dose_patr.search(sweight_string)
            if single_dose_search:
                unit_string = single_dose_search.group()
                unit_string += "/kg"
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*"+unit_string)
                per_minute_match = per_minute_patr.search(str)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True

    # 获取剂量单位
    if unit_string!="":
        single_dose_unit = dose_unit_patr.search(unit_string)
        if single_dose_unit:
            dose_result["single_dose_unit"] = single_dose_unit.group()
            if per_minute:
                dose_result["single_dose_unit"]+= "/min"
    return dose_result


limit_num_patr = re.compile("\d*\.?\d+")
# 极量所在句，后面有句子时，往后再匹配最多一句
limit_2sen = "[,，。;；]?[^,，。;；]*极量.?[^,，。;；]*[,，。;；]?[^,，。;；]*[,，。;；]?"
limit_1day = re.compile("(?:一日|—日|每日|日|每天|每晚|晚上|24小时)[^,，。;；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|μg|mg|ml|g|%)")
limit_1time = re.compile("(?:每次|一次|初量|开始时|开始|初次量|初始量|最大滴定剂量)[^,.;，。；]*\d*\.?\d+(?:mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g|%)")
def get_stimeday_limit(limit_sentence):

    limit_result = {}
    time_search = limit_1time.search(limit_sentence)
    unit_string = ""
    if time_search:
        unit_string = time_search.group()
        limit_1timestr = limit_num_patr.search(time_search.group())
        if limit_1timestr:
            limit_result["limit_1time"] = limit_1timestr.group()

    day_search = limit_1day.search(limit_sentence)
    if day_search:
        if unit_string == "":
            unit_string = day_search.group()
        limit_1daystr = limit_num_patr.search(day_search.group())
        if limit_1daystr:
            limit_result["limit_1day"] = limit_1daystr.group()

    # 如果单次剂量为空，此时剂量单位应该也为空，补充为剂量极值的单位
    per_minute = False
    if limit_result.get("single_dose_unit", "") == "":
        if unit_string !="":
            single_dose_unit = dose_unit_patr.search(unit_string)
            if single_dose_unit:
                limit_result["single_dose_unit"] = single_dose_unit.group()
                per_minute_patr = re.compile("[，。,;；][^，。,;；]*" + unit_string)
                per_minute_match = per_minute_patr.search(limit_sentence)
                if per_minute_match:
                    if "每分钟" in per_minute_match.group():
                        per_minute = True
                if per_minute:
                    dose_result["single_dose_unit"] += "/min"
    return limit_result

if __name__=="__main__":
    dose_result = {}
    #调试给药频次
    # string = "12小时4次"
    # string1 = "4周1次"
    # string2 = "一日6~8次"
    # string3 ="隔日1次"
    # string4 = "2小时一次"
    dose_result =  get_pingci(dose_result,"一日2〜4次。")
    print(dose_result)

    #调试
    dose_result = get_stime_sday("2.5〜10mg",'，一次2.5〜10mg,一日2〜4次。')
    print(dose_result)