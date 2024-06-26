import xlsxwriter

workbook = xlsxwriter.Workbook("出口报关单模板 - 副本.xlsx")
worksheet = workbook.add_worksheet("模板2")
# worksheet = workbook.get_worksheet_by_name("模板")
row = 46
col = 2

text = "A simple textbox with some text"
worksheet.insert_textbox(row, col, text)
worksheet.write('H1','中华人民共和国海关出口货物报关单')
worksheet.write('B1','World')  

workbook.close()