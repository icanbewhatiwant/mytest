#获得单次推荐剂量和单日推荐剂量
import re
#需要跟yaodian_getdruguse文件一致
#一次
fanwei_string = "[-|—|〜|～|~]"
unit_string = "(?:ug|μg|ug|mg元素铁|mg|Mg|ng|g氮|g（甘油三酯）|g脂质|g脂肪|g|BU|kU|万IU|IU|万U|U|MBq|MBq（\d*\.\d*mCi）|kBq|mCi|J|昭|ml|mmol|kcal|丸|片|袋|粒|枚|支|揿|喷|包|滴|瓶|枚|套)(?:\/[（(]kg.min[）)]|\/[（(]kg.d[）)]|\/[（(]kg.h[）)]|\/kg|\/mL|\/ml|\/h|\/d|\/L|\/min|\/m2|\/cm2)?"
percent_unit_string = "(?:ug|μg|ug|mg元素铁|mg|Mg|ng|g氮|g（甘油三酯）|g脂质|g脂肪|g|BU|kU|万IU|IU|万U|U|MBq|MBq（\d*\.\d*mCi）|kBq|mCi|J|昭|ml|mmol|kcal|%|丸|片|袋|粒|枚|支|揿|喷|包|滴|瓶|枚|套)(?:\/[（(]kg.min[）)]|\/[（(]kg.d[）)]|\/[（(]kg.h[）)]|\/kg|\/mL|\/ml|\/h|\/d|\/L|\/min|\/m2|\/cm2)?"

yici_string = "(?:每次|一次|单次|单剂|首次|初量|开始时|开始|初次量|初始量|最大滴定剂量|按体重)"
yiri_string = "(?:一日|—日|一天|首日|单日|每日|日|日服|每天|每晚|晚上|24小时.*|按体重)"

# cishu_string =  "(?:隔日|一日|—日|每日|单日|日|每天|分成|分|晚上|每晚|每?(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十])(?:小时|日|周))(?:\d*\.?\d*"+fanwei_string+"?\d*\.?\d*|[一二三四五六七八九十/])次"
cishu_string_before =  "(?:隔日|一日|—日|一天|单日|日|分成|晚上|每小时|每[天日周月年晚]|每?(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十])(?:小时|日|周|月|年))+[^,.;，。；]*(?:\d*\.?\d*"+fanwei_string+"?\d*\.?\d+|[一二三四五六七八九十/])次"
cishu_string_after =  "|分(?:\d*\.?\d*[-|—|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十/])次"
cishu_string = cishu_string_before+cishu_string_after

#加入片袋粒这些单位的话 范围前的数字  0.3mg|6袋|1/4包  范围后的数字 0.3mg|6袋|1/4包|半包|二袋  范围数字一般都是数字 不会用中文所以前面没有中文
before_num_string = "(?:\d+\/\d+|\d*\.?\d*万?)"
after_num_string = "(?:\d+\/\d+|\d*\.?\d+|[半两一二三四五六七八九十])"


# 一次……mg，一日……mg 单次推荐剂量 单日推荐剂量
dose_str1 = yici_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+".+?"+yiri_string+before_num_string+fanwei_string+"?"+after_num_string+unit_string
dose_str1_after =  "[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/次"+".+?"+yiri_string+before_num_string+fanwei_string+"?"+after_num_string+unit_string


# 一次……mg,一日……次  单次推荐剂量 推荐给药频次
dose_str7 = yici_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+".+?"+cishu_string
dose_str7_after = "[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/次"+".+?"+cishu_string

# 一次……mg 单次推荐剂量
dose_str2 = yici_string+"[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string
dose_str2_after = "[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/次"

#一日……mg，分N次  单日推荐剂量，推荐给药频次
dose_str3 = yiri_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+".*?"+cishu_string

# 一日……mg 单日推荐剂量
dose_str4 = yiri_string+"[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string
dose_str4_after = "[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"/[天日]"

