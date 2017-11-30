# flask server for handling the requests

from flask import Flask, jsonify
import api

HOST = '127.0.0.1'
PORT = '10011'
USER = 'serveradmin'
PASS = 'v8yL9+VH'

tn = api.connectToTelnet(HOST, PORT, USER, PASS)

app = Flask(__name__)


@app.route('/')
def index():
    return "useful help text"


@app.route('/<int:vserver>/channels/', methods=['GET'])
def get_channels(vserver):
    return jsonify( api.getChannelList(tn) )


@app.route('/<int:vserver>/channels/<int:cid>', methods=['GET'])
def get_channel(vserver ,cid):
    return jsonify( api.getChannelByCid(cid, api.getChannelList(tn)) )


if __name__ == "__main__":
    app.run(debug=True)

