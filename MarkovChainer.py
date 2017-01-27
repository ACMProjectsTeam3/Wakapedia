import string
import markovify
import nltk
import re
import grammar_check


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def CreateSentences(FILE_PATH, NUMSENTENCES):
	with open(FILE_PATH) as f:
	    text = f.read()
	FormattedText = re.sub(r'\[.+?\]\s*', '', text)
	FormattedText = FormattedText.replace('"', "")
	FormattedText = FormattedText.replace("   ", " ")
	FormattedText = FormattedText.replace("    ", " ")
	FormattedText = re.sub( '\s+', ' ', FormattedText ).strip()
	SHERLOCK = POSifiedText(FormattedText, state_size = 4)
	tool = grammar_check.LanguageTool('en-GB')
	text = ""
	for i in range(NUMSENTENCES):
		text = SHERLOCK.make_sentence(tries = 1)
		while (text == None):
			text = SHERLOCK.make_sentence(tries = 1)
		text = text.decode("utf8")
		matches = tool.check(text)
		text = grammar_check.correct(text, matches)
		print text,
		NewLine = randint(0,30)
		if NewLine == 1 or NewLine == 2 or NewLine == 3:
			print "\n"
