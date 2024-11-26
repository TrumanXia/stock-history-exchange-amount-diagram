import requests
import pandas as pd
import json
import schedule
import time
from datetime import datetime, timedelta
from mootdx.quotes import Quotes
import os


client = Quotes.factory(market="std")
# 尝试读取现有的JSON文件，如果不存在则创建一个空的列表
try:
    with open("data.json", "r") as f:
        data_storage = json.load(f)
except FileNotFoundError:
    data_storage = []

### 获取昨天数据

# 获取今天的日期
today = datetime.now()

# 获取前一天的日期
yesterday = today - timedelta(days=1)
date_to_access = yesterday.strftime("%Y-%m-%d")
today_str = today.strftime("%Y-%m-%d")

# 将数据转换为字典，以日期为键
data_dict = {item["date"]: item["data"] for item in data_storage}
if date_to_access in data_dict:
    # 将每一条数据映射为键值对
    minute_volume_dict_yesterday = {
        entry["minute"]: entry["volume"] for entry in data_dict[date_to_access]
    }
    minute_volume_dict_today = {
        entry["minute"]: entry["volume"] for entry in data_dict[today_str]
    }
    print(f"获取到{date_to_access} 的分钟成交量数据，并做映射")
    print(minute_volume_dict_today)
else:
    print(f"没有找到 {date_to_access} 的数据。")

minute_volume_dict_today = {}


def fetch_data():
    # 调用API接口
    sz_sh = client.quotes(symbol=["399001", "999999"])
    # 计算总amount
    total_amount = (sz_sh["amount"].iloc[0] + sz_sh["amount"].iloc[1]) // 100000000

    # 获取当前时间和日期
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_minute = now.strftime("%H:%M")

    # 检查是否需要创建新的日期条目
    date_entry = next(
        (item for item in data_storage if item["date"] == current_date), None
    )
    if date_entry is None:
        date_entry = {"date": current_date, "data": []}
        data_storage.append(date_entry)

    # 添加数据到日期条目
    date_entry["data"].append({"minute": current_minute, "volume": total_amount})
    print(current_minute + " " + str(total_amount) + "亿")
    minute_volume_dict_today[current_minute] = total_amount
    # 出错后，内存中的数据没有读进来
    # draw_conclusion()


def save_to_json():
    with open("data.json", "w") as f:
        json.dump(data_storage, f, indent=4)


def is_day_break():
    now = datetime.now()
    # 定义时间范围
    start_time = datetime.strptime("11:31:00", "%H:%M:%S").time()
    end_time = datetime.strptime("13:00:00", "%H:%M:%S").time()
    kaipan_time = datetime.strptime("9:29:00", "%H:%M:%S").time()
    shoupan_time = datetime.strptime("15:02:00", "%H:%M:%S").time()
    # 检查当前时间是否在指定范围内
    if (
        now.time() < kaipan_time
        or start_time <= now.time() <= end_time
        or shoupan_time < now.time()
    ):
        print("当前时间不开盘，跳过执行任务。")
        return True


