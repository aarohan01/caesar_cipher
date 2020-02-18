# caesar_cipher
Extended version of ceaser cipher that supports ASCII encoded in ASNI, as well as ASCII,UNICODE encoded as UTF-8, UTF-16 LE, UTF-16 BE etc.  
Encrytion and decryption of text as well as file input.  
Key can be explicitly given or randomly selected.  
Encrypted files are generated as .cen .  
Decrypted files will be generated from .cen files to create .cde files.  

Arguments can be passed as both command line or interactively.  


This is just a fun project to implement caesar cipher. As caesar cipher is a primitive and weak cipher, these are not intended for real encryption use cases.  


### Usage :  
Recommended to use notepad to view files since it supports ASCII or Unicode.  
Recommeneded to encrypt or decrypt in file rather than text, as cmd cannot display unicode characters properly.  


Run cmd and go to location of caesar.py  

# Interactive mode ->  
caesar.py  or caesar.py -i   

# Commandline interface ->
Encryption : caesar.py -e -f test.txt -k 10083982  
Decryption : caesar.py -d -f test.cen -k 10083982  

### IMP ###  
Note that after encryption a new file with extension ".cen" will be generated.  
While decryption do not forget to use this file instead of the original.  
After decryption a new file with extension ".cde" will be generated from ".cen"  



