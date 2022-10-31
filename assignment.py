from cgitb import text
from distutils import extension, text_file
from importlib.resources import path
from re import S
from tkinter.tix import InputOnly
from wsgiref import headers
from numpy import fabs, positive
import pandas as pd
from pyparsing import enable_all_warnings
from requests import delete, head 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from nltk import word_tokenize,sent_tokenize
import pandas as pd
import string
from regex import F
import re


filename='articledata.txt'                      # file name
f = open(filename,"w",encoding = 'utf-8')        #opening a file


df = pd.read_excel('Input.xlsx')             #reading input file

for idx in df.index:                           #iterating through all file indexes
    link= df['URL'][idx]                       # declaring URL in variable
    driver = webdriver.Chrome()                 #Controls the ChromeDriver and allows you to drive the browser.
    driver.get(link)                            # Loads a web page in the current browser session.
    try:
        #headlines= driver.find_element(By.CLASS_NAME, 'entry-category')   # Find an element given a By strategy and locator
        data = driver.find_element(By.CLASS_NAME,'td-post-content')
        #print(headlines.text)
        f.write(data.text)      #writing file 
                                             #Thrown when a command does not complete in enough time.

        with open('articledata.txt', 'r',encoding='utf-8') as fileinput:
            for line in fileinput:
                line = line.rstrip().lower()
                #print(line)
        
        filenames = ['StopWords_Auditor.txt','StopWords_Currencies.txt','StopWords_DatesandNumbers.txt','StopWords_Generic.txt','StopWords_GenericLong.txt','StopWords_Geographic.txt','StopWords_Names.txt']
        #masterdict='negative-words.txt','positive-words.txt'
        
        for filename in filenames:
            with open(filename,'r') as f:
                stop_words = f.read()
            stop_words = stop_words.split('\n')
            print(f'Total number of Stop Words are {len(stop_words)}')

        #positive and negative dictionary files
        with open ('positive-words.txt','r') as p:
            positive_words = p.read()

        
        with open('negative-words.txt','r') as n:
            negative_words =n.read()

        def tokenize(text):
            if not text:
                print('The text to be tokenized is a None type. Defaulting to blank string.')
                text = ' '
            text = re.sub(r'[^A-Za-z]',' ',text.upper())
            tokenized_words = word_tokenize(text)
            return tokenized_words   

        def remove_stopwords(words, stop_words):
            return [x for x in words if x not in stop_words]

        
        def countfunc(store, words):
            score = 0
            for x in words:
                if(x in store):
                    score = score+1
            return score
        def subjectivity(positive_score, negative_score, num_words):
            return (positive_score+negative_score)/(num_words+ 0.000001)
    

        def polarity(positive_score, negative_score):
            return (positive_score - negative_score)/((positive_score + negative_score)+ 0.000001)
        

        def syllable_morethan2(word):
            if(len(word) > 2 and (word[-2:] == 'es' or word[-2:] == 'ed')):
                return False
            
            count =0
            
            vowels = ['a','e','i','o','u']
            for i in word:
                if(i.lower() in vowels):
                    count = count +1
                
            if(count > 2):
                return True
            else:
                return False
        
        def fog_index_cal(average_sentence_length, percentage_complexwords):
            return 0.4*(average_sentence_length + percentage_complexwords)

        # Sentiment Analysis

        #tokenise
        wordstoken = tokenize(data)
        #stopwords removed
        updt_words = remove_stopwords(wordstoken,stop_words)
        #number words
        num_words = len(updt_words)
        #assigning scores
        positive_score = countfunc(positive_words,updt_words)
        negative_score = countfunc(negative_words,updt_words)
        polarity_score = polarity(positive_score ,negative_score)
        subjectivity_score = subjectivity(positive_score, negative_score, num_words)
        
        sentences = sent_tokenize(data)
        num_sentences = len(sentences)
        average_sentence_length = num_words/num_sentences
        
        num_complexword =0

        for word in updt_words:
            if(syllable_morethan2(word)):
                num_complexword = num_complexword+1
        #print(num_complexword)
        percentage_complexwords = num_complexword/num_words

        fog_index = fog_index_cal(average_sentence_length, percentage_complexwords)
        print(fog_index)

        from openpyxl import load_workbook
        wb = load_workbook('outputdata.xlsx')
        df = pd.DataFrame({'URL_ID': idx,'URL':link,
                            'POSITIVE SCORE':positive_score,
                            'NEGATIVE SCORE':negative_score,
                            'POLARITY SCORE':polarity_score,
                            'SUBJECTIVITY SCORE':subjectivity_score,
                            'AVERAGE SENTENCE LENGTH':average_sentence_length,
                            'No. of Complex Words': num_complexword,
                            'percentage_complex':percentage_complexwords,
                            'fog Index':fog_index,
                            })
        df.to_excel('outputdata.xlsx',index=False)
        wb.save('outputdata.xslx')

        driver.close()                          #Closes the current window
        o.close()                           
        f.close() 





    except (NoSuchElementException,TimeoutException,AttributeError):     #handling Error
        pass