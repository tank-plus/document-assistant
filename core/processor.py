from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font
from openpyxl.styles import Border, Side
from core.util import *
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText
from model.order import Order
import os

# 定义边框样式
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# 定义字体
font12_bold = Font(size=12, bold=True, name="Times New Roman")
font10_common = Font(size=10, name="Times New Roman")
font10_bold_underline = Font(size=10, bold=True, underline='single', name="Times New Roman")


class OrderPIProcessor:
    def __init__(self, order: Order, template="./template/order_pi_template.xlsx"):
        self.order = order
        if not os.path.exists("./static/pi_confirm"):
            os.makedirs("./static/pi_confirm")
        self.file_name = f"./static/pi_confirm/{self.order.get_file_name()}"
        self.template = template

    def process(self):
        # 加载Excel文件
        workbook = load_workbook(filename=self.template, data_only=False)  # 替换为你的Excel文件名
        # 遍历所有sheet
        for sheet_name in workbook.sheetnames:
            description_row = None
            print(f"正在处理Sheet: {sheet_name}")
            if sheet_name == 'PI':
                data_rows = 0
                total_amount = 0.0
                # TODO 从order中解析出真实数据
                order_real_data = {
                    "FIREPLACE MANTEL": [
                        ["13058-X-VBM", "120PCS/120CTNS", 111.20, 13344.00],
                        ["8700-X-CHBW", "109PCS/218CTNS", 154.90, 16884.10],
                        ["8701-X-CHBW", "110PCS/110CTNS", 154.90, 16884.10],
                        ["13058-X-VBM", "120PCS/120CTNS", 111.20, 13344.00],
                        ["8700-X-CHBW", "109PCS/218CTNS", 154.90, 16884.10],
                        ["8701-X-CHBW", "110PCS/110CTNS", 154.90, 16884.10],
                        ["13058-X-VBM", "120PCS/120CTNS", 111.20, 13344.00],
                        ["8700-X-CHBW", "109PCS/218CTNS", 154.90, 16884.10]
                    ],
                    "FIREPLACE MANTEL TOPS": [
                        ["8700-X-CHBW TOPS", "5PCS/5CTNS", 50.00, 250.00],
                    ]
                }

                sheet = workbook[sheet_name]
                for row in sheet.iter_rows():
                    for cell in row:
                        # 查找Description所在的行
                        if cell.value == "Description":
                            description_row = cell.row

                        if cell.value and "The Seller:" in str(cell.value):
                            picture_row = cell.row
                            print(f"picture_row:{picture_row}")

                if description_row:
                    for key, value in order_real_data.items():
                        data_rows += len(value)
                        for record in value:
                            total_amount += float(record[3])

                    print(f"data_rows:{data_rows}")

                    sheet.insert_rows(description_row + 2, data_rows)  # 插入行

                # 拆分数据区域内的合并单元格
                list = []
                for cell_range in sheet.merged_cells:
                    list.append(cell_range)

                for cell_range in list:
                    try:
                        start_row = cell_range.min_row
                        end_row = cell_range.max_row
                        if start_row >= description_row + 2 and end_row <= description_row + 2 + data_rows:
                            print(f"{cell_range}")
                            sheet.unmerge_cells(str(cell_range))
                    except Exception as e:
                        print(e)

                start_row = description_row + 2
                for key, records in order_real_data.items():
                    for i, data_row in enumerate(records, start=start_row):
                        for j, value in enumerate(data_row, start=1):
                            cell = sheet.cell(row=i, column=j)
                            cell.value = value
                            cell.border = thin_border
                            cell.number_format = '$#,##0.00'
                            cell.font = font10_common
                    start_row += len(records)

                total_row = description_row + 2 + len(order_real_data)

                print(f"total_row:{total_row}")

                total_cell1 = sheet.cell(row=total_row, column=1)
                total_cell1.value = 'TOTAL:'
                total_cell1.border = thin_border
                total_cell1.font = font12_bold
                total_cell1.alignment = Alignment(horizontal='right', vertical='center')

                total_cell5 = sheet.cell(row=total_row, column=5)
                total_cell5.value = total_amount
                total_cell5.border = thin_border
                total_cell5.number_format = '$#,##0.00'
                total_cell5.font = font10_bold_underline

                sheet.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=2)

                sheet.cell(row=total_row + 1, column=2, value=number_to_words(total_amount))
                sheet.merge_cells(f"B{total_row + 1}:E{total_row + 1}")
                cell = sheet[f'B{total_row + 2}']
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = thin_border

                # TODO 类别相关的列合并
                sheet.merge_cells(f"A{description_row + 2}:A{description_row + 1 + len(order_real_data)}")
                cell_new = sheet[f"A{description_row + 2}"]
                cell_new.alignment = Alignment(horizontal='center', vertical='center')

                rich_text_a8 = CellRichText('To:', TextBlock(InlineFont(rFont='Times New Roman', u='single'), self.order.customer.id))
                rich_text_a8.font = Font(size=12, bold=True, name="Times New Roman")
                sheet["A8"] = rich_text_a8

                rich_text_a9 = CellRichText('Add:', TextBlock(InlineFont(rFont='Times New Roman', u='single'),self.order.customer.address))
                rich_text_a9.font = Font(size=12, bold=True, name="Times New Roman")
                sheet["A9"] = rich_text_a9

                rich_text_a10 = CellRichText('Tel/Fax:',TextBlock(InlineFont(rFont='Times New Roman', u='single'),self.order.customer.tel_fax))
                rich_text_a10.font = Font(size=12, bold=True, name="Times New Roman")
                sheet["A10"] = rich_text_a10

                img = Image('logo.png')  # 替换为图片文件的路径

                # 设置图片的宽度和高度
                img.width = 200  # 设置宽度为100像素
                img.height = 100  # 设置高度为100像素

                sheet.add_image(img, f'B{picture_row + len(order_real_data) + 1}')

        # 保存Excel文件
        workbook.save(self.output_path)


if __name__ == "__main__":
    data = {
        "{{pi_num}}": "NBHB/RFC2331",
        "{{po_num}}": "606234",
        "{{po_date}}": "2021-01-01",
        "{{customer_name}}": "Real Flame Company Inc.  ",
        "{{customer_address}}": "7800 Northwestern Avenue,Racine, WI 53406",
        "{{customer_tel_fax}}": "800 6541704",
        "{{payment_method}}": "NO DEPOSIT. T/T WITHIN 21DAYS AFTER SHIPMENT",
        "{{delivery_date}}": "AUG 18TH, 2023",
        "{{port_of_loading}}": "NINGBO, CHINA",
        "{{port_of_destination}}": "MONTREAL, CANADA",
        "mantel": [
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS", "$111.2", "$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS", "$111.2", "$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS", "$111.2", "$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS", "$111.2", "$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS", "$154.90", "$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS", "$154.90", "$16,884.10 "]
        ]
    }

    processor = OrderPIProcessor(data, "output.xlsx")
    processor.process()
