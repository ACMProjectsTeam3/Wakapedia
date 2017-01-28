import string
import markovify
import nltk
import re
import language_check
import random


class POSifiedText(markovify.Text): #part of the markovify library, basically just allows me to perform markov chain operations using the POS (part of speech) tagging function in NLTK. In simpler terms, it makes everything slightly slower, but also helps generate more gramatically sound sentences
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def CreateSentences(FILE_PATH, NUMSENTENCES): #definition to generate text. First parameter is the file-path to the .txt file you'll be using to train the model, the second parameter is how many sentences you want out of the markov model.
	with open(FILE_PATH) as f:
	    text = f.read() #open text file
	FormattedText = re.sub(r'\[.+?\]\s*', '', text) #mostly for wikipedia articles, just takes out the brackets + everything between the brackets. This is kind of a 'hacky' solution to the problem of the markov model creating only one bracket and never 'closing it' (which also happens with quotations btw), so we should fix this later
	FormattedText = FormattedText.replace("   ", " ") #takes out every 2 spaces, which sometimes happens 
	FormattedText = FormattedText.replace("    ", " ") #takes out every 3 spaces, which sometimes happens 
	FormattedText = re.sub( '\s+', ' ', FormattedText ).strip() #gonna be honest, I have zero clue what this does
	SHERLOCK = POSifiedText(FormattedText, state_size = 4) #creates a markov model (using POS) from the formatted test of state_size 4
	with open("/Users/abhishaikemahajan/Documents/RandomTextFiles/SATIRE.txt") as f:
		text = f.read()
	FormattedText = re.sub(r'\[.+?\]\s*', '', text)
	FormattedText = FormattedText.replace("   ", " ")
	FormattedText = FormattedText.replace("    ", " ")
	FormattedText = re.sub( '\s+', ' ', FormattedText ).strip()
	SATIRE = POSifiedText(FormattedText, state_size = 4) 
	tool = language_check.LanguageTool('en-GB')
	text = ""
	SHERLOCK = markovify.combine([SHERLOCK, SATIRE], [ .99, .01 ])
	for i in range(NUMSENTENCES): #creates 'NUMSENTENCES' sentence, where NUMSENTENCES is an integer
		text = SHERLOCK.make_sentence(tries = 1) #this, along with the next while loop, basically just forces the markov model to try an infinite number of times to have SOMETHING come out. 
		while (text == None):
			text = SHERLOCK.make_sentence(tries = 1)
		matches = tool.check(text) #checks the grammar of the generated text
		text = language_check.correct(text, matches) #corrects any mistakes the grammar checker found in the text
		print (text, end="") #prints text. The 'end' is just there to ensure that no new line is created
		NewLine = random.randint(0,30) #there is a 10% chance that a new line is created every time a sentence is created. This just makes the generated text not a huge block, and a little more natural looking 
		if NewLine == 1 or NewLine == 2 or NewLine == 3:
			print ("\n")


			
			
			
