import stanza, re
import streamlit as st
from itertools import tee
from psc_functions import *

@st.cache_resource
def load_NLP():
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,ner', verbose=False)
    return nlp
#     # https://stanfordnlp.github.io/stanza/
nlp = load_NLP()

with st.sidebar:
    st.subheader("About")
    st.caption('This app uses Natural Language Processing provided by Stanza (CoreNLP) to capitalize named entities, in addition to a host of other common English capitalization rules.')
    st.markdown('If you are interested in learning more about what things this app will attempt to capitalize, and limitations of the app, please visit the project\'s <a href="https://github.com/TAMUsquirrel/ProperSentenceCase">GitHub Repository</a>.', unsafe_allow_html=True)
    st.subheader("Contact")
    st.markdown('This is a work-in-progress. If you discover any issues, please submit them <a href="https://github.com/TAMUsquirrel/ProperSentenceCase/issues">here</a>. For anything else, you\'re welcome to reach out to me <a href="mailto:the@andrewharris.dev">via email</a>.', unsafe_allow_html=True)
    
st.title('Proper Sentence Case Converter')
st.subheader('Check sidebar for more information.')
with st.container():
    input_sentence = st.text_area("Please input text here. (maximum 800 words)")
    submit = st.button('Convert Text')

# # ====================================================================================================================
                                        # CLEANUP SPACES/TABS/NEWLINES
# # ====================================================================================================================
sentence_case = str(input_sentence.capitalize())
stripped = sentence_case.strip()
double_spaces_removed = " ".join(stripped.split())
# # ====================================================================================================================
NLP_Doc_1 = nlp(double_spaces_removed)            # 1ST PASS USING STANZA FOR ANNOTATION
# # ====================================================================================================================
NLP_Dict_1 = NLP_Doc_1.to_dict()     # CONVERT OUTPUT DATA STRUCTURE TO [LIST[LIST{DICT}]]

if input_sentence == '':
    final_output = ''
elif len(NLP_Dict_1[0]) == 1:
    final_output = input_sentence.capitalize()
else:
    Sents_Capped = sentence_1st_char_capitalizer(NLP_Dict_1, sentence_2nd_char_capitalizer(NLP_Dict_1, double_spaces_removed))

    List_of_Single_Word_Titles = ['agent', 'brother', 'cantor', 'captain', 'chairperson', 'chancellor', 'chef', 'chief', 'commissioner', 'darth', 'dame', 'dean', 'deputy', 'detective', 'director', 'doctor', 'father', 'governor', 'judge', 'king', 'queen', 'prince', 'princess', 'czar', 'lady', 'laird', 'lieutenant', 'lord', 'madame', 'master', 'miss', 'officer', 'pastor', 'president', 'principal', 'professor', 'provost', 'rabbi', 'rector', 'regent', 'reverend', 'saint', 'sensei', 'sheriff', 'sister', 'student', 'trainer', 'warden']
    Basics_Capped = Capitalize_Word2(NLP_Dict_1, Capitalize_Word1(NLP_Dict_1, Sents_Capped))
    titles_capped = title_triwise_front_capper(NLP_Dict_1, title_quadwise_back_capper(NLP_Dict_1, Basics_Capped))

    with open('common_acronyms') as cas:
        com_acs = cas.read()
        Draft1_acronyms_capped = re.sub(f"( )({com_acs})( |\/|\.|\?)", common_acronym_capitalizer, titles_capped, flags=re.IGNORECASE)
    Draft1_2_dot_acronyms_capped = re.sub("( )(.\..\.)", another_acronym_capitalizer, Draft1_acronyms_capped, flags=re.IGNORECASE)
    Draft1_3_dot_acronyms_capped = re.sub("( )(.\..\..\.)", another_acronym_capitalizer, Draft1_2_dot_acronyms_capped, flags=re.IGNORECASE)
    Draft1_lowercase_domains = re.sub("(\.)(com|net|org|co|us|ru|ir|in|uk|au|de|ua|gov)( |\/|\.|\?)", lowercaser2, Draft1_3_dot_acronyms_capped, flags=re.IGNORECASE)
    capitalize_celtic = re.sub("( )(Mc|Mac|O\' )(...)", celtic_basic_capitalizer, Draft1_lowercase_domains, flags=re.IGNORECASE)

    with open('pokemon_names_file') as p:
        pokemon_names = p.read()
        pokemon_capped = re.sub(f"{pokemon_names}", basic_capitalizer, capitalize_celtic, flags=re.IGNORECASE)

    with open('HoustonRoadList.txt') as roads:
        road_names = roads.read()
        roads_capped = re.sub(f"{road_names}", basic_capitalizer, pokemon_capped, flags=re.IGNORECASE)
        
    with open('special_NERs') as names:
        else_names = names.read()
        else_capped = re.sub(f"{else_names}", basic_capitalizer, roads_capped, flags=re.IGNORECASE)

    unNatural_uncapped = re.sub("unNatural", basic_lowercaser, else_capped)
    unNat_fixed = re.sub("UnNatural", basic_capitalizer, unNatural_uncapped)

    # ====================================================================================================================
    NLP_Doc_2 = nlp(unNat_fixed)            # 2ND PASS USING STANZA FOR ANNOTATION
    # ====================================================================================================================
    NLP_Dict_2 = NLP_Doc_2.to_dict()     # CONVERT OUTPUT DATA STRUCTURE TO [LIST[LIST{DICT}]]

    final_output = Capitalize_Word_Recheck(NLP_Dict_2, unNat_fixed)

with st.container():
    st.subheader("Output")
    st.write(final_output)
