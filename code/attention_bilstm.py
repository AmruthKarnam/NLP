import numpy
import numpy as np
from numpy import asarray
from numpy import zeros
import pandas as pd

numpy.random.seed(1337)
from spellchecker import SpellChecker
import re
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential,Model
from keras.layers import *
from keras.layers import Dense, Flatten, Embedding
from keras.layers import LSTM, Dropout, Activation , Bidirectional,Dense,Flatten,Activation,RepeatVector,Permute,Multiply
from keras.layers.embeddings import Embedding
from keras.layers.core import*
from keras import initializers, regularizers, constraints, Input
from keras.layers.recurrent import LSTM
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras import backend as K
import codecs
import csv
from nltk import word_tokenize
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import emoji
import gensim
import time
import os
import sys 
import json
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm

spell = SpellChecker()
seed = 7
numpy.random.seed(seed)
class Attention(Layer):
		def __init__(self, W_regularizer=None, b_regularizer=None, W_constraint=None, b_constraint=None, bias=True, **kwargs):
			self.supports_masking = True
			self.init = initializers.get('glorot_uniform')
			self.W_regularizer = regularizers.get(W_regularizer)
			self.b_regularizer = regularizers.get(b_regularizer)
			self.W_constraint = constraints.get(W_constraint)
			self.b_constraint = constraints.get(b_constraint)
			self.bias = bias
			super(Attention, self).__init__(**kwargs)


def ReadOpen(filename,Labelfile):
		data = []
		with codecs.open(filename, 'r',encoding="utf-8", errors="replace") as readFile:
			reader = csv.reader(readFile)
			lines = list(reader)
		count = 0
		for i in lines:
			temp = []
			sentence = ' '.join(i)
			for j in word_tokenize(sentence):
				temp.append(j.lower()) 
				count += 1	  
			data.append(temp)
		labels_pd = pd.read_csv(Labelfile,index_col=False)
		labels = numpy.asarray(labels_pd)

		return data[1:],labels, count-1


def extract_emojis(sentence):
	return [word for word in sentence.split() if str(word.encode('unicode-escape'))[2] == '\\' ]


def char_is_emoji(character):
	if character in emoji.UNICODE_EMOJI:
		return True
	else:
		return False

def process(docs,count):

	# prepare tokenizer
	t = Tokenizer()
	t.fit_on_texts(docs)
	# vocab_size = len(t.word_index) + 1
	# print(vocab_size)
	# integer encode the documents
	encoded_docs = t.texts_to_sequences(docs)
	# pad documents to a max length of 4 words
	# max_length = 4
	padded_docs = pad_sequences(encoded_docs, padding='post')
	l = len(padded_docs[0])
	# load the whole embedding into memory
	embeddings_index = dict()
	f = open('glove.6B.300d.txt',encoding="utf8")
	for line in tqdm(f):
		values = line.split()
		word = values[0]
		coefs = asarray(values[1:], dtype='float32')
		embeddings_index[word] = coefs
	f.close()
	print('Loaded %s word vectors.' % len(embeddings_index))

	e2v = gensim.models.KeyedVectors.load_word2vec_format('emoji2vec.bin', binary=True)
	nf = 0
	# create a weight matrix for words in training docs
	embedding_matrix = zeros((count, 300))
	for word, i in t.word_index.items():
		embedding_vector = embeddings_index.get(word)
		if embedding_vector is not None:
			embedding_matrix[i] = embedding_vector
		else:
			# print(word)
			new_em = []
			em = extract_emojis(word)
			for ej in em:
				for c in ej:
					if char_is_emoji(c):
						new_em.append(c)
			# print(new_em)
			try:
				if new_em:
						row = []
						for e in new_em:

							row.append(e2v[e])
						embedding_matrix[i] = np.average(np.asarray(row),axis=0).tolist()
				else:
					embedding_matrix[i] = [0] * 300
			except:
				embedding_matrix[i] = [0] * 300
				nf += 1

	print(str(nf)+" words not found in vocabulary")

	return padded_docs, embedding_matrix,l

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


def PrepModel(count,embedding_matrix,l,lrate=0.01):
	model1 = Sequential()
	model2 = Sequential()
	input = Input(shape = (926,))
	#model1.add(input)
	#model2.add(input)
	embedded1 = Embedding(count,300, weights=[embedding_matrix],trainable=False)(input)
	embedded2 = Embedding(count,300, weights=[embedding_matrix],trainable=False)(input)
	#model1.add(embedded1)
	#model2.add(embedded2)
	#print("here1\n")
	
	lstm1 = Bidirectional(LSTM(100,kernel_initializer='he_normal', activation='sigmoid', dropout=0.5,recurrent_dropout=0.5, unroll=False, return_sequences=False))(embedded1)
	lstm2 = Bidirectional(LSTM(100,kernel_initializer='he_normal', activation='sigmoid', dropout=0.5,recurrent_dropout=0.5, unroll=False, return_sequences=True))(embedded2)
	#model1.add(lstm1)
	#model2.add(lstm2)
	print("here2\n")
	#model.add(Bidirectional(LSTM(75,kernel_initializer='he_normal', activation='sigmoid', dropout=0.5,recurrent_dropout=0.5, unroll=False, return_sequences=False)))
	#model.add(Attention())
	#print("here3\n")
	dense = Dense(1, activation='tanh')(lstm2)
	flatten = Flatten()(dense)
	activation_1 = Activation('softmax')(flatten)
	repeat_vector = RepeatVector(100)(activation_1)
	permute = Permute([2,1])(repeat_vector)
	#model2.add(Dense(1, activation='tanh'))
	#model2.add(Flatten())
	#model2.add(Activation('softmax'))
	#model2.add(RepeatVector(100))
	#model2.add(Permute([2, 1]))
	dense_1 = Dense( 100, activation='sigmoid', name='attention_probs')(lstm1)
	model1 = Model(inputs = input,output = dense_1)
	model2 = Model(inputs = input,output = permute)
	#model1.add(Dense( 100, activation='sigmoid', name='attention_probs'))
	mergedOut = Multiply()([model1.output,model2.output])
	mergedOut = Flatten()(mergedOut)
	#attention_mul = multiply([lstm, attention_probs], name='attention_mul')
	#model.add(attention_mul)
	#model.add(Dense(1, activation='sigmoid'))
	mergedOut = Dense(1,activation="sigmoid")(mergedOut)
	model = Model(inputs = input,output = mergedOut)
	model.compile(optimizer=Adam(lr=lrate), loss='binary_crossentropy', metrics=[f1])
	print('No of parameter:', model.count_params())
	print(model.summary())
	print(K.eval(model.optimizer.lr))
	return model

