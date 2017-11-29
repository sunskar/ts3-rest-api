import telnetlib

def connectToTelnet(host, port, user, password):
    telnet = telnetlib.Telnet(host, port)
    print telnet.read_until('\n\r')
    print telnet.read_until('\n\r')
    telnet.write('login ' + user + ' ' + password + '\r\n')
    print telnet.read_until('\n\r')
    telnet.write('use 1\r\n')
    print telnet.read_until('\n\r')
    telnet.write('whoami\r\n')
    whoami = parseResponseToDictionary(telnet.read_until('\n\r')[:-2])
    print telnet.read_until('\n\r')
    telnet.write('clientupdate client_nickname=' + whoami['client_nickname'][:whoami['client_nickname'].index('\\s')] + '\svia\sAPI\r\n')
    print telnet.read_until('\n\r')  
    return telnet


def getChannelList(telnet):
    telnet.write('channellist\r\n')
    channellist = telnet.read_until('\n\r')[:-2]
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
        info = item.split('=')
        if '=' in str(item): 
            iteminfo[info[0]] = info[1]
        else:
            iteminfo[info[0]] = ''

    return iteminfo

def pokeClient(clid, telnet, message):
    telnet.write( 'clientpoke clid=' + str(clid) + ' msg=' + str(message) + '\r\n')
    response = telnet.read_until('\n\r')
    if response == 'error id=0 msg=ok\n\r':
        return response
    else:
        return response

def sendCommand(command, params, telnet, expect_response):
    #works if we're lucky, pls clean up at some point
    cmd = ''
    for param in command.split(' '):
        if str(param)[-1:] == '=':
            cmd = cmd + ' ' + param + params[param[:-1]]
    command = command[:command.index(' ')] + cmd
    print ( str(command) + '\r\n' )
    telnet.write( str(command) + '\r\n' )
    if expect_response:
        response = telnet.read_until('\n\r')
    error = telnet.read_until('\n\r')
    if error != 'error id=0 msg=ok\n\r':
        return error
    if expect_response:
        return response
    else:
        return error
