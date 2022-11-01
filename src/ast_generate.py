import astpretty
import clang.cindex
from clang.cindex import Index  #主要API
from clang.cindex import Config  #配置
from clang.cindex import CursorKind  #索引结点的类别
from clang.cindex import TypeKind    #节点的语义类别
from file_pre_process import pre_process


libclangPath = r'C:/Program Files/LLVM/bin/libclang.dll'
if Config.loaded:
    print("Config.loaded == True:")
    #pass
else:
    Config.set_library_file(libclangPath)
    print("install path")

def preorder_travers_AST(cursor):
    node_list = []
    for cur in cursor.get_children():
        #do something
        node_list.append(cur.spelling)
        preorder_travers_AST(cur)
    return node_list

def get_ast(src_path):
    pre_process(src_path)
    index = Index.create()
    tu = index.parse('temp_file/temp.c')
    AST_root_node = tu.cursor  # cursor根节点
    node_list = preorder_travers_AST(AST_root_node)
    cursor_content = []
    for token in AST_root_node.get_tokens():
        # 针对一个节点，调用get_tokens的方法。
        cursor_content.append(token.spelling)
    return node_list,cursor_content

src_path = r'F:/1GIT/code_different_comparision/test_c_file/STC8H8K64U_keil_complie/main.c'
ast_test, token = get_ast(src_path)
print(token)
