from openpyxl import load_workbook


BASIC = {}
FIREPLACE_MANTEL = []
FIREPLACE_MANTEL_TOP = []
CUSTOMER = []


# 加载Excel文件
workbook = load_workbook(filename='order_pi_template.xlsx', data_only=False)  # 替换为你的Excel文件名

# 遍历所有sheet
for sheet_name in workbook.sheetnames:

    description_row = None
    print(f"正在处理Sheet: {sheet_name}")
    

    if sheet_name == 'PI':
    
        sheet = workbook[sheet_name]

        

        for row in sheet.iter_rows():
            for cell in row:
                # 查找Description所在的行
                if cell.value == "Description":
                    description_row = cell.row
                    break
            
        
        if description_row:
            new_data =[
                ['FIREPLACE MANTEL', '13058-X-VBM', '120PCS/120CTNS','$111.20','$13,344.00'],
                ['FIREPLACE MANTEL', '13058-X-VBM', '120PCS/120CTNS','$111.20','$13,344.00'],
                ['FIREPLACE MANTEL', '13058-X-VBM', '120PCS/120CTNS','$111.20','$13,344.00'],
                ['FIREPLACE MANTEL', '13058-X-VBM', '120PCS/120CTNS','$111.20','$13,344.00'],
                ['FIREPLACE MANTEL', '13058-X-VBM', '120PCS/120CTNS','$111.20','$13,344.00'],
                ['FIREPLACE MANTEL', '13058-X-VBM', '120PCS/120CTNS','$111.20','$13,344.00']
            ]
            sheet.insert_rows(description_row + 2, len(new_data))  # 插入行

            # 拆分单元格
            # for row in range(description_row + 3, description_row + 3 + len(new_data)-1):
            #     range_name = f"B{row}:E{row}"
            #     print(f"正在处理行: {range_name}")
            #     sheet.unmerge_cells(range_name)


            for i, data_row in enumerate(new_data, start=description_row + 2):
                for j, value in enumerate(data_row, start=1):
                    sheet.cell(row=i, column=j, value=value)

            
# 保存Excel文件
workbook.save('output_with_description.xlsx')