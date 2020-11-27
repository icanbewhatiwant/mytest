#200-400变量# 断句

# 给药方式 已经合并
#年龄 已合并
#功能

#1-200的功能字符串
function_12_str = "(?:镇静.催眠|镇静.镇痛|镇静.?催眠.急性乙醇戒断|镇静催眠、急性酒精戒断|抗焦虑.镇静催眠|镇痛麻醉|手术后镇痛|分娩镇痛|镇静|催眠|镇痛|抗恐惧|抗癫痫.抗惊厥|小儿惊厥|癫痫持续状态和严重复发性癫痫|癫痫持续状态|一般性失眠|抗?癫痫|抗?失眠|抗?惊厥|抗?焦虑|乙醇戒断|基础麻醉或静脉全麻" \
               "|术前准备|麻醉前用药|麻醉前给药|表面麻醉.神经阻滞麻醉及硬膜外麻醉|神经阻滞或硬膜外麻醉|剖宫产手术硬膜外麻醉|硬膜外麻醉用?|术后应用|诱导麻醉|维持麻醉|表面麻醉|入睡困难|睡眠维持障碍|基础麻醉|抗躁狂或抗精神病|偏头痛的?预防性?治?疗?|偏头痛和慢性每?日?头痛的治疗|偏头痛的发作期治疗|用于|中重度妊娠高血压征、先兆子痫和子痫" \
               "|早产与治疗妊娠高血压|帕金森病、多发性硬化症及痉挛状态|帕金森病|不宁腿综合征|抽动秽语综合征|肝豆状核变性|用于急性严?重?疼痛|中枢性呼吸及循环功能不全|中枢抑制催醒|术?后?催醒|急性脑血栓和脑栓塞|治疗深静脉血栓|治疗急性血栓栓塞|预防手术后深静脉血栓|深静脉血栓或肺栓塞" \
               "|缺血性脑卒中或短暂性脑缺血发作（TIA）|左房室瓣病或心房颤动伴栓塞|蛛网膜下隙出血|蛛网膜下隙阻滞|急性脑血管病恢复期|脑动脉硬化，脑梗死恢复期|中枢性和外周性眩晕|椎动脉供血不足|特发性耳鸣|间歇性跛行|缺血性脑血管病急性期及其他缺血性血管疾病" \
               "|脑梗死急性期|脑外伤及脑手术后的意识障碍|良性记忆障碍|阿尔茨海默病和?.{0,3}血管性痴呆|阿尔茨海默病|重症肌无力、肌营养不良症、多发性周围神经病|确?诊?重症肌无力的?确?证?|治疗重症肌无力|重症肌无力" \
               "|获得性振动性眼球震颤|神经性膀胱功能障碍|假性近视|术后腹胀气或尿潴|对抗非去极化型肌松药的肌松作用|麻醉诱导|全麻.?诱导|全身麻醉|全麻维持量?|全麻诱导|平衡麻醉|全凭静脉麻醉|局部麻醉或椎管内麻醉辅助用药" \
               "|眼科用|耳鼻喉科用|髄管阻滞|硬膜外阻滞?|区域阻滞|神经传导阻滞|外周神经阻滞麻醉|外周神经阻滞|交感神经节阻滞|神经干（丛）阻滞|胃镜检査|尿道扩张术或膀胱镜检査|臂丛神经阻滞麻?醉?|紙管阻滞|硬脊膜外阻滞|局部浸润麻?醉?" \
               "|硬膜外腔阻滞麻?醉?|电休克|快?速?气管插管|维持肌肉松弛|半去极化肌松药的拮抗|青光眼|呕吐|精神分裂症|肾功能不全|肝功能不全|遗尿症|抗高胆红素血症|缓释制剂|治疗心律失常|拮抗东芨着碱中毒" \
               "|静脉全麻|神经阻滞麻醉|吸入麻醉|缓释片|神经阻滞或浸润麻醉|表面局麻|腰麻|神经阻滞|"

dose_forbid_12=["维持量","极量","限量","最大量","最大剂量","总量","维持","继以","患者的耐受情况","耐受的用量","患者的反应和耐受程度"]



