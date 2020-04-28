import sys
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from nltk import word_tokenize
from keras.models import load_model

from keras import backend as K

def f1(y_true, y_pred):
	def recall(y_true, y_pred):

		true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
		possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
		recall = true_positives / (possible_positives + K.epsilon())
		return recall

	def precision(y_true, y_pred):

		true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
		predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
		precision = true_positives / (predicted_positives + K.epsilon())
		return precision
	precision = precision(y_true, y_pred)
	recall = recall(y_true, y_pred)
	return 2*((precision*recall)/(precision+recall+K.epsilon()))

def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


tweet = sys.argv[1:]
temp = []
data = []
sentence = ' '.join(tweet)
for j in word_tokenize(sentence):
    temp.append(j.lower())

data.append(temp)
t = Tokenizer()
t.fit_on_texts(data)
encoded_tweet = t.texts_to_sequences(data)
padded_tweet = pad_sequences(encoded_tweet, padding='post',maxlen=926)
dependencies = {
    'f1':f1,
    'precision':precision,
    'recall':recall
}

model = load_model('sarcasm_model.h5',custom_objects = dependencies)
predicted_class = model.predict(padded_tweet)[0][0]
if(predicted_class > 0.23):
    print(1)
else:
    print(0)



