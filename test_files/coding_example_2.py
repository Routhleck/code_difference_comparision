import sys

s = "Hallo Welt"
s = "Hallo Österreich"

s_iso88591 = "Hallo Österreich"

# Text nach Unicode umwandeln
s_unicode = b's_iso88591'.decode("iso-8859-1")

# Text nach UTF-8 umwandeln
s_utf8 = s_unicode.encode("utf-8")

print (type(s_iso88591))
print (type(s_unicode))
print (type(s_utf8))

try:
    print (s_iso88591)
except:
    print ("Nicht darstellbar...")

try:
    print (s_unicode)
except:
    print ("Nicht darstellbar...")


