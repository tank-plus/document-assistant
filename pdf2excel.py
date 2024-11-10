import pdfplumber
import pandas as pd
import base64
from PIL import Image
from io import BytesIO

# #显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)

# def image_to_base64(image):
#     buffered = BytesIO()
#     image.save(buffered, format="PNG")  # 保存图像为PNG格式
#     img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
#     return img_base64

# with pdfplumber.open("example.pdf") as pdf:
#     for page in pdf.pages:
#         words = page.extract_words()

#         # 手动分组文本，根据每个单词的坐标，进行行或列上的分组
#         # for word in words:
#         #     print(word['text'], word['x0'], word['top'])  # 输出文本和坐标
            
#         # print(f"------------ Page {page.page_number} has {len(words)} words")
        
#         for i, img_info in enumerate(page.images, start=1):
#             # 裁剪图像
#             x0, top, x1, bottom = img_info["x0"], img_info["top"], img_info["x1"], img_info["bottom"]
#             cropped_image = page.within_bbox((x0, top, x1, bottom)).to_image().original
            
#             # 转换为base64
#             img_base64 = image_to_base64(cropped_image)
#             print(f"Image {i} on Page {page.page_number}: {img_base64}\n")

def save_image(image, filename):
    image.save(filename, format="PNG")  # 保存图像为PNG格式

with pdfplumber.open("example.pdf") as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        for i, img_info in enumerate(page.images, start=1):
            # 获取图片的边界框坐标
            x0, top, x1, bottom = img_info["x0"], img_info["top"], img_info["x1"], img_info["bottom"]
            cropped_image = page.within_bbox((x0, top, x1, bottom)).to_image().original
            
            # 生成文件名并保存
            filename = f"page_{page_number}_image_{i}.png"
            save_image(cropped_image, filename)
            print(f"Saved {filename}")

# # 打开PDF文件
# with pdfplumber.open('example.pdf') as pdf:
#     # 提取第一页中的所有表格
#     first_page = pdf.pages[0]
#     tables = first_page.extract_tables()

# print(tables)

# # 将提取的表格数据转换为DataFrame
# df = pd.DataFrame(tables[2])

# # 打印DataFrame
# print(df)