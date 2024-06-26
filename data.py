from openpyxl import load_workbook


BASIC = {}
FIREPLACE_MANTEL = []
FIREPLACE_MANTEL_TOP = []
CUSTOMER = []


# 加载Excel文件
workbook = load_workbook(filename='数据.xlsx', data_only=True)  # 替换为你的Excel文件名

# 遍历所有sheet
for sheet_name in workbook.sheetnames:
    print(f"正在处理Sheet: {sheet_name}")
    
    
    sheet = workbook[sheet_name]

    if "基本信息" == sheet_name:
        # 遍历sheet中的所有行和单元格
        for row in sheet.iter_rows(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row, values_only=False):
            BASIC["{{" + row[0].value + "}}"] = row[1].value
        print(BASIC)
        
    if "FIREPLACE_MANTEL" == sheet_name:
        index = 0
        for row in sheet.iter_rows(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row, values_only=False):
            record = []
            for cell in row:
                record.append(cell.value)
            FIREPLACE_MANTEL.append(record)
            index = index + 1
        print(FIREPLACE_MANTEL)
        
        
    if "FIREPLACE_MANTEL_TOP" == sheet_name:
        index = 0
        for row in sheet.iter_rows(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row, values_only=False):
            record = []
            for cell in row:
                record.append(cell.value)
            FIREPLACE_MANTEL_TOP.append(record)
            index = index + 1
        print(FIREPLACE_MANTEL_TOP)
        
    if "客户信息" == sheet_name:
        index = 0
        for row in sheet.iter_rows(min_row=1, max_col=sheet.max_column, max_row=sheet.max_row, values_only=False):
            record = []
            for cell in row:
                record.append(cell.value)
            CUSTOMER.append(record)
            index = index + 1
        print(CUSTOMER)