
# from util.yaodianRe import get_bracket_str #引入同一包下的模块，文件夹下创建__init__文件()，代表目录是一个包，模块名就是util

import re
admin_route_str = "(餐?后?口服成?人?|含服|涂敷患?处?|喷于患处|外用|肌内或缓?慢?静脉缓?慢?注射|静脉或肌内注射|静脉注射或肌内注射|肌内注射或缓?慢?静脉缓?慢?注射" \
                  "|肌内注射或缓?慢?静脉缓?慢?推注|静脉注射|静脉滴注|深?部?肌内注射|皮下或肌内注射|肌内或皮下注射|冲服|嚼服|浸润局麻|浸润麻醉|外周神经\(丛\)阻滞|外用" \
                  "|滴眼|滴鼻|冲洗|阴道给药|肛门内?给药|舌下含服|阴道用药|瘤体注射|皮下注射|静脉推注|吸入|阴道冲洗|漱口|关节腔注射|处方|灌肠|直肠灌注|贴患处|口服.灌肠" \
                  "|保留灌肠|注入脐静脉|神经阻滞麻醉|硬膜外麻醉|腰麻|臂丛神经阻滞麻醉|黏膜表面局麻|表面麻醉|涂抹|表面麻醉.神经阻滞麻醉及硬膜外麻醉|局部浸润麻?醉?" \
                  "|神经阻滞或浸润麻醉|硬膜外腔阻滞麻醉|神经阻滞或硬膜外麻醉|外周神经阻滞麻醉|镇静.镇痛|气管插管|缓释制剂|靶控输注系统给药)"

admin_route_str1 = "(餐?后?口服成?人?)"

function_str = "(镇静|催眠|镇静.催眠|抗恐惧|抗?癫痫|抗?失眠|一般性失眠|抗癫痫.抗惊厥|抗?惊厥|小儿惊厥|抗?焦虑|抗焦虑.镇静催眠|镇静.催眠.急性乙醇戒断|镇静催眠、急性酒精戒断|乙醇戒断|基础麻醉或静脉全麻|癫痫持续状态和严重复发性癫痫" \
               "|术前准备|麻醉前用药|麻醉前给药|术后应用|诱导麻醉|维持麻醉|癫痫持续状态|入睡困难|睡眠维持障碍|基础麻醉|镇痛|抗躁狂或抗精神病|偏头痛的?预防性?治?疗?|偏头痛和慢性每?日?头痛的治疗|偏头痛的发作期治疗|用于|中重度妊娠高血压征、先兆子痫和子痫" \
               "|早产与治疗妊娠高血压|帕金森病|不宁腿综合征|抽动秽语综合征|肝豆状核变性|用于急性严?重?疼痛|中枢性呼吸及循环功能不全|术?后?催醒|中枢抑制催醒|急性脑血栓和脑栓塞|治疗深静脉血栓|治疗急性血栓栓塞|预防手术后深静脉血栓|深静脉血栓或肺栓塞" \
               "|缺血性脑卒中或短暂性脑缺血发作（TIA）|左房室瓣病或心房颤动伴栓塞|蛛网膜下隙出血|急性脑血管病恢复期|脑动脉硬化，脑梗死恢复期|中枢性和外周性眩晕|椎动脉供血不足|特发性耳鸣|间歇性跛行|缺血性脑血管病急性期及其他缺血性血管疾病" \
               "|脑梗死急性期|脑外伤及脑手术后的意识障碍|良性记忆障碍|阿尔茨海默病.血管性痴呆|阿尔茨海默病和?.{0,3}血管性痴呆|阿尔茨海默病|重症肌无力、肌营养不良症、多发性周围神经病|帕金森病、多发性硬化症及痉挛状态" \
               "|获得性振动性眼球震颤|神经性膀胱功能障碍|假性近视|确?诊?重症肌无力的?确?证?|治疗重症肌无力|重症肌无力|术后腹胀气或尿潴|对抗非去极化型肌松药的肌松作用|麻醉诱导|全麻.?诱导|全身麻醉|全麻诱导|平衡麻醉|全凭静脉麻醉|全麻维持量|全麻维持|局部麻醉或椎管内麻醉辅助用药" \
               "|眼科用|耳鼻喉科用|硬膜外麻醉用|髄管阻滞|硬膜外阻滞?|区域阻滞|神经传导阻滞|黏膜表面麻醉|蛛网膜下隙阻滞|外周神经阻滞|交感神经节阻滞|神经干（丛）阻滞|胃镜检査|尿道扩张术或膀胱镜检査|臂丛神经阻滞|紙管阻滞|硬脊膜外阻滞|局部浸润" \
               "|硬膜外腔阻滞|神经阻滞|手术后镇痛|分娩镇痛|手?术中维持肌松|维持肌松|电休克|气管插管|维持肌肉松弛|半去极化肌松药的拮抗|青光眼|呕吐|精神分裂症|肾功能不全|肝功能不全|遗尿症|抗高胆红素血症|缓释制剂|治疗心律失常|外科硬膜外腔阻滞麻醉|拮抗东芨着碱中毒|用于青光眼|静脉全麻)"

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
    take_str = result[0]
    take_patr_b = re.compile("^([（(]\d[）)])+")
    # (1)序号前有字符串（服药方式）,拼接
    if not take_patr_b.search(take_str):
        result = ["".join(i) for i in zip([take_str]*(len(result)-1),result[1::1])]
    return result
