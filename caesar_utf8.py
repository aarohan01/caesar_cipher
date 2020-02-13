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

# In[2]:


import string
import sys
from os import path
from random import randint


# In[3]:


#DICT = string.printable
DICT = [chr(letter) for letter in range(sys.maxunicode)]
### MASHUP ###
DICT = DICT[::3] + DICT[1::3] + DICT[2::3]
DICT_LEN = sys.maxunicode


# In[4]:


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
            file = path.abspath(file)
            try:
                with open(file,'r', encoding="utf-8") as f:
                    f_contents = f.read()
            except FileNotFoundError:
                print('File not found !!! Try again.')
            except UnicodeDecodeError:
                with open(file,'r') as f:
                    f_contents = f.read()
                    break
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
        

    


# In[5]:


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
    def get_key():
        
        ''' This function is to get key value from user. '''
        ### DICT_KEYS are the map of original letters ###
        DICT_KEYS = dict()
        
        ### Input ###
        while True:
            try:
                en_key = int(input('Enter the key. Normal or shortened. : '))
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


# In[6]:


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


# In[7]:


def key_choice():
    
    ''' This function decides whether user wants to enter a key or not. '''
    while True:
        cyn = str(input('Want to enter a key or select a random key [Y/N] ? :')).lower()
        if cyn not in {'y','n'}:
            continue
        break
    return cyn


# In[8]:


def main():
    
    ''' This is the main function. This controls enverything. '''
    ### Welcome ###
    print('Welcome to extended caesar cipher. This utility encrypts text or file using caesar cipher\'s principle.' )
    print('Encryption will take place for ascii characters only.')
    print('Enter either text or file you want to encrypt and a key.')
    print('For multiline input, use the file option.')
    print('Key can be a positive or negative number.')
    print('\nHave fun!!!  ¯\_(^^)_/¯ \n\n')
    
    ### Choices ###
    ced, ctf = choices()
    if ced == 'e':      ### Encrypt ###
        
        e = Encrypt()
        
        if ctf == 't':      ### Text input ###
            text = e.get_text()
            cyn = key_choice()
            
            if cyn == 'y':      ### Key input ###
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
        


# In[9]:


### This is to convert ipynb files to py if run in Jupyter notebook ###
### Also this will cause no problem even if .py file is directly run ###
try :
    terminal = get_ipython().__class__.__name__ 
except Exception:
    pass
else :
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        get_ipython().system('jupyter nbconvert --to script caesar_cipher.ipynb')
        get_ipython().system('pylint caesar_cipher.py')
        get_ipython().system('autopep8 --in-place --aggressive caesar_cipher.py')
        get_ipython().system('pylint caesar_cipher.py  ')
finally :
    if __name__ == "__main__" :
        main()
        


# In[ ]:





# In[ ]:




