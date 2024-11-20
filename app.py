import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# 读取JSON文件
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 根据选择的日期获取数据
def get_data_by_date(data, selected_date):
    for item in data:
        if item['date'] == selected_date:
            return item['data']
    return None

# 主应用
def main():
    st.title('成交额图表展示')

    # 加载数据
    data = load_data('data.json')

    # 获取所有日期
    dates = [item['date'] for item in data]

    # 日期选择器
    selected_date = st.selectbox('选择日期', dates)

    # 获取选择日期的数据
    date_data = get_data_by_date(data, selected_date)

    if date_data:
        # 转换为DataFrame
        df = pd.DataFrame(date_data)

        # 绘制图表
        fig, ax = plt.subplots()
        ax.plot(df['minute'], df['volume'], marker='o')
        ax.set_xlabel('分钟')
        ax.set_ylabel('成交额')
        ax.set_title(f'成交额图表 - {selected_date}')
        st.pyplot(fig)
    else:
        st.write('没有找到数据')

if __name__ == '__main__':
    main()