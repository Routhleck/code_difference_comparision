import numpy as np

"""
This implementation is not used for similarity calculation anymore, because of performance reasons.
Difflib's SequenceMatcher returns the same results and is much faster at the same time
Anyway the module is still present to illustrate how to calculate levenshtein distance
"""

# Levenshtein distance using numpy
def lvs_distance(s1, s2):
    x_size = len(s1) + 1
    y_size = len(s2) + 1
    mtx = np.zeros((x_size, y_size))

    # Initialize row/column numbers
    for x in range(x_size):
        mtx [x, 0] = x
    for y in range(y_size):
        mtx [0, y] = y

    # Calculate distance
    for x in range(1, x_size):
        for y in range(1, y_size):

            # Two chars were equal
            if s1[x-1] == s2[y-1]:
                mtx [x,y] = min(
                    mtx[x-1, y] + 1,    # Deletion
                    mtx[x-1, y-1],      # Equals
                    mtx[x, y-1] + 1     # Insertion
                )

            # Two chars were different
            else:
                mtx [x,y] = min(
                    mtx[x-1,y] + 1,     # Deletion
                    mtx[x-1,y-1] + 1,   # Replacement
                    mtx[x,y-1] + 1      # Insertion
                )

    # Right hand side lower corner of matrix holds result 
    return (mtx[x_size - 1, y_size - 1])