from time import time
import_start = time()
import stanza, re
from itertools import pairwise, tee, zip_longest
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,ner', verbose=False)
#     # https://stanfordnlp.github.io/stanza/
import_end = time()
input_sentence = input('''
Please enter the text that will be converted: 

''')
time_start = time()
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
sentence_case = str(input_sentence.capitalize())
    # First: Capitalize the first character of every sentence (any character following a period)
    # also, makes the rest of the characters lower case.

try: # Defining some capitalization tools
    def basic_sentence_capitalizer(a):
        return a.group(1) + a.group(2).title()
    def basic_capitalizer(a):
        return a.group(1) + a.group(2).title() + a.group(3)
    def forced_uppercase(a):
        return a.group(1) + a.group(2) + a.group(3).upper()
    def alt_basic_capitalizer(a):
        return a.group(1) + a.group(2) + a.group(3).title()
    def celtic_basic_capitalizer(a):
        return a.group(1) + a.group(2).title() + a.group(3).title()
except: # Literally just putting these in try/except so I can minimize them on VSC.
    pass
try: # Capitalizing a bunch of stuff
    capitalized_initials = re.sub("( )(.)(\. )", basic_capitalizer, sentence_case)
    capitalize_letter_after_period = re.sub("(\. )(.)", basic_sentence_capitalizer, capitalized_initials)
    capitalized_i = re.sub("( )(i)( )", basic_capitalizer, capitalize_letter_after_period)
    title_abbreviations = "dr|mr|ms|mrs|jr|sr|lt|col|sgt|ofc|capt|gen|maj|cpl|pvt|spc|lt col|prof|det|cmd|inv|asst"
    capitalized_title_abbreviations = re.sub(f"( )({title_abbreviations})(\. )", basic_capitalizer, capitalized_i)
    paved_lane_abbreviations = "cir|blvd|rd|st|ave|pl|ln|ct|hwy|fwy"
    capitalized_location_abbreviations = re.sub(f"( )({paved_lane_abbreviations})(\. )", basic_capitalizer, capitalized_title_abbreviations)
    capitalized_spoken_sentences = re.sub("(, )(“|\")(.)", alt_basic_capitalizer, capitalized_location_abbreviations)
    capitalize_letter_after_punct_quotes = re.sub("(\.|\?|\!)(” |\" )(.)", alt_basic_capitalizer, capitalized_spoken_sentences)
    capitalized_i_contractions = re.sub(f"( )(i)('|')", basic_capitalizer, capitalize_letter_after_punct_quotes)
    capitalized_letter_following_quotation = re.sub(f"( )(\")(.)", forced_uppercase, capitalized_i_contractions)
    capitalized_US = re.sub("(the |The)(united states)", basic_capitalizer, capitalized_letter_following_quotation)
except: # Literally just putting these in try/except so I can minimize them on VSC.
    pass
base_text = capitalized_letter_following_quotation

# # ====================================================================================================================
nlp_doc = nlp(base_text)            # FIRST TIME USING STANZA FOR ANNOTATION
# # ====================================================================================================================
dic_nlp_doc = nlp_doc.to_dict()     # CONVERT OUTPUT DATA STRUCTURE TO [LIST[LIST{DICT}]]
NLP_base_text = nlp_doc.text

# compare location of text in NLP to the location in the original text using start/end char markers
# change the original text based on the NLP annotation, creating a new value each time 
# has the benefit of retaining the original spacing!!!

def NNP_capitalizer(input_text):
    output_document = ''
    for sentence in dic_nlp_doc:
        for word in sentence:
            word_start = int(word['start_char'])
            word_end = int(word['end_char'])
            word_location = input_text[word_start:word_end]
            if word['xpos'] in ['NNP', 'NNPS']:
                output_document += word_location.title()
                try:
                    if input_text[word_end] == ' ':
                        output_document += ' '
                except IndexError:
                    continue
            else:
                output_document += word_location
                try: 
                    if input_text[word_end] == ' ':
                        output_document += ' '
                except IndexError:
                    continue
    return output_document
