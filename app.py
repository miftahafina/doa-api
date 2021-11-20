from flask import Flask, jsonify
from markupsafe import escape
from doa_list import doa_list
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(doa_list)

@app.route("/show/<doa_id>")
def show(doa_id):
    doa_id = escape(doa_id)
    result = []

    for doa in doa_list:
        if doa['doa_id'] == doa_id:
            result.append(doa)

    return jsonify(result)

@app.route("/stem/<query>")
def stem(query):
    query = escape(query)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    return stemmer.stem(query)