# result = get_bracket_str(bracket_str)
# print("get_bracket_str",result)

# import re
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
# result1 = get_circle_str("（2）肌内或静脉注射成人①催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；②抗惊厥（常 用于治疗癫痫持续状态），缓慢静脉注射300〜500 mg。 成人极量一次0. 25 g,—日0. 5g。")
# print("circle_cut:",result1)


#1-200页句内按指定字符切分，仅拼接句前部分句子以及服用方式
semicolon_str = "([；;]用于|[；;]或|[；;]用作|[；;]硬膜外麻醉|[；;]臂丛神经阻滞麻醉|[；;]各种神经阻滞或硬膜外麻醉|[；;]镇静|[；;]催眠|[；;]抗惊厥|[；;]皮下或肌内注射)+"
#100-200页内分号切分个例
semicolon_12_zd = "([；;]用于|[；;]或|[；;]用作|[；;]硬膜外麻醉|[；;]臂丛神经阻滞麻醉|[；;]各种神经阻滞或硬膜外麻醉|[；;]镇静|[；;]催眠|[；;]抗惊厥|[；;]皮下或肌内注射|[;；]快速气管插管|[;；]癫痫持续状态|[;；]麻醉前用药|[;；]术后应用|[;；]拮抗东芨着碱中毒|[;；]癫痫持续状态|[;；]牙科|[;；]肋间神经|[;；]宫颈旁浸润|[;；]椎旁脊神经阻滞" \
                  "|[;；]阴部神经|药物诱发的锥体外系反应|药物诿发的锥体外系反应|注入蛛网膜下隙|硬膜外PCA|，背景输注量|重度疼痛|如不能控制|用作胶原酶合成抑制剂时|一过性失眠" \
                  "|或按体表面积|用量视患者的耐受情况|全麻维持，成人可釆用连续静脉滴注|辅助椎管内麻醉|使用靶控输注系统给药|尿道扩张术|治疗心律失常|；0.5%溶液|；0.75%溶液|外科硬膜外腔阻滞麻醉|用于神经阻滞麻醉" \
                  "|用于硬膜外腔阻滞麻醉|用于硬膜外阻滞|,吸入麻醉|用作静脉全麻|肛门给药栓剂|缓释片用法|对精神分裂患者|高龄患者|部分患者|也有患者|正在使用西咪替丁治疗)+"
semiconlon_patr = re.compile(semicolon_12_zd)
take_patr = re.compile(admin_route_str)
function_patr = re.compile(function_str)

