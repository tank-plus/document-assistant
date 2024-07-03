from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# 创建工作簿
wb = Workbook()

# 选择活动工作表
ws = wb.active

# 设置标题和公司信息
ws['A1'] = 'NINGBO HARBOR IMPORT & EXPORT CO.,LTD'
ws['A3'] = 'Bizhu Chenjia Village, Xikou Town, Fenghua City, Zhejiang Province, China'
ws['A4'] = 'Tel: +86-574-88807585'
ws['A5'] = 'Fax: +86-574-88806858'

# 合并单元格
ws.merge_cells('A1:D1')
ws.merge_cells('A3:D3')

# 格式化标题和公司信息
title_font = Font(bold=True, size=14)
title_alignment = Alignment(horizontal='center', vertical='center')
title_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                      top=Side(style='thin'), bottom=Side(style='thin'))
title_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

for row in ws['1:5']:
    for cell in row:
        cell.font = title_font
        cell.alignment = title_alignment
        cell.border = title_border
        cell.fill = title_fill

# 客户信息
ws['A7'] = 'To:'
ws['B7'] = 'Real Flame Company Inc.'
ws['B8'] = '7800 Northwestern Avenue, Racine, WI 53406'
ws['B9'] = 'Tel/Fax: 800 6541704'
ws['A10'] = 'P/I NO.: NBHB/RFC2425'
ws['B10'] = 'PO NO.: 607132'
ws['A11'] = 'Date: 2024.5.3'

# 表格头部
headers = ["Description", "Model No.", "Quantity", "Unit Price", "Total Amount"]
ws.append(headers)

# 设置头部样式
for cell in ws[ws.max_row-1]:
    cell.font = Font(bold=True)
    cell.border = Border(left=Side(style='medium'), right=Side(style='medium'),
                         top=Side(style='medium'), bottom=Side(style='medium'))
    cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

# 表格数据
items = [
    ["FIREPLACE MANTEL", "1290-X-AGR", "84PCS/168CTNS", 155.8, 13087.2],
    ["FIREPLACE MANTEL", "1290-X-W", "84PCS/168CTNS", 150.1, 12608.4],
]

# 填充数据
for item in items:
    ws.append(item)

# 总计
ws['A14'] = 'TOTAL:'
ws['C14'] = '168PCS/336CTNS'
ws['D14'] = 150.1
ws['E14'] = 25695.6

# 总计说明
total_text = "SAY US DOLLARS TWENTY FIVE THOUSAND SIX HUNDRED AND NINETY FIVE CENTS SIXTY ONLY."
ws['A15'] = total_text
ws['A16'] = total_text.upper()

# 条款和条件
ws['A18'] = "TERMS OF PAYMENT:"
ws['A19'] = "NO DEPOSIT, T/T WITHIN 21DAYS AFTER SHIPMENT"
ws['A20'] = "TIME OF SHIPMENT:     JUN 11TH, 2024"
ws['A21'] = "PORT OF LOADING:      NINGBO, CHINA"
ws['A22'] = "PORT OF DESTINATION:  SACRAMENTO, CA, USA"

# 银行信息
bank_info = [
    "BENEFICIARY’S BANK:",
    "Account with institution: ZHEJIANG RURAL CREDIT COOPERATIVE UNION, HANGZHOU, CHINA",
    "SWIFT BIC:ZJRCCN2N",
    "NO.660 QIUTAO ROAD, HANGZHOU, ZHEJIAHG PROVINCE, CHINA, 310016",
    "Beneficiary: NINGBO HARBOR IMPORT & EXPORT CO.,LTD",
    "Account Number: 201000134920721",
]

ws.append(bank_info)

# 保存工作簿
wb.save('ProformaInvoice_complete_example.xlsx')