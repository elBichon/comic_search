from flask import Flask, render_template, request, flash, session
import re
import utils
from elasticsearch import Elasticsearch
import os
es = Elasticsearch('127.0.0.1', port=9200)
app = Flask(__name__)

@app.route("/") 
def home():
	return render_template("index.html")

@app.route("/search", methods=["POST", "GET"]) 
def suscribe():
	try:
		if request.method == "POST":
			if len(str(request.form["search_text"])) > 0 and isinstance(request.form["search_text"], str) == True:
				text = str(request.form["search_text"])
				res = es.search(
				index='movies',
				body={
				"query": {"multi_match": {"query":text,"fields": ["fields.plot","fields.title"]}}})
				print(res)
				return render_template("search.html", res=res)
			else:
				flash("Some informations are missing or incorrect","info")
				return render_template("search.html")
		else:
			return render_template("search.html")
	except:
		return render_template("search.html")

if __name__ == "__main__":
	app.debug = True
	app.run()
