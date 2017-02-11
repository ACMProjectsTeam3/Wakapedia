# Wakapedia

run this thing with: 

TrainAndSave("/Users/abhishaikemahajan/Documents/Wakapedia/WIKITEXT.txt", '/Users/abhishaikemahajan/Documents/Wakapedia/texter.txt')

where:

TrainAndSave(FILEPATH, FILENAME):

FILENAME is created on the spot, and is a json text file of the markov chain created 

FILEPATH is the training corpus 



CreateSentences("/Users/abhishaikemahajan/Documents/RandomTextFiles/META.txt", '/Users/abhishaikemahajan/Documents/Wakapedia/texter.txt', 20)

where:

CreateSentences(FILE_PATH_OF_INPUT, FILE_PATH_OF_OLDSTUFF, NUMSENTENCES):

FILE_PATH_OF_INPUT is the file path of the text file you want the generated text to focus on

FILE_PATH_OF_INPUT is the file path of the text file you want the generated text to use as a word corpus, but not as a main focus of the generated sentences
