#!/usr/bin/env python
# coding: utf-8

# In[1]:


''' This module is to encrypt text by using "Caesar cipher". This module uses extended ascii letters from string modules. '''


# 1. option to choose file or enter text - done 
# 2. if key is 0 or equivalent take a random key - not required 
# 3. select random key for encryption itself - done 
# 4. file not found break - done
# 5. Issue with \n\r etc - done
# 6. positional parameters 
# 7. brute force
# 8. auto convert to py - done
# 9. if letter not found return same letter - done 
# 10. Unicode support - done 
# 11. command line arguments 
# 12. better file memory management
# 13. Improved questions
# 14. improved file names saved
# 15. save key in a file 
# 16. make a exe

# In[2]:


import chardet
import argparse
import sys
from os import path
from random import randint


# In[3]:


DICT = [chr(letter) for letter in range(sys.maxunicode)]
DICT_LEN = sys.maxunicode


# In[4]:


### Mashup ###
result = list()
for num in range(0,DICT_LEN,25) :
    result += DICT[num:num+25]
DICT = result


# In[5]:


def detect_encoding(file):
    
    with open(file, "rb") as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
    return charenc


# In[6]:


class Encrypt():
    
    ''' This class is a collection of all methods used to encrypt text. ''' 
        
    @staticmethod
    def get_text():
        
        ''' This function is to get the text that is to be encrypted. '''
        text = str(input('Enter the text to be encrypted : '))
        return text
    
    
    @staticmethod    
    def get_text_from_file():
        
        ''' This function is to get the text from a file that is to be encrypted. '''  
        while True:
            file = str(input('''Enter the file with path to be encrypted :  '''))
            file = path.abspath(file)          # Get absolute path 
            charenc = detect_encoding(file)    # Detect encoding
            
            try:
                with open(file,'r', encoding=charenc) as f:
                    f_contents = f.read()
            except FileNotFoundError:
                print('File not found !!! Try again.')
            #except UnicodeDecodeError:
            #    with open(file,'r') as f:
            #        f_contents = f.read()
            #        break
            else:
                break
        
        return f_contents, file
    
                
    
    @staticmethod
    def get_key(en_key=None):
        
        ''' This function is to get key value from user. '''
        ### DICT_KEYS are the map of original letters ###
        DICT_KEYS = dict()
        
        ### Input ###
        if en_key == None:
            while True:
                try:
                    en_key = int(input('Enter the key. Key needs to be a positive or negative number! : '))
                    if type(en_key) == type(float()):
                        raise ValueError
                except ValueError:
                    print(f'Key can only be a positive or negative integer number!')
                else:
                    break
        
        original_key = en_key
        
        ### TURN THE LETTERS ###
        if en_key == 0:       # Key is 0   
           
            DICT_KEYS = { letter:letter for letter in DICT }
        
        else:                      # Key is positive or negative
            
            en_key %= DICT_LEN   #If absolute value of key greater DICT_LEN it will reduce the key else will remain same 
            for index,letter in enumerate(DICT):

                new_index = (en_key  + index) % DICT_LEN   # since new_index will go over dict_len , cycle  
                DICT_KEYS[letter] = DICT[new_index]        # Creates dictionary map

        return DICT_KEYS, original_key, en_key                   
    
    
    @staticmethod
    def encrypt_text(text, dict_keys, original_key, new_key):
        
        ''' This function returns encrypted text. '''
        ### Return mapped letter if present or return letter [ Other than ascii characters ] ###
        return ''.join([ dict_keys[letter] if letter in dict_keys else letter for letter in text ]), original_key, new_key

    
    @staticmethod
    def encrypt_text_to_file(text, file, dict_keys, original_key, new_key):
        
        ''' This function writes encrypted text to file. '''
        new_file = path.splitext(file)[0] +  '.cen'
        ### Return mapped letter if present or return letter [ Other than ascii characters ] ###
        text = ''.join([ dict_keys[letter] if letter in dict_keys else letter for letter in text ])
        with open(new_file,'w', encoding="utf-8") as f:
            f.write(text)
        
        return new_file, original_key, new_key
        

    


# In[7]:


class Decrypt():
    
    ''' This class is a collection of all methods used to encrypt text. ''' 
        
    @staticmethod
    def get_text():
        
        ''' This function is to get the text that is to be decrypted. '''
        text = str(input('Enter the text to be Decrypted : '))
        return text
    
    
    @staticmethod    
    def get_text_from_file():
        
        ''' This function is to get the text from a file that is to be decrypted. ''' 
        while True:
            file = str(input('''Enter the file with path to be decrypted :  '''))
            file = path.abspath(file)
            try:
                with open(file,'r', encoding="utf-8") as f:
                    f_contents = f.read()
            except FileNotFoundError:
                print('File not found !!! Try again.')
            else:   
                return f_contents, file 
                break
    
    
    @staticmethod
    def get_key(key=False):
        
        ''' This function is to get key value from user. '''
        ### DICT_KEYS are the map of original letters ###
        DICT_KEYS = dict()
        
        ### Input ###
        while True:
            try:
                
                if key == False:                     # no cmdline 
                    en_key = int(input('Enter the key. Normal or shortened. : '))
                else:
                    en_key = key 
                if type(en_key) == type(float()):
                    raise ValueError
            except ValueError:
                print(f'Key can only be a positive or negative integer number!')
            else:
                break
        
        original_key = en_key
        
        ### TURN THE LETTERS ###
        if en_key == 0:       # Key is 0   
           
            DICT_KEYS = { letter:letter for letter in DICT }
        
        else:                      # Key is positive or negative
            
            en_key %= DICT_LEN      #If absolute value of key greater DICT_LEN it will reduce the key else will remain same 
            en_key = -(en_key)      #Decrypt means , negative key 
            for index, letter in enumerate(DICT):

                #new_index = abs( index - en_key ) % DICT_LEN   # since new_index will go over dict_len , cycle  
                new_index = (en_key  + index) % DICT_LEN
                DICT_KEYS[letter] = DICT[new_index]            # Creates dictionary map

        
        #print(DICT_KEYS)
        return DICT_KEYS, original_key, abs(en_key)                   
    
    
    @staticmethod
    def decrypt_text(text, dict_keys, original_key, new_key):
        
        ''' This function returns decrypted text. '''
        ### Return mapped letter if present or return letter [ Other than ascii characters ] ###
        return ''.join([ dict_keys[letter] if letter in dict_keys else letter for letter in text ]), original_key, new_key
   
    @staticmethod
    def decrypt_text_to_file(text, file, dict_keys, original_key, new_key):
        
        ''' This function writes decrypted text to file. '''
        new_file = path.splitext(file)[0] + '.cde'
        ### Return mapped letter if present or return letter [ Other than ascii characters ] ###
        text = ''.join([ dict_keys[letter] if letter in dict_keys else letter for letter in text ])
        with open(new_file, 'w', encoding="utf-8") as f:
            f.write(text)
        
        return new_file, original_key, new_key


# In[8]:


def choices():
    
    ''' This function takes in initial user choices. '''
    while True:
        ced = str(input('Encryption or Decryption [E/D] ? : ')).lower() 
        if ced not in {'e','d'}:
            continue
        while True:
            ctf = str(input('Text or File [T/F] ? : ')).lower() 
            if ctf not in {'t','f'}:
                continue
            break
        break
    return ced, ctf


# In[9]:


def key_choice():
    
    ''' This function decides whether user wants to enter a key or not. '''
    while True:
        cyn = str(input('Want to enter a key or select a random key [Y/N] ? :')).lower()
        if cyn not in {'y','n'}:
            continue
        break
    return cyn


# In[10]:


def cmdline():

    
    parser = argparse.ArgumentParser()
    
    ### Interactive mode ###
    parser.add_argument("-i", "--interactive", dest="i", action="store_true", help="Interactive mode") 

    ### Mutually exclusive group of text and file, since both cannot be together ###
    group_tf = parser.add_mutually_exclusive_group()
    group_tf.add_argument("-t", "--text", dest="t", type=str, help="Text input")
    group_tf.add_argument("-f", "--file-path", dest="f", type=str, help="File input")
    
    ### Mutually exclusive group of encrypt and decrypt, since both cannot be together ###
    group_ed = parser.add_mutually_exclusive_group()
    group_ed.add_argument("-e", "--encypt", dest="e", action="store_true", help="Encrypt") 
    group_ed.add_argument("-d", "--decrypt", dest="d", action="store_true", help="Decrypt") 
    
    ### key parameter ###
    parser.add_argument("-k", "--key", dest="k", type=str, default='x', nargs='?', help="Key") #remember to convert key to int 
    
 
    args = parser.parse_args()
    
    

    print(args)
    ### Interactive mode ###
    #if args.i == True:
    #    return 0
    
    ### T or F condition only ###
    if args.t != None or args.f != None:
        if args.e != True and args.d != True:
            print('\n\n')
            parser.error('usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        if args.k == 'x':
            print('\n\n')
            parser.error('usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
            
            
    ### E or F condition only ###
    if args.e == True or args.d == True:
        if args.t == None and args.f == None:
            print('\n\n')
            parser.error('usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        if args.k == 'x':
            print('\n\n')
            parser.error('usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
    
    ### K condition only ###
    if args.k  != 'x':
        if args.e != True and args.d != True:
            print('\n\n')
            parser.error('usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        if args.t == None and args.f == None:
            print('\n\n')
            parser.error('usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        
    return args
    


# In[11]:


def main(ced=None,ctf=None,cyn=None,text=None,file=None,key=False):
    
    ''' This is the main function. This controls enverything. '''
    
 
    ### Welcome ###
    print('Welcome to extended caesar cipher. This utility encrypts text or file using caesar cipher\'s principle.' )
    print('Encryption will take place for ascii characters only.')
    print('Enter either text or file you want to encrypt and a key.')
    print('For multiline input, use the file option.')
    print('Key can be a positive or negative number.')
    print('\n')
    print('Have fun!!!  ¯\_(^^)_/¯ ')
    print('\n\n')
        
    ### Choices ###
    if ced == None and cft == None:     # no cmdline 
        ced, ctf = choices()
        
    if ced == 'e':      ### Encrypt ###
            
        e = Encrypt()
            
        if ctf == 't':      ### Text input ###
            if text == None:         # no cmdline
                text = e.get_text()
            if cyn == None:          # no cmdline
                cyn = key_choice()
    
            
            if cyn =='x':      # cmdline 
                dict_keys, original_key, new_key = e.get_key(en_key=key)   
            elif cyn == 'y':      ### Key input ###
                dict_keys, original_key, new_key = e.get_key()
            else:
                dict_keys, original_key, new_key = e.get_key(en_key=randint(1,99999))
                
                
            result = e.encrypt_text(text, dict_keys, original_key, new_key)      ### Encryption ###
            print('\n\n')
            print(f'''Encrypted text : '{result[0]}' ''')
            print(f'''Key            : '{result[1]}' ''')  
            print(f'''Shortened key  : '{result[2]}' ''')
            
            
        if ctf == 'f':      ### File input ###
            text, file = e.get_text_from_file()
            cyn = key_choice()
            if cyn == 'y':      ### Key input ### 
                dict_keys, original_key, new_key = e.get_key()
            else:
                dict_keys, original_key, new_key = e.get_key(en_key=randint(1,sys.maxunicode))
                    
            result = e.encrypt_text_to_file(text, file, dict_keys, original_key, new_key)
                
            print('\n\n')
            print(f'''Encrypted file : '{result[0]}' ''')
            print(f'''Key            : '{result[1]}' ''')  
            print(f'''Shortened key  : '{result[2]}' ''')
                               
    else:
            
        d = Decrypt()
    
        if ctf == 't':      ### Text input ###
            text = d.get_text()            
            dict_keys, original_key, new_key = d.get_key()
                
            result = d.decrypt_text(text, dict_keys, original_key, new_key)      ### Decryption ###
                
            print('\n\n')
            print(f'''Decrypted text : '{result[0]}' ''')
            print(f'''Key            : '{result[1]}' ''')  
            print(f'''Shortened key  : '{result[2]}' ''')
                
    
        if ctf == 'f':      ### File input ###
            text, file = d.get_text_from_file()
            dict_keys, original_key, new_key = d.get_key()
                    
            result = d.decrypt_text_to_file(text, file, dict_keys, original_key, new_key)
                
            print('\n\n')
            print(f'''Decrypted file : '{result[0]}' ''')
            print(f'''Key            : '{result[1]}' ''')  
            print(f'''Shortened key  : '{result[2]}' ''')

        


# In[12]:


### This is to convert ipynb files to py if run in Jupyter notebook ###
### Also this will cause no problem even if .py file is directly run ###
try :
    terminal = get_ipython().__class__.__name__ 
except Exception:
    pass
else :
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        get_ipython().system('jupyter nbconvert --to script caesar_cmd.ipynb')
        get_ipython().system('pylint caesar_cmd.py')
        get_ipython().system('autopep8 --in-place --aggressive caesar_cmd.py')
        get_ipython().system('pylint caesar_cmd.py  ')
finally :
    if __name__ == "__main__" :
        cmd = cmdline()
        if cmd.i:
            main()
        else:
            
            ### encrypt or decrypt ###
            if cmd.e:
                ced ='e'
            else:
                ced ='d'
            
            ### text or file ###
            if cmd.t != None:
                ctf = 't'
            else:
                ctf = 'f'
            
            ### Key or No key ###
            #if cmd.k == None:
            #    cyn = 'n'
            #else: 
            #    cyn = 'y'
            cyn = 'x'    
                
            
        main(ced,ctf,cyn,cmd.t,cmd.f,cmd.k)
        


# In[ ]:





# In[ ]:




