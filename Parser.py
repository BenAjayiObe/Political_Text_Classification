#
# The purpose of this project will be to try and predict the outcome of votes during politcal debates in parliament.
#
from __future__ import division
import nltk, re, pprint
from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist
from nltk import *
from nltk.corpus import  names
import random
import pandas as pd
from pandas import DataFrame, Series
import csv

import urllib2
import urllib
import zipfile
import cStringIO
from bs4 import BeautifulSoup


def switch(name):
	temp = name
	temp = temp.split()
	if len(temp)==2:
		return temp[1] + " " + temp[0]
	elif len(temp)==3:
		return temp[1] + " " + temp[2] + " " + temp[0]
	else:
		return name



def Exract_Name_Text_TWFY(Name, soup):
	DuncanCorpus=""
	for tag in soup.findAll("speech", {"speakername":Name}):
		DuncanCorpus += ' ' + tag.get_text().replace("\n", " ").rstrip()
	return DuncanCorpus

# Function that extracts features from text given corpus in string form.
def Extract_Features(Corpus):
	features = {}
	num_letters = len(Corpus)
	DuncanWords = nltk.word_tokenize(Corpus)
	sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
	Duncansentences = sent_tokenizer.tokenize(Corpus)
	numWordsPerSentence = len(DuncanWords) / len(Duncansentences)
	numLettersPerWord = num_letters / len(DuncanWords)

	features['Words_Per_Sentence'] = numWordsPerSentence
	features['Letters_Per_Word'] = numLettersPerWord
	features['Vocab_Size'] = len(set(Corpus))
	return features

#print "Extracting Duncan"
def Clean_Names_In_File(Soup):
	nameList = []
	for names in Soup.findAll('Member'):
		nameList.append(names.contents[0].encode('utf-8').strip().replace('\n',' ').replace(',',' ').replace(':',''))

	return filter(None, nameList)

def Names_In_File(Soup):
	nameList2 = []
	for names in Soup.findAll('Member'):
		nameList2.append(names.contents[0].encode('utf-8').strip())

	return filter(None, nameList2)

def switch(name):
	temp = name
	temp = temp.split()
	if len(temp)==2:
		return temp[1] + " " + temp[0]
	elif len(temp)==3:
		return temp[1] + " " + temp[2] + " " + temp[0]
	else:
		return name

def first_name(name):
	return name.split()[1]

def gender_features(word):
	return {'suffix1':word[-1],
			'suffix2':word[-2]}



hansard = open("data/scrapedxml/debates/debates2015-12-07b.xml", "r")
hanSoup = BeautifulSoup(hansard, 'xml')

if(False):
	feed = urllib2.urlopen('http://api.data.parliament.uk/resources/files/feed?dataset=14').read()
	soup = BeautifulSoup(feed)
	soup.prettify()

	zipURL = soup.findAll('id')[1].contents[0]
	parentZip = urllib2.urlopen(str(zipURL))
	#parentZip = urllib.urlretrieve(str(zipURL))
	memZip = cStringIO.StringIO(parentZip.read())
	archive = zipfile.ZipFile(memZip, 'r')
	fileName = archive.namelist()[0]
	#print fileName
	memZipChild = cStringIO.StringIO(archive.read(fileName))
	archiveChild = zipfile.ZipFile(memZipChild)
	hansard = archiveChild.read(archiveChild.namelist()[0])

	hanSoup = BeautifulSoup(hansard, 'xml')
	hanSoup = hanSoup.prettify()

	#for heading in hanSoup.findAll('hs_para'):
	#	for element in heading.contents:
	#			element = element.encode('utf-8').replace("\n","")

	hanSoupString = hanSoup
	hanSoupString = hanSoupString.encode('utf-8')#.replace("\n","")
	file = open("2015-05-07_house_of_commons_debate.xml", "w")
	file.write(hanSoupString)
	file.close()


	hansard = open("2015-05-07_house_of_commons_debate.xml", "r")
	hanSoup = BeautifulSoup(hansard, 'xml')
	#print hanSoup.prettify()

	#[inner.extract() for inner in hanSoup.findAll('member')]
	#print hanSoup
	#paragraphs = []


	df = DataFrame(pd.read_csv("MP_Party_Constituent.csv"))
	df.colmuns = ["Name","Party", "Constituent"]
	df["WordsPerSentence"] = ""
	df["LettersPerWord"] = ""




	Names = Names_In_File(hanSoup)
	Names2 = Clean_Names_In_File(hanSoup)
	Names2[400] = Names2[400].replace("  ", " ")
	print len(Names)
	print len(Names2)

	name_df = DataFrame(Names)
	name_df.colmuns = ["Name", "Clean_Name"]
	name_df["Clean_Name"] = Names2

	#print name_df.iloc[400]["Clean_Name"]
	indexStore = 0


	#nameList = [switch(x) for x in nameList]
names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)

train_names = names[6000:]
devtest_names = names[4000:6000]
test_names = names[:1500]

train_set = [(gender_features(n), g) for (n,g) in train_names]
devtest_set = [(gender_features(n), g) for (n,g) in devtest_names] 
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, devtest_set)

#	Creating concatonations

df = DataFrame(pd.read_csv("MP_Party_Constituent.csv"))
df.colmuns = ["Name","Party", "Constituent"]
df["Gender"] = ""
df["Corpus"] = ""
df["WordsPerSentence"] = ""
df["LettersPerWord"] = ""
df["VocabSize"] = ""


# Concatenating features from corpus
for index, row in df.iterrows():
	corpus = Exract_Name_Text_TWFY(switch(row["Name"]), hanSoup)
	if len(corpus) > 0:
		row["Corpus"] = corpus
		temp = Extract_Features(row["Corpus"])
		row["WordsPerSentence"] = temp["Words_Per_Sentence"]
		row["LettersPerWord"] = temp["Letters_Per_Word"]
		row["VocabSize"] = temp["Vocab_Size"]
	row["Gender"] = classifier.classify(gender_features(first_name(row["Name"])))

print df
	


def main():
	train = Extract_Features(HannahCorpus)
	train2 = Extract_Features(DuncanCorpus)
	train3 = Extract_Features(RichardCorpus)
	train_set = [(train,0), (train2,1), (train3,1)]

	test = {'Words_Per_Sentence':6,'Letters_Per_Word':19}
	test2 = {'Words_Per_Sentence':3,'Letters_Per_Word':6}
	test3 = {'Words_Per_Sentence':8,'Letters_Per_Word':10}
	test_set = [(test,1),(test2,0), (test3,1)]

	classifier = nltk.NaiveBayesClassifier.train(train_set)
	print nltk.classify.accuracy(classifier,test_set)


#print len(dun)
# Frequency distribution of words
#duncanFreq = FreqDist(DuncanCorpus)
#print duncanFreq.keys()[:10]
#print duncanFreq.values()[:10]


#text = nltk.Text(word.lower() for word in duncanTokens)
#print text.similar('and')

# Removes punctuation
#tokenizer = RegexpTokenizer(r' \w+')
#duncanTokens = tokenizer.tokenize(DuncanCorpus)

# Properly tokenises the object
#DuncanWords = nltk.word_tokenize(DuncanCorpus)
#sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
#Duncansentences = sent_tokenizer.tokenize(DuncanCorpus)