def sentence_1st_char_capitalizer(input_text):
    output_document = ''
    for sentence in dic_nlp_doc:
        sent_start = int(sentence[0]['start_char'])
        rest_of_sent_start = sent_start+1
        sent_end = int(sentence[-1]['end_char'])
        first_letter = input_text[sent_start]
        rest_of_sent = input_text[rest_of_sent_start:sent_end]
        output_document += first_letter.upper()+rest_of_sent
        try:
            if input_text[sent_end] == ' ':
                output_document += ' '
        except IndexError:
            continue
    return output_document
def sentence_2nd_char_capitalizer(input_text):
    output_document = ''
    for sentence in dic_nlp_doc:
        sent_start = int(sentence[0]['start_char'])
        first_char_end = int(sentence[0]['end_char'])
        first_word = input_text[sent_start:first_char_end]
        sec_char_start = int(sentence[1]['start_char'])
        rest_of_sent_start = sec_char_start+1
        sent_end = int(sentence[-1]['end_char'])
        # sent_location = input_text[sent_start:sent_end]
        sec_char_letter = input_text[sec_char_start]
        rest_of_sent = input_text[rest_of_sent_start:sent_end]
        output_document += first_word
        try: 
            if input_text[first_char_end] == ' ':
                output_document += ' '
        except:
            continue
        if sentence[0]['upos'] == 'PUNCT':
            output_document += sec_char_letter.upper()+rest_of_sent
            try:
                if input_text[sent_end] == ' ':
                    output_document += ' '
            except IndexError:
                continue
        else:
            output_document += sec_char_letter+rest_of_sent
            try:
                if input_text[sent_end] == ' ':
                    output_document += ' '
            except IndexError:
                continue
    return output_document

NNPs_capped = NNP_capitalizer(NLP_base_text)
capitalize_celtic = re.sub("( )(Mc|Mac|O\' )(...)", celtic_basic_capitalizer, NNPs_capped)
Sents_1st_capped = sentence_1st_char_capitalizer(capitalize_celtic)
Sents_2nd_capped = sentence_2nd_char_capitalizer(Sents_1st_capped)

# # ====================================================================================================================
nlp_doc2 = nlp(Sents_2nd_capped)    # 2ND TIME USING STANZA, THIS TIME FOR (BETTER) NAMED ENTITY RECOGNITION
# # ====================================================================================================================
NLP_entities = nlp_doc2.to_dict()   # CONVERT OUTPUT DATA STRUCTURE TO [LIST[LIST{DICT}]]

def GPE_ORG_Capitalizer(input_text):
    output_document = ''
    for sentence in NLP_entities:
        for word in sentence:
            word_start = int(word['start_char'])
            word_end = int(word['end_char'])
            word_location = input_text[word_start:word_end]
            if (word['ner'].endswith('GPE') and int(word['end_char'])-int(word['start_char']) == 2) or word['text'] in ['usa', 'Usa', 'USA']:
                output_document += word_location.upper()
                try:
                    if input_text[word_end] == ' ':
                        output_document += ' '
                except IndexError:
                    continue
            elif word['ner'].endswith('GPE') and int(word['end_char'])-int(word['start_char']) > 2:
                output_document += word_location.title()
                try:
                    if input_text[word_end] == ' ':
                        output_document += ' '
                except IndexError:
                    continue
            elif word['ner'].endswith('ORG') and int(word['end_char'])-int(word['start_char']) > 3:
                output_document += word_location.title()
                try:
                    if input_text[word_end] == ' ':
                        output_document += ' '
                except IndexError:
                    continue
            else:
                output_document += word_location
                try:
                    if input_text[word_end] == ' ':
                        output_document += ' '
                except IndexError:
                    continue
    return output_document
