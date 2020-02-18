#!/usr/bin/env python
# coding: utf-8

# In[1]:


''' This module is to encrypt text by using "Caesar cipher". This module uses extended ascii letters from string modules. '''


# In[2]:


import sys
from os import path
from random import randint
import chardet
import argparse


# In[3]:


DICT = [chr(letter) for letter in range(sys.maxunicode)]
DICT_LEN = sys.maxunicode


# In[4]:


### Mashup ###
result = list()
for num in range(0, DICT_LEN, 3):
    result += DICT[num:num + 3]
DICT = result


# In[5]:


def detect_encoding(file):
    ''' This function is to detect file encoding. '''
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
    def get_text_from_file(file=None):
        ''' This function is to get the text from a file that is to be encrypted. '''
        while True:

            if file is not None:
                file = path.abspath(file)          # Get absolute path
                if not path.exists(file):
                    print('File not found !!! Try again.')
                    exit()                         # If cmdline path not exist exit
            else:
                file = str(
                    input('''Enter the file with path to be encrypted :  '''))

            file = path.abspath(file)          # Get absolute path
            charenc = detect_encoding(file)    # Detect encoding

            try:
                with open(file, 'r', encoding=charenc) as f:
                    f_contents = f.read()
            except FileNotFoundError:
                print('File not found !!! Try again.')
            # except UnicodeDecodeError:
            #    with open(file,'r') as f:
            #        f_contents = f.read()
            #        break
            else:
                break

        return f_contents, file, charenc

    @staticmethod
    def get_key(en_key=None):
        ''' This function is to get key value from user. '''
        ### DICT_KEYS are the map of original letters ###
        DICT_KEYS = dict()

        ### Input ###
        if en_key is None:
            while True:
                try:
                    en_key = int(
                        input('Enter the key. Key needs to be a positive or negative number! : '))
                    if isinstance(en_key, type(float())):
                        raise ValueError
                except ValueError:
                    print(f'Key can only be a positive or negative integer number!')
                else:
                    break

        original_key = en_key

        ### TURN THE LETTERS ###
        if en_key == 0:       # Key is 0

            DICT_KEYS = {letter: letter for letter in DICT}

        else:                      # Key is positive or negative

            # If absolute value of key greater DICT_LEN it will reduce the key
            # else will remain same
            en_key %= DICT_LEN
            for index, letter in enumerate(DICT):

                # since new_index will go over dict_len , cycle
                new_index = (en_key + index) % DICT_LEN
                # Creates dictionary map
                DICT_KEYS[letter] = DICT[new_index]

        return DICT_KEYS, original_key, en_key

    @staticmethod
    def encrypt_text(text, dict_keys, original_key, new_key):
        ''' This function returns encrypted text. '''
        # Return mapped letter if present or return letter [ Other than ascii
        # characters ] ###
        return ''.join(
            [dict_keys[letter] if letter in dict_keys else letter for letter in text]), original_key, new_key

    @staticmethod
    def encrypt_text_to_file(text, file, dict_keys,
                             original_key, new_key, charenc):
        ''' This function writes encrypted text to file. '''
        new_file = path.splitext(file)[0] + '.cen'
        # Return mapped letter if present or return letter [ Other than ascii
        # characters ] ###
        text = ''.join(
            [dict_keys[letter] if letter in dict_keys else letter for letter in text])
        # with open(new_file,'w', encoding="utf-8") as f:
        with open(new_file, 'w', encoding=charenc) as f:
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
    def get_text_from_file(file=None):
        ''' This function is to get the text from a file that is to be decrypted. '''
        while True:

            if file is not None:
                file = path.abspath(file)          # Get absolute path
                if not path.exists(file):
                    print('File not found !!! Try again.')
                    exit()                         # If cmdline path not exist exit
            else:
                file = str(
                    input('''Enter the file with path to be decrypted :  '''))

            file = path.abspath(file)
            charenc = detect_encoding(file)

            try:
                with open(file, 'r', encoding=charenc) as f:
                    f_contents = f.read()
            except FileNotFoundError:
                print('File not found !!! Try again.')
            else:
                return f_contents, file, charenc
                break

    @staticmethod
    def get_key(en_key=None):
        ''' This function is to get key value from user. '''
        ### DICT_KEYS are the map of original letters ###
        DICT_KEYS = dict()

        ### Input ###
        if en_key is None:
            while True:
                try:
                    en_key = int(
                        input('Enter the key. Normal or shortened. : '))
                    if isinstance(en_key, type(float())):
                        raise ValueError
                except ValueError:
                    print(f'Key can only be a positive or negative integer number!')
                else:
                    break

        original_key = en_key

        ### TURN THE LETTERS ###
        if en_key == 0:       # Key is 0

            DICT_KEYS = {letter: letter for letter in DICT}

        else:                      # Key is positive or negative

            # If absolute value of key greater DICT_LEN it will reduce the key
            # else will remain same
            en_key %= DICT_LEN
            en_key = -(en_key)  # Decrypt means , negative key
            for index, letter in enumerate(DICT):

                # new_index = abs( index - en_key ) % DICT_LEN   # since
                # new_index will go over dict_len , cycle
                new_index = (en_key + index) % DICT_LEN
                # Creates dictionary map
                DICT_KEYS[letter] = DICT[new_index]

        # print(DICT_KEYS)
        return DICT_KEYS, original_key, abs(en_key)

    @staticmethod
    def decrypt_text(text, dict_keys, original_key, new_key):
        ''' This function returns decrypted text. '''
        # Return mapped letter if present or return letter [ Other than ascii
        # characters ] ###
        return ''.join(
            [dict_keys[letter] if letter in dict_keys else letter for letter in text]), original_key, new_key

    @staticmethod
    def decrypt_text_to_file(text, file, dict_keys,
                             original_key, new_key, charenc):
        ''' This function writes decrypted text to file. '''
        new_file = path.splitext(file)[0] + '.cde'
        # Return mapped letter if present or return letter [ Other than ascii
        # characters ] ###
        text = ''.join(
            [dict_keys[letter] if letter in dict_keys else letter for letter in text])
        with open(new_file, 'w', encoding=charenc) as f:
            f.write(text)

        return new_file, original_key, new_key


