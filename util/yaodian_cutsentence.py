import re
import json
#"|"或是有先后顺序的，先匹配左边再匹配右边，所以短文本应该尽量在包含它的长文本后面，新加入的也要注意这个顺序
admin_route_str = "(口服.灌肠|餐?后?口服成?人?|含服|涂敷患?处?|喷于患处|外用|肌内注?射?或缓?慢?静脉缓?慢?注射|静脉注?射?或肌内注射" \
                  "|肌内注射或缓?慢?静脉缓?慢?推注|皮下或肌内注射|肌内或皮下注射|静脉注射|静脉滴注|深?部?肌内注射|皮下注射|静脉推注|冲服|嚼服|浸润局麻|浸润麻醉|外周神经\(丛\)阻滞|外用" \
                  "|滴眼|滴鼻|冲洗|阴道给药|肛门内?给药|舌下含服|阴道用药|瘤体注射|吸入|阴道冲洗|漱口|关节腔注射|处方|保留灌肠|灌肠|直肠灌注|贴患处" \
                  "|注入脐静脉|涂抹|靶控输注系统给药|注入)"

function_str = "(镇静.催眠|镇静.镇痛|镇静.?催眠.急性乙醇戒断|镇静催眠、急性酒精戒断|抗焦虑.镇静催眠|镇痛麻醉|手术后镇痛|分娩镇痛|镇静|催眠|镇痛|抗恐惧|抗癫痫.抗惊厥|小儿惊厥|癫痫持续状态和严重复发性癫痫|癫痫持续状态|一般性失眠|抗?癫痫|抗?失眠|抗?惊厥|抗?焦虑|乙醇戒断|基础麻醉或静脉全麻" \
               "|术前准备|麻醉前用药|麻醉前给药|表面麻醉.神经阻滞麻醉及硬膜外麻醉|神经阻滞或硬膜外麻醉|剖宫产手术硬膜外麻醉|硬膜外麻醉用?|术后应用|诱导麻醉|维持麻醉|表面麻醉|入睡困难|睡眠维持障碍|基础麻醉|抗躁狂或抗精神病|偏头痛的?预防性?治?疗?|偏头痛和慢性每?日?头痛的治疗|偏头痛的发作期治疗|用于|中重度妊娠高血压征、先兆子痫和子痫" \
               "|早产与治疗妊娠高血压|帕金森病、多发性硬化症及痉挛状态|帕金森病|不宁腿综合征|抽动秽语综合征|肝豆状核变性|用于急性严?重?疼痛|中枢性呼吸及循环功能不全|中枢抑制催醒|术?后?催醒|急性脑血栓和脑栓塞|治疗深静脉血栓|治疗急性血栓栓塞|预防手术后深静脉血栓|深静脉血栓或肺栓塞" \
               "|缺血性脑卒中或短暂性脑缺血发作（TIA）|左房室瓣病或心房颤动伴栓塞|蛛网膜下隙出血|蛛网膜下隙阻滞|急性脑血管病恢复期|脑动脉硬化，脑梗死恢复期|中枢性和外周性眩晕|椎动脉供血不足|特发性耳鸣|间歇性跛行|缺血性脑血管病急性期及其他缺血性血管疾病" \
               "|脑梗死急性期|脑外伤及脑手术后的意识障碍|良性记忆障碍|阿尔茨海默病和?.{0,3}血管性痴呆|阿尔茨海默病|重症肌无力、肌营养不良症、多发性周围神经病|确?诊?重症肌无力的?确?证?|治疗重症肌无力|重症肌无力" \
               "|获得性振动性眼球震颤|神经性膀胱功能障碍|假性近视|术后腹胀气或尿潴|对抗非去极化型肌松药的肌松作用|麻醉诱导|全麻.?诱导|全身麻醉|全麻维持量?|全麻诱导|平衡麻醉|全凭静脉麻醉|局部麻醉或椎管内麻醉辅助用药" \
               "|眼科用|耳鼻喉科用|髄管阻滞|硬膜外阻滞?|区域阻滞|神经传导阻滞|外周神经阻滞麻醉|外周神经阻滞|交感神经节阻滞|神经干（丛）阻滞|胃镜检査|尿道扩张术或膀胱镜检査|臂丛神经阻滞麻?醉?|紙管阻滞|硬脊膜外阻滞|局部浸润麻?醉?" \
               "|硬膜外腔阻滞麻?醉?|电休克|快?速?气管插管|维持肌肉松弛|半去极化肌松药的拮抗|青光眼|呕吐|精神分裂症|肾功能不全|肝功能不全|遗尿症|抗高胆红素血症|缓释制剂|治疗心律失常|拮抗东芨着碱中毒" \
               "|静脉全麻|神经阻滞麻醉|吸入麻醉|缓释片|神经阻滞或浸润麻醉|表面局麻|腰麻|神经阻滞)"

