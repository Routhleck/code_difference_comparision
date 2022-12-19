import streamlit as st
import base64
from io import StringIO
from src.similarity import Code
from src.plot import CodePlot

# renders the logo, so it can be printed 
@st.cache
def renderSvg(svg):
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    html = r'<img id="pygiatorLogo" src="data:image/svg+xml;base64,%s"/>' % b64
    return html

# shows similarity using winnowing algorithm
def winnowing(c1, c2):
    winnowing_expander = st.beta_expander('算法参数设置')
    with winnowing_expander:
        col1, col2 = st.beta_columns(2)
        with col1:
            k_size = st.slider('KGrams大小', 2, 15, 5)
        with col2:
            win_size = st.slider('滑动窗口大小', 2, 15, 4)
        st.write('Winnowing-相似度: **{:.0f}%**'.format(c1.winnowing_similarity(c2, k_size, win_size) * 100))
        st.write("请查看[论文](https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf)以获得更多信息")
        blankLine()

# outputs the heatmaps
def printResult(c1, c2):
    threshold = st.sidebar.slider('选择相似度阈值', 1, 100, 90) / 100
    c1.similarity_threshold = threshold
    c2.similarity_threshold = threshold
    st.write('**{:.0f}%** 的 \'*{}*\' 被认为是抄袭'.format(c1.getSimScore() * 100, c1.name))
    st.write('**{:.0f}%** 的 \'*{}*\' 被认为是抄袭'.format(c2.getSimScore() * 100, c2.name))

    # creates the plot 
    p = CodePlot(c1, c2, threshold) 
    st.plotly_chart(p.fig, use_container_width=True)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def computeCode(f1, f2):
    if None in [f1,f2]:
        return 0,0

    fileOne = f1.read().decode(errors='忽略')
    fileTwo = f2.read().decode(errors='忽略')

    if len(fileOne) == 0 or len(fileTwo) == 0:
        st.error('错误: 文件为空')
        return 0,0

    c1 = Code(fileOne, f1.name)
    c2 = Code(fileTwo, f2.name)
    c1.calculate_similarity(c2) # Calculate similarity
    
    return c1, c2 

def blankLine():
    st.write('')

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
            #pygiatorLogo{{
                width: 70%;
                height: auto;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def run_app():
    st.set_page_config('Pygiator', layout='centered')
    appStyle()

    # sidebar
    file_1 = st.sidebar.file_uploader('第一个文件', key='file1in', type=['py'])
    file_2 = st.sidebar.file_uploader('第二个文件', key='file2in', type=['py'])

    # main page
    st.title('代码查重系统 - Python语言 - 贺思超/陈杰')

    c1, c2 = computeCode(file_1, file_2)

    if 0 not in [c1, c2]: 
        winnowing(c1, c2)
        blankLine()

        printResult(c1, c2)

    else: # home page is printed if no files selected
        a = st.beta_container()
        logo_file = open('./misc/logo.svg', encoding='utf-8')
        logo_data = logo_file.read()
        st.write(renderSvg(logo_data), unsafe_allow_html=True)
        logo_file.close()
        a.write('在左侧栏选择比较的Python源文件')
  
run_app()