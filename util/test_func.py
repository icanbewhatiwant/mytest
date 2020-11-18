import re


dose_str1 = "(一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(每日|一日|—日|每晚)\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(次|mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g)?"
string3 = " （1）镇痛①口服成人常用量：一次50〜100mg,一日200〜400mg。"

# yiriyiri = re.compile(dose_str1)
# yiriyiri_match = yiriyiri.search(string3)
# if yiriyiri_match:
#     print(yiriyiri_match.group())


dose_str3 = "(每次|一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|～|~]?\d*\.?\d+(mg\/kg|μg\/kg|IU\/kg|IU|mg|ml|g).+?(每日|一日|—日|每晚|(?:\d|[一二三四五六七八九十])(?:小时|日|周))(?:\d*\.?\d*[-|〜|～|~]?\d*\.?\d+|[一二三四五六七八九十])次"
string4 = " （1）镇痛①口服成人常用量：一次50〜100mg,一日200〜400mg。"

string = " 口服。每次5～15mg(1～3粒)，三日1次，严重病人可遵医嘱增至每次30mg（6粒），每日三次。"
string1 = "（1）口服成人①抗焦虑，一日2.5〜10mg,分2〜4次。"
yirijici = re.compile(dose_str3)
yirijici_match = yirijici.search(string)
if yirijici_match:
    print(yirijici_match.group())