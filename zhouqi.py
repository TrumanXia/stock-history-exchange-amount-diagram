import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 创建一个周期表的数据结构
elements = {
    1: {'name': 'Hydrogen', 'symbol': 'H', 'atomic_number': 1},
    2: {'name': 'Helium', 'symbol': 'He', 'atomic_number': 2},
    # ... 添加所有元素的数据
}

# 绘制周期表的函数
def draw_periodic_table(elements):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title('Periodic Table')
    ax.set_xticks(range(len(elements)))
    ax.set_yticks(range(len(elements)))
    ax.set_xticklabels([elem['symbol'] for elem in elements.values()], rotation=90)
    ax.set_yticklabels([elem['name'] for elem in elements.values()])
    ax.grid(True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    return fig

# 在Streamlit应用中显示周期表
st.set_option('deprecation.showPyplotGlobalUse', False)
fig = draw_periodic_table(elements)
st.pyplot(fig)