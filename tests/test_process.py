from core.processor import OrderPIProcessor


def test_process():
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