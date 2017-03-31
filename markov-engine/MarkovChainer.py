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
    

class EditedTextClass(POSifiedText):
    def __init__(self, input_text, state_size=2, chain=None, runs=None):
        self.input_text = input_text
        self.state_size = state_size
        self.runs = runs or list(self.generate_corpus(self.input_text))
        self.rejoined_text = self.sentence_join(map(self.word_join, self.runs))
        self.chain = chain or markovify.Chain(self.runs, state_size)
    def to_dict(self):
        return {
            "input_text": self.input_text,
            "state_size": self.state_size,
            "chain": self.chain.to_json(),
            "runs": self.runs
        }
    @classmethod
    def from_dict(cls, obj):
        return cls(
            obj["input_text"],
            state_size=obj["state_size"],
            chain=markovify.Chain.from_json(obj["chain"]),
            runs=obj["runs"]
        )



def CreateSentences(Bundle): #definition to generate text. Firstword = word.replace(letter,"!") parameter is the file-path to the .txt file you'll be using to train the model, the second parameter is how many sentences you want out of the markov model.
	NEW_MODEL = None
	for x in Bundle.categories:
		FILE_PATH_OF_OLDSTUFF = x
		FILE_PATH_OF_OLDSTUFF = FILE_PATH_OF_OLDSTUFF[FILE_PATH_OF_OLDSTUFF.find("Category:") + 9:]
		for letter in FILE_PATH_OF_OLDSTUFF:
			if letter == ' ':
				FILE_PATH_OF_OLDSTUFF = FILE_PATH_OF_OLDSTUFF.replace(letter,"_")
		FILE_PATH_OF_OLDSTUFF = "Categories/%s.mc" % FILE_PATH_OF_OLDSTUFF
		with open(FILE_PATH_OF_OLDSTUFF) as json_file:  
			model2_json = json.load(json_file)
		OLD_MODEL = EditedTextClass.from_json(model2_json)
		NEW_MODEL = markovify.combine(OLD_MODEL, NEW_MODEL)
	tool = language_check.LanguageTool('en-GB')
	Text = ""
	paragraphText = ""
	for key in Bundle.paragraphs.keys():
		NumberOfSentences = random.randint(1,15)
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
	text_model = EditedTextClass(corpus, state_size=3, chain=None)
	model1_json = text_model.to_json()
	with open(FILENAME, 'w') as outfile:  
	    json.dump(model1_json, outfile)
