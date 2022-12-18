#!/usr/bin/python 
print ("Hallo,") 
print ("Welt!" )

# Calculator
# Complex Numbers
print (1+89765)
print (2**10)
print (100/5)
print (19%3)
print (1j * 1j)  #imaginary numbers are written with a suffix of j or J
print (complex(0,1)) #complex numbers, are always represented as floating point numbers
a = 1.5+0.5j
print (a.real)
print (a.imag)
# I am a comment

# zuletzt verwendetes element
tax = 12.5 / 100
price = 100.50
price * tax
#print price + _ # funktioniert nur in der Konsole
#print round(_,2) # funktioniert nur in der Konsole

# Stringcomparison
# Verhalten von Zeichenketten
word1 = "hello"
word2 = "hallo"
word3 = "hallo"

print (word1==word2)
print (word1 is word2)
print (word2 is word3)
print (word2==word3)

test1 = "Das ist ein verdammt langer String und\n ich moechte ihn nicht einer Zeile anzeigen lassen."
print (test1)

print (""" 
USAGE
Ich moechte diesen Text anzeigen so wie er
da steht
ohne extra auf newlines zu achten
""")

# Typeconversion
# explizite Typumwandlung
s = 'Ich bin ein String'
i = 122345
type(s)
type(i)
print (str(i) + ' ' + s + '!')

print ('%d %s!' % (i, s))


w = 'Skriptsprachen'
print (w[4])
print (w[0:4])
print (w[:2]) # first two characters
print (w[2:]) # everything exapt the first two characters
print (w[:2]+w[2:])
print ("\n")
#selbe mit negativen zahlen
print (w[:-2]) # alles ausser die letzten 2 Buchstaben
print (w[-2:]) # die letzten beiden Buchstaben
print (w[:-2]+w[-2:])

print (w[-0]) # -0 is das selbe wie 0

print (len(w))

#Umlaute
#print "Hööö"






