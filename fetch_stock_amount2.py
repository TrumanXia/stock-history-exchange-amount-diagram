import requests
import pandas as pd
import json
import schedule
import time
from datetime import datetime
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')
# 尝试读取现有的JSON文件，如果不存在则创建一个空的列表
try:
    with open('data.json', 'r') as f:
        data_storage = json.load(f)
except FileNotFoundError:
    data_storage = []

def fetch_data():
    # 调用API接口
    sz_sh = client.quotes(symbol=["399001", "999999"])
    # 计算总amount
    total_amount = (sz_sh['amount'].iloc[0] + sz_sh['amount'].iloc[1]) // 100000000
    
    # 获取当前时间和日期
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_minute = now.strftime("%H:%M")
    
    # 检查是否需要创建新的日期条目
    date_entry = next((item for item in data_storage if item['date'] == current_date), None)
    if date_entry is None:
        date_entry = {
            "date": current_date,
            "data": []
        }
        data_storage.append(date_entry)
    
    # 添加数据到日期条目
    date_entry['data'].append({
        "minute": current_minute,
        "volume": total_amount
    })

def save_to_json():
    with open('data.json', 'w') as f:
        json.dump(data_storage, f, indent=4)

def job():
    print("执行任务")
    fetch_data()
    print("数据已保存到data.json")
    save_to_json()

# 每分钟执行一次job
schedule.every(1).minutes.do(job)
print("任务已启动")
# 运行调度器
while True:
    schedule.run_pending()
    # time.sleep(1)