'''
利用排序好的字符串和坐标信息生成表格
'''

import re
import openpyxl
from scipy.cluster.hierarchy import fclusterdata
import numpy as np
from scipy import stats

# 读取文件中的数据
data = []
with open(r'C:\Users\Alex\PycharmProjects\Table_rec_system\table_restore\output1.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        match = re.match(r'(.*) \((\d+), (\d+)\) \((\d+), (\d+)\)', line.strip())
        if match:
            string, x1, y1, x2, y2 = match.groups()
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
            data.append((string, (x1, y1), (x2, y2)))

# 按照左上角坐标从上到下，从左到右排序
#data.sort(key=lambda x: (x[1][1], x[1][0]))
def sort_key(item):
    x1, y1 = item[1]
    x2, y2 = item[2]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_y, center_x

data.sort(key=sort_key)


# 计算表格的行数和列数
coords = np.array([[(item[1][0] + item[2][0]) / 2, (item[1][1] + item[2][1]) / 2] for item in data])
# 使用 Z-score 方法进行离群值检测
z_scores = stats.zscore(coords)
outliers = np.where(np.abs(z_scores) > 3)
outliers = list(outliers[0])
print(outliers)
# 删除异常样本
new_data = []
for i in range(len(data)):
    if i not in outliers:
        new_data.append(data[i])

row_clusters = fclusterdata(coords[:, 1:], 40, criterion='distance')
col_clusters = fclusterdata(coords[:, :2], 150, criterion='distance')

# 计算每个字符串的行号和列号
new_data = []
for i in range(len(data)):
    item = data[i]
    string, coord = item[0], item[1]
    row = row_clusters[i]
    col = col_clusters[i]
    new_data.append((string, row, col))

# 创建一个新的 Excel 工作簿
wb = openpyxl.Workbook()
ws = wb.active

# 将数据写入 Excel 表格
for item in new_data:
    string, row, col = item
    ws.cell(row=row, column=col).value = string

# 保存 Excel 文件
wb.save('TiltCorrectionOutput.xlsx')