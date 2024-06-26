import os
from datetime import datetime, timedelta, timezone

def list_all_files(directory, suffix=".csv", only_name=True,with_order=True):
    list = []
    csv_files = [file for file in os.listdir(directory) if file.endswith(suffix)]
    
    if with_order:
        csv_files = sorted(csv_files)
        
    if only_name:
        return csv_files
    
    for file in csv_files:
        list.append(os.path.join(directory, file))
    return list
    
    
def current_time():
    # 获取当前UTC时间
    current_utc_time = datetime.now(timezone.utc)

    # 定义目标时区
    shanghai_tz = timezone(timedelta(hours=8))

    # 转换为目标时区的当前时间
    current_shanghai_time = current_utc_time.astimezone(shanghai_tz)

    # 打印指定时区的当前时间
    return current_shanghai_time

def check_non_string_elements(arr):
    for element in arr:
        try:
            # 尝试将元素分别转换为整数、浮点数、布尔型和时间格式
            int(element)
        except ValueError:
            try:
                float(element)
            except ValueError:
                try:
                    bool(element)
                except ValueError:
                    try:
                        datetime.strptime(element, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        continue
            continue
        return True
    return False

# 自定义装饰器
def wrap_response(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return {'code': 200, 'message': 'Success', 'data': data}
    return wrapper