#将句首中的给药方式作为拼接字符串返回
def get_concat_str(search_string):
    concat_string = ""
    admin_search = take_patr.search(search_string)
    if admin_search:
        # admin_route = admin_search.groups() #返回re.compile()中字符串中所有括号匹配部分
        admin_route = take_patr.findall(search_string)#以列表形式返回全部能匹配的子串
        concat_string +=  ','.join(admin_route)
    return concat_string

def get_semi_cut(str):
    #切分
    str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    semi_result = []
    result = []
    if semiconlon_patr.search(str):
        result = re.split(semicolon_12_zd,str)
    else:
        semi_result.append(str)
    len_semi = len(result)
    if len_semi > 1:
        semi_result.append(result[0])
        result12last = [''.join(i) for i in zip(result[1::2],result[2::2])]
        semi_result.extend(result12last)
    #拼接给药方式
    take_patr_b = re.compile("^([（(]\d[）)])+")
    take_patr_cir = re.compile("([①②③④⑤⑥⑦⑧⑨⑩])+")
    b_match = take_patr_b.search(str)
    cir_match = take_patr_cir.search(str)

    if semi_result:
        if len_semi >1:
            concat_str = semi_result[0]
            for i,con in enumerate(semi_result):
                concat_string = ""
                if i == 0:
                    continue
                #判断句子是否有服药方式，有则不需拼接需要方式，没有要拼接
                take_search = take_patr.search(con)
                # 有（1）标号
                if b_match:
                    # 有（1）标号，有①标号，直接拼接(1)和①标号之间的内容，①标号后开始断句处判断是否有作用，没有则拼接
                    if cir_match:
                        concat_strb = str[:cir_match.start()]  # (1)……
                        concat_strcir = str[cir_match.start():]  # ①……
                        param_str = [concat_strb, cir_match.group()]
                        if param_str:
                            begin_str = ''.join(param_str)
                            concat_string += begin_str
                        if not take_search:
                            concat_string += get_concat_str(concat_strcir)
                    # 有（1）标号，没有①标号，判断断句是否有服用方式，没有则拼接包含标号（1）的首句中的服用方式
                    else:
                        param_str = [b_match.group()]
                        if param_str:
                            begin_str = ''.join(param_str)
                            concat_string += begin_str
                        if not take_search:
                            concat_string += get_concat_str(concat_str)
                    # 无（1）标号
                else:
                    # 没有(1)标号，有①标号，前面有文字的直接拼接，①标号后断句判断是否有服用方式，没有拼接句首中服用方式
                    if cir_match:
                        before_cir_str = concat_str[:cir_match.start()]
                        param_str = [before_cir_str, cir_match.group()]
                        after_cir_str = concat_str[cir_match.start():]
                        if param_str:
                            begin_str = ''.join(param_str)
                            concat_string += begin_str
                        if not take_search:
                            concat_string += get_concat_str(after_cir_str)
                    # 没有(1)标号，没有①标号，判断本句有没有服用方式，没有的话判断前面第一句（下标0）是否有服用方式，本句有则不拼接，没有拼接
                    else:
                        param_str = []
                        if not take_search:
                            concat_string = get_concat_str(concat_str)
                # 这一段决定不用了，因为拼接作用有出错的可能性，而作用并不需要体现在断句正确性中，所以这里不拼接作用了
                #本句没有作用，则拼接第一句的作用
                # function_search = function_patr.search(con)
                # if not function_search:
                #     begin_function_search = function_patr.search(concat_str)
                #     if begin_function_search:
                #         function_list = begin_function_search.groups()
                #         concat_string += ','.join(function_list)
                semi_result[i] = concat_string + con
    # 断句部分还要补充
    return semi_result
