import telnetlib

def connectToTelnet(host, port, vserver, user, password, nickname):
    telnet = telnetlib.Telnet(host, port)    
    telnet.read_until('\n\r')
    telnet.read_until('\n\r')
    
    error = sendCommand('login ' + user + ' ' + password, {}, telnet, False)
    if error['msg'] != 'ok':
        return error
    
    error = sendCommand('use ' + str(vserver), {}, telnet, False)
    if error['msg'] != 'ok':
        return error
    
    whoami = sendCommand('whoami', {}, telnet, True)
    whoami = parseResponseToDictionary(whoami)
    if nickname == '':
        nickname = whoami['client_nickname'][:whoami['client_nickname'].index('\\s')] + '\svia\sAPI'
    sendCommand('clientupdate', {'client_nickname': str(nickname)}, telnet, False)
    return telnet
    

def checkCredentials(host, port, user, password):
    telnet = telnetlib.Telnet(host, port)    
    telnet.read_until('\n\r')
    telnet.read_until('\n\r')
    telnet.write('login ' + user + ' ' + password + '\r\n')
    return getErrorResponse(telnet)

def getChannelList(telnet):
    channellist = sendCommand('channellist', {}, telnet, True)
    channels = channellist.split('|')
    list_of_channels = []
    for channel in channels:
        cid = parseResponseToDictionary(channel)['cid']
        info = sendCommand('channelinfo', {'cid': cid}, telnet, True)
        info = parseResponseToDictionary(info)
        info['cid'] = cid
        list_of_channels.append(info)
    return list_of_channels


def getChannelByCid(cid, list_of_channels):
    for channel in list_of_channels:
        if int(channel['cid']) == int(cid):
            return channel
    return -1


def getClientList(telnet):
    clientlist = sendCommand('clientlist', {}, telnet, True)
    clients = clientlist.split('|')
    list_of_clients = [] 
    for client in clients:
        clid = parseResponseToDictionary(client)['clid']
        info = sendCommand('clientinfo', {'clid': clid}, telnet, True)
        info = parseResponseToDictionary(info)
        info['clid'] = clid
        list_of_clients.append(info)
    return list_of_clients


def getClientByClid(clid, list_of_clients):
    for client in list_of_clients:
        if int(client['clid']) == int(clid):
            return client
    return -1


def parseResponseToDictionary(response):
    iteminfo = {}
    for item in response.split(' '):
        if '=' not in str(item):
            iteminfo['message_type'] = item
        else:
            info = item.split('=')
            iteminfo [info[0]] = info[1]
    return iteminfo


def getErrorResponse(telnet):
    response = telnet.read_until('\n\r')[:-2]
    if response == '':
        return 'no error found'
    return parseResponseToDictionary(response)


def pokeClient(clid, telnet, message):
    response = sendCommand( 'clientpoke', { 'clid': clid, 'msg': message }, telnet, False )
    return response


def sendCommand(command, params, telnet, expect_response):
    for param in params:
        command = command + ' ' + str(param) + '=' + str(params[param])
    telnet.write( str(command) + '\r\n' )
    if expect_response:
        response = telnet.read_until('\n\r')
    error = getErrorResponse(telnet)
    if error['msg'] != 'ok':
        return error
    if expect_response:
        return response.decode('string_escape')
    else:
        return error
