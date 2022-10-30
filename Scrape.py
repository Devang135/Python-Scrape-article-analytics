from cgitb import text
from distutils import extension, text_file
from importlib.resources import path
from re import S
from tkinter.tix import InputOnly
from wsgiref import headers
from numpy import fabs
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


filename='Article Data.txt'                      # file name
f = open(filename,"w",encoding = 'utf-8')        #opening a file


df = pd.read_excel('Input.xlsx')             #reading input file

for idx in df.index:                           #iterating through all file indexes
    link= df['URL'][idx]                       # declaring URL in variable
    driver = webdriver.Chrome()                 #Controls the ChromeDriver and allows you to drive the browser.
    driver.get(link)                            # Loads a web page in the current browser session.
    try:
        headlines= driver.find_element(By.CLASS_NAME, 'entry-category')   # Find an element given a By strategy and locator
        data = driver.find_element(By.CLASS_NAME,'td-post-content')
        print(headlines.text)
        f.write(headlines.text+'\n'+data.text)      #writing file 
                                             #Thrown when a command does not complete in enough time.

        import nltk
        import pandas as pd
        import string

        from regex import F

        with open('articledata.txt', 'r',encoding='utf-8') as fileinput:
            for line in fileinput:
                line = line.rstrip().lower()
                print(line)

        #Cleaning using Stop Words Lists

        import glob
        
        path_dir = 'C:/Users/devan/Desktop/blackdata/stopwords'

        text_file = glob.glob(path_dir+'//*.txt')

        deletelist = []
        for file in text_file:
            with open(file,'r') as f:
                s_text_list = f.readlines()
                deletelist.append(s_text_list)



        with open('removedata_articledata.txt','w+') as fout:
            line_ =[]
            for line_ in f:
                for word in deletelist:
                    line_ = line_.replace(word,'')
                    fout.write(line_)
            fout.close()

    # Assigning Positive and negative Score 

        filename1='outputdata.xlsx'
        
        o = open(filename,'w+',encoding= 'utf-8')
        headers ='URL_ID,URL,POSITIVE SCORE,NEGATIVE SCORE,POLARITY SCORE,SUBJECTIVITY SCORE,AVG SENTENCE LENGTH,PERCENTAGE OF COMPLEX WORDS,FOG INDEX,AVG NUMBER OF WORDS PER SENTENCE,COMPLEX WORD COUNT,WORD COUNT,SYLLABLE PER WORD,PERSONAL PRONOUNS,AVG WORD LENGTH'
        o.write(headers)
        
        from nltk.tokenize import word_tokenize,sent_tokenize

        tokenized_words =[word_tokenize(_idx) for _idx in line ]

        path_dir = 'C:/Users/devan/Desktop/blackdata/MasterDictionary'

        text_p = glob.glob(path_dir+'positive-words.txt')
        text_n = glob.glob(path_dir+'negative-words.txt')

        line1= []
        pos,neg,pol=0,0,0
        for word in text_p:
            with open('positive-words','r') as sc:
                line1 =  sc.readlines()
                
            for line1 in word:
                pos +=1
            sc.close()
        
        for word in text_n:
            with open('positive-words','r') as sc:
                line1 =  sc.readlines()
                
            for line1 in word:
                neg +=1
            sc.close()
        
        pol = (pos-neg)/ ((pos + neg) + 0.000001)
        
        #Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
        #Subjectivity SCore

        sub_score = (pos+neg)/((len(line_))+0.000001)

        #Analysis of Readability
        #Average Sentence Length = the number of words / the number of sentences


        o.close()
        

        #counting words 

        countWord = 0
        for content in line:
            wrd = content.split()
            countWord = countWord+len(wrd)
        count_sente = 0
        #Avg Sentence length
        n_of_sen = sent_tokenize(line)
        count_sente = len(n_of_sen)

        avg_sentence_len=countWord/count_sente

        #complex words

        from nltk.corpus import cmudict
        import syllapy
        counterforsyllablecalls= 0
        d = cmudict.dict()    
        def syllable_count(word):
            try:
                counterforsyllablecalls+=1
                return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]

            except KeyError:
                #if word not found in cmudict
                return syllapy.count(word)

        #calculating Syllables

        syllables_no = syllable_count(word)
        No_of_Complex = 0

        if syllables_no>=2:
            No_of_Complex += 1

        #finding Percentage of Complex words
        percentageofcomplex = No_of_Complex/count_sente

        #fog Index

        fog_index = 0.4*(avg_sentence_len+percentageofcomplex)


        #Average Number of Words Per Sentence

        #Average Number of Words Per Sentence = the total number of words / the total number of sentences
        Avg_no_of_words_per_sent = countWord/count_sente
        
        #complex word count

        Complexwordcount = No_of_Complex

         #Word Count
        No_of_wordcounts = len(tokenized_words)


        #Syllable-Count Per Word
        print(counterforsyllablecalls)

        #PERSONAL PRONOUNS
        import re

        pronounRegex =  re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)  in line_

        #AVG WORD LENGTH
        def totalwords():
            characters = 0 
            for line in line_:
                pass

        from openpyxl import load_workbook
        wb = load_workbook('outputdata.xlsx')
        df = pd.DataFrame({'URL_ID': idx,'URL':link,
                            'POSITIVE SCORE':pos,
                            'NEGATIVE SCORE':neg,
                            'POLARITY SCORE':pol,
                            })
        df.to_excel('outputdata.xlsx',index=False)
        wb.save('outputdata.xslx')


        driver.close()                                #  Closes the current window.
        f.close()                                         #  close the file
    
    except (NoSuchElementException,TimeoutException):     #handling Error
        pass

