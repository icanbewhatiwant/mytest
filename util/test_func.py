import re

d2d_idx = 1
lowd_idx = 2
highd_idx = 3
person_idx = 0
# 数字年龄+人物描述

idx_dict = {"d2d_idx": d2d_idx, "lowd_idx": lowd_idx, "highd_idx": highd_idx, "person_idx": person_idx}
# 对字典按value排序
idx_dict_sort = sorted(idx_dict.items(), key=lambda x: x[1])
sort_string = idx_dict_sort[0][0]
print(idx_dict_sort)
print(type(sort_string))