#200-400
function_24_str = "治疗抑郁症|治疗强迫症|缓慢用药法|抗过敏|过敏性休克|预防心绞痛|治疗佐林格埃利森综合征|抢救感染中毒性休克|抗心律失常|缓解内脏绞痛|治疗心绞痛|术前用药)"

function_24 = function_12_str+function_24_str

#200-400的指定切分字符串
zd_24 = "(?:预防用药剂量|与丙戊酸钠合用|与酶诱导药（除丙戊酸钠之外）合用时|用于肾血管性高血压药物诊断|肾功能损害时|酒石酸盐美托洛尔|用于心律失常的急症处理|心功能Ⅲ〜IV级" \
            "|氢溟酸右美沙芬颗粒|氢漠酸右美沙芬糖浆|氢漠酸右美沙芬缓释片|硫酸沙丁胺醇缓释片|硫酸沙丁胺醇粉雾剂|;控释片|体重≥20kg|肾功能不全患者（肾小球滤过率≤50ml/min）" \
            "|；严重时|粉雾吸入：|；或者|溶液雾化吸入|症状严重者|反流性食管炎，|反流性食管炎的对症治疗|肌酐淸除率为15〜30ml/min|肌酐清除率小于15ml/min时|十二指肠溃疡患者" \
            "|皿度或IV度|注射用药：|＞20kg,|NERD|对严重中毒|单用时：对轻度中毒|对中度中毒|对重度中毒|气管插管|外周血管疾病|球后注射|中度肾功能不全时|粉雾吸入：" \
            "|在肾功能障碍时|肌酐清除率10〜40ml/min时|肌酊清除率＜10ml/min|维拉帕米缓释片|严重心律失常应急|需要静脉给药时|结膜下注射|用于体外电除颤无效的室颤时" \
            "|反流性食管炎，|中度至重度食管炎|反流性食管炎的长期治疗|消化性溃疡：|治疗Hp感染|但在根除Hp治疗|抢救感染中毒性休克、改善微循环)+"

#按年龄、功能、作用切分时 含部分关键字的时候不进行切分
dose_forbid_24 = []
forbid_24 = ["门诊患者","住院患者","大部分患者","90%以上患者","1周疗法","应对患者进一步检査","对于反流性疾病的症状治疗","无发作","老年人及肝肾功能不全者","疗效不佳者可增加剂量",
                  "根据患者的疗效和耐受情况","密切观察患者","大多数患者","根据患者的临床反应","成人处方极量","根据患者年龄和症状适当增减","通常对成人","患者耐受情况","已接受全剂量",
                  "耐受的情况","患者可耐受","体重＜85kg","体重≥85kg","耐受调整剂量","但必须告诉患者","一般药量为每小时","患者的需要和耐受性","可控制症状","在1周疗法中","如患者无发作"]

dose_forbid_24.extend(dose_forbid_12)
dose_forbid_24.extend(forbid_24)

#400-600的功能字符串
function_46_str = "抗休克|治疗严重的三叉神经痛|治疗腹痛|治疗血栓闭塞性脉管炎|治疗急性左心衰竭|治疗慢性肾功能不全|治疗高血压危象)"
function_46 = function_12_str +function_46_str

