# ProperSentenceCase
Changes the input text to "Proper Sentence Case," which capitalizes recognized named entities within the input text, in addition to a host of other common English capitalization rules.

=============================================================

Hello! You're probably wondering, 'What all does it capitalize?' Great question!

In addition to a wealth of simple (English-only) capitalization rules, this program utilizes CoreNLP, more specifically, Stanza, for Natural Language Processing to further this program's ability to recognize parts of speech and named entities for capitalization.

Here is a list of current features:

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
          
      Note: I'd love to continue adding to the list of titles, but that has been placed on the to-do list for now.
      If there is a title you'd like to see added, please let me know!
 
	6. [Title] of Something
		  example: "Yugi Moto is the King of Games."
            Note: Uses the same list of titles as the previous entry.
      
  	7. [_____] University/College /// "University of [____]
		  examples: "Texas A&M University" or "University of Texas"
    
	8. The word Honorable/Honourable if it precedes the word 'Judge' or 'Judges'
        Why? …I have a background in criminal justice, and wanted to see this.
        If there are other scenarios where a capitalized adjective can precede a specific title, please let me know and I can add it to the list!
	
	9. Pokemon names (existing as of 3/7/2023).
	
	10. The names of approximately 12,000 roads in the Houston area, when the text uses the shorthand street abbreviation. This will be removed in the future when a better solution for capitalizing street names is developed.
	
	11. Common super-hero names, excluding names that might be mistaken for basic nouns. E.g. Hulk or Black Widow


LIMITATIONS:

	1. Because CoreNLP annotates text on a sentence-by-sentence basis, sometimes you will notice that it will capitalize a name in one place, but not in another. For Example: "Did you ever hear the tragedy of [darth plagueis] the wise? I thought not. It’s not a story the [jedi] would tell you. It’s a [sith] legend. [Darth Plagueis] was a dark lord of the [sith], so powerful and so wise he could use the force to influence the midichlorians to create life."
	2. This is not a spell or grammar check project. If the input text is grammatically incorrect, or words are spelled incorrectly that are essential to understanding the structure of the sentence, the results will likely suffer.