semi_str1 = "（2）肌内或静脉注射成人①催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；"
# semi_cut: ['（2）肌内或静脉注射成人①催眠，一次100〜200mg', '（2）肌内或静脉注射成人①；镇静，一次30〜50mg,一日2〜3次；']
semi_str2="（1） 口服 成人 抗癫痫一般一次 0.03g，一日3次；或0. 09 g睡前顿服。极量一次0. 25 g。一日 0. 5g。"
# semi_cut: ['（1）口服成人抗癫痫一般一次0.03g，一日3次', '（1）口服成人。或0.09g睡前顿服。极量一次0.25g。一日0.5g。']
semi_str3 = "肌内或静脉注射成人①催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；"
# semi_cut: ['肌内或静脉注射成人①催眠，一次100〜200mg', '肌内或静脉注射成人①；镇静，一次30〜50mg,一日2〜3次；']
semi_str4 = "肌内或静脉注射成人催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；"
# semi_cut: ['肌内或静脉注射成人催眠，一次100〜200mg', '肌内或静脉注射。；镇静，一次30〜50mg,一日2〜3次；']
test_zd="可口服、皮下注射、肌内注射、静脉注 射及肛门内给药。一次50〜100 mg,一日2〜3次。一日不 超过400 mg,老年患者一日不超过300 mg。重度疼痛可一 次100 mg开始。肛门给药栓剂一次100 mg,一日1〜2次。"
# semi_cut: ['可口服、皮下注射、肌内注射、静脉注射及肛门内给药。一次50〜100mg,一日2〜3次。一日不超过400mg,老年患者一日不超过300mg。', '口服,皮下注射,肌内注射,静脉注射,肛门内给药。重度疼痛可一次100mg开始。', '肛门给药栓剂一次100mg,一日1〜2次。']

# print("semi_cut:",get_semi_cut(semi_str2))

#按年龄、作用、给药方式+判断是否有单次服用剂量来切分句子
age_str = "(成人|肝、肾功能损害者|老年人|老年和体弱或肝功能不全患者|老年人?[或及、和]?体弱患者|老年体弱者|年老体弱者|年老或体弱患者|特殊人群：严重肝损患者|老年或虚弱的患者|老年人?或虚弱患?者|老年、重病和肝功能受损患者" \
          "|老年患者|重症患者|肝、肾疾病患者|老年、女性、非吸烟、有低血压倾向、严重肾功能损害或中度肝功能损害患者|新生儿|幼儿和儿童|幼儿|儿童|儿童青?少年" \
          "|<?\d*岁|\d*[-|〜|~|~]?\d*岁小儿|\d岁以上患儿|\d*[-|〜|~|~]\d*岁|\d*岁以上|\d*岁以下|>\d*岁||d*岁或以上者|小儿)+"

age_zd="……的患者"

