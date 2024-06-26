import win32com.client

# 启动Word应用程序
word_app = win32com.client.Dispatch("Word.Application")
word_app.Visible = False  # 设为True可以看到Word应用程序窗口

# 打开指定的Word文档
doc = word_app.Documents.Open(r"D:/宁波好博报关单OOLU214240922.docx")


new_text = "9403910090\n中文品名: 立式壁炉架配件\n用途: 家用\n材质: MDF(密度板)\n规格: 1621x432x120mm\n其它\n"

for i in range(doc.Shapes.Count, 0, -1):
    shape = doc.Shapes(i)
    if shape.Type == 17:  # msoTextBox 类型
       # 打印文本框的名称
        print(f"文本框名称: {shape.Name}")
        # 打印文本框内的内容
        if shape.TextFrame.HasText:
            print(f"文本框内容: {shape.TextFrame.TextRange.Text}")
        
        shape.TextFrame.TextRange.Text = new_text

        # shape.Delete()  # 删除文本框

# 添加新的文本框
left = 50    # 文本框左边距
top = 50     # 文本框上边距
width = 200  # 文本框宽度
height = 100 # 文本框高度
new_textbox = doc.Shapes.AddTextbox(Orientation=1, Left=left, Top=top, Width=width, Height=height)  # Orientation=1 表示水平文本框

# 设置新的文本框的文本内容，包含换行符
new_text = "这是新的文本内容\n带有换行符的第二行\n第三行内容"
new_textbox.TextFrame.TextRange.Text = new_text

# 另存为新文件

doc.SaveAs(r"D:/宁波好博报关单OOLU214240922_new.docx")

# 关闭文档和Word应用程序
doc.Close(False)
word_app.Quit()