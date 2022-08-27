from os import sep
import re

#regex [a-zA-Z0-9.]*@[a-zA-Z0-9.]*

f = open("Expressões Regulares/email/input-email.txt", 'r') 
texto = f.read()
f.close()
listEmail = []
separator = " "

email = re.findall(r"((?<=\<)[a-zA-Z0-9.]*@[a-zA-Z0-9.]*(?=\>))",texto)
f=open('Expressões Regulares/email/output-email.txt', "w") 
for pos in email:
    f.write(pos)
    f.write('\n')
f.close()