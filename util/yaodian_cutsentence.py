import re
import json
import os
#200-400变量
from util.parameter_store import function_24
from util.parameter_store import zd_24
from util.parameter_store import dose_forbid_24
#400-600变量
from util.parameter_store import function_46
from util.parameter_store import zd_46
from util.parameter_store import dose_forbid_46
#600-800变量
from util.parameter_store import function_68
from util.parameter_store import zd_68
from util.parameter_store import dose_forbid_68
#800-1000
from util.parameter_store import function_810
from util.parameter_store import zd_810
from util.parameter_store import dose_forbid_810
#1000-1200
from util.parameter_store import function_1012
from util.parameter_store import zd_1012
from util.parameter_store import dose_forbid_1012
#1200-1400
from util.parameter_store import function_1214
from util.parameter_store import zd_1214
from util.parameter_store import dose_forbid_1214
#1400-1539
from util.parameter_store import function_1415
from util.parameter_store import zd_1415
from util.parameter_store import dose_forbid_1415



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

function_12 = "(镇静.催眠|镇静.镇痛|镇静.?催眠.急性乙醇戒断|镇静催眠、急性酒精戒断|抗焦虑.镇静催眠|镇痛麻醉|手术后镇痛|分娩镇痛|镇静|催眠|镇痛|抗恐惧|抗癫痫.抗惊厥|小儿惊厥|癫痫持续状态和严重复发性癫痫|癫痫持续状态|一般性失眠|抗?癫痫|抗?失眠|抗?惊厥|抗?焦虑|乙醇戒断|基础麻醉或静脉全麻" \
               "|术前准备|麻醉前用药|麻醉前给药|表面麻醉.神经阻滞麻醉及硬膜外麻醉|神经阻滞或硬膜外麻醉|剖宫产手术硬膜外麻醉|硬膜外麻醉用?|术后应用|诱导麻醉|维持麻醉|表面麻醉|入睡困难|睡眠维持障碍|基础麻醉|抗躁狂或抗精神病|偏头痛的?预防性?治?疗?|偏头痛和慢性每?日?头痛的治疗|偏头痛的发作期治疗|用于|中重度妊娠高血压征、先兆子痫和子痫" \
               "|早产与治疗妊娠高血压|帕金森病、多发性硬化症及痉挛状态|帕金森病|不宁腿综合征|抽动秽语综合征|肝豆状核变性|用于急性严?重?疼痛|中枢性呼吸及循环功能不全|中枢抑制催醒|术?后?催醒|急性脑血栓和脑栓塞|治疗深静脉血栓|治疗急性血栓栓塞|预防手术后深静脉血栓|深静脉血栓或肺栓塞" \
               "|缺血性脑卒中或短暂性脑缺血发作（TIA）|左房室瓣病或心房颤动伴栓塞|蛛网膜下隙出血|蛛网膜下隙阻滞|急性脑血管病恢复期|脑动脉硬化，脑梗死恢复期|中枢性和外周性眩晕|椎动脉供血不足|特发性耳鸣|间歇性跛行|缺血性脑血管病急性期及其他缺血性血管疾病" \
               "|脑梗死急性期|脑外伤及脑手术后的意识障碍|良性记忆障碍|阿尔茨海默病和?.{0,3}血管性痴呆|阿尔茨海默病|重症肌无力、肌营养不良症、多发性周围神经病|确?诊?重症肌无力的?确?证?|治疗重症肌无力|重症肌无力" \
               "|获得性振动性眼球震颤|神经性膀胱功能障碍|假性近视|术后腹胀气或尿潴|对抗非去极化型肌松药的肌松作用|麻醉诱导|全麻.?诱导|全身麻醉|全麻维持量?|全麻诱导|平衡麻醉|全凭静脉麻醉|局部麻醉或椎管内麻醉辅助用药" \
               "|眼科用|耳鼻喉科用|髄管阻滞|硬膜外阻滞?|区域阻滞|神经传导阻滞|外周神经阻滞麻醉|外周神经阻滞|交感神经节阻滞|神经干（丛）阻滞|胃镜检査|尿道扩张术或膀胱镜检査|臂丛神经阻滞麻?醉?|紙管阻滞|硬脊膜外阻滞|局部浸润麻?醉?" \
               "|硬膜外腔阻滞麻?醉?|电休克|快?速?气管插管|维持肌肉松弛|半去极化肌松药的拮抗|青光眼|呕吐|精神分裂症|肾功能不全|肝功能不全|遗尿症|抗高胆红素血症|缓释制剂|治疗心律失常|拮抗东芨着碱中毒" \
               "|静脉全麻|神经阻滞麻醉|吸入麻醉|缓释片|神经阻滞或浸润麻醉|表面局麻|腰麻|神经阻滞)"


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
# bracket_str = "（1） 口服成人抗焦虑，一次0.5〜 1 mg,一日2〜3次。镇静催眠。睡前服2〜4 mg。年老体弱 者应减量。12岁以下小儿安全性与剂量尚未确定。&nsp（2）\t肌内注射抗焦虑、镇静催眠,一次按体重 0. 05 mg/kg,总量不超过4 mg。&nsp（3）\t静脉注射 用于癌症化疗止吐，在化疗前30分 钟注射2〜4 mg,与奋乃静合用效果更佳,必要时重复使 用给药；癫痫持续状态,按体重0. 05 mg/kg,一次不超过 4 mg,如10〜15分钟后发作仍继续或再发。可重复注射 0. 05 mg/kg,如再经10〜15分钟仍无效。需采用其他措 施，12小时内用量一般不超过8 mg。"
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
# cir_str = "ttt（1）未用过左旋多巴的患者，开始 时110mg,一日3次，以后视需要及耐受情况，每隔1〜2 日逐渐增加每日量。如已用过左旋多巴治疗的患者，改 用本品时，须先停用左旋多巴至少8小时。①过去每日 用左旋多巴少于1.5g的患者，开始时110 mg,一日3〜4 次;②过去每日用左旋多巴大于1. 5 g的患者，开始275 mg, 一日3〜4次；均视需要及耐受情况，每隔1〜2日逐渐增 加每日量。成人最大日剂量可达1375 mg。"
# result1 = get_circle_str(cir_str)
# print("circle_cut:",result1)