def draw_conclusion():
    start_time_1 = datetime.strptime("9:30:00", "%H:%M:%S").time()
    end_time_1 = datetime.strptime("9:31:00", "%H:%M:%S").time()
    start_time_2 = datetime.strptime("9:36:00", "%H:%M:%S").time()
    end_time_2 = datetime.strptime("9:37:00", "%H:%M:%S").time()
    start_time_3 = datetime.strptime("9:43:00", "%H:%M:%S").time()
    end_time_3 = datetime.strptime("9:44:00", "%H:%M:%S").time()
    start_time_3_1 = datetime.strptime("9:56:00", "%H:%M:%S").time()
    end_time_3_1 = datetime.strptime("9:57:00", "%H:%M:%S").time()
    start_time_4 = datetime.strptime("10:26:00", "%H:%M:%S").time()
    end_time_4 = datetime.strptime("10:27:00", "%H:%M:%S").time()
    start_time_5 = datetime.strptime("11:21:00", "%H:%M:%S").time()
    end_time_5 = datetime.strptime("11:22:00", "%H:%M:%S").time()

    start_time_6 = datetime.strptime("13:06:00", "%H:%M:%S").time()
    end_time_6 = datetime.strptime("13:07:00", "%H:%M:%S").time()
    start_time_7 = datetime.strptime("13:13:00", "%H:%M:%S").time()
    end_time_7 = datetime.strptime("13:14:00", "%H:%M:%S").time()
    start_time_8 = datetime.strptime("13:26:00", "%H:%M:%S").time()
    end_time_8 = datetime.strptime("13:27:00", "%H:%M:%S").time()
    start_time_9 = datetime.strptime("14:51:00", "%H:%M:%S").time()
    end_time_9 = datetime.strptime("14:52:00", "%H:%M:%S").time()
    now = datetime.now()
    flag = 0
    # 下面的if语句可以使用 if elif else 结构来简化代码逻辑
    if start_time_1 < now.time() < end_time_1:
        flag = 1
    if start_time_2 < now.time() < end_time_2:
        flag = 2
    if start_time_3 < now.time() < end_time_3:
        flag = 3
    if start_time_3_1 < now.time() < end_time_3_1:
        flag = 31
    if start_time_4 < now.time() < end_time_4:
        flag = 4
    if start_time_5 < now.time() < end_time_5:
        flag = 5
    if start_time_6 < now.time() < end_time_6:
        flag = 6
    if start_time_7 < now.time() < end_time_7:
        flag = 7
    if start_time_8 < now.time() < end_time_8:
        flag = 8
    if start_time_9 < now.time() < end_time_9:
        flag = 9

    if flag > 0:
        current_date = now.strftime("%Y-%m-%d")
        # 定义文件夹路径和文件名
        folder_path = "conclusions"  # 替换为您的子文件夹名称
        file_name = current_date + ".txt"  # 替换为您想要检查和写入的文件名称
        file_path = os.path.join(folder_path, file_name)

        # 检查文件夹是否存在，如果不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"文件夹 '{folder_path}' 不存在，已创建。")

        # 检查文件是否存在
        if os.path.exists(file_path):
            print(f"文件 '{file_path}' 存在，将向文件追加内容。")
            # 文件存在，以追加模式打开文件
            with open(file_path, "a") as file:
                do_conclusion(file, flag)
        else:
            print(f"文件 '{file_path}' 不存在，已创建并向其中写入内容。")
            # 文件不存在，以写入模式打开文件
            with open(file_path, "w") as file:
                do_conclusion(file, flag)


""" 
区间统计成交量变化
    上午 9:30 开盘 放量 ** 亿
    上午开盘后前 5 分钟 放量 ** 亿 9:36
    上午开盘后前 12 分钟 放量 ** 亿 9:43
    上午开盘后前 25 分钟 放量 ** 亿 9:56
    上午开盘后前 55 分钟 放量 ** 亿 10:26
    上午 10:30 至 11:20 放量 ** 亿 11:21

    下午开盘后前 5 分钟 放量 ** 亿 13:06
    下午开盘后前 12 分钟 放量 ** 亿 13:13
    下午开盘后前 25 分钟 放量 ** 亿 13:26
    
    下午 14:30 至 14:50 放量 ** 亿 14:51
"""


# f" ☝ {change}" if change > 0 else f" ➖ {-change}" 🍎🍏
def do_conclusion(file, flag):
    if flag == 1:
        change = (
            minute_volume_dict_today["09:29"] - minute_volume_dict_yesterday["09:29"]
        )
        file.write(f"上午 9:30 开盘 {rendering(change > 0)} {change} 亿\n")
    if flag == 2:
        change = do_minus("09:35", "09:29")
        file.write(f"上午开盘后前 5 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 3:
        change = do_minus("09:42", "09:29")
        file.write(f"上午开盘后前 12 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 31:
        change = do_minus("09:55", "09:29")
        file.write(f"上午开盘后前 25 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 4:
        change = do_minus("10:25", "09:29")
        file.write(f"上午开盘后前 55 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 5:
        change = do_minus("11:20", "10:29")
        file.write(f"上午 10:30 至 11:20 {rendering(change > 0)} {change} 亿\n")
    if flag == 6:
        change = do_minus("13:05", "13:00")
        file.write(f"下午开盘后前 5 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 7:
        change = do_minus("13:12", "13:00")
        file.write(f"下午开盘后前 12 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 8:
        change = do_minus("13:25", "13:00")
        file.write(f"下午开盘后前 25 分钟 {rendering(change > 0)} {change} 亿\n")
    if flag == 9:
        change = do_minus("14:50", "14:30")
        file.write(f"下午 14:30 至 14:50 {rendering(change > 0)} {change} 亿\n")


def rendering(up):
    return f"🍎" if up else f"🍏"


def do_minus(end_time, start_time):
    change = minute_volume_dict_today[end_time] - minute_volume_dict_today[start_time]
    -(minute_volume_dict_yesterday[end_time] - minute_volume_dict_yesterday[start_time])
    return change


def job():
    if is_day_break():
        return
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
    time.sleep(1)
