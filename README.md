# code_different_comparision
软件测试与系统保障课设-代码查重 

本项目已部署在 https://routhleck-code-different-comparision-streamlit-app-1s0mx2.streamlit.app/

## 代码结构

- res - 资源目录，用于存放logo图标等
- src - 源代码目录
  - categories.py - 使用pyments将python的代码替换成对应的token，并对每个token的颜色
  - levenshtein.py - 使用numpy计算levenshtein距离(已经使用DiffLib替代)
  - plot.py - plot的创建用于可视化代码token
  - similarity.py - 主要实现block类和相似度计算的实现
  - winnowing.py - 实现winnowing算法
- test_files - 存放测试的.py文件目录
- requirements.txt - 项目环境配置信息
- streamlit_app.py streamlit主程序 