def get_number_str(str):
    result = []
    result1 = re.split(r'(\d、)', str)
    if result1:
        str0 = result1[0]
        if str0 != "":
            result.append(str0)
        result1 = ["".join(i) for i in zip(result1[1::2], result1[2::2])]
        result.extend(result1)
    # ①前匹配到给药方式时，拼接。序列前的文字一般是汇总，应该进行拼接
    take_str = result[0]
    take_patr_b = re.compile("([①②③④⑤⑥⑦⑧⑨⑩]+)")
    if take_patr_b.search(take_str):
        result = ["".join(i) for i in zip([take_str] * (len(result) - 1), result[1::1])]
    return result

#100-200页内分号切分个例
zd_12 = "([；;]或|牙科|肋间神经|宫颈旁浸润|椎旁脊神经阻滞" \
                  "|阴部神经|药物诱发的锥体外系反应|药物诿发的锥体外系反应|注入蛛网膜下隙|注入硬膜外间隙|硬膜外PCA|重度疼痛|如不能控制|用作胶原酶合成抑制剂时|一过性失眠" \
                  "|用量视患者的耐受情况|辅助椎管内麻醉|尿道扩张术|用于神经阻滞麻醉)+"
dose_forbid_12=["维持量","极量","限量","最大量","总量","维持","继以","患者的耐受情况","耐受的用量"]

