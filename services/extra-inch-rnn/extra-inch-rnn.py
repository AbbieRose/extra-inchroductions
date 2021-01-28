import numpy
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

#Source: https://stackabuse.com/text-generation-with-python-and-tensorflow-keras/

file = open("introductions.txt").read()

# they're making everything lower case, so I guess I will too.

def tokenize_words(input) :
    input = input.lower()

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(input)

    filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
    return " ".join(filtered)

processed_inputs = tokenize_words(file)

# gotta map the words to numbers because neural nets work on numbers, not words
chars = sorted(list(set(processed_inputs)))
char_to_num = dict((c, i) for i, c in enumerate(chars))

# the example I used wanted to print the inputs here, I don't really feel like I need to know this information but just in case, here it is:
input_len = len(processed_inputs)
vocab_len = len(chars)
print("Total number of characters:", input_len)
print("Total vocab:", vocab_len)

# ok so they want segments of 100 for the training and I don't know why. I do not want that. The nature of my text is fundamentally different, so I think I want shorter ones. For now, I'll go with 50, but I might need to change this.
seq_length = 50
x_data = []
y_data = []

# ok, so what this is doing is taking sequences of 50 characters, and then looking at the 51st character. We will use it to predict- given the characters I have now, what will the next one be?
for i in range(0, input_len - seq_length, 1) :
    in_seq = processed_inputs[i:i + seq_length]
    out_seq = processed_inputs[i + seq_length]

    x_data.append([char_to_num[char] for char in in_seq])
    y_data.append(char_to_num[out_seq])

n_patterns = len(x_data)
print("Total Patterns:", n_patterns)

# this is preprocessing to pass the thing to the model, but I don't know if I really understand why we're doing this.
X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
X = X/float(vocab_len)

y = np_utils.to_categorical(y_data)

model = Sequential() # note to self: what is a sequential model
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax')) #what is softmax

model.compile(loss='categorical_crossentropy', optimizer='adam')

# saving weights in case it takes a long time
file = "model_weights_saved.hdf5"
checkpoint = ModelCheckpoint(file, monitor='loss', verbose=1, save_best_only=True, mode='min')
desired_callbacks = [checkpoint]

model.fit(X, y, epochs=20, batch_size=256, callbacks=desired_callbacks)

#now load weights once done
filename = "model_weights_saved.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

num_to_char = dict((i, c) for i, c in enumerate(chars))

# now we're going to generate the characters. The original program uses a random character, but I feel like we just want to start with And. We will try this in a minute
start = numpy.random.randint(0, len(x_data) - 1)
pattern = x_data[start]
print("Random Seed:")
print("\"", ''.join([num_to_char[value] for value in pattern]), "\"")

# is this going to make it 1000 characters long? I guess so. Will play with this too.
for i in range(1000) :
    x = numpy.reshape(pattern, (1, len(pattern), 1))
    x = x / float(vocab_len)
    prediction = model.predict(x, verbose=0)
    index = numpy.argmax(prediction)
    result = num_to_char[index]
    seq_in = [num_to_char[value] for value in pattern]

    # why not print?
    sys.stdout.write(result)
    
    pattern.append(index)
    pattern = pattern[1:len(pattern)]