dose_str = ""
# 一次……，一日……
dose_str1 = "(一次|初量|开始时|开始|初次量|初始量)[^,.;，。；]*\d*\.?\d*[-|〜|~|~]?\d*\.?\d*(mg\/kg|IU\/kg|IU|mg|ml|g).+?(一日|—日|每晚)\d*\.?\d*[-|〜|~|~]?\d*\.?\d*(次|ml)?"
# 一次……mg
dose_str2 = "(一次)[^,.;，。；(不超过)]*\d*\.?\d*[-|〜|~|~]?\d*\.?\d*(mg\/kg|IU\/kg|IU|mg|ml|g)"
#一日，分N次
dose_str3 = "(一日|—日|按体重)[^,.;，。；]*\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|IU\/kg|IU|mg|ml|g).?(分成|分)\d*\.?\d*[-|〜|~]?\d*\.?\d*(次)?"
# 一日……一日……
dose_str4 = "(一日|—日)[^,.;，。；]*\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|IU\/kg|IU|mg|ml|g).?(一日|—日)\d*\.?\d*[-|〜|~]?\d*\.?\d*(次)?"
#0. 4〜0.8mg
dose_str5 = "\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|IU\/kg|IU|mg|ml|g)"
# 每1kg体重0.15〜0.2mg。
dose_str6 = "每\d*kg体重\d*\.?\d*[-|〜|~]?\d*\.?\d*[mg|ml|g]"
# 排除语句
age_patr = re.compile("[，。,;；][^，。,;；]*(<1岁|5〜10岁小儿)")
dose_patr = re.compile(dose_str5)
def get_age_fun_take(str):
    result = []
    str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    age_result= []
    #按照年龄进行切分，包含年龄所在的句子，前面和后面都有用药剂量时切分
    age_match = age_patr.search(str)
    if age_match:
        age_list = age_patr.findall(str)
        age_num = len(age_list)
        if age_num == 1:
            cut_idx = age_match.start()
            begin_str = str[:cut_idx+1]
            rest_str = str[cut_idx+1:]
            if dose_patr.search(begin_str) and dose_patr.search(rest_str):
                age_result.append(begin_str)
                age_result.append(rest_str)
            else:
                age_result.append(str)
        elif age_num >=2:
            f = re.finditer(age_patr, str)
            if f:
                indexes = [i.start() for i in f]
                #只要当前分段前的任意一个分段有用药剂量，当前分段也有用药剂量，则当前分段是可以切分的
                dose_flag = 0
                for i in range(len(indexes)):
                    if i ==0:
                        age_cut_begin = str[:indexes[i] + 1]
                        age_cut_str = str[indexes[i] + 1:indexes[i + 1]]
                        if dose_patr.search(age_cut_begin):
                            dose_flag=1
                        if dose_flag ==1:
                            if dose_patr.search(age_cut_str):
                                age_result.append(age_cut_begin)
                                age_result.append(age_cut_str)
                        else:
                            if dose_patr.search(age_cut_str):
                                dose_flag = 1
                                # age_result.append(str[:indexes[i+1]])

                    elif i == len(indexes)-1:
                        age_cut_str = str[indexes[i] + 1:]
                        if dose_patr.search(age_cut_str) and dose_flag == 1:
                            age_result.append(age_cut_str)
                    elif 1 <=i and i <len(indexes) - 1:
                        age_cut_str = str[indexes[i] + 1:indexes[i+1]]
                        if dose_flag==1:
                            if dose_patr.search(age_cut_str) :
                                age_result.append(age_cut_str)
                        else:
                            age_result.append(str[:indexes[i+1]])
                        if dose_patr.search(age_cut_str):
                            dose_flag =1
    else:
        age_result.append(str)
    return age_result

agenum1_str ="③癫痫持续状态和严重复发 性癫痫，开始静脉注射10 mg,每间隔10〜15分钟可按 需增加甚至达最大限用量。破伤风时可能需要较大药量。老年和体弱患者,肌内注射或静脉注射的用量减半。静脉注射宜缓慢，每分钟2〜5 mg。"
agenum3_str = "（1） 口服 <1岁，一日1- 2.5 mg；幼儿一日不超过5 mg；5〜10岁小儿一日不超 过 10 mg。"
# ['（1）口服<1岁，一日1-2.5mg；', '幼儿一日不超过5mg', '5〜10岁小儿一日不超过10mg。']
agenum2_str = "（1） 口服 <1岁，一日1- 2.5 mg；一日不超过5 mg；5〜10岁小儿一日不超 过 10 mg。"
# ['（1）口服<1岁，一日1-2.5mg；幼儿一日不超过5mg；', '5〜10岁小儿一日不超过10mg。']
age_nobefore_dose = "（1） 口服 <1岁，测试无数据；5〜10岁小儿一日不超 过 10 mg。"
# ['（1）口服<1岁，测试无数据；5〜10岁小儿一日不超过10mg。']
print(get_age_fun_take(age_nobefore_dose))


    #
    # f = re.finditer(age_patr,str)#获取匹配年龄字段的indx
    # if f:
    #     indexes = [i.start() for i in f]
    #     start = 0
    #     for i, indx in enumerate(indexes):
    #         sbstr = str[start:indx+1]
    #         age_result.append(sbstr)
    #         if i == len(indexes) - 1:
    #             sbstr1 = str[indx+1:]
    #             age_result.append(sbstr1)
    #         start = indx+1
    # if age_result:
    #     b_str = ""
    #     circle_match = circle_sub_patr.search(age_result[0])
    #     if circle_match:
    #         b_str = circle_match.group()
    #     if b_str !="":
    #         rlen = len(age_result)
    #         for i in range(1,rlen):
    #             age_result[i] = b_str+age_result[i]
    # else:
    #     age_result.append(str)
    #
    # return age_result





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



if __name__=="__main__":
    pass