GPE_ORG_capped = GPE_ORG_Capitalizer(Sents_2nd_capped)
def uni_college_back_capper(input_text):
    output_document = ''
    for sentence in NLP_entities:
        output_document += sentence[0]['text']
        if input_text[int(sentence[0]['end_char'])] == ' ':
            output_document += ' '
        for this_word, next_word in pairwise(sentence):
            next_word_start = int(next_word['start_char'])
            next_word_end = int(next_word['end_char'])
            next_word_location = input_text[next_word_start:next_word_end]
            list_of_uni_types = ['college', 'university']
            if this_word['upos'] == 'PROPN' and next_word['text'] in list_of_uni_types:
                output_document += next_word_location.title()
                if input_text[next_word_end] == ' ':
                    output_document += ' '
            else:
                output_document += next_word_location
                if input_text[next_word_end] == ' ':
                    output_document += ' '
    return output_document
def uni_college_front_capper(input_text):
    output_document = ''
    for sentence in NLP_entities:
        for this_word, next_word in pairwise(sentence):
            this_word_start = int(this_word['start_char'])
            this_word_end = int(this_word['end_char'])
            word_location = input_text[this_word_start:this_word_end]
            list_of_uni_types = ['college', 'university']
            if this_word['text'] in list_of_uni_types and next_word['text'] in ['of']:
                output_document += word_location.title()
                if input_text[this_word_end] == ' ':
                    output_document += ' '
            else:
                output_document += word_location
                if input_text[this_word_end] == ' ':
                    output_document += ' '
        else:
            output_document += sentence[-1]['text']+' '
    return output_document

try: # Defining some capitalization tools
    def common_acronym_capitalizer(a):
        return a.group(1) + a.group(2).upper() + a.group(3)
    def another_acronym_capitalizer(a):
        return a.group(1) + a.group(2).upper()
    def lowercaser2(a):
        return a.group(1) + a.group(2).lower() + a.group(3)
    def Title_Caser(a):
        return a.group(1).title()+a.group(2)
except: # Literally just putting these in try/except so I can minimize them.
    pass

try: # More Capitalization Stuff
    common_acronyms = "usa|omg|rsvp|asap|lmk|brb|dob|tba|tbd|eta|tgif|fomo|imo|n/a|aka|ner|diy|fyi|faq|atm|id|iq|gmo|nlp|pc|pr|hr|awol|ce|bce|ocd|md|byob|og|yolo|captcha|madd|ikea|geico|fifa|nasdaq|"
    Draft1_acronyms_capped = re.sub(f"( )({common_acronyms})( |\/|\.|\?)", common_acronym_capitalizer, GPE_ORG_capped, flags=re.IGNORECASE)
    Draft1_2_dot_acronyms_capped = re.sub(f"( )(.\..\.)", another_acronym_capitalizer, Draft1_acronyms_capped, flags=re.IGNORECASE)
    Draft1_3_dot_acronyms_capped = re.sub(f"( )(.\..\..\.)", another_acronym_capitalizer, Draft1_2_dot_acronyms_capped, flags=re.IGNORECASE)
    Draft1_lowercase_domains = re.sub(f"(\.)(com|net|org|co|us|ru|ir|in|uk|au|de|ua|gov)( |\/|\.|\?)", lowercaser2, Draft1_3_dot_acronyms_capped, flags=re.IGNORECASE)
    Draft1_lowercase_of_the = re.sub(f"( )(of the|of)( )", lowercaser2, Draft1_lowercase_domains, flags=re.IGNORECASE)
except: # Literally just putting these in try/except so I can minimize them on VSC.
    print('Uh oh, this isn\'t supposed to be here. Check the second pass of capitalization stuff around line 190.')
List_of_Single_Word_Titles = ['agent', 'brother', 'cantor', 'captain', 'chairperson', 'chancellor', 'chef', 'chief', 'commissioner', 'dame', 'dean', 'deputy', 'detective', 'director', 'doctor', 'father', 'governor', 'judge', 'king', 'queen', 'prince', 'princess', 'czar', 'lady', 'laird', 'lieutenant', 'lord', 'madame', 'master', 'miss', 'officer', 'pastor', 'president', 'principal', 'professor', 'provost', 'rabbi', 'rector', 'regent', 'reverend', 'sensei', 'sheriff', 'sister', 'student', 'trainer', 'warden']

