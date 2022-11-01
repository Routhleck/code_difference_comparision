# 用于去除cpp文件中注释和空行的工具类

import logging

logging.basicConfig(level=logging.INFO)


# 判断dictSymbols的key中，最先出现的符号是哪个，并返回其所在位置以及该符号
def get1stSymPos(s, fromPos=0):
    # 清除注释用，对能干扰清除注释的东西，进行判断
    g_DictSymbols = {'"': '"', '/*': '*/', '//': '\n'}
    listPos = []  # 位置,符号
    for b in g_DictSymbols:
        pos = s.find(b, fromPos)
        listPos.append((pos, b))  # 插入位置以及结束符号
    minIndex = -1  # 最小位置在listPos中的索引
    index = 0  # 索引
    while index < len(listPos):
        pos = listPos[index][0]  # 位置
        if minIndex < 0 and pos >= 0:  # 第一个非负位置
            minIndex = index
        if 0 <= pos < listPos[minIndex][0]:  # 后面出现的更靠前的位置
            minIndex = index
        index = index + 1
    if minIndex == -1:  # 没找到
        return (-1, None)
    else:
        return (listPos[minIndex])


# print(get1stSymPos(r'sdjfljkej""/*\'\'\'//\''))
# print(get1stSymPos('adsofiuwioghsdahg*kdhieghkhgkdjhg/'))

# 去掉cpp文件的注释
def rmCommentsInCFile(s):
    # 全局变量，清除注释用，对能干扰清除注释的东西，进行判断
    g_DictSymbols = {'"': '"', '/*': '*/', '//': '\n'}
    if not isinstance(s, str):
        raise TypeError(s)
    fromPos = 0
    while (fromPos < len(s)):
        result = get1stSymPos(s, fromPos)
        logging.info(result)
        if result[0] == -1:  # 没有符号了
            return s
        else:
            endPos = s.find(g_DictSymbols[result[1]], result[0] + len(result[1]))
            if result[1] == '//':  # 单行注释
                if endPos == -1:  # 没有换行符也可以
                    endPos = len(s)
                s = s.replace(s[result[0]:endPos], '', 1)
                fromPos = result[0]
            elif result[1] == '/*':  # 区块注释
                if endPos == -1:  # 没有结束符就报错
                    raise ValueError("块状注释未闭合")
                s = s.replace(s[result[0]:endPos + 2], '', 1)
                fromPos = result[0]
            else:  # 字符串
                if endPos == -1:  # 没有结束符就报错
                    raise ValueError("符号未闭合")
                fromPos = endPos + len(g_DictSymbols[result[1]])
    return s


# 去除程序中的空行
def rm_emptyline(ms):
    if not isinstance(ms, str):
        raise TypeError(ms)
    ms = "".join([s for s in ms.splitlines(True) if s.strip()])
    return ms


# 去除程序中的头文件
def rm_includeline(ms):
    if not isinstance(ms, str):
        raise TypeError(ms)
    ms = "".join([s for s in ms.splitlines(True) if '#include' not in s])
    return ms


if __name__ == '__main__':
    # func_def = open("D:/desktop/t1.c", encoding='utf-8').read()
    # s1 = rmCommentsInCFile(func_def)
    # print(repr(s1))
    ms = '   #include awf   as\n\nfae\nqae\n\n\n\n\nde'
    print(ms)
    ms = rm_emptyline(ms)
    s = rm_includeline(ms)
    print(s)

