import string
import markovify
import nltk
import re
import language_check
import random
import json
import os
import random
from random import randint


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
    

def CreateSentences(Bundle): #definition to generate text. Firstword = word.replace(letter,"!") parameter is the file-path to the .txt file you'll be using to train the model, the second parameter is how many sentences you want out of the markov model.
	FILE_PATH_OF_OLDSTUFF = None
	while (FILE_PATH_OF_OLDSTUFF == None):	
		FILE_PATH_OF_OLDSTUFF = random.choice(Bundle.categories)
	FILE_PATH_OF_OLDSTUFF = FILE_PATH_OF_OLDSTUFF[FILE_PATH_OF_OLDSTUFF.find("Category:") + 9:]
	for letter in FILE_PATH_OF_OLDSTUFF:
			if letter == '_':
				FILE_PATH_OF_OLDSTUFF = FILE_PATH_OF_OLDSTUFF.replace(letter, ' ')
 	FILE_PATH_OF_OLDSTUFF = "Categories/%s.mc" % FILE_PATH_OF_OLDSTUFF
 	with open(FILE_PATH_OF_OLDSTUFF) as json_file:  
 		model2_json = json.load(json_file)
 	NEW_MODEL = EditedTextClass.from_json(model2_json)
	tool = language_check.LanguageTool('en-GB')
	Text = ""
	paragraphText = ""
	for key in Bundle.paragraphs.keys():
		NumberOfSentences = random.randint(1,12)
		for i in range(NumberOfSentences): #creates 'NUMSENTENCES' sentence, where NUMSENTENCES is an integer
			Text = NEW_MODEL.make_sentence(tries = 1) #this, along with the next while loop, basically just forces the markov model to try an infinite number of times to have SOMETHING come out. 
			while (Text == None): 
				Text = NEW_MODEL.make_sentence(tries = 1)
			matches = tool.check(Text) #checks the grammar of the generated text
			paragraphText += language_check.correct(Text, matches) #corrects any mistakes the grammar checker found in the text
			paragraphText += " "
		Bundle.paragraphs[key] = paragraphText
		paragraphText = ""
	return Bundle

		
		

def TrainAndSaveString(String, name):
	FILENAME  = name
	os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
	corpus = String
	corpus = re.sub( '\s+', ' ', corpus ).strip()
	text_model = markovify.Text(corpus, state_size=4, chain=None)
	model1_json = text_model.to_json()
	with open(FILENAME, 'w') as outfile:  
	    json.dump(model1_json, outfile)
