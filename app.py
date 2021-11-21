from flask import Flask, jsonify
from markupsafe import escape
from doa_list import doa_list
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(doa_list)

@app.route("/show/<id_doa>")
def show(id_doa):
    id_doa = escape(id_doa)
    result = []

    for doa in doa_list:
        if doa['id_doa'] == id_doa:
            result.append(doa)

    return jsonify(result)

@app.route("/stem/<query>")
def stem(query):
    query = escape(query)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    return stemmer.stem(query)
