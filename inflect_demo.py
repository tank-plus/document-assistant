import inflect # type: ignore

def number_to_words(amount):
    p = inflect.engine()
    
    # 分离整数部分和小数部分
    dollars, cents = format(amount,'.2f').split('.')
    # print(f"{dollars}, {cents}")
    
    # 将整数部分转换为英文
    words = p.number_to_words(dollars).upper()
    
    # 处理美元和分的连接逻辑
    # if int(dollars) == 1:
    #     words += " DOLLAR"
    # else:
    #     words += " DOLLARS"
    
    if int(cents) > 0:
        # 将小数部分转换为英文，并且处理单数和复数
        cents_words = p.number_to_words(cents).upper()
        words += " CENTS " + cents_words + " ONLY"
    else:
        words += " ONLY"
        
    return words.replace(",","").replace("-"," ")

# 例子
amount = 30478.22
print(number_to_words(amount))