from flask import Flask, jsonify
from markupsafe import escape
from generated_doa_list import generated_doa_list
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import operator

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def index():
    result = {
        "name": "Tanyadoa API",
        "author": {
            "name" : "Miftah Afina",
            "email": "surat@miftahafina.com",
            "blog" : "miftahafina.com"
        },
        "endpoints": {
            "/all": "Get all doa",
            "/search/<keywords>": "Search doa by keywords",
            "/show/<id_doa>": "Search doa by id_doa",
        }
    }

    return jsonify(result)


@app.route("/all")
def all():
    result = {
        "code"   : 200,
        "message": "Success",
        "data"   : generated_doa_list
    }

    return jsonify(result)


@app.route("/show/<id_doa>")
def show(id_doa):
    id_doa = escape(id_doa)
    result = {
        "code"   : None,
        "message": None,
        "data": []
    }

    for doa in generated_doa_list:
        if doa["id_doa"] == id_doa:
            result["data"].append(doa)

    if result["data"]:
        result["code"]    = 200
        result["message"] = "Success"
    else:
        result["code"]    = 404
        result["message"] = "Not Found"

    return jsonify(result)


@app.route("/search/<search_query>")
def search(search_query):
    search_query = escape(search_query)
    stemmer      = StemmerFactory().create_stemmer()
    query_list   = stemmer.stem(search_query).split(" ")
    result_list  = []
    final_result = {
        "code"   : None,
        "message": None,
        "data": []
    }

    for query in query_list:
        for doa in generated_doa_list:
            if query != "doa" and query in doa["kata_kunci"]:
                if not any(result["id_doa"] == doa["id_doa"] for result in result_list):
                    # does not exists in result_list
                    result_list.append({
                        "id_doa"   : doa["id_doa"],
                        "kecocokan": 1,
                        # "nama" : doa["nama"],
                        # "kata_kunci" : " ".join(doa["kata_kunci"]),
                        "doa_data" : doa
                    })
                else:
                    # exists in result_list
                    for result in result_list:
                        if result["id_doa"] == doa["id_doa"]:
                            result["kecocokan"] += 1

    if result_list:
        result_list.sort(key=operator.itemgetter("kecocokan"), reverse=True)
        # return jsonify(result_list) # comment this line on production server

        highest_kecocokan = result_list[0]["kecocokan"]

        for result in result_list:
            if highest_kecocokan == result["kecocokan"]:
                result["doa_data"]["kecocokan"] = result["kecocokan"]
                final_result["data"].append(result["doa_data"])

        final_result["code"]    = 200
        final_result["message"] = "Success"

    else:
        final_result["code"]    = 404
        final_result["message"] = "Not Found"

    return jsonify(final_result)