def clean(dataset):
	for index in tqdm(range(len(dataset))):
		data = dataset[index]
		data = ' '.join(data)		
		data = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", data).split())
		data = ' '.join(re.sub("(\w+://\S+)", " ", data).split())
		data = ' '.join(re.sub("[.,!?:;-=]", " ", data).split())
		data = data.lower()
		data = re.sub(r'\bthats\b', 'that is', data)
		data = re.sub(r'\bive\b', 'i have', data)
		data = re.sub(r'\bim\b', 'i am', data)
		data = re.sub(r'\bya\b', 'yeah', data)
		data = re.sub(r'\bcant\b', 'can not', data)
		data = re.sub(r'\bwont\b', 'will not', data)
		data = re.sub(r'\bid\b', 'i would', data)
		data = re.sub(r'wtf', 'what the fuck', data)
		data = re.sub(r'\bwth\b', 'what the hell', data)
		data = re.sub(r'\br\b', 'are', data)
		data = re.sub(r'\bu\b', 'you', data)
		data = re.sub(r'\bk\b', 'OK', data)
		data = re.sub(r'\bsux\b', 'sucks', data)
		data = re.sub(r'\bno+\b', 'no', data)
		data = re.sub(r'\bcoo+\b', 'cool', data)
		data = data.split()
		misspelled = spell.unknown(data)
		for word in misspelled:
			data[data.index(word)] = spell.correction(word)
		dataset[index] = data
	return dataset

def ReadTest(filename,Labelfile):

	data = []

	with codecs.open(filename, 'r',encoding="utf-8", errors="replace") as readFile:
		reader = csv.reader(readFile)
		lines = list(reader)
	count = 0
	for i in lines:
		temp = []
		sentence = ' '.join(i)
		for j in word_tokenize(sentence):
			temp.append(j.lower()) 
			count += 1
	  
		data.append(temp)

	labels_pd = pd.read_csv(Labelfile,index_col=False)
	labels = numpy.array(labels_pd['Labels'])
	# labels = numpy.asarray(labels_pd)

	t = Tokenizer()
	t.fit_on_texts(data)
	encoded_docs = t.texts_to_sequences(data)
	padded_docs = pad_sequences(encoded_docs, padding='post',maxlen=926)

	return padded_docs,labels



if __name__ == "__main__":

	with open('settings.json') as data_file:
		data = json.load(data_file)
	lrate = data["Model_settings"]["Learning_rate"]
	num_epochs = data["Model_settings"]["Epochs"]
	filename = data["FileNames"]["Training_file"]
	Labelfile = data["FileNames"]["Label_file"]
	print('Reading data...')
	data,labels,count = ReadOpen(filename,Labelfile)
	data=clean(data)
	print('Getting Embeddings...')
	padded_docs, embedding_matrix,l = process(data,count)
	print('Preparing model...')
	model = PrepModel(count,embedding_matrix,l,lrate)
	print('Training...')
	#print("here4\n")
	"""earlyStopping=keras.callbacks.EarlyStopping(monitor='val_loss', patience=0, verbose=1, mode='auto')
	kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
	cvscores = []
	fold = 1
	for train, test in kfold.split(padded_docs, labels):
		print("K-fold : ",fold)
		fold += 1
		X_train, X_val, y_train, y_val = train_test_split(padded_docs[train], labels[train], test_size=0.2, random_state=seed)
		model.fit(X_train, y_train, validation_data=(X_val,y_val), nb_epoch=num_epochs, verbose=1, callbacks=[earlyStopping])
		scores = model.evaluate(padded_docs[test], labels[test], verbose=0)
		print("Accuracy : %.2f%%" % (scores[1]*100))
		cvscores.append(scores[1] * 100)
	
	print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))"""
	X_train, X_test, y_train, y_test = train_test_split(padded_docs, labels, test_size=0.2, random_state=seed)
	X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=seed)
	earlyStopping=keras.callbacks.EarlyStopping(monitor='val_loss', patience=0, verbose=1, mode='auto')
	print("here33\n")
	model.fit(X_train, y_train, validation_data=(X_val,y_val), nb_epoch=num_epochs, verbose=1, callbacks=[earlyStopping])
	loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
	print('Accuracy: %f' % (accuracy*100))
