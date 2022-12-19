from pygments.lexers import PythonLexer
from operator import itemgetter
from src.categories import get_category
from statistics import mean
from difflib import SequenceMatcher
from src.winnowing import winnowing_similarity
import numpy as np


# 为一个block创建tokens
class Block(object):
    def __init__(self, tokens, similarity=0, compared=False):
        self._similarity = similarity
        # self._compared = compared
        self._tokens = tokens

    @property
    def similarity(self):
        return self._similarity

    @similarity.setter
    def similarity(self, s):
        self._similarity = s

    @property
    def tokens(self):
        return self._tokens

    # 运算符重载
    def __len__(self):
        return len(self.tokens)

    def __str__(self):
        return (''.join(str(t[0]) for t in self.tokens))

    # 对象方法:

    # 使用token比较两个block
    def compare(self, other):
        if (isinstance(other, Block)):
            # 使用DIFFLIB计算相似度
            return SequenceMatcher(None, str(self), str(other)).ratio()

    # 使用原始字符串比较两个block
    def compare_str(self, other):
        if (isinstance(other, Block)):
            return SequenceMatcher(None, self.clnstr(), other.clnstr()).ratio()

    def clnstr(self):
        return (''.join(str(t[3].lower()) for t in self.tokens))

    def max_row(self):
        return max(self.tokens, key=itemgetter(1))[1]

    def max_col(self):
        return max(self.tokens, key=itemgetter(2))[2]


# 将源代码用tokens表示，实现相似性比较
class Code:
    def __init__(self, text, name="", similarity_threshold=0.9):
        self._blocks = []
        self._max_row = 0
        self._max_col = 0
        self._name = name
        self._similarity_threshold = similarity_threshold
        self._lvs_blocksize = 8
        self.__tokenizeFromText(text)

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, b):
        self._blocks = b

    @property
    def name(self):
        return self._name

    @property
    def similarity_threshold(self):
        return self._similarity_threshold

    @similarity_threshold.setter
    def similarity_threshold(self, t):
        self._similarity_threshold = t

    # 为源代码文件生成tokens
    def __tokenize(self, filename):
        file = open(filename, "r")
        text = file.read()
        file.close()
        self.__tokenizeFromText(text)

    def __tokenizeFromText(self, text):
        lexer = PythonLexer()  # 使用lexer做词法分析, 判断属于哪种编程语言
        tokens = lexer.get_tokens(text)
        tokens = list(tokens)  # 转化为list
        result = []
        prev_c = ''  # 前一个的类别
        row = 0
        col = 0

        # 使用category简化tokens
        for token in tokens:
            c = get_category(token)

            if (c is not None):
                # 换行检测,更新坐标但不加入result
                if c == 'L':
                    row = row + 1
                    col = 0

                # 检测到新的block, prev_c为\n且不为缩进
                elif prev_c == 'L' and c != 'I' and result:
                    self.blocks.append(Block(result))
                    result = []

                # 不为空行
                if c != 'L':
                    # 区分函数调用和变量
                    if prev_c == 'V' and token[1] == '(':
                        result[-1] = 'A', result[-1][1], result[-1][2], result[-1][3]

                    result.append((c, row, col, token[1]))
                    col += 1
                    if col > self._max_col:
                        self._max_col = col
            prev_c = c
        self._max_row = row  # 依照代码的行数更新最大行数

        # 结果不为空则追加最后一个block
        if result:
            self.blocks.append(Block(result))

    # 返回相似度的numpy数组表示
    def get_sim_array(self):
        data = np.zeros((self._max_row, self._max_col), dtype=float)

        for block in self.blocks:
            sim = block.similarity
            for t in block.tokens:
                data[t[1]][t[2]] = sim

        return data

    # 返回清晰字符串的numpy数组表示
    def get_clnstr_array(self):
        data = np.zeros((self._max_row, self._max_col), dtype=object)

        for block in self.blocks:
            for t in block.tokens:
                data[t[1]][t[2]] = t[3]

        return data

    # 返回category表示的numpy数组
    def get_ctg_array(self):
        data = np.zeros((self._max_row, self._max_col), dtype=int)  # Initialize empty array

        for block in self.blocks:
            for t in block.tokens:
                data[t[1]][t[2]] = ord(t[0])

        return data

    # 重置所有block的相似度
    def resetSimilarity(self):
        for block in self.blocks:
            block.similarity = 0

    # 使用string compare和annotate方法查找能匹配的block
    def __pre_process(self, other):
        other_blocks = other.blocks
        for block_a in self.blocks:
            for block_b in other_blocks:
                if block_a.similarity == 1:
                    break
                if block_a.clnstr() == block_b.clnstr():
                    block_a.similarity = 1.0
                    block_b.similarity = 1.0

    def __process_similarity(self, other):
        for block_a in self.blocks:
            if block_a.similarity == 0:
                best_score = 0  # 记录最佳匹配分数
                for block_b in other.blocks:
                    if len(block_a) > self._lvs_blocksize:
                        score = block_a.compare(block_b)
                    else:
                        score = block_a.compare_str(block_b)

                    # 找到最大的匹配分数
                    if score >= best_score:
                        best_score = score

                        # 也为代码b设置最佳匹配数
                        if block_b.similarity < best_score:
                            block_b.similarity = best_score

                block_a.similarity = best_score

    # 计算每个块的相似度分数（使用levensthein计算方法）
    def calculate_similarity(self, other):
        self.resetSimilarity()
        other.resetSimilarity()
        self.__pre_process(other)
        self.__process_similarity(other)
        other.__process_similarity(self)

    # 返回计算的相似度,为超过相似度阈值的block数除以总block数
    def getSimScore(self):
        total_len = 0
        len_plagiat = 0
        for block in self.blocks:
            total_len += len(block)
            if (block.similarity >= self._similarity_threshold):
                len_plagiat += len(block) * block.similarity
        return len_plagiat / total_len

    # 计算每个块的相似度分数（使用使用winnowing方法）
    def winnowing_similarity(self, other, size_k=5, window_size=4):
        score = winnowing_similarity(str(self), str(other), size_k, window_size)
        return score

    # 返回代码的行数
    def __len__(self):
        # Define length as row count of code
        return self._max_row

    # 返回代码的字符串表示
    def __str__(self):
        return "".join(str(x) for x in self.blocks)
