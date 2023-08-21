# code_different_comparision

## General Framework of the System

Basic Points:
- res - Resource directory for storing logos and ICONS
- src - Source directory
    - categories.py - Replace python's code with the corresponding token using pyments package, matching the color of each token
    - levenshtein.py - Calculate levenshtein distance using numpy (DiffLib has been used instead)
    - plot.py - The creation of plot is used to visualize code tokens
    - similarity.py - The main implementation of block class and similarity calculation
    - winnowing.py - Implementation of winnowing algorithm
- test_files - The directory where the.py file for the test is stored
- requirements.txt - Project environment configuration information
- streamlit_app.py Main program

## Overall Strategy and Approach

### Similarity Testing Strategy

1. Token block - Block by block comparison:
Use the pygments module to translate the source code from texts to tokens, and Separate tokens into blocks according to newline and indentation. Finally, compare the blocks in code a with the blocks in code b one by one using the difflib module, take the highest score as the similarity of the blocks of code a (between 0 and 1), and calculate the overall similarity of code a If the degree of similarity exceeds the threshold, it will be counted + 1, and the overall similarity is the number of blocks exceeding the threshold divided by the number of all blocks.
The similarity of code b is calculated analogously to the above function.
2. Winnowing algorithm
A fingerprint for an entire source code is created through the combination of a hashing process and a sliding window. A document's fingerprint consists of a set of hash values. The Jaccard coefficient can be used to obtain the similarity between two source codes.
Jaccard coefficient: $J(A,B)=\frac{|A\cap B|}{|A\cup B|}$


### Similarity Test Data

Ten python source code (in test_file folder).

## System Execution Explanation

1. How to translate the source code from texts to tokens:

use the lexer of pygments module 
```python
def __tokenizeFromText(self, text):
    lexer = PythonLexer()
    tokens = lexer.get_tokens(text)
    tokens = list(tokens)
```

2. How to separate tokens into blocks

separate tokens into blocks according to newline and indentation
```python
for token in tokens:
    c = get_category(token)

    if (c is not None):
        # Line feed detection, updates coordinates but does not add result
        if c == 'L':
            row = row + 1
            col = 0

        # New block detected with prev_c \n and not indented
        elif prev_c == 'L' and c != 'I' and result:
            self.blocks.append(Block(result))
            result = []

        # Not a blank line
        if c != 'L':
            # Distinguish between function calls and variables
            if prev_c == 'V' and token[1] == '(':
                result[-1] = 'A', result[-1][1], result[-1][2], result[-1][3]

            result.append((c, row, col, token[1]))
            col += 1
            if col > self._max_col:
                self._max_col = col
    prev_c = c
```
3. How to Visualize Code Diagrams

use the graph_objects of plotly module Display the properties of each block. And Use the streamlit frontend to display the plot.

## User Manual

1.	Open https://routhleck-code-different-comparision-streamlit-app-1s0mx2.streamlit.app/ to enter the home page of our software and you will see the page like this.

![1](1.png)

2.	Then you can choose two files that you need to compare on these two buttons

![2](2.png)

3.	Finally, when the two chosen files gotten successfully, you will see the page like this

![3](3.png)

The marked red area means these column or code module are considered have high similarity ，and when you put your mouse pointer on the marked area,the area will show you the detail information like this.

![4](4.png)

Besides,you can change the KGrams and the size of Sliding window on this panel

![5](5.png)

you also can change the view mode here,the "High similarity blocks " can show you the similarity by token like this.

![6](6.png)

## References:
```
[1] Schleimer S ,  Wilkerson D S ,  Aiken A . Winnowing: Local Algorithms for Document Fingerprinting[C]// Proceedings of the 2003 ACM SIGMOD International Conference on Management of 	Data, San Diego, California, USA, June 9-12, 2003. ACM, 2003.
[2] Hao X ,  Yan H ,  Li Z , et al. BUAA_AntiPlagiarism: A System To Detect Plagiarism for C Source Code[C]// International Conference on Computational Intelligence & Software Engineering. IEEE, 2009.
```
