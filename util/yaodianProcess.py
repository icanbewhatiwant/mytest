from docx import Document
import json
import re
import os

def data2Excel(drug_dict,drug_list,pra_len,file_name):
    pra_lens = pra_len-1
    dk = 0 #记录什么时候添加数据到list
    for i,par in enumerate(paragraphs): #获得段落对象列表
        par_str = par.text
        # print("i",i)
        # if i <=50:
        if par_str =="" :
            continue
        # print("dk",dk)
        if drug_dict and dk == 3:
            # print(drug_dict)
            drug_list.append(drug_dict)
            drug_dict = {}
            dk = 0

        #提取药品中、英文名称
        drug_match = label_drug.search(par_str)
        if drug_match and dk==0:
            dk += 1
            #匹配到药品名称前的@符号时，字典内容作为一个整体存入list
            drug_name = par_str
            yb_info = ""
            en_name = ""
            if dk ==1:
                k = i + 1
                while True:#第二个@符号匹配医保信息
                    if k <= pra_lens:
                        next_text = paragraphs[k].text
                        if next_text == "":
                            k += 1
                            continue
                        if label_drug.search(next_text):#是否包含@符号
                            dk += 1
                            if dk==2:
                                yb_info = next_text
                                # break
                        elif label_patr.search(next_text):#是否包含“【】”，药品名称后面既没有YB信息，也没有英文名称
                            break
                        else:#本句没匹配到标题或医保，判断下一句是否匹配到标签符号，匹配到则本句是英文名称
                            m = k + 1
                            while True:
                                if m <=pra_lens:
                                    nex_nex_text = paragraphs[m].text
                                    if nex_nex_text =="":
                                        m += 1
                                        continue
                                    if  label_patr.search(nex_nex_text) :#下下句包含“【】”，下句为英文名称
                                        en_name = next_text
                                        break
                                    else:#可能有两行英文名称
                                        en_name += next_text
                                        while True:
                                            m +=1
                                            if m <=pra_lens:
                                                nn_text = paragraphs[m].text
                                                if nn_text == "":
                                                    continue
                                                if label_patr.search(nn_text):
                                                    en_name +=nex_nex_text
                                                    break
                                            else:
                                                break
                                else:
                                    break
                        k += 1
                    else:
                        break

                    if en_name != "":
                        # dk = 0
                        break

                drug_dict["enName"] = en_name
                drug_dict["drugName"] = drug_name
                drug_dict["yb_info"] = yb_info

        #提取各种标签及其对应内容
        label_match = label_patr.search(par_str)
        if label_match:
            label_str = label_match.group()
            #因为括号中可能有.或者其他符号，找到括号中的全部中文，拼接为label
            label_cmatch = label_con.findall(label_str)
            label = ""
            if label_cmatch:
                label = ''.join(label_cmatch)

            label_len = len(label_str)
            content = par_str[label_len:]

            #下一段可能还是继续当前标签内容，判断并拼接
            j = i+1
            while True:
                if j <=pra_lens:
                    next_text = paragraphs[j].text
                    # 下一段是否为空
                    if next_text =="":
                        j+=1
                        continue

                    # 下一段匹配到药品名称
                    nex_label_match = label_drug.search(next_text)
                    if nex_label_match:
                        dk =3
                        break

                    # 下一段匹配到label
                    if label_patr.search(next_text):
                        break

                    # p = j+1
                    # if p <pra_lens:#同一段末尾有换行
                    #     pp_text = paragraphs[p].text

                    if paras_patr.search(next_text):
                        next_text= "&nsp"+next_text
                    content += next_text
                    j+=1
                else:
                    break
            drug_dict[label] = content

            # print("label",label)
            # print("content",content)
            # print()
        # else:
        #     break
    if drug_list:
        with open("C:/产品文档/转换器测试数据/json/"+file_name+".json", "w", encoding='utf-8') as fp:
            for drug in drug_list:
                fp.write(json.dumps(drug, indent=4,ensure_ascii=False))#unicode串转中文传入
                fp.write('\n')

#遍历文件得到label名称，去重作为列名
# 得到：['【药理】', '【不良反应】', '【禁忌证】', '【注意事项】', '【用法与用量】', '【儿科用法与用量】', '【制剂与规格】', '【适应证】', '【儿科注意事项】', '【药物相互作用】', '【给药说明】']
def getLabellist():
    label_list=[]

    for i, par in enumerate(paragraphs):
        par_str = par.text
        if par_str == "":
            continue

            # 提取各种标签及其对应内容
        match = label_patr.search(par_str)
        if match:
            label_str = match.group()
            label_cmatch = label_con.findall(label_str)
            # if label_cmatch:
            #     label = ''.join(label_cmatch)
            #     if label not in label_list:
            #         label_list.append(label)
            if label_str not in label_list:
                label_list.append(label_str)

    print(label_list)


if __name__ == "__main__":

    # 标签，前面括号格式有中英文全半角的各种格式组合
    label_drug = re.compile("[＠|@]")
    #标签对应内容提取
    label_patr = re.compile("^(.{,2}【|\[|\[:|［:|［|.【)[^】|\]|］]+(】|\]|］)")  # 中间不能有】，实现非贪婪
    label_con = re.compile("[\u4e00-\u9fa5]+")
    #一段中的内容换行后包含换行符，需要判断是同一段内容
    paras_patr = re.compile("^([（(]\d[）)])?(\\t)?")

    filepath = "C:/产品文档/转换器测试数据/已整理数据源/"
    # file_name_list = ["1-200","201-400","401-600","601-800","801-1000","1001-1200","1201-1400","1401-1539"]
    file_name_list = ["1401-1539"]
    for file_name in file_name_list:
        doc_path = filepath+file_name+".docx"
        if os.path.exists(doc_path):
            doc = Document(doc_path)
            # 获取文档所有段落对象
            paragraphs = doc.paragraphs
            pra_len = len(paragraphs)
            drug_dict = {}
            drug_list = []

            data2Excel(drug_dict, drug_list, pra_len, file_name)
            print("file {} word2json finished!".format(file_name+".docx"))







