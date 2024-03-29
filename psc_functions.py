import re
from itertools import tee

def pwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
def sentence_1st_char_capitalizer(NLP_Dict, input_text):
    output_document = ''
    for sentence in NLP_Dict:
        try:
            sent_start, sent_end = int(sentence[0]['start_char']), int(sentence[-1]['end_char'])
            first_letter = input_text[sent_start]
            output_document += first_letter.upper()
        except IndexError:
            continue
        try:
            rest_of_sent_start = sent_start+1
            rest_of_sent =  input_text[rest_of_sent_start:sent_end]
        except IndexError:
            continue
        try:
            output_document += rest_of_sent
        except IndexError:
            continue
        try:
            if input_text[sent_end] == ' ':
                output_document += ' '
        except IndexError:
            continue
    return output_document
def sentence_2nd_char_capitalizer(NLP_Dict, input_text):
    output_document = ''
    for sentence in NLP_Dict:
        sent_start, first_char_end = int(sentence[0]['start_char']), int(sentence[0]['end_char'])
        first_word = input_text[sent_start:first_char_end]
        try:
            sec_char_start = int(sentence[1]['start_char'])
            rest_of_sent_start = sec_char_start+1
            sent_end = int(sentence[-1]['end_char'])
            sec_char_letter = input_text[sec_char_start]
            rest_of_sent = input_text[rest_of_sent_start:sent_end]
        except IndexError:
            continue
        output_document += first_word
        try: 
            if input_text[first_char_end] == ' ':
                output_document += ' '
        except:
            continue
        if sentence[0]['upos'] == 'PUNCT':
            output_document += sec_char_letter.upper()+rest_of_sent+' '
        else:
            output_document += sec_char_letter+rest_of_sent+' '
    return output_document

List_of_Single_Word_Titles = ['agent', 'brother', 'cantor', 'captain', 'chairperson', 'chancellor', 'chef', 'chief', 'commissioner', 'darth', 'dame', 'dean', 'deputy', 'detective', 'director', 'doctor', 'father', 'governor', 'judge', 'king', 'queen', 'prince', 'princess', 'czar', 'lady', 'laird', 'lieutenant', 'lord', 'madame', 'master', 'miss', 'officer', 'pastor', 'president', 'principal', 'professor', 'provost', 'rabbi', 'rector', 'regent', 'reverend', 'saint', 'sensei', 'sheriff', 'sister', 'student', 'trainer', 'warden']

def Capitalize_Word1(NLP_Dict, input_text):
    # Capitalizing Names of People, organizations, and geopolitical entities
    # Also capitalizing honorable if it precedes 'judge'
    # Also caps titles preceding proper nouns
    output_document = ''
    for sentence in NLP_Dict:
        # sentence_start, sentence_end = sentence[0]['start_char'], sentence[-1]['end_char']
        # trigger_word_seen = False
        last_word_input_text = input_text[int(sentence[-1]['start_char']):int(sentence[-1]['end_char'])]
        for word, next_word in pwise(sentence):
            word_start, word_end = int(word['start_char']), int(word['end_char'])
            next_word_start, next_word_end  = int(next_word['start_char']), int(next_word['end_char'])
            word_input_text, next_word_input_text = input_text[word_start:word_end], input_text[next_word_start:next_word_end]
            space_in_between_words = next_word_start-word_end
            if (word['text'] in List_of_Single_Word_Titles and next_word['upos'] == 'PROPN') or word['xpos'] in ['NNP', 'NNPS'] or (word['text'] in ['honorable', 'Honorable', 'Honourable', 'honourable'] and next_word['text'] in ['judge', 'Judge', 'Judges', 'judges']) or (word['ner'].endswith('GPE') and int(word['end_char'])-int(word['start_char']) > 2) or (word['ner'].endswith('ORG') and int(word['end_char'])-int(word['start_char']) > 3) or (word in ['college', 'university'] and next_word['text'] in ['of']):
                capitalized_word = word_input_text.title()
                output_document += capitalized_word+space_in_between_words*' '
            elif (word['ner'].endswith('GPE') and int(word['end_char'])-int(word['start_char']) == 2) or word['text'] in ['usa', 'Usa', 'USA']:
                output_document += word_input_text.upper()
            else:
                output_document += word_input_text+space_in_between_words*' '
        else:
            word = sentence[-1]
            if word['xpos'] in ['NNP', 'NNPS']:
                capitalized_last_word = last_word_input_text.title()
                try:
                    output_document += capitalized_last_word+space_in_between_words*' '
                except UnboundLocalError:
                    continue
            else:
                output_document += last_word_input_text+' '
    return output_document
def Capitalize_Word2(NLP_Dict, input_text):
    # back capper for pwise couples.
    # uni/college back cappers
    output_document = ''
    for sentence in NLP_Dict:
        first_word_input_text = input_text[int(sentence[0]['start_char']):int(sentence[0]['end_char'])]    
        output_document += first_word_input_text
        for word, next_word in pwise(sentence):
            word_start, word_end = int(word['start_char']), int(word['end_char'])
            next_word_start, next_word_end = int(next_word['start_char']), int(next_word['end_char'])
            word_input_text, next_word_input_text = input_text[word_start:word_end], input_text[next_word_start:next_word_end]
            space_in_between_words = next_word_start-word_end
            if word['upos'] == 'PROPN' and next_word['text'] in ['university', 'college', 'universities', 'colleges']:
                capitalized_word = next_word_input_text.title()
                output_document += (space_in_between_words*' ')+capitalized_word
            else:
                output_document += (space_in_between_words*' ')+next_word_input_text
        else:
            output_document +=' '
    return output_document

