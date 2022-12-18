# -*- coding: iso-8859-1 -*-
import sys
# Encoding cookie muss in der ersten oder zweiten Zeile im Modul stehen
# eigentlich Windows cp1252
# ansonsten iso-8859-1-
##de_DE       -->  # -*- coding: iso-8859-1 -*-
##de_DE@euro  -->  # -*- coding: iso-8859-15 -*-
##de_DE.utf8  -->  # -*- coding: utf-8 -*-
#
##de_AT       -->  # -*- coding: iso-8859-1 -*-
##de_AT@euro  -->  # -*- coding: iso-8859-15 -*-
##de_AT.utf8  -->  # -*- coding: utf-8 -*-

# Python verwendet als Basis unicode

# Die Umwandlung nach Unicode wird von decode() und die Umwandlung von
# Unicode in ein anderes Encoding wird von encode() erledigt.

s = "Hallo Welt"
s = "Hallo �sterreich"

s_iso88591 = "Hallo �sterreich"

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

try:
    print (s_utf8)
except:
    print ("Nicht darstellbar...")
