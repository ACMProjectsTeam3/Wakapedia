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

def CreateSentences(FILE_PATH_OF_INPUT, FILE_PATH_OF_OLDSTUFF, NUMSENTENCES): #definition to generate text. First parameter is the file-path to the .txt file you'll be using to train the model, the second parameter is how many sentences you want out of the markov model.
	with open(FILE_PATH_OF_INPUT) as f:
	    text = f.read() #open text file
	FormattedText = re.sub( '\s+', ' ', text ).strip() #gonna be honest, I have zero clue what this does
	NEW_MODEL = POSifiedText(FormattedText, state_size = 4) #creates a markov model (using POS) from the formatted test of state_size 4
	with open(FILE_PATH_OF_OLDSTUFF) as json_file:  
		model2_json = json.load(json_file)
	OLD_MODEL = POSifiedText.from_json(model2_json)
	tool = language_check.LanguageTool('en-GB')
	text = ""
	NEW_MODEL = markovify.combine([NEW_MODEL, OLD_MODEL], [ .80, .20 ])
	for i in range(NUMSENTENCES): #creates 'NUMSENTENCES' sentence, where NUMSENTENCES is an integer
		text = NEW_MODEL.make_sentence(tries = 1) #this, along with the next while loop, basically just forces the markov model to try an infinite number of times to have SOMETHING come out. 
		while (text == None):
			text = NEW_MODEL.make_sentence(tries = 1)
		matches = tool.check(text) #checks the grammar of the generated text
		text = language_check.correct(text, matches) #corrects any mistakes the grammar checker found in the text
		print (" ", end = "")
		print (text, end="") #prints text. The 'end' is just there to ensure that no new line is created
		NewLine = random.randint(0,30) #there is a 10% chance that a new line is created every time a sentence is created. This just makes the generated text not a huge block, and a little more natural looking 
		if NewLine == 1 or NewLine == 2 or NewLine == 3:
			print ("\n")


def TrainAndSave(FILEPATH, FILENAME):
	corpus = open(FILEPATH).read()
	corpus = re.sub( '\s+', ' ', corpus ).strip()
	text_model = POSifiedText(corpus, state_size=4)
	model1_json = text_model.to_json()
	with open(FILENAME, 'w') as outfile:  
	    json.dump(model1_json, outfile)





