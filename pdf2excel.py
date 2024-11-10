import pdfplumber
import pandas as pd

# #显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)


# 打开PDF文件
with pdfplumber.open('example.pdf') as pdf:
    # 提取第一页中的所有表格
    first_page = pdf.pages[0]
    tables = first_page.extract_tables()

print(tables)

# 将提取的表格数据转换为DataFrame
df = pd.DataFrame(tables[2])

# 打印DataFrame
print(df)