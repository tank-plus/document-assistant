from openpyxl import load_workbook

class OrderPIProcessor:
    def __init__(self, data, ouput_path, template="./template/order_pi_template.xlsx"):
        self.data = data
        self.output_path = ouput_path
        self.template = template
        
    def process(self):
        wb = load_workbook(self.template)
        for sheet in wb:
    
            description_row = None
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.value == "Description":
                        description_row = cell.row + 1
                    if cell.value in self.data:
                        cell.value = self.data[cell.value]
                        
            
            
                        
                        
            if description_row:
                mantel = self.data.get("mantel", [])
                sheet.insert_rows(description_row + 1, len(mantel))
                for i, data_row in enumerate(mantel, start=description_row + 1):
                    for j, value in enumerate(data_row, start=1):
                        sheet.cell(row=i, column=j, value=value)
                    sheet.unmerge_cells(start_row=i, start_column=3, end_row=i, end_column=len(data_row))
                        
                        
        wb.save(self.output_path)
        
        
if __name__ == "__main__":
    data = {
        "{{pi_num}}": "NBHB/RFC2331",
        "{{po_num}}":"606234",
        "{{po_date}}": "2021-01-01",
        "{{customer_name}}": "Real Flame Company Inc.  ",
        "{{customer_address}}": "7800 Northwestern Avenue,Racine, WI 53406",
        "{{customer_tel_fax}}": "800 6541704",
        "{{payment_method}}":"NO DEPOSIT. T/T WITHIN 21DAYS AFTER SHIPMENT",
        "{{delivery_date}}":"AUG 18TH, 2023",
        "{{port_of_loading}}": "NINGBO, CHINA",
        "{{port_of_destination}}":"MONTREAL, CANADA",
        "mantel": [
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS","$111.2","$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS","$111.2","$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS","$111.2","$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "13058-X-VBM", "120PCS/120CTNS","$111.2","$13,344.00"],
            ["FIREPLACE MANTEL", "8700-X-CHBW", "109PCS/218CTNS","$154.90","$16,884.10 "],
            ["FIREPLACE MANTEL", "8701-X-CHBW", "110PCS/110CTNS","$154.90","$16,884.10 "]
        ]
    }
    
    processor = OrderPIProcessor(data, "output.xlsx")
    processor.process()
                                
                