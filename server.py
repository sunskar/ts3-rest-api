# flask server for handling the requests

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import api

HOST = '127.0.0.1'
PORT = '10011'

app = Flask(__name__)
restapi = Api(app)
auth = HTTPBasicAuth()


class root(Resource): # /
    def get(self):
        return "useful help text"


class execute_command(Resource): # /<str:command>?param=""
    @auth.login_required
    def get(self, command):
        username = request.authorization.username
        password = request.authorization.password
        tn = api.connectToTelnet(HOST, PORT, username, password)
        param = request.args.get("param")
        return jsonify(api.sendCommand(command, param, tn, True))


class get_channel_list(Resource): # /<int:vserver>/channel/
    @auth.login_required
    def get(self, vserver):
        return jsonify("return channellist from virtualsever"+str(vserver))


class get_channel(Resource): # /<int:vserver>/channel/<int:cid>
    @auth.login_required
    def get(self, cid, vserver):
        return jsonify("return channelinfo on channel with"+str(cid)+"at virtualserver"+str(vserver))


@auth.verify_password
def verify(username, password):
    return username == password


restapi.add_resource(root, "/")
restapi.add_resource(execute_command, "/<string:command>")
restapi.add_resource(get_channel_list, "/<int:vserver>/channel")
restapi.add_resource(get_channel, "/<int:vserver>/channel/<int:cid>")

if __name__ == "__main__":
    app.run(debug=True)