def Honorable_Judger(input_text):
    output_document = ''
    for sentence in NLP_entities:
        for this_word, next_word in pairwise(sentence):
            this_word_start = int(this_word['start_char'])
            this_word_end = int(this_word['end_char'])
            word_location = input_text[this_word_start:this_word_end]
            if this_word['text'] in ['honorable', 'Honorable', 'Honourable', 'honourable'] and next_word['text'] in ['judge', 'Judge', 'Judges', 'judges']:
                output_document += word_location.title()
                if input_text[this_word_end] == ' ':
                    output_document += ' '
            else:
                output_document += word_location
                if input_text[this_word_end] == ' ':
                    output_document += ' '
        else:
            output_document += sentence[-1]['text']+' '
    return output_document

def triwise(iterable):
    a, b = tee(iterable)
    a, c = tee(iterable)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)
def title_triwise_back_capper(input_text):
    output_document = ''
    for sentence in NLP_entities:
        output_document += sentence[0]['text']
        if input_text[int(sentence[0]['end_char'])] == ' ':
            output_document += ' '
        output_document += sentence[1]['text']
        if input_text[int(sentence[1]['end_char'])] == ' ':
            output_document += ' '        
        for word1, word2, word3 in triwise(sentence):
            word3_start = int(word3['start_char'])
            word3_end = int(word3['end_char'])
            word3_location = input_text[word3_start:word3_end]
            if word1['text'] in List_of_Single_Word_Titles and word2['text'] in ['of', 'the'] and word3['upos'] in ['PROPN', 'NOUN']:
                output_document += word3_location.title()
                if input_text[word3_end] == ' ':
                    output_document += ' '
            else:
                output_document += word3_location
                if input_text[word3_end] == ' ':
                    output_document += ' '
    return output_document
def title_triwise_front_capper(input_text):
    output_document = ''
    for sentence in NLP_entities:      
        for word1, word2, word3 in triwise(sentence):
            word1_start = int(word1['start_char'])
            word1_end = int(word1['end_char'])
            word1_location = input_text[word1_start:word1_end]
            if word1['text'] in List_of_Single_Word_Titles and word2['text'] in ['of', 'the'] and word3['upos'] in ['PROPN', 'NOUN']:
                output_document += word1_location.title()
                if input_text[word1_end] == ' ':
                    output_document += ' '
            else:
                output_document += word1_end
                if input_text[word1_end] == ' ':
                    output_document += ' '
        else:
            output_document += sentence[-2]['text']
            if input_text[int(sentence[-2]['end_char'])] == ' ':
                output_document += ' '
            output_document += sentence[-1]['text']
            if input_text[int(sentence[-1]['end_char'])] == ' ':
                output_document += ' '  
    return output_document
def basic_Position_Title_Capper(input_text):
    output_document = ''
    for sentence in NLP_entities:
        for this_word, next_word in pairwise(sentence):
            this_word_start = int(this_word['start_char'])
            this_word_end = int(this_word['end_char'])
            word_location = input_text[this_word_start:this_word_end]
            if this_word['text'] in List_of_Single_Word_Titles and next_word['upos'] == 'PROPN':
                output_document += word_location.title()
                if input_text[this_word_end] == ' ':
                    output_document += ' '
            elif this_word['text'] in List_of_Single_Word_Titles and next_word['text'] in ['of']:
                output_document += word_location.title()
                if input_text[this_word_end] == ' ':
                    output_document += ' '
            else:
                output_document += word_location
                if input_text[this_word_end] == ' ':
                    output_document += ' '
        else:
            output_document += sentence[-1]['text']+' '
    return output_document
Draft_Pre = uni_college_front_capper(uni_college_back_capper(Honorable_Judger(basic_Position_Title_Capper(Draft1_lowercase_of_the))))
Draft1_final = basic_Position_Title_Capper(title_triwise_back_capper(uni_college_front_capper(uni_college_back_capper(Honorable_Judger(Draft1_lowercase_of_the)))))
print(Draft_Pre)
print()
nlp_doc3 = nlp(Draft1_final)
# print(nlp_doc3)
final_output = Draft1_final
print()
print(final_output)
print()
time_end = time()
print(f'The process took {time_end-time_start} second(s).')
print(f'The imports took {import_end-import_start} second(s).')