exclude_patr = re.compile("[^，。,;；]+[，。,;；]?")#获取功能、年龄后的第一个句子
#加入片袋粒这些单位的话 范围前的数字  0.3mg|6袋|1/4包  范围后的数字 0.3mg|6袋|1/4包|半包|二袋  范围数字一般都是数字 不会用中文所以前面没有中文
before_num_string = "(?:\d+\/\d+|\d*\.?\d*万?)"
after_num_string = "(?:\d+\/\d+|\d*\.?\d+|[半两一二三四五六七八九十])"
# #0. 4〜0.8mg
fanwei_string = "[-|—|〜|～|~]"
unit_string = "(?:ug|μg|ug|mg元素铁|mg|Mg|ng|g氮|g（甘油三酯）|g脂质|g脂肪|g|BU|kU|万IU|IU|万U|U|MBq|MBq（\d*\.\d*mCi）|kBq|mCi|J|昭|ml|mmol|kcal|片|袋|粒|枚|支|揿|喷|包|滴|瓶|枚|套)(?:\/[（(]kg.min[）)]|\/[（(]kg.d[）)]|\/[（(]kg.h[）)]|\/kg|\/mL|\/ml|\/h|\/d|\/L|\/min|\/m2|\/cm2)?"
percent_unit_string = "(?:ug|μg|ug|mg元素铁|mg|Mg|ng|g氮|g（甘油三酯）|g脂质|g脂肪|g|BU|kU|万IU|IU|万U|U|MBq|MBq（\d*\.\d*mCi）|kBq|mCi|J|昭|ml|mmol|kcal|%|片|袋|粒|枚|支|揿|喷|包|滴|瓶|枚|套)(?:\/[（(]kg.min[）)]|\/[（(]kg.d[）)]|\/[（(]kg.h[）)]|\/kg|\/mL|\/ml|\/h|\/d|\/L|\/min|\/m2|\/cm2)?"

dose_str5 = before_num_string+"%?"+fanwei_string+"?"+after_num_string+percent_unit_string


dose_patr = re.compile(dose_str5)

#按作用切分句子
def get_zd_cut(str):
    zd_patr = re.compile(zd_str)
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

                # 含部分关键字的不切分  exclude_patr匹配到功能、年龄、指定字段所在的一句话
                # zd_next_first_match = exclude_patr.search(zd_next)
                # zd_next_first = zd_next_first_match.group()
                # for forbi in dose_forbid:
                #     if forbi in zd_next_first:
                #         forbi_flag = True
                #         break
                # if not forbi_flag:

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

rongye_end_patr = re.compile("("+before_num_string+"%?"+fanwei_string+"?"+after_num_string+"%?溶液[,，])$")
ml_begin_patr = re.compile("^("+before_num_string+fanwei_string+"?"+after_num_string+unit_string+")")


#按作用切分句子
def get_function_cut(str):
    fuction_patr = re.compile("[，。,;；][^，。,;；]*" + function_str + "[^，。,;；]*[，。,;；]")
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

age_dot = "\d*\.?\d+" #有2.5岁的
age_unit_string = "(?:岁|个?月person2age_string|天person2age_string|日person2age_string)"
person2age_string = "(?:成人|新生儿|婴幼?儿|幼儿|儿童|青少年|小儿|少儿|老年人|老人)"
age_str = "(肝、肾功能损害者|高龄患者|老年和体弱或肝功能不全患者|老年人?[或及、和]?体弱患?者|老年人?[或及、和]?虚弱的?患?者|老年人|年老[或及、和]?体弱患?者|特殊人群：严重肝损患者|老年、重病和肝功能受损患者" \
           "|老年患者|重症患者|肝、肾疾病患者|老年、女性、非吸烟、有低血压倾向、严重肾功能损害或中度肝功能损害患者|新生儿|幼儿和儿童|幼儿|儿童青?少年|儿童|婴儿|婴幼儿|早产儿" \
           "|<"+age_dot+age_unit_string+"|≤"+age_dot+age_unit_string+"|小于"+age_dot+age_unit_string+"|"+age_dot+age_unit_string+"|"+age_dot+age_unit_string+"以上|"+age_dot+age_unit_string+"?"+fanwei_string+age_dot+age_unit_string+"|"\
          +age_dot+age_unit_string+"以下|>"+age_dot+age_unit_string+"|≥"+age_dot+age_unit_string+"|大于"+age_dot+age_unit_string+"|小儿|的?患?者|患儿)"

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


