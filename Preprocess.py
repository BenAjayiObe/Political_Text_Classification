from bs4 import BeautifulSoup
import csv
import pandas as pd
from pandas import DataFrame, Series

def Exract_Name_Text_TWFY(Name, soup):
	DuncanCorpus=""
	for tag in soup.findAll("speech", {"speakername":Name}):
		DuncanCorpus += ' ' + tag.get_text().replace("\n", " ").rstrip()
	return DuncanCorpus

def switch(name):
	temp = name
	temp = temp.split()
	if len(temp)==2:
		return temp[1] + " " + temp[0]
	elif len(temp)==3:
		return temp[1] + " " + temp[2] + " " + temp[0]
	else:
		return name

hansard = open("data/scrapedxml/debates/debates2015-12-07b.xml", "r")
hanSoup = BeautifulSoup(hansard, 'xml')

df = DataFrame(pd.read_csv("MP_Party_Constituent.csv"))
df.colmuns = ["Name","Party","Constituent"]
df["Corpus"] = ""


for index, row in df.iterrows():
	corpus = Exract_Name_Text_TWFY(switch(row["Name"]), hanSoup)
	if len(corpus) > 0:
		row["Corpus"] = corpus

print df