import telnetlib

def connectToTelnet(host, port, user, password):
    telnet = telnetlib.Telnet(host, port)    
    print telnet.read_until('\n\r')
    print telnet.read_until('\n\r')
    telnet.write('login ' + user + ' ' + password + '\r\n')
    print getErrorResponse(telnet)
    telnet.write('use 1\r\n')
    print getErrorResponse(telnet)
    telnet.write('whoami\r\n')
    whoami = parseResponseToDictionary(telnet.read_until('\n\r')[:-2])
    print getErrorResponse(telnet)
    telnet.write('clientupdate client_nickname=' + whoami['client_nickname'][:whoami['client_nickname'].index('\\s')] + '\svia\sAPI\r\n')
    print getErrorResponse(telnet)
    return telnet


def getChannelList(telnet):
    telnet.write('channellist\r\n')
    channellist = telnet.read_until('\n\r')[:-2]
    print channellist + '\n channellist is aboove \n'
    telnet.read_until('\n\r')
    channels = channellist.split('|')
    list_of_channels = []
    for channel in channels:
        list_of_channels.append( parseResponseToDictionary(channel) )
    return list_of_channels


def getChannelByCid(cid, list_of_channels):
    for channel in list_of_channels:
        if int(channel['cid']) == int(cid):
            return channel
    return -1


def getClientList(telnet):
    telnet.write('clientlist\r\n')
    clientlist = telnet.read_until('\n\r')[:-2]
    telnet.read_until('\n\r')
    clients = clientlist.split('|')
    list_of_clients = [] 
    for client in clients:
        list_of_clients.append( parseResponseToDictionary(client) )
    return list_of_clients


def parseResponseToDictionary(response):
    iteminfo = {}
    for item in response.split(' '):
        if '=' not in str(item):
            iteminfo['message_type'] = item
        else:
            info = item.split('=')
            iteminfo[info[0]] = info[1]
    return iteminfo


def getErrorResponse(telnet):
    print '-\n-\ngetErrorResponse\n-\n-'
    response = telnet.read_until('\n\r')[:-2]
    if response == '':
        return 'no error found'
    print response
    error = parseResponseToDictionary(response)
    print error
    return error


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
    if error != 'error id=0 msg=ok\n\r':
        return error
    if expect_response:
        return response
    else:
        return error
