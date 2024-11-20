import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 模拟一些数据
data = {
    'minute': list(range(1, 11)),
    'volume': [120, 130, 135, 145, 150, 160, 170, 180, 190, 200]
}
df = pd.DataFrame(data)

# 创建交互式图表
fig = go.Figure(data=go.Scatter(
    x=df['minute'],
    y=df['volume'],
    mode='lines+markers',
    marker=dict(size=10),
    line=dict(width=2),
))

# 设置图表布局
fig.update_layout(
    title='成交额图表',
    xaxis_title='分钟',
    yaxis_title='成交额',
    hovermode='closest',
)

# 显示图表
st.plotly_chart(fig, use_container_width=True)

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