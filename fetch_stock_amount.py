import requests
import pandas as pd
import json
import schedule
import time
from datetime import datetime
from mootdx.quotes import Quotes
from mootdx import consts
from mootdx.reader import Reader

client = Quotes.factory(market='std')

# 初始化存储数据的列表
data_storage = []
def fetch_data():
    # 调用API接口
    sz = client.quotes(symbol=["399001", "999999"])
    
    # 检查响应状态码是否为200
    # if sz.status_code != 200 or sh.status_code != 200:
    #     print("Failed to get data from one of the APIs")
    #     return

    # 假设API返回的是JSON格式，并且可以直接转换为DataFrame
    # df1 = pd.DataFrame(sz.json())
    # df2 = pd.DataFrame(sh.json())
    
    # 只保留amount字段
    amount1 = sz['amount'].astype('float64').sum()
    amount2 = sh['amount'].astype('float64').sum()
    
    # 计算总amount
    total_amount = amount1 + amount2
    
    # 获取当前时间和日期
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_minute = now.strftime("%H:%M")
    
    # 检查是否需要创建新的日期条目
    if not data_storage or data_storage[-1]['date'] != current_date:
        data_storage.append({
            "date": current_date,
            "data": []
        })
    
    # 添加数据到最新的日期条目
    data_storage[-1]['data'].append({
        "minute": current_minute,
        "volume": total_amount
    })

def save_to_json():
    with open('data.json', 'a') as f:
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