bracket_str = "（1） 口服成人抗焦虑，一次0.5〜 1 mg,一日2〜3次。镇静催眠。睡前服2〜4 mg。年老体弱 者应减量。12岁以下小儿安全性与剂量尚未确定。&nsp（2）\t肌内注射抗焦虑、镇静催眠,一次按体重 0. 05 mg/kg,总量不超过4 mg。&nsp（3）\t静脉注射 用于癌症化疗止吐，在化疗前30分 钟注射2〜4 mg,与奋乃静合用效果更佳,必要时重复使 用给药；癫痫持续状态,按体重0. 05 mg/kg,一次不超过 4 mg,如10〜15分钟后发作仍继续或再发。可重复注射 0. 05 mg/kg,如再经10〜15分钟仍无效。需采用其他措 施，12小时内用量一般不超过8 mg。"


#按大括号切分句子  效果：[……(1)……,……(2)……，……]
def get_bracket_str(str):
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


# 按圆序号切分句子  效果：['（1）这一段的原内容 ①……', '（1）这一段的原内容②……']
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
cir_str = "ttt（1）未用过左旋多巴的患者，开始 时110mg,一日3次，以后视需要及耐受情况，每隔1〜2 日逐渐增加每日量。如已用过左旋多巴治疗的患者，改 用本品时，须先停用左旋多巴至少8小时。①过去每日 用左旋多巴少于1.5g的患者，开始时110 mg,一日3〜4 次;②过去每日用左旋多巴大于1. 5 g的患者，开始275 mg, 一日3〜4次；均视需要及耐受情况，每隔1〜2日逐渐增 加每日量。成人最大日剂量可达1375 mg。"
# result1 = get_circle_str(cir_str)
# print("circle_cut:",result1)


#100-200页内分号切分个例
zd_12 = "([；;]或|牙科|肋间神经|宫颈旁浸润|椎旁脊神经阻滞" \
                  "|阴部神经|药物诱发的锥体外系反应|药物诿发的锥体外系反应|注入蛛网膜下隙|注入硬膜外间隙|硬膜外PCA|重度疼痛|如不能控制|用作胶原酶合成抑制剂时|一过性失眠" \
                  "|用量视患者的耐受情况|辅助椎管内麻醉|尿道扩张术|用于神经阻滞麻醉)+"
zd_patr = re.compile(zd_12)
exclude_patr = re.compile("[^，。,;；]+[，。,;；]?")#获取功能、年龄后的第一个句子
dose_forbid=["维持量","极量","限量","最大量","总量","维持","继以","患者的耐受情况","耐受的用量"]

#按作用切分句子
def get_zd_cut(str):
    zd_result = []
    # 只要当前分段前的任意一个分段有用药剂量，当前分段也有用药剂量，当前分段可切分
    zd_match = zd_patr.search(str)
    if zd_match:
        # 每次判断当前作用前面整段句子，以及当前作用和下一个作用之间的句子，是否有用药剂量，都满足时，存储当前作用index用于断句，结果是满足断句的作用的index list
        idxes_list = []
        f = re.finditer(zd_patr, str)
        if f:
            indexes = [i.start() for i in f]
            for i, idx in enumerate(indexes):
                forbi_flag = False
                zd_begin = str[:idx]
                zd_next = str[idx:] if i == len(indexes) - 1 else str[idx:indexes[i + 1]]


                # 含部分关键字的不切分
                zd_next_first_match = exclude_patr.search(zd_next)
                zd_next_first = zd_next_first_match.group()
                for forbi in dose_forbid:
                    if forbi in zd_next_first:
                        forbi_flag = True
                        break
                if not forbi_flag:

                    if dose_patr.search(zd_begin) and dose_patr.search(zd_next):
                        idxes_list.append(idx)
        # 用于断句的index_list,存放满足条件的年龄的index，切分即可
        if idxes_list:
            for j, idxx in enumerate(idxes_list):
                cut_string = str[:idxx] if j == 0 else str[idxes_list[j - 1]:idxx]
                zd_result.append(cut_string)
                if j == len(idxes_list) - 1:
                    cut_end_string = str[idxx:]
                    zd_result.append(cut_end_string)
        else:
            zd_result.append(str)
    else:
        zd_result.append(str)
    return zd_result


take_patr = re.compile(admin_route_str+"+")
dose_str = ""
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

fuction_patr = re.compile("[，。,;；][^，。,;；]*"+function_str+"[^，。,;；]*[，。,;；]")
dose_patr = re.compile(dose_str5)
rongye_end_patr = re.compile("(\d*\.?\d*%?[-|〜|~]?\d*\.?\d*%?溶液[,，])$")
ml_begin_patr = re.compile("^(\d*\.?\d*[-|〜|~]?\d*\.?\d*(mg\/kg|mg|ml|g))")


#按作用切分句子
def get_function_cut(str):
    function_result = []
    # 只要当前分段前的任意一个分段有用药剂量，当前分段也有用药剂量，当前分段可切分
    fuction_match = fuction_patr.search(str)
    if fuction_match:
        # 每次判断当前作用前面整段句子，以及当前作用和下一个作用之间的句子，是否有用药剂量，都满足时，存储当前作用index用于断句，结果是满足断句的作用的index list
        idxes_list = []
        f = re.finditer(fuction_patr, str)
        if f:
            indexes = [i.end()-1 if i.group().endswith((";","；")) else i.start()for i in f]  #当作用所在句子以分号结尾时，idx取句子结尾，不取开头
            for i, idx in enumerate(indexes):
                forbi_flag = False
                fuction_begin = str[:idx + 1]
                fuction_next = str[idx + 1:] if i == len(indexes) - 1 else str[idx + 1:indexes[i + 1]]
                #含部分关键字的不切分

                fuction_next_first_match = exclude_patr.search(fuction_next)
                if fuction_next_first_match:
                    fuction_next_first = fuction_next_first_match.group()
                    for forbi in dose_forbid:
                        if forbi in fuction_next_first:
                            forbi_flag = True
                            break
                #如果不含部分关键字，再判断前一句是否以  0.25%溶液，结尾 。后一句是否以15〜30ml开头（0.25%溶液，15〜30ml是一个整体，不应该切分）
                if forbi_flag == False:
                    if rongye_end_patr.search(fuction_begin) and ml_begin_patr.search(fuction_next):
                        forbi_flag = True

                if not forbi_flag:

                    if dose_patr.search(fuction_begin) and dose_patr.search(fuction_next):
                        idxes_list.append(idx + 1)
        # 用于断句的index_list,存放满足条件的年龄的index，切分即可
        if idxes_list:
            for j, idxx in enumerate(idxes_list):
                cut_string = str[:idxx] if j == 0 else str[idxes_list[j - 1]:idxx]
                function_result.append(cut_string)
                if j == len(idxes_list) - 1:
                    cut_end_string = str[idxx:]
                    function_result.append(cut_end_string)
        else:
            function_result.append(str)
    else:
        function_result.append(str)
    return function_result
fuction1_str = "口服成人镇痛：一次100〜 200 mg,—日4次；或每4小时口服1次。缓释制剂：一 次200〜300 mg,一日2次。"
# ['口服成人镇痛：一次100〜200mg,—日4次；或每4小时口服1次。', '缓释制剂：一次200〜300mg,一日2次。']
function2_str = "（2）肌内或静脉注射成人①催眠，一次100〜200 mg；镇静，一次30〜50 mg,一日2〜3次；②抗惊厥（常 用于治疗癫痫持续状态），缓慢静脉注射300〜500 mg。 成人极量一次0. 25 g,—日0. 5g。"
# ['（2）肌内或静脉注射成人①催眠，一次100〜200mg；', '镇静，一次30〜50mg,一日2〜3次；', '②抗惊厥（常用于治疗癫痫持续状态），缓慢静脉注射300〜500mg。成人极量一次0.25g,—日0.5g。']
no_function_str = "（2）抗惊厥 口服或灌肠 一次40〜60 mg/kg。"
# print(get_function_cut(no_function_str))


age_str = "(肝、肾功能损害者|高龄患者|老年和体弱或肝功能不全患者|老年人?[或及、和]?体弱患?者|老年人?[或及、和]?虚弱的?患?者|老年人|年老[或及、和]?体弱患?者|特殊人群：严重肝损患者|老年、重病和肝功能受损患者" \
           "|老年患者|重症患者|肝、肾疾病患者|老年、女性、非吸烟、有低血压倾向、严重肾功能损害或中度肝功能损害患者|新生儿|幼儿和儿童|幼儿|儿童青?少年|儿童" \
           "|<?\d*岁|\d*[-|〜|~|~]?\d*岁小儿|\d*岁以上患?儿?|\d*[-|〜|~|~]\d*岁|\d*岁以下|d*岁或以上者|>\d*岁|小儿|的?患?者)"

age_patr = re.compile("[，。,;；][^，。,;；]*(维持量[,，。：:]?)?"+age_str)

# 不用管年龄、作用后面的用药关键字，被限制的可能性很小，因为年龄、作用本身就可以作为独立断句的标准了


#按年龄切分句子
def get_age_cut(str):
    # str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    age_result= []
    # 只要当前分段前的任意一个分段有用药剂量，当前分段也有用药剂量，则当前分段是可以切分的
    age_match = age_patr.search(str)
    if age_match:
        #每次判断当前年龄前面整段句子，以及当前年龄和下一个年龄之间的句子，是否有用药剂量，都满足时，存储当前年龄index用于断句，结果是满足断句的年龄的index list
        idxes_list = []
        f = re.finditer(age_patr, str)
        if f:
            indexes = [i.start() for i in f]
            for i,idx in enumerate(indexes):
                forbi_flag = False
                age_begin = str[:idx + 1]
                age_next = str[idx + 1:] if i == len(indexes)-1 else str[idx+1:indexes[i+1]]
                age_next_first_match = exclude_patr.search(age_next) #排除句中部分的关键字，很少，几乎可以不做
                age_next_first = age_next_first_match.group()
                for forbi in dose_forbid:
                    if forbi in age_next_first:
                        forbi_flag = True
                        break
                if not forbi_flag:
                    if dose_patr.search(age_begin) and dose_patr.search(age_next):
                        idxes_list.append(idx+1)
        #用于断句的index_list,存放满足条件的年龄的index，切分即可
        if idxes_list:
            for j,idxx in enumerate(idxes_list):
                    cut_string = str[:idxx] if j == 0 else str[idxes_list[j-1]:idxx]
                    age_result.append(cut_string)
                    if j ==len(idxes_list)-1:
                        cut_end_string=str[idxx:]
                        age_result.append(cut_end_string)
        else:
            age_result.append(str)
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
age_huanzhe = "（2）	当用卡比多巴：左旋多巴（1 ： 10）片剂疗效不 理想时，可改用1 ： 4的片剂，每日总量酌情减少。卡比 多巴左旋多巴控释片是1份卡比多巴与4份左旋多巴 混合而成，有卡比多巴左旋多巴控释片50/200 （250 mg）与卡比多巴左旋多巴控释片25/100（125 mg） 两种。250 mg片剂可整片或半片服用,125 mg只可整 片服用；两种片剂均不可咀嚼或捣碎。①从未用过左旋 多巴的轻症患者，开始时125 mg,一日2次，需要较大量 左旋多巴的中、重度患者，初次量也可用250 mg,一日 2次，但间隔时间至少需6小时；②对正在应用卡比多巴 左旋多巴普通片（1 ：10）治疗的患者，换服控释片50/ 200（250 mg）的剂量应调节至每日能供给比原先剂量约多 10%以上的左旋多巴，视治疗反应每日最多可加至比原先 剂量多30%的左旋多巴。白天控释片的两剂间隔时间应为 4〜8小时;③对正在单用左旋多巴的患者，在开始给卡比多 巴左旋多巴控释片50/200（250 mg）前，须先停用左旋多巴 至少8小时,且控释片应提供比原先约多25%的左旋多巴 量。轻、中度患者初始量用250 mg,一日2次。"
age_zhe = "口服 一次50〜100mg，一日2〜3 次，一般不超过一日300 mg，最大量为400 mg。肾功能 障碍者应减量5mg。儿童不用。"
test_zhe = "口服(1)肝豆状核变性成人开 始一日用量为250 mg，逐渐增量；轻症一日1000 mg,分 2〜4次口服；重症一日2000〜2500 mg,分4次。维持量，成人一日750〜1000 mg。可根据24小时尿铜指标 对青霉胺用量进行调整。可行间歇疗法。青霉胺排铜 的方案有两种：①持续疗法：适用于病程较长、症状较重 的患者，持续给予青霉胺治疗。0.5〜1年，根据临床表现 的变化和实验室检查各项指标分析，决定是否改为间歇 疗法或逐渐减量。②间歇疗法：用于稳定期或症状前期 的治疗，以及部分症状较轻的患者。方法有服用2周停 2周、服用10天停10天、服用1周停1周等方法。成人 多釆用服用2周停2周法。"
# print(get_age_func(age_huanzhe))


#将句首中的给药方式作为拼接字符串返回
def get_concat_str(search_string):
    admin_route_str = ""
    admin_search = take_patr.search(search_string)
    if admin_search:
        admin_route = take_patr.finditer(search_string)#以列表形式返回全部能匹配的子串
        admin_route_list = [f.group() for f in admin_route]
        admin_route_str = admin_route_list[-1]
    return admin_route_str


#按年龄和功能切分①后句子，并拼接
def get_age_func_cut(str_fun,ori_str):
    # ori_str = ori_str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    take_patr_b = re.compile("([（(]\d[）)])+")
    take_patr_cir = re.compile("([①②③④⑤⑥⑦⑧⑨⑩])+")
    b_match = take_patr_b.search(ori_str)
    cir_match = take_patr_cir.search(ori_str)
    str = ""
    concat_string = ""
    take_string = ""
    # 获得句首拼接字符串
    # 只有……（1）……①  -->  ①……
    if b_match:
        # 有（1）标号，有①标号，直接拼接(1)和①标号之间的内容，①标号后开始第二句断句开始判断是否有服药方式，没有则拼接第一个断句的服药方式，第一个断句没有也不用拼接
        if cir_match:
            str = ori_str[cir_match.end():] #①后内容（不包含①）
            concat_string = ori_str[:cir_match.end()]# ……(1)……①
        # ……（1）……  -->  （1）……
        # 有（1）标号，没有①标号，判断断句是否有服用方式，没有则拼接包含标号（1）的首句中的服用方式
        else:
            str = ori_str[b_match.end():]
            concat_string = ori_str[:b_match.end()] #……(1)
    else:# ……①……  -->  ①……
        # 没有(1)标号，有①标号，前面有文字的直接拼接，①标号后断句判断是否有服用方式，没有拼接句首中服用方式
        if cir_match:
            str = ori_str[cir_match.end():]# ……①标号后内容(不包含①标号)
            concat_string = ori_str[:cir_match.end()] #……①
        # 没有(1)标号，没有①标号，判断本句有没有服用方式，没有的话判断前面第一句（下标0）是否有服用方式，本句有则不拼接，没有拼接
        #…… --> ……
        else:
            str = ori_str

    #按指定年龄或者功能切分
    age_fun_result = []
    tmp_result =[]
    cat_fun_result = []
    fun_patrr = re.compile("[，。,;；][^，。,;；]*"+str_fun)
    #按作用切分
    if fun_patrr.search(str):
        cat_fun_result = get_function_cut(str)
    else:
        cat_fun_result.append(str)

    #按年龄切分
    for fun_con in cat_fun_result:
            # tmp_result.append(get_age_cut(fun_con))
            age_result = get_age_cut(fun_con)
            #按指定字符串切分
            for agestr in age_result:
                    tmp_result.append(get_zd_cut(agestr))

    # 拼接给药方式和前面内容
    if tmp_result:
        #take_string 搜索给药方式的字符串 需要拼接切分句子的首句，以及拼接按年龄切分句子的句首，最后选择拼接字符串中离后面断句最近的给药方式，拼接到后面的断句
        take_string = tmp_result[0][0]
        admin_route_string = ""
        for i,con in enumerate(tmp_result):
            #判断断句是否有服药方式，有则不需拼接服药方式，没有要拼接
            len_con = len(con)
            if len_con>1:
                take_string += con[0]
            for k in con:
                take_search = take_patr.search(k)
                if not take_search:
                    admin_route_string = get_concat_str(take_string)
                age_fun_result.append(concat_string +admin_route_string+ k)
                admin_route_string = ""
        return age_fun_result
test_str="（1） 口服 催眠，30〜100 mg,晚上 一次顿服；镇静，一次15〜30 mg,一日2〜3次；抗惊厥， 一日90~180 mg,可在晚上一次顿服，或30〜60 mg, 一 日3次。极量一次250 mg,—日500 mg。老年人或虚弱 患者应减量，常用量即可产生兴奋、精神错乱或抑郁。 抗高胆红素血症，一次30〜60 mg,一日3次。"
# print(get_age_func_cut(age_str,function_str,test_str))


#从头开始完整处理一个句子
def get_sentence_cut(str):
    str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    bracket_patr = re.compile("([（(]\d[）)]){1}")
    circle_patr = re.compile(r'([①②③④⑤⑥⑦⑧⑨⑩]+)')
    bracket_list=[]
    circle_list=[]
    function_age_result = []
    #str有括号（），切分（）
    # 效果：[……(1)……,……(2)……，……]
    if bracket_patr.search(str):
        bracket_list = get_bracket_str(str)
    else:
        bracket_list.append(str)

    #判断是否有①圆括号
    # 结果效果：['（1）这一段的原内容 ①……', '（1）这一段的原内容②……']
    if bracket_list:
        for ci in bracket_list:
            yuan_list = circle_patr.findall(ci)
            if len(yuan_list)>1:
                cir_list = get_circle_str(ci)
                circle_list.extend(cir_list)
            else:
                circle_list.append(ci)

    if circle_list:
        for cir in circle_list:
            function_age_reslut1=get_age_func_cut(function_str, cir)
            function_age_result.append(function_age_reslut1)
    return function_age_result

if __name__=="__main__":
    tt_str = "（1） 口服 成人 ①抗焦虑，一次 2.5〜10 mg,一日2〜4次。②镇静、催眠、急性乙醇戒 断,第一日，一次10 mg。一日3〜4次,以后按需要减少到一次5mg,一日3〜4次。老年或体弱患者应减量。（2）肌内或静脉注射  成人①基础麻醉或静脉全麻。10-30 mg。②镇静、催眠或急性乙醇戒断，开始 10 mg,以后按需每隔3〜4小时加5〜10 mg。24小时 总量以40〜50 mg为限。③癫痫持续状态和严重复发 性癫痫，开始静脉注射10 mg,每间隔10〜15分钟可按 需增加甚至达最大限用量。破伤风时可能需要较大药量。老年和体弱患者,肌内注射或静脉注射的用量减半。静脉注射宜缓慢，每分钟2〜5 mg。"
    tt_str1 = "口服 成人临睡前服7. 5 mg,老年 和体弱或肝功能不全患者3. 75 mg。"
    zd_str = "（1）麻醉用成人常用量①表面 麻醉：2%〜4%溶液一次不超过100 mg。②髄管阻滞： 用1%溶液，以200 mg为限。③硬膜外阻滞：胸腰段用 1. 5%〜2%溶液，250〜300 mg。" \
             "④浸润麻醉或静脉注射 区域阻滞：用0. 25% ~0. 5%溶液，50〜300 mg。⑤外周 神经阻滞：臂丛（单侧）用1.5%溶液，250〜300 mg；牙科 用2%溶液，20〜100 mg；" \
             "肋间神经（每支）用1%溶液 30 mg,300 mg为限；宫颈旁浸润用0. 5%〜1%溶液，左右 侧各100 mg；椎旁脊神经阻滞（每支）用1. 0%溶液30〜 50 mg,300 mg为限；" \
             "阴部神经用0.5%〜1%溶液，左右侧 各100 mg。⑥交感神经节阻滞:颈星状神经节用1.0%溶 液50 mg；⑦一次限量：不加肾上腺一般不要超过200 mg （4 mg/kg）,加肾上腺素为300〜350 mg（6 mg/kg）,静脉 注射区域阻滞极量4 mg/kg。"

    rongye_str = "③硬脊膜外阻滞时，0.25%〜0.375%溶液，10〜20ml可用于镇痛；0.5%溶液，10〜20ml,可用于一般的下腹部手术；0.75%溶液，10〜20ml用于中上腹部手术。"
    test_begin = "口服（1）成人第1日50 mg,第 2日100 mg,第3日200 mg,第4日300 mg,以后逐渐增 加剂量到有效剂量范围。可根据患者的疗效和耐受情 况调整剂量，一般一日为300〜750 mg,分2次给药。&nsp（2）儿童青少年 起始剂量一次25 mg, 一日2次；根据病情和耐受情况逐渐加量，一次增加25〜50 mg,至 有效剂量或最大耐受剂量。最大剂量一日750 mg。&nsp（3）老年 用药应慎重，第1日为25 mg,以后每日 增加25〜50 mg,直到产生疗效。&nsp缓释片用法：应整片服下，一日1次,晚间服用。对 精神分裂患者的推荐的起始剂量为一日300 mg。滴定至 —日400 mg〜800 mg的范围。"
    #
    # result =  get_sentence_cut(test_begin)
    # print(result)


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

    filepath = "C:/产品文档/转换器测试数据/已整理1-200_20201116.json"
    def data_pro_2list(filepath):
        tmp = []
        json_str = ""
        for line in open(filepath, 'r', encoding='UTF-8'):
            json_str += line.replace("\n", "").replace("'"," ")
            if check_json_format(json_str):
                tmp.append(json.loads(json_str))
                json_str = ""

        if tmp:
            for drug_info in tmp:
                take_way = drug_info.get("用法与用量","")
                erke_take_way = drug_info.get("儿科用法与用量","")
                if take_way != "":
                    sentence_cut = get_sentence_cut(take_way)
                    drug_info["sentence_cut"] = sum_brackets(sentence_cut)

                if erke_take_way != "":
                    erke_sentence_cut = get_sentence_cut(erke_take_way)
                    drug_info["erke_sentence_cut"] = sum_brackets(erke_sentence_cut)

            with open("C:/产品文档/转换器测试数据/1-200_20201116_cutsentence2.json", "w", encoding='utf-8') as fp:
                for drug in tmp:
                    fp.write(json.dumps(drug, indent=4, ensure_ascii=False))
                    fp.write('\n')


    data_pro_2list(filepath)