zd_46 = "(?:闭角型青光眼急性发作，一次125|对于儿童患者|口服溶液剂|急性绞痛发作时|手术前、后|；混悬液|控释制剂|同时服稀盐酸|对于高剂量顺钳|肠镜、钡灌肠|具体用法如下|急性发作降结肠受累|缓解期|滴丸|门冬氨酸钾镁葡萄糖注射液" \
        "|慢性肝炎或肝硬化|缓慢静脉注射、肌内注射|静脉或肌内注射|当急性肺水肿或口服用药疗效不佳|缓释片：|国外临床使用|长效缓释剂|枸橼酸、枸橼酸钠和枸橼酸钾复方溶液|达促红素" \
        "|；甲氧基聚乙二醇促红素|妊娠期妇女，|防止新生儿出血|静脉注射时溶解于|普外科手术时|高度血栓形成倾向时|在矫形外科手术中|合并肺栓塞时|根据性别和体重选择剂量|急性发作期" \
        "|非急性发作期|或于三餐前及睡前口服|直肠给药栓剂注入肛门|或将本品注射液|严重病例|用于胆汁反流性胃炎|当急性肺水肿或口服用药疗效不佳时|或0.75ug/kg|直接缓慢静脉注射时" \
        "|如果失血量是已知的|体重小于6kg|静脉滴注一次0.25g（|或按体表面积20000U/mL24小时|弥散性血管内凝血时|51kg＜体重＜70kg|体重＞70kg|50＜体重（kg）＜59|60＜体重（kg）＜69" \
        "|70＜体重（kg）＜79|80＜体重（kg）＜89|90＜体重（kg）＜99|体重（kg）＞100|51＜体重（kg）＜59|可按表8-2决定剂量|51＜体重（kg）＜70|体重（kg）＞70|80kg或80kg以上女性" \
        "|术后每晚皮下注射|也可于术前|术后8〜12小时|对于接受髄关节大手术|对于接受膝关节大手术|如果在“一次15mg、一日2次”|如果在“一次20mg、一日1次”|或本品60ug溶解于氯化钠" \
        "|术后预防静脉血栓|如存在其他毒副反应|b.如基础ANC低于|b.如基础血小板计数为|c.如基础血小板计数低于|如未达到血液学缓解|如第三次出现|以后根据血清生|一般疗程为3个月〜3年" \
        "|如已有乳汁分泌|抑制已有的泌乳|夜间遗尿症|男性每隔|女性可一次|或一次2mg|或一次口服|待病情改善和稳定后|或一次160mg|月经周期第11〜25日,)"

dose_forbid_46 = []
forbid_46 = ["对于肝肾移植的儿童","当患者衰弱时","后者留置30分钟","适合更长的治疗周期","有高度出血倾向的血液透析","1 个月〜2岁","对恶心和呕吐的预防作用","6岁以下请遵医嘱","，12〜18 岁，",
             ",12〜18 岁，","，12~18岁，","肾功能不全患者","有反复者","前者留置1小时","后者留置30分钟","除个别成人需强化治疗外","患者应立即补服利伐沙班","根据患者中心静脉压（CVP）"]

dose_forbid_46.extend(dose_forbid_12)
dose_forbid_46.extend(forbid_46)

#600-800
function_68_str = "治疗无并发症的急性尿路感染|预防感染性心内膜炎|治疗尿路感染时|治疗单纯性尿路感染|治疗复杂性尿路感染时|治疗军团菌病|预防链球菌感染|治疗肺孢菌病|治疗流行性脑脊髓膜炎)"
function_68 = function_12_str+function_68_str

zd_68 = "(?:甲状腺危象时|经随机临床研究证实|或口服复方碘溶液|多釆用持续静脉滴注|或按体重0.1〜0.2U/kg|也可一次0.25g|也可一次1.25mg|12周后如空腹血糖下降|甲泼尼龙醋酸酯混悬液" \
        "|关节腔内注射量|或一日0.25|气雾剂|妊娠期妇女|哺乳期妇女，|如有皮肤组织氟化物损伤|心室内注射|活动期佝偻病|严重病例|或一次给予|血钙正常后|或一日800〜1600mg|或70mg" \
        "|可将总剂量于一次性|鼻喷剂一日1次|流行性脑脊髓膜炎一日20万|肺炎链球菌脑膜炎及亚急性心内膜炎一日40万|出生15〜30天时|严重感染每日|严重感染一日|严重感染，一日80" \
        "|血流感染、医院获得性肺炎|肌内注射，每日100|本品用低剂量＜5g时|剂量为5g时|静脉滴注首剂1200mg|较重的感染|重症感染。|重症感染每日|或每次3.375g|肠球菌性心内膜炎" \
        "|较重感染，一日|肝性脑病的辅助治疗|结肠手术前准备|或每12小时2.5|或每次0.5-1.0g|衣原体或溶脉脉原体感染|或每次400mg|或每次15〜25mg/kg|或每日500mg顿服|静脉滴注，社区获得性肺炎" \
        "|盆腔感染，|或按如下方法给药：|体重为26~35kg|体重为36~45kg|或采用5日疗法|静脉滴注，一次500mg|以50mg本品|21日后|或5%、10%乳膏剂|复杂性尿路感染，|非淋菌性宫颈炎和尿道炎|医院获得性肺炎，)"

