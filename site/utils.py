import re
import spacy
import flask
from flask import Flask, render_template, request, flash, session
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
import gensim
from gensim.models import Word2Vec
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_data(text):
	try:
		if len(str(text)) > 0 and isinstance(text, str) == True:
			nlp = spacy.load('en_core_web_sm')
			nlp.max_length = 1500000
			stemmer = SnowballStemmer(language='english')
			text = remove_stopwords(text).lower()
			text = (re.sub("[^a-zA-Z]"," ",text)).rstrip().lstrip()
			return text
		else:
			return False
	except:
		return False


def get_data(df,text,query):
	try:
		if len(str(query)) > 0 and isinstance(query, str) == True and len(str(text)) > 0 and isinstance(text, list) == True:
			vectorizer = TfidfVectorizer()
			X = vectorizer.fit_transform(text)
			vectorizer.fit(text)
			vector = vectorizer.transform([query])
			results = cosine_similarity(X,vector).reshape((-1,))
			df['grades'] = results
			df = df.sort_values(by=['grades'], ascending=False)
			return df[['title','recommendations','artist','publisher','writer','genres','summary']].head(100)
		else:
			return False
	except:
		return False

def read_data(dataset):
	try:
		if len(str(dataset)) > 0 and isinstance(dataset, str) == True:
			df = pd.read_csv(dataset)
			if len(df) > 0 and isinstance(df, pd.DataFrame) == True:
				return df
			else:
				return False
		else:
			return False
	except:
		return False

def execute_search(input_data,search_field,df):
	try:
		query = clean_data(input_data)
		if query != False:
			text = df[search_field].values.tolist()
			df = get_data(df,text,query)	
			return df
		else:
			return False
	except:
		return False

def advanced_type_search(input_data,df,search_type):
	try:
		if search_type == 'title' and df['title'].str.contains(input_data).any() == True:
			print(input_data)
			df['occ'] = df['title'].str.contains(input_data) 
			df1 = df.loc[df['occ'] == True]
		elif search_type == 'genres' and df['genres'].str.contains(input_data).any() == True:
			df['occ'] = df['genres'].str.contains(input_data) 
			df1 = df.loc[df['occ'] == True]
		elif search_type == 'artist' and  df['artist'].str.contains(input_data).any() == True:
			df['occ'] = df['artist'].str.contains(input_data)
			df1 = df.loc[df['occ'] == True]
		elif search_type == 'publisher' and df['publisher'].str.contains(input_data).any() == True:
			df['occ'] = df['publisher'].str.contains(input_data)
			df1 = df.loc[df['occ'] == True]
		elif search_type == 'writer' and df['writer'].str.contains(input_data).any() == True:
			df['occ'] = df['writer'].str.contains(input_data)
			df1 = df.loc[df['occ'] == True]
		else:
			df1 == False
		return df1
	except:
		return False

def generate_answer(type_request,query,df):
	try:
		if len(type_request) > 0 and isinstance(type_request, str) == True and len(str(type_request)) > 0 and isinstance(type_request, str) == True and len(query) > 0 and isinstance(query, str) == True and len(str(query)) > 0 and isinstance(query, str) == True: 
			if str(type_request) == "title_search":
				df = execute_search(str(query),"title",df)	
				return df
			elif  str(type_request) == "plot_search":
				df = execute_search(str(query),"clean_summary",df)	
				return df
			else:
				return render_template("search.html")
		else:
			return render_template("search.html")
	except:
		return render_template("search.html")