# In[8]:


def choices():
    ''' This function takes in initial user choices. '''
    while True:
        ced = str(input('Encryption or Decryption ? : [E|D] ')).lower()
        if ced not in {'e', 'd'}:
            continue
        while True:
            ctf = str(input('Text or File input ? : [T|F] ')).lower()
            if ctf not in {'t', 'f'}:
                continue
            break
        break
    return ced, ctf


# In[9]:


def key_choice():
    ''' This function decides whether user wants to enter a key or not. '''
    while True:
        cyn = str(
            input('Want to enter a key or select a random key? : [Y|N] ')).lower()
        if cyn not in {'y', 'n'}:
            continue
        break
    return cyn


# In[10]:


def cmdline():
    ''' This function is to accept command line arguments.'''
    parser = argparse.ArgumentParser()

    ### Interactive mode ###
    parser.add_argument(
        "-i",
        "--interactive",
        dest="i",
        action="store_true",
        help="Interactive mode")

    # Mutually exclusive group of text and file, since both cannot be together
    # ###
    group_tf = parser.add_mutually_exclusive_group()
    group_tf.add_argument(
        "-t",
        "--text",
        dest="t",
        type=str,
        help="Text input")
    group_tf.add_argument(
        "-f",
        "--file-path",
        dest="f",
        type=str,
        help="File input")

    # Mutually exclusive group of encrypt and decrypt, since both cannot be
    # together ###
    group_ed = parser.add_mutually_exclusive_group()
    group_ed.add_argument(
        "-e",
        "--encypt",
        dest="e",
        action="store_true",
        help="Encrypt")
    group_ed.add_argument(
        "-d",
        "--decrypt",
        dest="d",
        action="store_true",
        help="Decrypt")

    ### key parameter ###
    parser.add_argument(
        "-k",
        "--key",
        dest="k",
        type=int,
        default=False,
        nargs='?',
        help="Key")  # remember to convert key to int

    args = parser.parse_args()

    ### Interactive mode ###
    if args.i == True or len(
            sys.argv) <= 1:        # sys.argv is to check number of command line arguments
        return 0

    ### T or F condition only ###
    if args.t is not None or args.f is not None:
        if args.e != True and args.d != True:
            print('\n\n')
            parser.error(
                'usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        if args.k == False:
            print('\n\n')
            parser.error(
                'usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')

    ### E or F condition only ###
    if args.e == True or args.d == True:
        if args.t is None and args.f is None:
            print('\n\n')
            parser.error(
                'usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        if args.k == False:
            print('\n\n')
            parser.error(
                'usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')

    ### K condition only ###
    if args.k or not args.k:
        if args.e != True and args.d != True:
            print('\n\n')
            parser.error(
                'usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')
        if args.t is None and args.f is None:
            print('\n\n')
            parser.error(
                'usage: caesar [-e|-d]  [-t|-f] <TEXT>/<FILE_PATH>  -k <INT>/<EMPTY>')

    return args


# In[11]:


def welcome():
    ''' This funtion is to print welcome message. '''
    ### Welcome ###
    print('Welcome to extended caesar cipher. This utility encrypts text or file using caesar cipher\'s principle.')
    print('Encryption will take place for ascii characters only.')
    print('Enter either text or file you want to encrypt and a key.')
    print('For multiline input, use the file option.')
    print('Key can be a positive or negative number.')
    print('\n')
    print(r'Have fun!!!  ¯\_(^^)_/¯ ')
    print('\n\n')
    print('''Encryption :\n\tInput -> test.txt\n\tOutput -> test.cen\nDecryption :\n\tInput -> test.cen\n\tOutput -> test.cde''')
    print('''\nUse notepad to open text files encrypted or decrypted.''')


# In[12]:


def print_result(result, action, source):
    ''' This function prints the final result output. '''
    print('\n\n')
    print(f'''{action} {source} : '{result[0]}' ''')
    print(f'''Key            : '{result[1]}' ''')
    print(f'''Shortened key  : '{result[2]}' ''')


# In[13]:


def main_cmd(args):
    ''' This is the main function. This controls enverything. '''
    welcome()

    ### Choices ###
    if args.e:  # Encrypt ###

        e = Encrypt()

        if args.t is not None:  # Text input ###
            text = args.t

            if args.k is not None:  # Key input ###
                dict_keys, original_key, new_key = e.get_key(en_key=args.k)
            else:
                dict_keys, original_key, new_key = e.get_key(
                    en_key=randint(1, sys.maxunicode))

            result = e.encrypt_text(
                text,
                dict_keys,
                original_key,
                new_key)  # Encryption ###
            print_result(result, 'Encrypted', 'text')

        if args.f is not None:  # File input ###
            text, file, charenc = e.get_text_from_file(args.f)

            if args.k is not None:  # Key input ###
                dict_keys, original_key, new_key = e.get_key(en_key=args.k)
            else:
                dict_keys, original_key, new_key = e.get_key(
                    en_key=randint(1, sys.maxunicode))

            result = e.encrypt_text_to_file(
                text, file, dict_keys, original_key, new_key, charenc)
            print_result(result, 'Encrypted', 'file')

    else:

        d = Decrypt()

        if args.t is not None:  # Text input ###
            text = args.t
            if args.k is not None:  # Key input ###
                dict_keys, original_key, new_key = d.get_key(en_key=args.k)

            result = d.decrypt_text(
                text,
                dict_keys,
                original_key,
                new_key)  # Decryption ###
            print_result(result, 'Decrypted', 'text')

        if args.f is not None:  # File input ###
            text, file, charenc = d.get_text_from_file(args.f)
            if args.k is not None:
                dict_keys, original_key, new_key = d.get_key(en_key=args.k)

            result = d.decrypt_text_to_file(
                text, file, dict_keys, original_key, new_key, charenc)
            print_result(result, 'Decrypted', 'file')


# In[14]:


def main():
    ''' This is the main function. This controls enverything. '''
    welcome()

    ### Choices ###
    ced, ctf = choices()
    if ced == 'e':  # Encrypt ###

        e = Encrypt()

        if ctf == 't':  # Text input ###
            text = e.get_text()
            cyn = key_choice()

            if cyn == 'y':  # Key input ###
                dict_keys, original_key, new_key = e.get_key()
            else:
                dict_keys, original_key, new_key = e.get_key(
                    en_key=randint(1, 99999))

            result = e.encrypt_text(
                text,
                dict_keys,
                original_key,
                new_key)  # Encryption ###
            print_result(result, 'Encrypted', 'text')

        if ctf == 'f':  # File input ###
            text, file, charenc = e.get_text_from_file()
            cyn = key_choice()
            if cyn == 'y':  # Key input ###
                dict_keys, original_key, new_key = e.get_key()
            else:
                dict_keys, original_key, new_key = e.get_key(
                    en_key=randint(1, sys.maxunicode))

            result = e.encrypt_text_to_file(
                text, file, dict_keys, original_key, new_key, charenc)
            print_result(result, 'Encrypted', 'file')

    else:

        d = Decrypt()

        if ctf == 't':  # Text input ###
            text = d.get_text()
            dict_keys, original_key, new_key = d.get_key()

            result = d.decrypt_text(
                text,
                dict_keys,
                original_key,
                new_key)  # Decryption ###
            print_result(result, 'Decrypted', 'text')

        if ctf == 'f':  # File input ###
            text, file, charenc = d.get_text_from_file()
            dict_keys, original_key, new_key = d.get_key()

            result = d.decrypt_text_to_file(
                text, file, dict_keys, original_key, new_key, charenc)
            print_result(result, 'Decrypted', 'file')


# In[15]:


### This is to convert ipynb files to py if run in Jupyter notebook ###
### Also this will cause no problem even if .py file is directly run ###
try:
    terminal = get_ipython().__class__.__name__
except Exception:
    pass
else:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        get_ipython().system('jupyter nbconvert --to python caesar.ipynb')
        get_ipython().system('pylint caesar.py')
        get_ipython().system('autopep8 --in-place --aggressive caesar.py')
        get_ipython().system('pylint caesar.py  ')
finally:
    if __name__ == "__main__":

        ### Get commandline arguments if any ###
        args = cmdline()

        ### Interactive or Commandline ###
        if args == 0:
            main()
        else:
            main_cmd(args)


# In[ ]:


# In[ ]:
