# 环境安装 
```bash
cd python
# 点击 python-3.8.8-amd64.exe按默认配置进行安装 
cd pip-24.0
python setup.py install

pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com

# 离线安装 
cd ../../
pip install --no-index --find-links=./pkgs -r requirements.txt
```



# 使用方法
pip install --no-index --find-links=./pkgs -r requirements.txt 

1. template存放各个单据的模板，**需要是xlsx格式的excel文件**
2. 数据.xlsx包含4个sheet
   1. 基本信息 第一列填变量名称 第二列填变量值，模板文件里的{{变量名称}}统一会被替换成具体的值
   2. FIREPLACE_MANTEL FIREPLACE_MANTEL产品列表，每一行记录一条实际记录，具体看哪个值需要汇总，之后模板内的{{TOTAL_FIREPLACE_MANTEL}}会被具体值替换
   3. FIREPLACE_MANTEL_TOP 同上一步，之后模板内的{{TOTAL_FIREPLACE_MANTEL_TOP}}会被具体值替换
   4. WOOD_REPAIR_PASTE 同上一步，之后模板内的{{TOTAL_WOOD_REPAIR_PASTE}}会被具体值替换
   5. 客户信息 每一行代表一个客户信息，备用

# 问题
1. 图片为丢失，需要生成后单独添加 安装pillow后就可以保留图片
```python
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

# 加载工作簿
wb = load_workbook('example.xlsx')

# 选择工作表
ws = wb.active

# 创建Image对象
img = Image('picture.png')

# 添加图片到工作表
ws.add_image(img, 'A1')  # 把图片添加到A1单元格的位置

# 保存工作簿
wb.save('example_with_picture.xlsx')
```


# 需要理解
商品列表是明确，一个PI可能是很多个商品的组合 
每个商品包含一个
包数
单价

原来是手工放在一个商品目录处理成单据后，再统一汇总到一个PI里
订单中可能会包含配件，现在阶段用手工输入即可
商品列表可能在下
订单中的会有件数PCS CTNS箱数 PCS*商品包数 = CTNS箱数
Description	Model No.	Quantity	Unit Price	Total Amount
         (FOB Ningbo)	

总价Total Amount = 单价 * 件数

TOTAL AMOUNT	SAY US DOLLARS THIRTY THOUSAND FOUR HUNDRED AND SEVENTY EIGHT CENTS TEN ONLY.			
(In Capital Letters)	  总价人工翻译


1. TERMS OF PAYMENT:  	NO DEPOSIT. T/T WITHIN 21DAYS AFTER SHIPMENT			-- 跟客户讨论方式，两种选择
2. TIME OF SHIPMENT:     	AUG 18TH, 2023			-- 来自于订单，可能来自于
3. PORT OF LOADING:      	NINGBO, CHINA	-- 基本不变，偶尔可能是上海		
4. PORT OF DESTINATION:  	MONTREAL, CANADA			-- 根据订单客户的地址来
5. BENEFICIARY’S BANK:	

   -- 收款信息不变
    Account with institution:  	ZHEJIANG RURAL CREDIT COOPERATIVE UNION, HANGZHOU, CHINA			
   SWIFT BIC:ZJRCCN2N			
   NO.660 QIUTAO ROAD, HANGZHOU, ZHEJIANG PROVINCE,			
   CHINA, 310016			
    Beneficiary: 	NINGBO HARBOR IMPORT & EXPORT CO.,LTD			
    Account Number:      	201000134920721			
   ADDRESS:  BIZHU CHENJIA VILLAGE, XIKOU TOWN, FENGHUA CITY, CHINA			





收到订单

*** 出单据阶段1
确认订单 PI PO#607117 1290 confirmation_20240503
1）单个PI情况 PI PO Date在订单到达时已经明确
   2.1 选择单个出，保留原来的格式
   2.2 PI合并时，可能PI会有几个值，取其中一个值即可，PO都显示空隔开
这一阶段只看PI
关键参数
PI
PO
Date

To
Add
Tex/Fax 根据客户信息来选取进行替换，目前就两个客户，需要维护一个客户列表



商品管理 H.S.Code
客户管理 -- 地址 + 港口，可能会有多种地址 + 港口组合  缩写名称 Marks会在商检CI中用到
订单管理 -- 客户发送来PDF文件，人工转成EXCEL 参考待出壁炉汇总240307_不能发客户.xlsx，不需要的字段留空
收货地址 -- 商检要用 中英文对照
确认订单管理
   1）单个PI情况 PI PO Date在订单到达时已经明确
      2.1 选择单个出，保留原来的格式
      2.2 PI合并时，可能PI会有几个值，取其中一个值即可，PO都显示空隔开
   这一阶段只看PI
   关键参数
   PI
   PO
   Date

   To
   Add
   Tex/Fax 根据客户信息来选取进行替换，目前就两个客户，需要维护一个客户列表
商检报关
   商检 报关 截单
   没有配件的时候，商检和报关一样，配件不需要报关
   商检可多报 报关需要按实际来
   出货清单 商检 报关 截单 -- 如果件数发生变化，前面所有的件数都变更即可
   1、商检和报关单据，在没有配件的情况下，是一模一样的 8700是商品型号，需要汇总
         单价变成了总价/件数，一个虚拟的单价
         有配件时，因为配件不需要商检，报关单据会多一行或多行配件信息
         商检和报关单据需要的主要信息是，品名，件数，箱数，价格，金额，净重，毛重，体积。所以一个品名就报一行，会对所有型号、颜色进行叠加
         可能一个订单报一票，也可能多个订单报一票，主要看货代怎么订的舱。

         这里使用的客户地址通常是指定的仓库地址 -- 地址跟确认阶段不一样，从收货地址里选择
         To: COMBI INC	
         Add: 8530 ERNEST CORMIER	
                  MONTREAL QC H1J1B4, CANADA
         

         CI 和 PL 的NO 和 DATE通常就是制作该单据的日期。假如一天做多套单据，会稍作调整，使得每套不同天不同号

         商检CI 以实际订单处理的日期来
         NO HB{日期}-{客户缩写} Date {日期} -- 默认当前时间，可以编辑
         PI/NO PO
         Issuer 固定不变
         To 中PI 收货地址一样
         Transport Detail
         跟PORT OF LOADING:      	NINGBO, CHINA						
         PORT OF DESTINATION:  	MONTREAL, CANADA 一致
         CI 读金额 H.S.Code 
         PL 读箱数		

         PL 重量和体积 N.W.(KGS)
         N.W.(KGS)		G.W.(KGS)			M.T.(CBM)
         22152.800 		25626.300 			116.442
         
   2. 报关 有配件 需要单加一行
      PI 配件另外加上去 跟着品名走，需要有手动输入的逻辑

   3. 报关单
   提运单号
   OOLU2142409220

   件数
   对应PI里的箱数
   H.S.CODE会根据商品编号出一个个框，规格从商品信息获取

国外清关
PI跟着确认订单时的逻辑走
CI PL的地址需要用实际的收货地址，即跟商检和报关时的一致
CI PL需要加一句话 40 CFR part 770 compliant for formaldehyde

出货清单 跟集装箱走






   # Backup
   2、报关单也可以EXCEL格式，内容主要跟报关单据走的，加入提单号、贸易国、运抵国、指运港、目的国等信息
         一个订单报一票时，合同协议号就时P/I NO., 多个订单报一票时，合同协议号选择一个P/I NO.
      这里的件数指总箱数，毛重指总毛重，净重指总净重

   3、小方格里时申报要素，有配件时，配件单独一行申报，并附上配件的申报要素

   4、出货清单Packing Slip: 需要列清颜色和数量
         这里的客户地址通常为指定的某一个仓库地址



最终的输出单拒

The Seller 放图片
The Buyer  留空，不要了




1. 一个产品一个颜色
变量有10几个，统一加到数据.xlsx中
数据给商检、海关各一份，数据汇总会有不同
柜分两个款式，数量相加，需要有计算公式