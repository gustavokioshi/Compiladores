from os import sep
import re

#regex ?<=href=["\'])https?://.+?(?=["\'])

f = open("Expressões Regulares/link/input-link.txt", 'r') 
link = f.read()
f.close()
listLink = []
separator = " "

linstLink = re.findall(r'(?<=href=["\'])https?://.+?(?=["\'])',link)
f=open('Expressões Regulares/link/output-link.txt', "w") 
for pos in linstLink:
    f.write(pos)
    f.write('\n')
f.close()