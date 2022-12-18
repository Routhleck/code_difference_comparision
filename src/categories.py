from pygments import token
from re import search
from operator import itemgetter



# Define single char representation and color of token categories
categories = {
    'Call':         ['A', 'rgb(80, 138, 44)'],
    'Builtin':      ['B', 'rgb(212, 212, 102)'],
    'Comparison':   ['C', 'rgb(176, 176, 176)'],
    'FunctionDef':  ['D', 'rgb(4, 163, 199)'],
    'Function':     ['F', 'rgb(199, 199, 72)'],
    'Indent':       ['I', 'rgb(237, 237, 237)'],
    'Keyword':      ['K', 'rgb(161, 53, 219)'],
    'Linefeed':     ['L', 'rgb(255, 255, 255)'],
    'Namespace':    ['M', 'rgb(232, 232, 209)'],
    'Number':       ['N', 'rgb(192, 237, 145)'],
    'Operator':     ['O', 'rgb(212, 212, 212)'],
    'Punctuation':  ['P', 'rgb(214, 216, 216)'],
    'Pseudo':       ['Q', 'rgb(14, 3, 163)'],
    'String':       ['S', 'rgb(194, 126, 0)'],
    'Variable':     ['V', 'rgb(184, 184, 176)'],
    'WordOp':       ['W', 'rgb(8, 170, 207)'],
    'NamespaceKw':  ['X', 'rgb(161, 53, 219)']
    # Categories left for assignment: EGHJQRTUYZ
}



# Categorize the tokens
def get_category(t):
    category = '' # represent category as single uppercase char

    #print(t) # Print actual pygments token

    if t[0] == token.Keyword.Namespace:
        category = categories['NamespaceKw'][0]
    elif t[0] == token.Name.Namespace:
        category = categories['Namespace'][0]
    elif t[0] == token.Name.Function:
        category = categories['Function'][0]
    elif t[0] == token.Name:
        category = categories['Variable'][0]
    elif t[0] == token.Name.Builtin.Pseudo:
        category = categories['Pseudo'][0]
    elif t[0] == token.Name.Builtin:
        category = categories['Builtin'][0]
    elif t[0] in token.Literal.Number:
        category = categories['Number'][0]
    elif t[0] in token.Literal.String and t[1] not in ['\'', '\"']  and t[0] not in token.Literal.String.Doc:
        category = categories['String'][0]
    elif t[0] == token.Keyword and t[1] == 'def':
        category = categories['FunctionDef'][0]
    elif t[0] == token.Keyword:
        category = categories['Keyword'][0]
    elif t[0] == token.Text and (search(r'\s{2,}\S', t[1]) is not None):
        category = categories['Indent'][0]
    elif t[0] == token.Operator.Word:
        category = categories['WordOp'][0]
    elif t[0] == token.Operator and (t[1] == '==' or t[1] == '!='):
        category = categories['Comparison'][0]
    elif t[0] == token.Punctuation:
        category = categories['Punctuation'][0]
    elif t[0] == token.Operator:
        category = categories['Operator'][0]
    elif t[0] == token.Text and t[1] == '\n':
        category = categories['Linefeed'][0]
    else:
        category = None # Ignore Comments and other tokens

    return category


# Create a cmap for the categories defined
def get_cmap():

    clist = []

    prev_c = [0, "rgb(255, 255, 255)"]

    # Build cmap from categories
    for key in categories:
        clist.append(prev_c)
        clist.append([ord(categories[key][0]), prev_c[1]])
        prev_c = [ord(categories[key][0]), categories[key][1]]

    # Normalize keys of colour representation
    # Needed for plotly
    max_ = max(clist,key=itemgetter(0))[0]
    min_ = min(clist,key=itemgetter(0))[0]
    converted = []
   
    for element in clist:
        converted.append([(element[0] - min_) / (max_ - min_), element[1]])

    # Return cmap for categories
    return converted