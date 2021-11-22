from flask import Flask, json, jsonify
from markupsafe import escape
from doa_list import doa_list
from generated_doa_list import generated_doa_list
import operator

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)

@app.route("/")
def index():
    result = {
        "data": generated_doa_list
    }

    return jsonify(result)


@app.route("/show/<id_doa>")
def show(id_doa):
    id_doa = escape(id_doa)
    result = {
        "data": []
    }

    for doa in generated_doa_list:
        if doa["id_doa"] == id_doa:
            result["data"].append(doa)

    return jsonify(result)


@app.route("/search/<search_query>")
def search(search_query):
    search_query = escape(search_query)
    stemmer      = StemmerFactory().create_stemmer()
    query_list   = stemmer.stem(search_query).split(" ")
    result_list  = []

    for query in query_list:
        for doa in generated_doa_list:
            if query != "doa" and query in doa["kata_kunci"]:
                if not any(result["id_doa"] == doa["id_doa"] for result in result_list):
                    # does not exists
                    result_list.append({
                        "id_doa"   : doa["id_doa"],
                        "kecocokan": 1,
                        # "nama" : doa["nama"],
                        # "kata_kunci" : ' '.join(doa["kata_kunci"])
                        "doa_data" : doa
                    })
                else:
                    # exists
                    for result in result_list:
                        if result["id_doa"] == doa["id_doa"]:
                            result["kecocokan"] += 1

    # check if not empty
    if result_list:
        # sort desc by kecocokan
        result_list.sort(key=operator.itemgetter('kecocokan'), reverse=True)

        # check kecocokan tertinggi ganda
        highest_kecocokan      = result_list[0]['kecocokan']
        # jumlah_kecocokan_ganda = 0
        final_result = {
            "data": []
        }
        
        for result in result_list:
            if highest_kecocokan == result['kecocokan']:
                # jumlah_kecocokan_ganda += 1
                result['doa_data']['kecocokan'] = result['kecocokan']
                final_result["data"].append(result['doa_data'])

        return jsonify(final_result)

    else:
        return jsonify({'status': 'Tidak ditemukan'})


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
