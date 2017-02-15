import string
import markovify
import nltk
import re
import language_check
import random
import json

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


class POSifiedText(markovify.Text):
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
	NEW_MODEL = EditedTextClass(FormattedText, state_size = 4) #creates a markov model (using POS) from the formatted test of state_size 4
	with open(FILE_PATH_OF_OLDSTUFF) as json_file:  
		model2_json = json.load(json_file)
	OLD_MODEL = EditedTextClass.from_json(model2_json)
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
	text_model = EditedTextClass(corpus, state_size=4, chain=None)
	model1_json = text_model.to_json()
	with open(FILENAME, 'w') as outfile:  
	    json.dump(model1_json, outfile)
