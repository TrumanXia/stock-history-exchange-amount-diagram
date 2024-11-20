import streamlit as st
import pandas as pd
import json
import plotly.graph_objs as go

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

# 计算指定时间段内的成交量变化
def calculate_volume_change(df, start_minute, end_minute):
    start_volume = df[df['minute'] == start_minute]['volume'].values[0]
    end_volume = df[df['minute'] == end_minute]['volume'].values[0]
    return end_volume - start_volume

# 主应用
def main():
    st.title('成交额图表展示与比较')

    # 加载数据
    data = load_data('data.json')

    # 获取所有日期
    dates = [item['date'] for item in data]

    # 日期选择器
    selected_dates = st.multiselect('选择日期进行比较', dates, default=[dates[0], dates[1]])

    # 创建图表
    fig = go.Figure()

    # 存储每个日期对应的DataFrame
    date_dfs = {}

    # 添加选择的日期的数据到图表
    for selected_date in selected_dates:
        date_data = get_data_by_date(data, selected_date)
        if date_data:
            df = pd.DataFrame(date_data)
            date_dfs[selected_date] = df
            fig.add_trace(go.Scatter(
                x=df['minute'],
                y=df['volume'],
                mode='lines+markers',
                name=selected_date,
                marker=dict(size=10),
                line=dict(width=2),
            ))

    # 设置图表布局
    fig.update_layout(
        title='成交额图表比较',
        xaxis_title='分钟',
        yaxis_title='成交额',
        hovermode='closest',
        yaxis=dict(
            tickformat=',.0f'  # 显示原始值，不进行单位转换
        )
    )

    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

    # 创建时间点选择器
    if fig.data:
        start_minute = st.number_input('选择开始时间点（分钟）', min_value=df['minute'].min(), max_value=df['minute'].max(), value=df['minute'].min())
        end_minute = st.number_input('选择结束时间点（分钟）', min_value=df['minute'].min(), max_value=df['minute'].max(), value=df['minute'].max())

        # 显示每个曲线在指定时间段内的成交量变化
        st.write('指定时间段内的成交量变化：')
        for selected_date in selected_dates:
            df = date_dfs[selected_date]
            if start_minute in df['minute'].values and end_minute in df['minute'].values:
                volume_change = calculate_volume_change(df, start_minute, end_minute)
                st.write(f"{selected_date}: 成交量变化为 {volume_change}")
            else:
                st.write(f"{selected_date}: 选择的时间点不在数据范围内")

if __name__ == '__main__':
    main()