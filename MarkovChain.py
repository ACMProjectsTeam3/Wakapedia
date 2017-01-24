import string
import markovify
import nltk
import re

#markovify class which actually creates the sentneces
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

#opens file (specific to my computer for now)
with open("/Users/abhishaikemahajan/Documents/RandomTextFiles/TEXT.txt") as f:
    text = f.read()

#cleans up text file (regex function will be primarily used to deal with the brackets in wikipedia articles [citations])
printable = set(string.printable)
FormattedText = filter(lambda x: x in printable, text)
FormattedText = re.sub(r'\[.+?\]\s*', '', FormattedText)

#creates the markov model. State_size basically refers to how 'natural sounding' a generated sentence will be. Going past 7 leads to diminishing returns, but for now, it must stay beneath 3 due to how little data we have. Little is relative btw, I'm using a corpus of an entire book (The Metamorphosis), and going past 3 leads to identical sentences being generated.
text_model = POSifiedText(FormattedText, state_size = 2)

#for loops that display generated sentences. First one displays any sentence of any length, second one generates sentences underneath a certain character length (230 for now). 
for i in range(10):
	print(text_model.make_sentence())
  
for i in range(10):
	(text_model.make_short_sentence(230))

