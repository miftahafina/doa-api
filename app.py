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
        if doa["id_doa"] == id_doa:
            result.append(doa)

    return jsonify(result)


@app.route("/stem/<query>")
def stem(query):
    query   = escape(query)
    stemmer = StemmerFactory().create_stemmer()

    return stemmer.stem(query)


@app.route("/generate-kata-kunci")
def generate_kata_kunci():
    kata_kunci_list = []
    stemmer         = StemmerFactory().create_stemmer()

    for doa in doa_list:
        nama_doa_stem     = stemmer.stem(doa["nama"])
        kata_kunci_list   = nama_doa_stem.split(" ")
        doa["kata_kunci"] = kata_kunci_list

        file = open("generated_doa_list.py", "w")
        file.write(str(doa_list))
        file.close

    return jsonify(doa_list)
