import streamlit as st
import pandas as pd
import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

        # 创建交互式图表
        fig = go.Figure(data=go.Scatter(
            x=df['minute'],
            y=df['volume'],
            mode='lines+markers',
            name='成交额',
            text=df['volume'],
            marker=dict(size=10),
            line=dict(width=2),
        ))

        # 添加交互式注释
        fig.update_layout(
            title=f'成交额图表 - {selected_date}',
            xaxis_title='分钟',
            yaxis_title='成交额',
            hovermode='closest',
            clickmode='event+select'
        )

        # 显示图表
        selected_points = st.plotly_chart(fig, use_container_width=True)

        # 处理选中的点
        if selected_points:
            if len(selected_points.point_inds) == 2:
                point1 = df.iloc[selected_points.point_inds[0]]
                point2 = df.iloc[selected_points.point_inds[1]]
                diff = point2['volume'] - point1['volume']
                st.write(f"选中两点的成交额差异为: {diff}")

    else:
        st.write('没有找到数据')

if __name__ == '__main__':
    main()