def triwise(iterable):
    a, b = tee(iterable)
    a, c = tee(iterable)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)
def quadwise(iterable):
    a, b = tee(iterable)
    a, c = tee(iterable)
    a, d = tee(iterable)
    next(b, None)
    next(c, None)
    next(c, None)
    next(d, None)
    next(d, None)
    next(d, None)
    return zip(a, b, c, d)


def title_quadwise_back_capper(NLP_Dict, input_text):
    output_document = ''
    for sentence in NLP_Dict:
        try:
            output_document += input_text[int(sentence[0]['start_char']):int(sentence[0]['end_char'])]
        except IndexError:
            continue
        try:
            output_document += (int(sentence[1]['start_char'])-int(sentence[0]['end_char']))*' '
        except IndexError:
            continue
        try:
            output_document += input_text[int(sentence[1]['start_char']):int(sentence[1]['end_char'])]
        except IndexError:
            continue
        try:
            output_document += (int(sentence[2]['start_char'])-int(sentence[1]['end_char']))*' '     
        except IndexError:
            output_document += ' '
            continue
        for word1, word2, word3, word4 in quadwise(sentence):
            word3_start, word3_end = int(word3['start_char']), int(word3['end_char'])          
            space_between_word3_word4 = (int(word4['start_char'])-int(word3['end_char']))*' '
            word3_input_text = input_text[word3_start:word3_end]
            if word1['text'] in List_of_Single_Word_Titles and word2['text'] in ['of'] and word3['upos'] in ['PROPN', 'NOUN']:
                output_document += word3_input_text.title()+space_between_word3_word4
            else:
                output_document += word3_input_text+space_between_word3_word4
        else:
            word_last_input_text = input_text[(int(sentence[-1]['start_char'])):(int(sentence[-1]['end_char']))]
            output_document += word_last_input_text+' '
    else:
        output_document += ' '
    return output_document
def title_triwise_front_capper(NLP_Dict, input_text):
    output_document = ''
    for sentence in NLP_Dict:      
        for word1, word2, word3 in triwise(sentence):
            word1_start, word1_end = int(word1['start_char']), int(word1['end_char'])
            word1_location = input_text[word1_start:word1_end]
            space_between_word1_word2 = (int(word2['start_char'])-int(word1['end_char']))*' '
            if word1['text'] in List_of_Single_Word_Titles and word2['text'] in ['of'] and word3['upos'] in ['PROPN', 'NOUN']:
                output_document += word1_location.title()+(space_between_word1_word2)
            else:
                output_document += word1_location+(space_between_word1_word2)
        else:
            try:
                output_document += input_text[int(sentence[-2]['start_char']):int(sentence[-2]['end_char'])]
            except IndexError:
                continue
            try:
                output_document += ((int(sentence[-1]['start_char'])-int(sentence[-2]['end_char']))*' ')
            except IndexError:
                continue
            try:
                output_document += input_text[int(sentence[-1]['start_char']):int(sentence[-1]['end_char'])]+' '
            except IndexError:
                continue
    else:
        output_document += ' '
    return output_document

def Capitalize_Word_Recheck(NLP_Dict, input_text):
    output_document = ''
    for sentence in NLP_Dict:
        last_word_input_text = input_text[int(sentence[-1]['start_char']):int(sentence[-1]['end_char'])]
        for word, next_word in pwise(sentence):
            word_start, word_end = int(word['start_char']), int(word['end_char'])
            next_word_start, next_word_end  = int(next_word['start_char']), int(next_word['end_char'])
            word_input_text, next_word_input_text = input_text[word_start:word_end], input_text[next_word_start:next_word_end]
            space_in_between_words = next_word_start-word_end
            if word['xpos'] in ['NNP', 'NNPS'] and word['text'][0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                capitalized_word = word_input_text.title()
                output_document += capitalized_word+space_in_between_words*' '
            else:
                output_document += word_input_text+space_in_between_words*' '
        else:
            word = sentence[-1]
            if word['xpos'] in ['NNP', 'NNPS']:
                capitalized_last_word = last_word_input_text.title()
                try:
                    output_document += capitalized_last_word+space_in_between_words*' '
                except UnboundLocalError:
                    continue
            else:
                output_document += last_word_input_text+' '
    return output_document

def common_acronym_capitalizer(a):
    return a.group(1) + a.group(2).upper() + a.group(3)
def another_acronym_capitalizer(a):
    return a.group(1) + a.group(2).upper()
def lowercaser2(a):
    return a.group(1) + a.group(2).lower() + a.group(3)
def Title_Caser(a):
    return a.group(1).title()+a.group(2)
def celtic_basic_capitalizer(a):
    return a.group(1) + a.group(2).title() + a.group(3).title()
def basic_capitalizer(a):
    return a.group().title()
def basic_lowercaser(a):
    return a.group().lower()
def mid_capitalizer(a):
    return a.group(1) + a.group(2).title() + a.group(3)
