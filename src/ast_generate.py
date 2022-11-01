from __future__ import print_function

from pycparser.c_ast import *

from util import rm_emptyline, rm_includeline, rmCommentsInCFile

sys.path.extend(['.', '..'])

from pycparser import c_parser

# 读取c文件程序的内容并去除注释、空行以及头文件，最后生成ast
# 返回内容为处理后的源代码 和 ast
def translate_to_c(filename):
    # 这里展示不用本地编译器的方法
    # 但读取的文本序列，需去除#include #define 以及注释 这类语句才能生成AST
    with open(filename, encoding='gbk') as f:
        txt = f.read()
    txt = rmCommentsInCFile(txt)  # 去除注释
    txt = rm_emptyline(txt)  # 去除空行
    txt = rm_includeline(txt)  # 去除头文件
    # print(txt)
    ast = c_parser.CParser().parse(txt)
    # print(ast)
    return txt, ast


# 直接将 源代码字符串 转变为 ast
# 返回内容为处理后的源代码 和 ast
def translate_to_c_txt(txt):
    txt = rmCommentsInCFile(txt)  # 去除注释
    txt = rm_emptyline(txt)  # 去除空行
    txt = rm_includeline(txt)  # 去除头文件
    # print(txt)
    ast = c_parser.CParser().parse(txt)
    # print(ast)
    return txt, ast


if __name__ == "__main__":
    src_path = r'F:/1GIT/code_different_comparision/test_c_file/9.c'
    txt, ast = translate_to_c(src_path)
    # ast.show()
    # print(ast)
    # 使用N-Gram算法，将ast转化为序列
    