dose_forbid_68 = []
forbid_68 = ["体温正常者","严重全身感染患","AIDS患者"]

dose_forbid_68.extend(dose_forbid_12)
dose_forbid_68.extend(forbid_68)

#800-1000
function_810_str ="治疗足趾甲癣|手指甲癣|治疗食管念珠菌病|预防流感|治疗疟疾|抗厌氧菌、治滴虫|治疗血吸虫病|治疗华支睾吸虫病|治疗并殖吸虫病|治疗姜片虫病|治疗肉瘤|治疗血管瘤)"
function_810 = function_12_str+function_810_str

zd_810 = "(?:静脉滴注，首剂|抗生素相关性肠炎|幽门螺杆菌相关性胃窦炎|口服首剂加倍|或每日15mg/kg|或一日1.5g|或每日按体重0.9|对敏感真菌所致感染|侵袭性曲霉菌病|再发性感染|反复发作性感染" \
         "|治疗拉沙热、流行性岀血热|如有流感暴发流行时|散剂一次|静脉滴注第1日|预防：口服一次|消灭恶性疟原虫配子体|体重在15kg至25kg|体重在25kg至35kg|体重在35kg以上|或总剂量按体重90" \
         "|可同时用栓剂|或同时用甲硝唑阴道|或一日20mg/kg|急性血吸虫病总剂|或一次20〜30mg|也可一次10〜20mg|或一次0.5g|慢性粒细胞白血病，起|或溶于氯化钠注射液|亦可一次80" \
         "|静脉滴注按体重一日0.5|鞘内注射25|静脉滴注大剂量1|或一次0.5-0.75g|或按体表面积一日140mg/m²|联合化疗一次200mg|5天方案：|口服每0|头颈部上皮癌|联合用药按体表面积" \
         "|或按体表面积一次60|联合用药按体表面积一次60|或单药治疗按体表面积一次35|根据不同病种|加速期和急变期一次)"

dose_forbid_810 = []
forbid_810 = ["成人首剂静脉滴注","应在接触流感","任何患者","治疗中严重的中性粒细胞减少"]

dose_forbid_810.extend(dose_forbid_12)
dose_forbid_810.extend(forbid_810)

#1000-1200
function_1012_str ="抗风湿|治疗肝豆状核变性|异烟麟中毒|预防胎儿先天性神经管畸形)"
function_1012 = function_12_str+function_1012_str

zd_1012 = "(?:也可开始|缓释片：|缓释胶囊:|缓释片（胶囊）|一般抗炎及术后抗炎|控、缓释制剂：|其他非感染性炎症：|或酌情增为|急性疼痛：|缓释片，|通常肠溶片|建议在开始的3个月内" \
          "|起效后改为一日2次|由于服用本品|静脉给药一日8|或一日15|出现肝酶异常、中性粒细胞计数降低、血小板计数降低时|肌内注射一次20mg|肌内注射一次25|肌酊清除率＜30ml/min时" \
          "|或睡前顿服10|干混悬剂：|体重＜3kg|或120mg|滴眼滴眼液|妊娠期妇女4000U|乳母每日|眼干燥症|肌内注射伴有干眼病|WHO推荐用量|妊娠期妇女1.5|乳母1.6|妊娠期由于维生素均缺乏而致神经炎" \
          "|嗜酒而致维生素3缺乏|重型，|维生素B.缺乏症：|妊娠期妇女1.6|乳母1.7|数日后减为补充膳食所需量|预防维生素|治疗一日50|妊娠期、哺乳期妇女预防用药|静脉缓注一次25|静脉注射一次25" \
          "|维生素C缺乏：|肌内或静脉注射一日100|肌内注射佝偻病|骨软化症（由|甲状旁腺功能减退|维生素D依赖佝偻病|慢性透析患者低钙|甲状腺功能低下|肾性骨萎缩|家族性低磷血症|低钙抽搐：" \
          "|甲状旁腺功能低下|慢性胆汁淤积：|溶液剂：|维生素AD滴剂|预防關齿|溶液或糖浆剂|妊娠期妇女一日40|哺乳期妇女一日|有机磷制剂静脉滴注|经周围静脉给药时|加入载体溶液时用量的调整" \
          "|当氨基酸需要量为2g（kg-d）时|与其他类型脂肪乳剂同时输注时|静脉滴注每日0.075|静脉滴注一次10|静脉注射低钙血症首剂|通过周围静脉给药时|静脉滴注按磷计|全静脉内营养:|静脉滴注2" \
          "|心肺复苏抢救时|严重高钾血症|必要时静脉输注|当本品与其他免疫抑制药合用时|对于儿童患者|首次20mg应于移植术前|治疗肾细胞癌|对体表肿瘤病灶|大出血时|其他手术前1小时|静脉滴注,成人常用)"

