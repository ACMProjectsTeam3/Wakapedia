from __future__ import division
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import model_from_json
import numpy as np
import random
import h5py

def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    if sum(a) > 1.0:  # occasionally getting 1.00000X, so handling for that
        a *= .999
    return np.argmax(np.random.multinomial(1, a, 1))


def train():
    path = "/Users/abhishaikemahajan/Documents/dummy/kimenet.txt"
    try:
        text = open(path).read().lower()
    except UnicodeDecodeError:
        import codecs
        text = codecs.open(path, encoding='utf-8').read().lower()
    print ("corpus length:") ,len(text)
    chars = set(text)
    words = set(text.split())
    print ("total number of unique words"), len(words)
    print ("total number of unique chars"), len(chars)
    word_indices = dict((c, i) for i, c in enumerate(words))
    indices_word = dict((i, c) for i, c in enumerate(words))
    maxlen = 30
    step = 3
    print ("maxlen:"), maxlen,("step:"), step
    sentences = []
    next_words = []
    next_words = []
    list_words = []
    sentences2 = []
    list_words = text.lower().split()
    for i in range(0, len(list_words) - maxlen, step):
        sentences2 = ' '.join(list_words[i: i + maxlen])
        sentences.append(sentences2)
        next_words.append((list_words[i + maxlen]))
    print ('length of sentence list:'), len(sentences)
    print ("length of next_word list"), len(next_words)
    print ('Vectorization...')
    X = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, word in enumerate(sentence.split()):
            X[i, t, word_indices[word]] = 1
        y[i, word_indices[next_words[i]]] = 1
    print ('Building model...')
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, len(words))))
    model.add(Dropout(0.2))
    model.add(LSTM(512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(len(words)))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    try:
        model.load_weights("NEW-word-weights-improvement-05-7.2198.hdf5")
    except Exception as e:
        print (e)
        pass
    for iteration in range(1, 750):
        print ('-' * 50)
        print ('Iteration'), iteration
        model.fit(X, y, batch_size=500, nb_epoch= 4)
        json_string = model.to_json()
        with open('<ARCHITEC-word-weights-improvement-05-7.2198.hdf5', 'w') as f:
            f.write(json_string)
        model.save_weights('NEW-word-weights-improvement-05-7.2198.hdf5', overwrite=True)


def generate_from_word_level_rnn(maxlen=30, diversity=1.0, min_sent_len=10, max_sent_len=65):
    with open("/Users/abhishaikemahajan/Documents/RandomTextFiles/META.txt", "r") as f:
        text = f.read().lower().split()[:4940]
    words = set(text)
    start_index = random.randint(0, len(text) - maxlen - 1)
    word_indices = dict((c, i) for i, c in enumerate(words))
    indices_word = dict((i, c) for i, c in enumerate(words))
    response = ""
    model = model_from_json(open('/Users/abhishaikemahajan/Documents/RandomTextFiles/META.txt').read())
    model.load_weights('word-weights-improvement-05-7.2198.hdf5')
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    sentence = text[start_index: start_index + maxlen]
    for i in range(random.randint(min_sent_len, max_sent_len)):
        x = np.zeros((1, maxlen, len(words)))
        for t, word in enumerate(sentence):
            x[0, t, word_indices[word]] = 1.
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_word = indices_word[next_index]
        if not response:
            response += ' {0}'.format(next_word)
        else:
            if response.split()[-1] != next_word:
                response += ' {0}'.format(next_word)
        del sentence[0]
        sentence.append(next_word)
    return response

if __name__ == "__main__":
    train()
    generate_from_word_level_rnn()


