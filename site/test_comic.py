import re
import spacy
from nltk.tokenize import word_tokenize
import nltk
import utils
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
import gensim
from gensim.models import Word2Vec
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def test_clean_data2():
	assert utils.clean_data('') == False

def test_clean_data3():
	assert utils.clean_data(1) == False

def test_read_data2():
	assert utils.read_data('') == False

def test_read_data3():
	assert utils.read_data(4) == False