dose_forbid_1012 = []
forbid_1012 = ["成人一次1〜2","口服维生素A10","首日口服10万","10岁以下","5岁以上小儿可用","对于肝肾移植的儿童","治疗肾病及肝硬化等慢性白蛋白缺乏症"]

dose_forbid_1012.extend(dose_forbid_12)
dose_forbid_1012.extend(forbid_1012)

#1200-1400
function_1214_str ="治疗甲真菌病)"
function_1214 = function_12_str+function_1214_str

zd_1214 = "(?:亦可开始用较低剂量|冠状动脉内溶栓|据国内的临床研究|器械消毒以5|0.3%浓度|重金属中毒用量|静脉滴注，一次0.5g|腹壁皮下注射，|经口严重中毒|中度中毒0.5|重度中毒2.0" \
          "|中度中毒2|重度中毒4|氰化物中毒一次|以后，如为甲氨蝶呤过量中毒|如为甲氧苄啶过量中毒|异烟肼口服中毒时|或静脉滴注1次5|逆行性肾盂造影|选择性脑动脉造影，碘海醇动脉内注射浓度300" \
          "|选择性脑动脉造影，碘海醇动脉内注射浓度350|下肢动脉造影，碘海醇动脉内注射浓度300|各种动脉造影，碘海醇动脉内注射浓度300|选择性冠状动脉造影，碘海醇动脉内注射浓度350" \
          "|关节腔造影，碘海醇静脉内注射浓度350|子宫输卵管造影，碘海醇静脉内注射浓度300||涎管造影，碘海醇静脉内注射浓度300|胃、十二指肠|静脉滴注，0.6|如果MRI增强扫描|体重≥75kg" \
          "|心肌显像时如做一天法检查|心肌显像时如做一天法检查|胆红素不正常时|显像结束后，患|1期临床耐受性研究中|Ⅱ期无对照开放的临床研究用药剂量|肿瘤直径大于8cm时" \
          "|足月引产首次剂量、开始时亦可使用选择性的测试剂量|细菌性阴道病|如为含0.5g片剂|外阴病变较重时|克霉嗖药膜阴道给药|如为每枚含0.2g栓剂|如为含0.4g栓剂|如为1.2g栓剂" \
          "|如外阴同时有感染|重症每日2粒|如已有乳汁分泌|若服时不良反应大|如仍无排卵|用于浅部真菌感染时|阴道栓每粒|栓剂治疗阴道念珠菌病|脂溢性皮炎，每日2次|头癣和手癣、足癣" \
          "|头皮脂溢性皮炎每周|手癣、足癣、花斑糠疹|甲搽剂还可为甲真菌病治愈后的预防用药|呼吸道真菌感染|真菌性角膜溃疡|注射液：皮损局部注射|使用洗剂|鱼鳞病、银屑病|开始治疗：" \
          "|治疗头部银屑病|如未测试|继发性青光眼和手术前降眼压|闭角型青光眼急性发作，一次125|肌内或静脉注射一次5)"

dose_forbid_1214 = []
forbid_1214 = ["造影或冠状动脉","有结石的","无结石","更精确的信息","大多数患者总剂量约为"]

dose_forbid_1214.extend(dose_forbid_12)
dose_forbid_1214.extend(forbid_1214)

