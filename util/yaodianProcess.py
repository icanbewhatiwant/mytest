from docx import Document
import json
import re

def data2Excel(drug_dict,drug_list,pra_len):
    pra_lens = pra_len-1
    dk = 0 #记录@出现次数
    for i,par in enumerate(paragraphs): #获得段落对象列表
        par_str = par.text
        # if i <=50:
        if par_str =="" :
            continue

        #提取药品中、英文名称
        drug_match = label_drug.search(par_str)
        if drug_match:
            dk+=1
            #匹配到药品英文名称时，字典内容作为一个整体存入list
            if drug_dict and dk==1:
                drug_list.append(drug_dict)
                drug_dict={}

            drug_name = par_str
            yb_info = ""
            en_name = ""
            if dk ==1:
                k = i + 1
                while True:#
                    if k <= pra_lens:
                        next_text = paragraphs[k].text
                        next_match = label_drug.search(next_text)
                        if next_match:
                            dk+=1
                            if dk==2:
                                yb_info = next_text
                                break
                        else:#本句没匹配到标题或医保，判断下一句是否匹配到标签符号，匹配到则本句是英文名称
                            while True:
                                m = k+1
                                if m <=pra_lens:
                                    nex_nex_text = paragraphs[m].text
                                    if nex_nex_text =="":
                                      continue
                                    label_match = label_patr.search(nex_nex_text)
                                    if label_match :
                                        en_name = next_text
                                    break
                    else:
                        break

            dk = 0
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
                        break

                    # 下一段匹配到label
                    if label_patr.search(next_text):
                        break

                    content += "&nsp"+next_text
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
        with open("C:/产品文档/转换器测试数据/1-100.json","w",encoding='utf-8') as fp:
            fp.write(json.dumps(drug_list, indent=4,ensure_ascii=False))#unicode串转中文传入

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
    # Document 类，不仅可以新建word文档，也可以打开一个本地文档
    # doc = Document('C:/产品文档/转换器测试数据/2015年版_1401-1539.docx')
    doc = Document('C:/产品文档/转换器测试数据/2015年版_1201-1400.docx')

    "获取文档所有段落信息："
    # 获取文档所有段落对象
    paragraphs = doc.paragraphs
    pra_len = len(paragraphs)

    # 源数据是pdf转word，数据不规范
    # 标签，前面括号格式有中英文全半角的各种格式组合
    label_drug = re.compile("[@|＠]")
    #标签对应内容提取
    label_patr = re.compile("^(.{,2}【|\[|\[:|［:|［|.【)[^】|\]|］]+(】|\]|］)")  # 中间不能有】，实现非贪婪
    label_con = re.compile("[\u4e00-\u9fa5]+")

    drug_dict = {}
    drug_list = []

    # getLabellist()
    data2Excel(drug_dict,drug_list,pra_len)




