# ProperSentenceCase
Changes the input text to "Proper Sentence Case," which capitalize entities within the input text in addition to the first character of each sentence.

Hello! You're probably wondering, 'What all does it capitalize?' Great question!

In addition to a wealth of simple (English-only) capitalization rules, this program utilizes CoreNLP, more specifically, Stanza, for Natural Language Processing to further this program's ability to recognize parts of speech and named entities for capitalization.


	1. The first letter of each sentence (duh).
  

 	2. NAMES OF PEOPLE, ORGANIZATIONS, & GEOPOLITICAL AREAS (GPE)
		a. When the name just-so-happens to trigger other capitalization rules
    b. When the name is recognized as a pronoun/NER by CoreNLP.
          The less ambiguous & more common the name of the person, org, or place is, the more likely it'll be recognized.
          For Example:
                "I would love to work at a company like Google or apple."
                "I would love to work at a company like Google or Apple Inc."
                
                Explanation: if you want it to recognize apple as the company (not the fruit), you need to call it by its actual name.
                Other company names that are not ambiguous are easily recognized, however. (e.g. Google, Samsung, etc.)
                
 	2. The word 'I'
  
	3. Common Title Abbreviations (like Mr., Ms., Dr., Asst., Prof.)
  
	4. Common Acronyms (USA, UK, PC, HR, etc.)
	
	5. (~40) Single-Word Titles (of Positions)
		  a. if the title precedes a proper noun
			    examples: Prince Charles, Father Jack, Agent Smith
		  b. if it's referring to the "[___] of something"
			    examples: Prince of Wales, King of France
          
      Note: I'd love to continue adding to this list, but I need to focus on other parts of the project right now.
      If there is a title you'd like to see added, please let me know! :)
 
	5. [Title] of Something
		  example: "Yugi Moto is the King of Games."
            Note: Uses the same list of titles as the previous entry.
      
  6. [_____] University/College /// "University of [____]
		  examples: "Texas A&M University" oe "University of Texas"
    
	8. The word Honorable/Honourable if it precedes the word 'Judge' or 'Judges'
        Why? …I have a background in criminal justice, and wanted to see this.
        If there are other scenarios where a capitalized adjective can precede a specific title, please let me know and I can add it to the list!![image](https://user-images.githubusercontent.com/126024439/222568317-0851060e-9c22-4d78-8a45-ce9dfa171465.png)
