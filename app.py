from flask import Flask, jsonify
# from markupsafe import escape
from doa_list import doa_list

app = Flask(__name__)

@app.route("/show/<id>")
def show(id):
    return jsonify(doa_list[int(id)])
