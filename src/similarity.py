from pygments.lexers import PythonLexer
from operator import itemgetter
from src.categories import get_category
from statistics import mean
from difflib import SequenceMatcher
from src.winnowing import winnowing_similarity
import numpy as np

# Hold tokens for a single block within own class instance
class Block(object):
    def __init__(self, tokens, similarity = 0, compared = False):
        self._similarity = similarity
        #self._compared = compared
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


    # OPERATOR OVERLOADS:
    #---------------------------------------------------------------------------
    def __len__(self):
        return len(self.tokens)

    def __str__(self):
        return (''.join(str(t[0]) for t in self.tokens))


    # OBJECTMETHODS:
    #---------------------------------------------------------------------------

    # Compare blocks using tokens
    def compare(self, other):
        # Get similarity comparing two blocks
        if (isinstance(other, Block)):

            # OLD IMPLEMENTATION USING OWN LEVENSHTEIN FUNCTION:
            #-------------------------------------------------------
            #ldis = lvs_distance(str(self),str(other))
            #max_t_len = max(len(str(self)), len(str(other)))
            #s_score = (1 - ldis/max_t_len) #Return similarity score

            # NEW IMPLEMENTATION USING DIFFLIB (much faster with same result!):
            return SequenceMatcher(None,str(self),str(other)).ratio()

    # Compare blocks using raw strings
    def compare_str(self, other):
        if (isinstance(other, Block)):
            return SequenceMatcher(None,self.clnstr(),other.clnstr()).ratio()


    def clnstr(self):
        return (''.join(str(t[3].lower()) for t in self.tokens))

    def max_row(self):
        return max(self.tokens, key=itemgetter(1))[1]

    def max_col(self):
        return max(self.tokens, key=itemgetter(2))[2]

# Represent a files source code as tokens, also implements similarity check
class Code:
    def __init__(self, text, name="", similarity_threshold = 0.9):
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

    # Generate tokens for file
    def __tokenize(self, filename):
        file = open(filename, "r")
        text = file.read()
        file.close()
        self.__tokenizeFromText(text)
        

    def __tokenizeFromText(self, text):
        lexer = PythonLexer() # Using pygments Python Lexer
        tokens = lexer.get_tokens(text)
        tokens = list(tokens) # Convert to tokens to list object
        result = []
        prev_c = '' # Remember previous category
        row = 0     # Remember position of row
        col = 0     # Remember position of column

        # Simplify tokens using categories and add additional coordinates
        for token in tokens:
            c = get_category(token)
            
            if (c is not None):
                # Linefeed detected -> do not append to result but change position
                if c == 'L':
                    row = row + 1 #Increment line position
                    col = 0 # Set back column after linefeed

                # New block detected
                elif prev_c == 'L' and c != 'I' and result:
                    self.blocks.append(Block(result))
                    result = []

                if c != 'L':
                    # Differentiate function calls from variables
                    if prev_c == 'V' and token[1] == '(':
                        result[-1] = 'A', result[-1][1], result[-1][2], result[-1][3]

                    result.append((c, row, col, token[1])) # Append result for single token
                    col += 1 #Increment column position
                    if col > self._max_col:
                        self._max_col = col
            prev_c = c
        self._max_row = row # Set max row for Tokens instance
        
        # Append last block if result not empty
        if result:
            self.blocks.append(Block(result))

    # Return numpy array representation of similarity
    def get_sim_array(self):
        data = np.zeros((self._max_row, self._max_col), dtype=float) #Initialize empty array
        
        for block in self.blocks:
            sim = block.similarity
            for t in block.tokens:
                data[t[1]][t[2]] = sim

        return data

    # Return numpy array representation of clearstrings
    def get_clnstr_array(self):
        data = np.zeros((self._max_row, self._max_col), dtype=object) #Initialize empty array
        
        for block in self.blocks:
            for t in block.tokens:
                data[t[1]][t[2]] = t[3]

        return data

    # Return numpy array representation of categories
    def get_ctg_array(self):
        data = np.zeros((self._max_row, self._max_col), dtype=int) #Initialize empty array
        
        for block in self.blocks:
            for t in block.tokens:
                data[t[1]][t[2]] = ord(t[0])

        return data


    # Set back all block similarities to zero
    def resetSimilarity(self):
        for block in self.blocks:
            block.similarity = 0


    # Find exact matches using stringcompare and annotate
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
            # Only was not compared already
            if block_a.similarity == 0:
                best_score = 0 # Remember the best matching score
                for block_b in other.blocks:
                    if len(block_a) > self._lvs_blocksize:
                        score = block_a.compare(block_b)
                    else:
                        score = block_a.compare_str(block_b)

                    # Set best score if found a better match
                    if score >= best_score:
                        best_score = score

                        # Set the best similarity score for code b as well
                        if block_b.similarity < best_score:
                            block_b.similarity = best_score

                block_a.similarity = best_score

    # Calculate similarity scores for each block (primary calculation method)
    def calculate_similarity(self, other):
        self.resetSimilarity()              # Reset block similarity scores of this code
        other.resetSimilarity()             # Reset block similarity scores of other code
        self.__pre_process(other)           # Do preprocessing step finding exact string matches
        self.__process_similarity(other)    # Compare remaining blocks using levensthein distance on token categories
        other.__process_similarity(self)

    # Calculate total result -> similarity score
    def getSimScore(self):
        total_len = 0
        len_plagiat = 0
        for block in self.blocks:
            total_len += len(block)
            if (block.similarity >= self._similarity_threshold):
                len_plagiat += len(block) * block.similarity
        return len_plagiat/total_len


    # Return winnowing similarity (a second calculation method for similarity score)
    def winnowing_similarity(self, other, size_k = 5, window_size = 4):
        score = winnowing_similarity(str(self), str(other), size_k, window_size)
        return score

    # Return length of code
    def __len__(self):
        # Define length as row count of code
        return self._max_row

    # Return all tokens of code as string
    def __str__(self):
        return "".join(str(x) for x in self.blocks)