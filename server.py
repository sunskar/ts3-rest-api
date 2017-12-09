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
    @auth.login_required
    def get(self):
        return jsonify("username: " + auth.username())


class execute_command(Resource): # /<int:vserver>/command/<str:command>?key=value&key2=value2
    @auth.login_required
    def get(self, vserver, command):
        username = request.authorization.username
        password = request.authorization.password
        tn = api.connectToTelnet(HOST, PORT, vserver, username, password, '')
        response = {'response': api.sendCommand(command, request.args, tn, True)}
        return jsonify(response)


class get_channel_list(Resource): # /<int:vserver>/channel/
    @auth.login_required
    def get(self, vserver):
        username = request.authorization.username
        password = request.authorization.password
        tn = api.connectToTelnet(HOST, PORT, vserver, username, password, '')
        channellist = api.getChannelList(tn)
        content = {'total': len(channellist), 'items': channellist}
        return jsonify(content)


class get_channel(Resource): # /<int:vserver>/channel/<int:cid>
    @auth.login_required
    def get(self, cid, vserver):
        username = request.authorization.username
        password = request.authorization.password
        tn = api.connectToTelnet(HOST, PORT, vserver, username, password, '')
        
        return jsonify(api.getChannelByCid(cid, api.getChannelList(tn)))

class get_client_list(Resource): # /<int:vserver>/client/
    @auth.login_required
    def get(self, vserver):
        username = request.authorization.username
        password = request.authorization.password
        tn = api.connectToTelnet(HOST, PORT, vserver, username, password, '')
        clientlist = api.getClientList(tn)
        content = {'total': len(clientlist), 'items': clientlist}
        return jsonify(content)


class get_client(Resource): # /<int:vserver>/client/<int:cid>
    @auth.login_required
    def get(self, clid, vserver):
        username = request.authorization.username
        password = request.authorization.password
        tn = api.connectToTelnet(HOST, PORT, vserver, username, password, '')
        return jsonify(api.getClientByClid(clid, api.getClientList(tn)))

class poke_client(Resource): # /<int:vserver>/poke/<int:cild>?msg=hey\swake\sup!&nickname=Nickname
    @auth.login_required
    def get(self, clid, vserver):
        username = request.authorization.username
        password = request.authorization.password
        message = ''
        nickname = ''
        if hasattr(request, 'args'):
            if 'msg' in request.args:
                message = request.args['msg']
            if 'nickname' in request.args:
                nickname = request.args['nickname']
        tn = api.connectToTelnet(HOST, PORT, vserver, username, password, nickname)
        return jsonify(api.pokeClient(clid, tn, message))


#class message_server(Resource): # /<int:vserver>/message/<int:vserver>?msg=hey\swake\sup!&nickname=Nickname
    
#class message_channel(Resource): # /<int:vserver>/channel/message/<int:cid>?msg=hey\swake\sup!&nickname=Nickname
    
#class message_client(Resource): # /<int:vserver>/client/message/<int:cild>?msg=hey\swake\sup!&nickname=Nickname
    


@auth.verify_password
def verify(username, password):
    return api.checkCredentials(HOST, PORT, username, password)['msg'] == 'ok'


restapi.add_resource(root, "/")
restapi.add_resource(execute_command, "/<int:vserver>/command/<string:command>")
restapi.add_resource(get_channel_list, "/<int:vserver>/channel")
restapi.add_resource(get_channel, "/<int:vserver>/channel/<int:cid>")
restapi.add_resource(get_client_list, "/<int:vserver>/client")
restapi.add_resource(get_client, "/<int:vserver>/client/<int:clid>")
restapi.add_resource(poke_client, "/<int:vserver>/poke/<int:clid>")
#restapi.add_resource(message_server, "/<int:vserver>/message/<int:vserver>"
#restapi.add_resource(message_channel, "/<int:vserver>/message/<int:vserver>"
#restapi.add_resource(message_client, "/<int:vserver>/message/<int:vserver>"


if __name__ == "__main__":
    app.run(debug=True)

