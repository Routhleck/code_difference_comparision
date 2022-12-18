#first of all, the sequence is printed as it is without the header, then the reverse sequence is printed.
#To accomplish this, the list is iterrated backwards and saved in a variable.
#Next the complementary sequence is generated. A is converted to T and vice versa, G is converted to C and vice versa. 
#To get the reversed complementary sequence both steps are combined.
def getKomp(c):
    if c == 'A':
        k = 'T'
    elif c == 'T':
        k = 'A'
    elif c == 'G':
        k = 'C'
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
        
        komp = ''
        for c in i:
            komp = komp + getKomp(c)
        print("\nKomplementaere Sequence\n" + komp)

        rkomp = ''
        for c in reversed(i):
            rkomp = rkomp + getKomp(c)
        print("\nR. k. Sequence\n" + rkomp)
file1.close()
