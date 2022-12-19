import streamlit as st
import base64
from io import StringIO
from src.similarity import Code
from src.plot import CodePlot

# logo渲染方法，将svg转换为base64编码
@st.cache
def renderSvg(svg):
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    html = r'<img id="CodeDCLogo" src="data:image/svg+xml;base64,%s"/>' % b64
    return html

# 展示使用winnowing算法的相似度
def winnowing(c1, c2):
    winnowing_expander = st.beta_expander('算法参数设置')
    with winnowing_expander:
        col1, col2 = st.beta_columns(2)
        with col1:
            k_size = st.slider('KGrams大小', 2, 15, 5)
        with col2:
            win_size = st.slider('滑动窗口大小', 2, 15, 4)
        st.write('Winnowing-相似度: **{:.0f}%**'.format(c1.winnowing_similarity(c2, k_size, win_size) * 100))
        # st.write("请查看[论文](https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf)以获得更多信息")
        blankLine()

# 展示代码热力图
def printResult(c1, c2):
    threshold = st.sidebar.slider('选择相似度阈值', 1, 100, 90) / 100
    plagrism_threshold_high = 90
    plagrism_threshold_medium = 60
    c1.similarity_threshold = threshold
    c2.similarity_threshold = threshold
    if (c1.winnowing_similarity(c2) * 100) > plagrism_threshold_high:
        st.write('\'*{}*\' 的相似度为 **{:.0f}%** 相似度高, 可以认为是抄袭'.format(c1.name, c1.getSimScore() * 100))
    elif (c1.winnowing_similarity(c2) * 100) > plagrism_threshold_medium:
        st.write('\'*{}*\' 的相似度为 **{:.0f}%** 相似度中等, 可以认为不是抄袭'.format(c1.name, c1.getSimScore() * 100))
    else:
        st.write('\'*{}*\' 的相似度为 **{:.0f}%** 相似度低, 可以认为不是抄袭'.format(c1.name, c1.getSimScore() * 100))
    if (c2.winnowing_similarity(c1) * 100) > plagrism_threshold_high:
        st.write('\'*{}*\' 的相似度为 **{:.0f}%** 可以认为是抄袭'.format(c2.name, c2.getSimScore() * 100))
    elif (c2.winnowing_similarity(c1) * 100) > plagrism_threshold_medium:
        st.write('\'*{}*\' 的相似度为 **{:.0f}%** 可以认为不是抄袭'.format(c2.name, c2.getSimScore() * 100))
    else:
        st.write('\'*{}*\' 的相似度为 **{:.0f}%** 可以认为不是抄袭'.format(c2.name, c2.getSimScore() * 100))

    # 展示热力图画布
    p = CodePlot(c1, c2, threshold) 
    st.plotly_chart(p.fig, use_container_width=True)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def computeCode(f1, f2):
    # 若文件为空，则返回0, 0
    if None in [f1,f2]:
        return 0,0

    file1 = f1.read().decode(errors='忽略')
    file2 = f2.read().decode(errors='忽略')

    if len(file1) == 0 or len(file2) == 0:
        st.error('错误: 文件为空')
        return 0,0

    c1 = Code(file1, f1.name)
    c2 = Code(file2, f2.name)
    c1.calculate_similarity(c2) # Calculate similarity
    
    return c1, c2 

def blankLine():
    st.write('')

# css样式
def appStyle():
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: 90%;
                padding-top: 0rem;
                padding-right: 1rem;
                padding-left: 1rem;
                padding-bottom: 1rem;
                margin-left: auto;
                margin-right: auto;
            }}
            .reportview-container .main {{
                color: black;
                background-color: white;
            }}
            #CodeDCLogo{{
                width: 70%;
                height: auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def run_app():
    st.set_page_config('CodeDC', layout='centered')
    appStyle()

    # 左侧边栏上传文件
    file_1 = st.sidebar.file_uploader('第一个文件', key='file1in', type=['py'])
    file_2 = st.sidebar.file_uploader('第二个文件', key='file2in', type=['py'])

    # 主页面
    st.title('代码查重系统 - Python语言 - 贺思超/陈杰')

    c1, c2 = computeCode(file_1, file_2)

    # 若文件不为空，则展示结果
    if 0 not in [c1, c2]: 
        winnowing(c1, c2)
        blankLine()

        printResult(c1, c2)

    # 若没有上传文件，则展示logo
    else:
        a = st.beta_container()
        logo_file = open('res/logo.svg', encoding='utf-8')
        logo_data = logo_file.read()
        st.write(renderSvg(logo_data), unsafe_allow_html=True)
        logo_file.close()
        a.write('在左侧栏选择比较的Python源文件')
  
run_app()