#0. 4〜0.8mg
dose_str5 = before_num_string+"%?"+fanwei_string+"?"+after_num_string+percent_unit_string

# 每1kg体重0.15〜0.2mg。
dose_str6 = "(?:每\d*kg体重|按体表面积)[^,.;，。；]*\d*\.?\d*"+fanwei_string+"?\d*\.?\d+"+unit_string
#需要跟yaodian_getdruguse文件一致

#一日……次，一次……mg 与上面顺序相反
dose_str_8 =  cishu_string+".+?"+yici_string+"[^,.;，。；]*"+before_num_string+fanwei_string+"?"+after_num_string+unit_string

dose_timestr = cishu_string

chi_dose_timestr = "[一二三四五六七八九十]次"

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

time_patr = re.compile(dose_timestr)
chi_time_patr = re.compile(chi_dose_timestr)
# num_patr = re.compile("\d*\.?\d+")
num_patr = re.compile("(?:\d+\/\d+|\d*\.?\d+)")
chi_num_patr = re.compile("[半两一二三四五六七八九十/每]+")
# dose_num_patr = re.compile("\d*\.?\d*%?万?"+fanwei_string+"?\d*\.?\d+")
dose_num_patr = re.compile("(?:\d+\/\d+|\d*\.?\d*%?万?)"+fanwei_string+"?(?:\d+\/\d+|\d*\.?\d+)")
dose_unit_patr = re.compile(percent_unit_string)
single_dose_patr = re.compile(dose_str5)
chi2num = {"半":"0.5","两":"2","每":"1","一":"1","/":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8","九":"9","十":"10"}

pingci = re.compile("隔日|一日|—日|每日|每天|分成|分|晚上|每晚|/|每?隔?(?:\d*"+fanwei_string+"?\d*|[一二三四五六七八九十])(?:小时|日|天|周|月|年)")
cishu = re.compile("(?:\d*\.?\d*"+fanwei_string+"?\d*\.?\d+|[一二三四五六七八九十/])次")
pingci_geri = re.compile("隔日")
pingci_1day = re.compile("一日|—日|每日|每天|分成|分|晚上|每晚|/日")
pingci_hour = re.compile("(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十每/])小时")
pingci_day = re.compile("(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十每/])[日天]")
pingci_week = re.compile("(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十每/])周")
pingci_month_year = re.compile("(?:\d*"+fanwei_string+"?\d+|[一二三四五六七八九十每/])[月年]")

#获取给药频次
def get_pingci(dose_result,stime_string):
    # 获取给药频次及其分解
    pingci_str =""
    pingci_str2 = ""
    pingci_des_str = ""
    time_match = time_patr.search(stime_string)
    if time_match:
        pingci_string = time_match.group()#每天/每周……次
        pingci_match = pingci.search(pingci_string)
        if pingci_match:
            pingci_des_str = pingci_match.group()
        hour_match = pingci_hour.search(pingci_string)
        week_match = pingci_week.search(pingci_string)
        month_year_match = pingci_month_year.search(pingci_string)
        day_match = pingci_day.search(pingci_string)
        desc_list =[]#给药频次描述里面的高低值保存 6,8

        cishu_match = cishu.search(stime_string)
        cishu_list = []
        if cishu_match:
            cishu_num = "0"
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
            #每8小时10 mg/kg或500mg/m² 没有匹配到次数的 默认按一次算
            if not cishu_list:
                cishu_list.append("1")
            desc_list = cishu_list

            if pingci_1day.search(pingci_string):
                pingci_str = "/1"
                pingci_str2 = pingci_str
            elif pingci_geri.search(pingci_string):
                pingci_str = "/2"
                pingci_str2 = pingci_str
            elif day_match:
                day_num_match = num_patr.search(pingci_string)
                if day_num_match:
                    day_num_list = num_patr.findall(pingci_string)
                    pingci_str = "/" +day_num_list[0]
                    pingci_str2 = pingci_str
                    if len(day_num_list)>1:
                        pingci_str2 =  "/" +day_num_list[1]
            elif hour_match:
                hour_num_match = num_patr.search(pingci_string)
                hour_num = "0"
                hour_num_list = []
                if hour_num_match:
                    # hour_num = hour_num_match.group()
                    hour_num_list = num_patr.findall(pingci_string)
                else:
                    chi_hour_match = chi_num_patr.search(pingci_string)
                    if chi_hour_match:
                        chi_num = chi_hour_match.group()
                    hour_num = chi2num.get(chi_num, "")
                    hour_num_list.append(hour_num)
                if hour_num_list:
                    pingci_str = "/1"
                    pingci_str2 = pingci_str
                    hour_num_len = len(hour_num_list)
                    if hour_num_len ==1:
                        if cishu_list:
                            hour_mul_num = 24 // int(hour_num_list[0])
                            cishu_list = [int(i)*int(hour_mul_num) for i in cishu_list]
                    elif hour_num_len>1:#处理6~8小时这种频次，估计出现6~8小时5~6次这种几乎不可能，直接按6~8小时5次这种处理
                        if cishu_list:
                            hour_mul_num1 = 24 // int(hour_num_list[0])
                            hour_mul_num2 = 24 // int(hour_num_list[1])
                            #前面数字小，24除出来数字大，频次高值为第二个，低值为第一个
                            cishu_list = [int(cishu_list[0])*int(hour_mul_num2),int(cishu_list[0])*int(hour_mul_num1)]


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
                if week_num != "0" and week_num !="":
                    pingci_str = "/" + str(int(week_num) * 7)
                    pingci_str2 = pingci_str
            elif month_year_match:
               pingci_str = "/" + month_year_match.group()
               pingci_str2 = pingci_str

        if cishu_list:
            dose_result["dose_time_low"] = str(cishu_list[0]) + pingci_str
            if len(cishu_list) > 1:
                 dose_result["dose_time_high"] = str(cishu_list[1]) + pingci_str2
            else:
                dose_result["dose_time_high"] = str(cishu_list[0]) + pingci_str2

        if desc_list:
            if pingci_des_str!= "":
                dose_result["dose_time_low_des"] = pingci_des_str + str(desc_list[0]) + "次"
                if len(desc_list) > 1:
                    dose_result["dose_time_high_des"] = pingci_des_str + str(desc_list[1]) + "次"
                else:
                    dose_result["dose_time_high_des"] = pingci_des_str + str(desc_list[0]) + "次"
            else:
                dose_result["dose_time_low_des"] = pingci_string
                dose_result["dose_time_high_des"] = pingci_string



    return dose_result


#获取单次、单日给药剂量
def get_stime_sday(single_dose_str,dose_sentence):
    dose_result = {}
    # 获取单次给药剂量，分解 单次给药低、高值，以及剂量单位
    # 单次剂量
    single_dose = dose_num_patr.search(single_dose_str)
    chi_num_match = chi_num_patr.search(single_dose_str)
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]
    elif chi_num_match:
        chi_num = chi_num_match.group()
        ci2_num = chi2num.get(chi_num, "")
        if ci2_num != "0":
            dose_result["sdose_low"] = ci2_num
            dose_result["sdose_high"] = ci2_num

    #单日剂量
    sday_match = dose_sday.search(dose_sentence)
    if sday_match:
        sday_string =sday_match.group()
        sday_low_high_match = single_dose_patr.search(sday_string)
        if sday_low_high_match:
            sday_low_high = num_patr.findall(sday_low_high_match.group())
            sday_low_high_len = 0
            sday_low_high_len = len(sday_low_high)

        #只有一个值而且有不超过关键字在单日剂量中时
        if "不超过" in sday_string and sday_low_high_len ==1:
            dose_result["sday_dose_high"] = sday_low_high[0]
        else:
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
    chi_num_match = chi_num_patr.search(single_dose_str)
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]
    elif chi_num_match:
        chi_num = chi_num_match.group()
        ci2_num = chi2num.get(chi_num, "")
        if ci2_num != "0":
            dose_result["sdose_low"] = ci2_num
            dose_result["sdose_high"] = ci2_num

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
    chi_num_match = chi_num_patr.search(single_dose_str)#中文数字匹配
    if day_dose:
        day_low_high = num_patr.findall(day_dose.group())
        dose_result["sday_dose_low"] = day_low_high[0]
        if len(day_low_high) > 1:
            dose_result["sday_dose_high"] = day_low_high[1]
        else:
            dose_result["sday_dose_high"] = day_low_high[0]
    elif chi_num_match:
        chi_num = chi_num_match.group()
        ci2_num = chi2num.get(chi_num, "")
        if ci2_num != "0":
            dose_result["sdose_low"] = ci2_num
            dose_result["sdose_high"] = ci2_num

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
# fanwei_string = "[-|—|〜|～|~]"
# unit_string = "(?:mg\/kg|μg\/kg|IU\/kg|ml\/kg|IU|μg|mg|ml|g)"
# percent_unit_string = "(?:mg\/kg|μg\/kg|IU\/kg|ml\/kg|IU|μg|mg|ml|g|%)"
# yici_string = "(?:每次|一次|初量|开始时|开始|初次量|初始量|最大滴定剂量)"
# yiri_string = "(?:一日|—日|每日|每天|每晚|晚上|24小时|按体重)"
pingci_repeat_time = re.compile(yici_string+"[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"[,.;，。；][^,.;，。；]*可重复")
pingci_repeat_day = re.compile(yiri_string+"[^,.;，。；]*?"+before_num_string+fanwei_string+"?"+after_num_string+unit_string+"[,.;，。；][^,.;，。；]*可重复")
one_time = re.compile("(?:睡前服用)")

#为前面没有一次关键词的句子 匹配频率
cishu_patr = re.compile(cishu_string)
def get_stime(single_dose_str,dose_result,dose_sentence):
    sindose_sentence = re.compile("[^，。,;；]*" + single_dose_str + "[，。,;；]?")
    sindose_sentence_match = sindose_sentence.search(dose_sentence)
    sindose_sentence_string = ""
    if sindose_sentence_match:
        sindose_sentence_string = sindose_sentence_match.group()
    pingci_match = pingci.search(sindose_sentence_string)

    # 获取单次给药剂量，分解 单次给药低、高值，以及剂量单位
    single_dose = dose_num_patr.search(single_dose_str)
    chi_num_match = chi_num_patr.search(single_dose_str)  # 中文数字匹配
    if single_dose:
        sindose_low_high = num_patr.findall(single_dose.group())
        dose_result["sdose_low"] = sindose_low_high[0]
        if len(sindose_low_high) > 1:
            dose_result["sdose_high"] = sindose_low_high[1]
        else:
            dose_result["sdose_high"] = sindose_low_high[0]
    elif chi_num_match:
        chi_num = chi_num_match.group()
        ci2_num = chi2num.get(chi_num, "")
        if ci2_num != "0":
            dose_result["sdose_low"] = ci2_num
            dose_result["sdose_high"] = ci2_num

    #获取频次
    if cishu_patr.search(dose_sentence):
        dose_result = get_pingci(dose_result,dose_sentence)
    elif pingci_match:
        dose_result = get_pingci(dose_result, sindose_sentence_string)
    elif pingci_repeat_time.search(dose_sentence):
        dose_result["dose_time_low_des"] = "需要时"
        dose_result["dose_time_high_des"] = "需要时"
        dose_result["dose_time_low"] = "1/1"
        dose_result["dose_time_high"] = "1/1"

    elif one_time.search(dose_sentence):
        one_time_match = one_time.search(dose_sentence)
        dose_result["dose_time_low_des"] = one_time_match.group()
        dose_result["dose_time_high_des"] = one_time_match.group()
        dose_result["dose_time_low"] = "1/1"
        dose_result["dose_time_high"] = "1/1"

    return dose_result

def get_sday(single_dose_str,dose_result,dose_sentence):
    # 获取单日给药剂量，分解 单次给药低、高值，以及剂量单位
    sindose_sentence = re.compile("[^，。,;；]*"+single_dose_str+"[，。,;；]?")
    sindose_sentence_match = sindose_sentence.search(dose_sentence)
    sindose_sentence_string = ""
    if sindose_sentence_match:
        sindose_sentence_string = sindose_sentence_match.group()
    pingci_day_match = pingci_day.search(sindose_sentence_string)

    day_dose = dose_num_patr.search(single_dose_str)
    chi_num_match = chi_num_patr.search(single_dose_str)  # 中文数字匹配
    if day_dose:
        day_low_high = num_patr.findall(day_dose.group())
        dose_result["sday_dose_low"] = day_low_high[0]
        if len(day_low_high) > 1:
            dose_result["sday_dose_high"] = day_low_high[1]
        else:
            dose_result["sday_dose_high"] = day_low_high[0]
    elif chi_num_match:
        chi_num = chi_num_match.group()
        ci2_num = chi2num.get(chi_num, "")
        if ci2_num != "0":
            dose_result["sdose_low"] = ci2_num
            dose_result["sdose_high"] = ci2_num

    # 获取频次
    if cishu_patr.search(dose_sentence):
        dose_result = get_pingci(dose_result, dose_sentence)
    elif pingci_day_match:
        pingci_day_string= pingci_day_match.group()
        dose_result["dose_time_low_des"] = pingci_day_string+"1次"
        dose_result["dose_time_high_des"] = pingci_day_string+"1次"
        day_list = num_patr.findall(pingci_day_string)
        if not day_list:#中文的日、天匹配
            if chi_num_patr.search(pingci_day_string):
                day_list = chi_num_patr.findall(pingci_day_string)
                if day_list:
                    day_list = [chi2num.get(i, "") for i in day_list]

        if day_list:
            dose_result["dose_time_low"] = "1/" + day_list[0]
            if len(day_list) > 1:
                dose_result["dose_time_high"] = "1/" + day_list[1]
            else:
                dose_result["dose_time_high"] = "1/" + day_list[0]

    elif pingci_repeat_day.search(dose_sentence):
        dose_result["dose_time_low_des"] = "需要时"
        dose_result["dose_time_high_des"] = "需要时"
        dose_result["dose_time_low"] = "1/1"
        dose_result["dose_time_high"] = "1/1"
    elif one_time.search(dose_sentence):
        one_time_match = one_time.search(dose_sentence)
        dose_result["dose_time_low_des"] = one_time_match.group()
        dose_result["dose_time_high_des"] = one_time_match.group()
        dose_result["dose_time_low"] = "1/1"
        dose_result["dose_time_high"] = "1/1"
    return dose_result

#极量关键字
#需要跟yaodian_getdruguse文件一致
limit_list = ["极量","极最","限量","限最","极限","为限","最大剂量","剂量最大","最高剂量","剂量最高","剂量不超过","剂量不得超过","剂量不宜超过","剂量不应超过","剂量应当不超过",
              "剂量不能超过","剂量最大","最大量","最大最","最髙量","最高量","最大日剂量","日剂量不超过","最大每日","最大每次","最大单次","最大滴定剂量","最高不能超过",
              "一次不得超过","一次不超过","一日剂量不得超过","—日剂量不宜超过","24小时不超过","最大用量","最大给药量","最大推荐剂量"]
#需要跟yaodian_getdruguse文件一致

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

def  get_rongye_dose(str,dose_result,single_dose_str,dose_1sentence_before_string):
    single_dose_patr = re.compile(dose_str5)  #0. 4〜0.8mg
    unit_string = ""

    rongye_stime_sday_search = dose_stime_sday.search(str)
    rongye_stime_search = dose_stime.search(str)
    rongye_sday_stime_search = dose_sday_stime.search(str)
    rongye_sday_search = dose_sday.search(str)
    rongye_sweight_search = dose_sweight.search(str)
    rongye_stime_jici_search = dose_stime_jici.search(str)

    # /次的模式
    rongye_stime_sday_after_search = dose_stime_sday_after.search(str)
    rongye_stime_jici_after_search = dose_stime_jici_after.search(str)
    rongye_stime_after_search = dose_stime_after.search(str)
    rongye_sday_after_search = dose_sday_after.search(str)

    # 一日几次，一次9mg
    dose_jici_match = dose_jici_stime.search(dose_1sentence_before_string)

    per_minute = False
    #直接搜索句子中第一次匹配到的单次用法用量数据
    if dose_jici_match:
        dose_result = get_stime_jici(single_dose_str, dose_1sentence_before_string)
    elif rongye_stime_sday_search or rongye_stime_sday_after_search:  # 一次……mg，一日……mg
        #获得单次、单日用量
        stime_sday_string = rongye_stime_sday_search.group()
        stime_string = dose_stime.search(stime_sday_string).group()
        sday_string = dose_sday.search(stime_sday_string).group()
        #判断用药单位后是否要添加“/min”


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

    elif rongye_stime_jici_search or rongye_stime_jici_after_search:# 一次……mg,一日……次
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
    elif rongye_stime_search or rongye_stime_after_search:# 一次……mg 单次推荐剂量  需要排除一些关键字(所在句子有：最大剂量,最大量,最大最,最髙量,最高量，不得超过，不超过)
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
    elif rongye_sday_search or rongye_sday_after_search:  # 一日……mg 单日推荐剂量
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

limit_num_patr = re.compile(after_num_string)
#需要跟yaodian_getdruguse文件一致
# fanwei_string = "[-|—|〜|～|~]"
# unit_string = "(?:mg\/kg|μg\/kg|IU\/kg|ml\/kg|IU|μg|mg|ml|g)"
# percent_unit_string = "(?:mg\/kg|μg\/kg|IU\/kg|ml\/kg|IU|μg|mg|ml|g|%)"
# yici_string = "(?:每次|一次|初量|开始时|开始|初次量|初始量|最大滴定剂量)"
# yiri_string = "(?:一日|—日|每日|每天|每晚|晚上|24小时|按体重)"
limit_1day = re.compile(yiri_string+"[^,，。;；]*"+after_num_string+percent_unit_string)
limit_1time = re.compile(yici_string+"[^,.;，。；]*"+after_num_string+percent_unit_string)
#需要跟yaodian_getdruguse文件一致
def get_stimeday_limit(limit_sentence,yaodian_result):

    limit_result = {}
    time_search = limit_1time.search(limit_sentence)
    unit_string = ""
    if time_search:
        unit_string = time_search.group()
        limit_str_time_match = single_dose_patr.search(unit_string)
        if limit_str_time_match:
            limit_1timestr = limit_num_patr.search(limit_str_time_match.group())
            if limit_1timestr:
                limit_result["limit_1time"] = limit_1timestr.group()

    day_search = limit_1day.search(limit_sentence)
    if day_search:
        if unit_string == "":
            unit_string = day_search.group()
            limit_str_match = single_dose_patr.search(unit_string)
            if limit_str_match:
                limit_1daystr = limit_num_patr.search(limit_str_match.group())
                if limit_1daystr:
                    limit_result["limit_1day"] = limit_1daystr.group()

    # 如果单次剂量为空，此时剂量单位应该也为空，补充为剂量极值的单位
    per_minute = False
    if yaodian_result.get("single_dose_unit", "") == "":
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
    dose_result =  get_pingci(dose_result,"以后每6〜8小时1次")
    print(dose_result)

    # #调试
    # dose_result = get_stime_sday("2.5〜10mg",'，一次2.5〜10mg,一日2〜4次。')
    # print(dose_result)