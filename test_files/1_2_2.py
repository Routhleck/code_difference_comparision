
def getComplementarySeq(c):
    if c == 'A':
        k = 'T'
	elif c == 'G':
        k = 'C'
    elif c == 'T':
        k = 'A'
    elif c == 'C':
        k = 'G'
    return k
	

file1 = open("DNA.txt", "r")
for i in file1.readlines():
    if i[0] is not '>':
        print("Sequence\n" + i)
        
        rev = ''
        for c in reversed(i):
            rev = rev + c
        print("\nReversed Sequence\n" + rev)
        
		rkomp = ''
        for c in reversed(i):
            rkomp = rkomp + getComplementarySeq(c)
        print("\nR. k. Sequence\n" + rkomp)
		
        komp = ''
        for c in i:
            komp = komp + getComplementarySeq(c)
        print("\nKomplementaere Sequence\n" + komp)

        
file1.close()
