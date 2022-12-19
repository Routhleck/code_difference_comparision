from plotly.subplots import make_subplots
from src.categories import get_cmap
import plotly.graph_objects as go
import numpy as np


class CodePlot:
    def __init__(self, code_a, code_b, threshold = 0.9):
        self._fig = go.Figure()
        self._code_a = code_a
        self._code_b = code_b
        self._threshold = threshold
        self.__create()

    @property
    def fig(self):
        return self._fig

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, t):
        self._threshold = t # 设置新的阈值

        # 用新的阈值更新cmap
        self._fig.data[2].update(colorscale=self.__overlay_cmap())

    def __overlay_cmap(self):
        return [[0, "rgb(255, 255, 255)"],[self._threshold, "rgb(255, 255, 255)"],
               [self._threshold, "rgb(255, 0, 0)"], [1, "rgb(255, 0, 0)"]]

    def __get_traces(self):
        filename_a = self._code_a.name
        filename_b = self._code_b.name
        data_a = self._code_a.get_ctg_array()
        data_a_sim = self._code_a.get_sim_array()
        data_b_sim = self._code_b.get_sim_array()
        data_b = self._code_b.get_ctg_array()
        labels_a = self._code_a.get_clnstr_array()
        labels_b = self._code_b.get_clnstr_array()

        # code_a的热力图
        trace_a = go.Heatmap(
            z=data_a, text=labels_a, name=filename_a, showscale=False, colorscale=get_cmap(), zmax=ord('X'), zmin=0,
            hovertemplate='Row: %{y}<br>Column: %{x}<br>String: \'%{text}\'<extra></extra>')

        # code_b的热力图
        trace_b = go.Heatmap(
            z=data_b, text=labels_b, name=filename_b, showscale=False, colorscale=get_cmap(), zmax=ord('X'), zmin=0,
            hovertemplate='Row: %{y}<br>Column: %{x}<br>String: \'%{text}\'<extra></extra>')

        # 对于code_a的相似度的热力图，将在code_a中使用滤镜覆盖
        trace_a_sim = go.Heatmap(z=data_a_sim, visible=True, showscale=False, zmax=1.0, zmin=0.0,
                        colorscale=self.__overlay_cmap(), opacity=0.6, hovertemplate='Similarity: %{z}\'<extra></extra>')

        # 对于code_b的相似度的热力图，将在code_b中使用滤镜覆盖
        trace_b_sim = go.Heatmap(z=data_b_sim, visible=True, showscale=False, zmax=1.0, zmin=0.0,
                        colorscale=self.__overlay_cmap(), opacity=0.6, hovertemplate='Similarity: %{z}\'<extra></extra>')

        return[trace_a, trace_b, trace_a_sim, trace_b_sim]


    def __make_subplots(self):
        traces = self.__get_traces()

        # 创建子图以并排显示两个代码
        self._fig = make_subplots(rows=1, cols=2, subplot_titles=[self._code_a.name, self._code_b.name])

        # 将所有热力图添加到子图中
        self._fig.append_trace(traces[0], 1, 1)
        self._fig.append_trace(traces[1], 1, 2)
        self._fig.append_trace(traces[2], 1, 1)
        self._fig.append_trace(traces[3], 1, 2)


    def __update_layout(self):
        # 更改布局以适应代码表示
        self._fig.update_yaxes(title_text="Row", autorange="reversed",
                            mirror=True, ticks='outside', showline=True, linecolor='black')
        self._fig.update_xaxes(title_text="Column",
                            mirror=True, ticks='outside', showline=True, linecolor='black')
        self._fig.update_layout(title_text="Visualized Result", title_font_size=33)

        marginTop = 100
        marginBottom = 10
        plotHeight = max([len(self._code_a), len(self._code_b)]) * 8 + marginTop + marginBottom

        if plotHeight < 600:
            plotHeight = 600

        self._fig.update_layout(height=plotHeight, margin=dict(t=marginTop, b=marginBottom, l=0),
                                width=900, hovermode='x',
                                # Make buttons to hide/unhide similarity overlay
                                updatemenus=[
                                    dict(
                                        type="buttons",
                                        active=0,
                                        showactive=True,
                                        buttons=list([
                                            dict(label="Show similar blocks",
                                                method="restyle",
                                                args=[{"opacity": 0.6}, [2,3]]),
                                            dict(label="Hide similar blocks",
                                                method="restyle",
                                                args=[{"opacity": 0.0}, [2,3]]),
                                        ]),

                                    )
                                ])


    def __create(self):
        self.__make_subplots()
        self.__update_layout()


    # 隐藏相似度热力图
    def hide_overlay(self):
        self._fig.data[2].update(opacity=0.0)