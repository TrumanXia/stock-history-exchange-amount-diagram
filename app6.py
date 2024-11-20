import streamlit as st
import pandas as pd
import json
import plotly.graph_objs as go
# from streamlit_autorefresh import st_autorefresh

# 设置定时刷新，interval 参数为刷新间隔时间（单位：毫秒），limit 参数为刷新次数上限
# count = st_autorefresh(interval=1000, limit=None, key="fizzbuzzcounter")

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
    st.title('成交额图表展示与比较')

    # 加载数据
    data = load_data('data.json')

    # 获取所有日期
    dates = [item['date'] for item in data]

    # 日期选择器 倒序取最新的两条数据
    selected_dates = st.multiselect('选择日期进行比较', dates, default=[dates[-1], dates[-2]])

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

    # 创建一个下拉菜单来选择曲线
    if fig.data:
        selected_trace = st.selectbox('选择曲线', options=list(range(len(fig.data))), format_func=lambda x: fig.data[x].name)

        # 获取选中曲线的DataFrame
        selected_date = fig.data[selected_trace].name
        df = date_dfs[selected_date]

        # 创建一个下拉菜单来选择点
        selected_index = st.selectbox('选择一个点', options=df.index, format_func=lambda x: f"分钟: {df.loc[x, 'minute']}, 成交额: {df.loc[x, 'volume']}")

        # 显示选中点的信息
        st.write(f"选中的点的信息: 分钟: {df.loc[selected_index, 'minute']}, 成交额: {df.loc[selected_index, 'volume']}")

        # 创建两个按钮来选择两个点
        point1_index = st.button('选择点1')
        point2_index = st.button('选择点2')

        # 使用session_state来存储选中的点
        if 'point1' not in st.session_state:
            st.session_state.point1 = None
        if 'point2' not in st.session_state:
            st.session_state.point2 = None

        if point1_index:
            st.session_state.point1 = df.loc[selected_index]
        if point2_index:
            st.session_state.point2 = df.loc[selected_index]

        # 显示两个选中的点的信息
        if st.session_state.point1 is not None:
            st.write(f"点1: 分钟: {st.session_state.point1['minute']}, 成交额: {st.session_state.point1['volume']}")
        if st.session_state.point2 is not None:
            st.write(f"点2: 分钟: {st.session_state.point2['minute']}, 成交额: {st.session_state.point2['volume']}")

        # 如果两个点都被选中，计算并显示它们之间的差异
        if st.session_state.point1 is not None and st.session_state.point2 is not None:
            diff = st.session_state.point2['volume'] - st.session_state.point1['volume']
            st.write(f"选中两点的成交额差异为: {diff}")

    else:
        st.write('没有找到数据')

if __name__ == '__main__':
    main()