from docx import Document

# Document 类，不仅可以新建word文档，也可以打开一个本地文档
doc = Document('C:/产品文档/转换器测试数据/临床用药须知 _化学药和生物制品卷_2015年版_1401-1539.docx')  # 想获取的文档文件名，这里是相对路径。
# sections = doc.sections
# print(sections)
# print(len(sections))
# for i,str in enumerate(sections):
#     if i <=10:
#         print(str)

"获取文档所有段落信息："
# 获取文档所有段落对象
paragraphs = doc.paragraphs
# print(paragraphs)
# print(len(paragraphs))

#paragraph对象中更小对象run，run对象包含锻炼文字信息，文字的字体、大小、下划线都包含在run对象中
# for i,par in enumerate(paragraphs):
#     if i <=8:
#         # print(runs)
#         for run in par.runs:
#             print(run.text)
#             print('字体名称：', run.font.name)
#             # 字体名称： 宋体
#             print('字体大小：', run.font.size)
#     else:
#         break

# 获取一个段落对象的文字信息
import re
yfyl_dict={}
grugStr=""
pattern = re.compile(u'[^\u4e00-\u9fa5]') #匹配药物名称，只有中文，其他段落有标点符号，基本可以区分
enpattern = re.compile(u'^[a-zA-Z\s]+$') #匹配药物英文名称，只有英文，没有标点符号
yfyl_patr = re.compile(r".*用法用量.*")
drug_name = ""
for i,par in enumerate(paragraphs): #获得段落对象列表
    par_str = par.text
    if i <=50:
        if par_str !="" :
            # print(par_str)
            pass
        #提取药品名称
        match = pattern.search(par_str)
        if match:
            pass
        else:
            drug_name = par_str
            print("drug_name",drug_name)

        #提取药品英文名称
        en_match = enpattern.search(par_str)
        if en_match:
            en_name = par_str
            print("en_name:", en_name)
        else:
            pass

        #提取用法与用量
        yfyl_match = yfyl_patr.search(par_str)
        if yfyl_match:
        # if "用法与用量" in par_str:
            begin_idx = par_str.find("【")
            end_idx = par_str.find("】")
            label = par_str[begin_idx + 1: end_idx]
            content = par_str[end_idx+1:]
            print("label",label)
            print("content",content)
            print()

    else:
        break

#
# # 获取所有段落文字信息
# pars_string = [par.text for par in paragraphs]
# print(pars_string)