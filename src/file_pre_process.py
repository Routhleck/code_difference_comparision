
# 打开文件
def pre_process(src_path):
    # 读取gbk
    with open(src_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 去除注释
    start = []
    end = []
    for i in range(len(lines)):
        if '//' in lines[i]:
            lines[i] = lines[i][:lines[i].index('//')]
        # 对于/*和 */做标注成对处理
        if '/*' in lines[i]:
            start.append(i)
        if '*/' in lines[i]:
            end.append(i)
    # 通过标注的位置，将注释去除
    for i in range(len(start)):
        for j in range(start[i], end[i] + 1):
            lines[j] = ''
    # 去除空行
    lines = [line for line in lines if line.strip() != '']
    # 将lines写入文件
    with open('temp_file/temp.c', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return