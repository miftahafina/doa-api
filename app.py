import random
from flask import Flask, jsonify
from markupsafe import escape
from doa_list import doa_list
from generated_doa_list import generated_doa_list
from random import randint

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)

@app.route("/")
def index():
    random = randint(1,9999)
    dict1 = {
        random: 0
    }

    dict1[random] += 1

    return jsonify(dict1)


@app.route("/show/<id_doa>")
def show(id_doa):
    id_doa = escape(id_doa)
    result = []

    for doa in doa_list:
        if doa["id_doa"] == id_doa:
            result.append(doa)

    return jsonify(result)


@app.route("/search/<query>")
def search(query):
    query       = escape(query)
    stemmer     = StemmerFactory().create_stemmer()
    query_stem  = stemmer.stem(query)
    query_list  = query_stem.split(' ')
    result_list = []

    random_value = randint(0, 9999)

    copied_generated_doa_list = {}
    copied_generated_doa_list[random_value] = generated_doa_list.copy()
    # return jsonify(copied_generated_doa_list)

    for item in query_list:
        for doa in copied_generated_doa_list[random_value]:
            if item != "doa" and item in doa['kata_kunci']:
                doa['peringkat'] += 1
                result_list.append(doa)

    # Setelah ini dimasukkan ke peringkat, sorting dan tampilkan yang teratas
    # peringkat terus bertambah jika refresh/reload halaman

    return jsonify(result_list)


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
        file.write(f"generated_doa_list = {str(doa_list)}")
        file.close

    return jsonify(doa_list)
