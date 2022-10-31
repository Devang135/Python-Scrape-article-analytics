
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