#从头开始完整处理一个句子
def get_sentence_cut(str,drug_name):
    str = str.replace("&nsp", "").replace("\t", "").replace(" ", "")
    drug_name = drug_name.replace(" ", "")
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
    #200-400的雷尼替丁含有1、2、这种标号的切分
    if drug_name == "@雷尼替丁":
        number_patr = re.compile("\d、")
        for i,cir in enumerate(circle_list):
            if number_patr.search(cir):
                del circle_list[i]
                circle_list.extend(get_number_str(cir))
    if circle_list:
        for cir in circle_list:
            function_age_reslut1=get_age_func_cut(function_str, cir)
            function_age_result.append(function_age_reslut1)
    return function_age_result

if __name__=="__main__":
    # function_str = function_810
    # zd_str = zd_810
    # dose_forbid = dose_forbid_810
    # test_begin = "(1)口服治疗慢性丙型肝炎成人，每日600mg。儿童，一日按体重10mg/kg，分4次服。疗程7〜14日。6岁以下儿童口服剂量未定。（2）静脉滴注①成人，一日500-1000mg，疗程3〜7日。②儿童，一日10〜15mg/kg，分2次给药，每次静脉滴注20分钟以上。疗程3〜7日。治疗拉沙热、流行性岀血热等严重病例时，成人首剂静脉滴注2g，继以每8小时0.5〜1g，共10日。（3）气雾吸入此用法必须严格按照给药说明中所述气雾发生器和给药方法进行。①儿童给药浓度为20mg/ml，一日吸药12〜18小时，疗程3〜7日。对于呼吸道合胞病毒性肺炎和其他病毒感染，也可持续吸药3〜6日；或一日3次，一次4小时，疗程3日。②成人，一日吸入1g。（4）滴鼻一次1〜2滴，每1〜2小时1次。"
    # result =  get_sentence_cut(test_begin,"@吡喹酮")
    # print(result)
    # print(get_number_str("（1）成人常用量①口服1、十二指肠溃疡和良性胃溃疡急性期治疗:标准剂量为一次150mg,一日2次，早、晚饭时服；或300mg睡前一次服。疗程4〜8周，如需要可治疗12周。大部分患者在4周内治愈，少部分在8周内治愈，有报道每晚一次服300mg,比一日服用2次、一次150mg的疗效好。十二指肠溃疡患者，一次300mg、一日2次的治疗方案，用药4周的治愈率高于一次150mg、一日2次或夜间服300mg的方案，且剂量增加并不提高不良反应的发生率。长期治疗：通常采用夜间顿服，一日150mg。对急性十二指肠溃疡愈合后患者，应进行一年以上的维持治疗，以避免溃疡复发。2、非甾体类抗炎药引起的胃黏膜损伤急性期治疗：一次150mg,一日2次或夜间顿服300mg,疗程8〜12周。预防：在非甾体类抗炎药治疗的同时服用，一次150mg,一日2次或夜间顿服300mg。3、胃溃疡一次150mg,—日2次，绝大部分患者于4周内治愈，未能完全治愈的患者通常在接下来的4周治愈。4、胃食管反流病急性反流性食管炎：一次150mg,一日2次或夜间服300mg,治疗8〜12周。中度至重度食管炎：剂量可增加至一次150mg,一日4次，治疗12周。反流性食管炎的长期治疗：口服一次150mg,一日2次。5、酒佐林格-埃利森综合征宜用大量，一日600〜1200mg。6、间歇性发作性消化不良标准剂量为一次150mg,一日2次，治疗6周。7、预防重症患者的应激性溃疡出血或消化性溃疡引起的反复出血一旦患者可恢复进食，可用口服一次150mg、一日2次，以代替注射给药。8、预防Mendelcon综合征于麻醉前2小时服用150mg,最好麻醉前一日晚上也服150mg。也可用注射剂。产科分娩患者可口服一次150mg,每6小时1次。如需要全身麻醉，应另外给予非颗粒的抗酸剂（如枸椽酸钠）。"))


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


    def data_pro_2list(filepath,file_name):
        tmp = []
        json_str = ""
        for line in open(filepath, 'r', encoding='UTF-8'):
            json_str += line.replace("\n", "").replace("'"," ")
            if check_json_format(json_str):
                tmp.append(json.loads(json_str))
                json_str = ""

        if tmp:
            for drug_info in tmp:
                drug_name = drug_info.get("drugName","")
                take_way = drug_info.get("用法与用量","")
                erke_take_way = drug_info.get("儿科用法与用量","")
                if take_way != "":
                    sentence_cut = get_sentence_cut(take_way,drug_name)
                    drug_info["sentence_cut"] = sum_brackets(sentence_cut)

                if erke_take_way != "":
                    erke_sentence_cut = get_sentence_cut(erke_take_way,drug_name)
                    drug_info["erke_sentence_cut"] = sum_brackets(erke_sentence_cut)

            with open("C:/产品文档/转换器测试数据/cutsentence/"+file_name+".json", "w", encoding='utf-8') as fp:
                for drug in tmp:
                    fp.write(json.dumps(drug, indent=4, ensure_ascii=False))
                    fp.write('\n')

    # #1-200
    # function_str = function_12
    # zd_str = zd_12
    # dose_forbid = dose_forbid_12
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "1-200" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "1-200")
    #     print("file {} druguse2sentence finished!".format("1-200" + ".json"))
    #
    # #201-400
    # function_str = function_24
    # zd_str = zd_24
    # dose_forbid = dose_forbid_24
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "201-400" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "201-400")
    #     print("file {} druguse2sentence finished!".format("201-400" + ".json"))
    #
    # #401-600
    # function_str = function_46
    # zd_str = zd_46
    # dose_forbid = dose_forbid_46
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "401-600" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "401-600")
    #     print("file {} druguse2sentence finished!".format("401-600" + ".json"))
    #
    # #601-800
    # function_str = function_68
    # zd_str = zd_68
    # dose_forbid = dose_forbid_68
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "601-800" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "601-800")
    #     print("file {} druguse2sentence finished!".format("601-800" + ".json"))

    #810-1000
    function_str = function_810
    zd_str = zd_810
    dose_forbid = dose_forbid_810
    doc_path = "C:/产品文档/转换器测试数据/json/" + "801-1000" + ".json"
    if os.path.exists(doc_path):
        data_pro_2list(doc_path, "801-1000")
        print("file {} druguse2sentence finished!".format("801-1000" + ".json"))

    # #1001-1200
    # function_str = function_1012
    # zd_str = zd_1012
    # dose_forbid = dose_forbid_1012
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "1001-1200" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "1001-1200")
    #     print("file {} druguse2sentence finished!".format("1001-1200" + ".json"))
    #
    # #1201-1400
    # function_str = function_1214
    # zd_str = zd_1214
    # dose_forbid = dose_forbid_1214
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "1201-1400" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "1201-1400")
    #     print("file {} druguse2sentence finished!".format("1201-1400" + ".json"))
    #
    # #1401-1539
    # function_str = function_1415
    # zd_str = zd_1415
    # dose_forbid = dose_forbid_1415
    # doc_path = "C:/产品文档/转换器测试数据/json/" + "1401-1539" + ".json"
    # if os.path.exists(doc_path):
    #     data_pro_2list(doc_path, "1401-1539")
    #     print("file {} druguse2sentence finished!".format("1401-1539" + ".json"))