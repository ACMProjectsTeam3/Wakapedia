import re
import sys
import string
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM
from keras.layers.embeddings import Embedding
import h5py

rawtext = open('/Users/abhishaikemahajan/Documents/RandomTextFiles/META.txt','r').read().split('\n')

rawtext = ' '.join(rawtext)
all_words = rawtext.split()
unique_words = sorted(list(set(all_words)))
n_vocab = len(unique_words)
print "Total Vocab:", n_vocab
word_to_int = dict((w, i) for i, w in enumerate(unique_words))
int_to_word = dict((i, w) for i, w in enumerate(unique_words))
raw_text = rawtext.split()
n_words = len(raw_text)

seq_length = 100
dataX = []
dataY = []
for i in xrange(0, n_words - seq_length):
    seq_in  = raw_text[i: i+seq_length]
    seq_out = raw_text[i+seq_length]
    dataX.append([word_to_int[word] for word in seq_in])
    dataY.append(word_to_int[seq_out])

n_patterns = len(dataX)

X_train = np.reshape(dataX, (n_patterns, seq_length, 1))/float(n_vocab)
Y_train = np_utils.to_categorical(dataY)

model = Sequential()
model.add(LSTM(100, batch_input_shape=(1, 100, 1), return_sequences=True, stateful = True))
model.add(Dropout(0.2))
model.add(LSTM(100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(Y_train.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adagrad')
print model.summary()

filepath="word-weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(X_train, Y_train, nb_epoch=10, batch_size=1, callbacks=callbacks_list)

#EVERYTHING BENEATH HERE IS NOT FOR NETWORK CREATION, BUT FOR TESTING THE CREATED NETWORK (using the weights)

# load the network weights
filename = "word-weights-improvement-05-7.2198.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adagrad')

start = np.random.randint(0, len(X_train)-1)
pattern = dataX[start]
result = []

print "Seed:"
print "\"", ' '.join([int_to_word[value] for value in pattern]), "\""

x = np.reshape(pattern, (1, len(pattern), 1))
x = x/float(n_vocab)
prediction = model.predict(x)
index = np.argmax(prediction)

for i in xrange(20):
	x = np.reshape(pattern, (1, len(pattern), 1))
	x = x/float(n_vocab)
	prediction = model.predict(x)
	index = np.argmax(prediction)
	result.append(int_to_word[index])
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
	x = pattern

print "\nGenerated Sequence:"
print ' '.join(result)
print "\nDone."



