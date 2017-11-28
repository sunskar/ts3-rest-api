import telnetlib


def connectToTelnet(host, port, user, password):
    telnet = telnetlib.Telnet(host, port)
    telnet.read_until('\n\r')
    telnet.read_until('\n\r')
    telnet.write('login ' + user + ' ' + password + '\r\n')
    telnet.read_until('\n\r')
    telnet.write('use 1\r\n')
    telnet.read_until('\n\r')
    telnet.write('whoami\r\n')
    whoami = parseResponseToDictionary(telnet.read_until('\n\r')[:-2])
    telnet.read_until('\n\r')
    telnet.write('clientupdate client_nickname=' + whoami['client_nickname'][:whoami['client_nickname'].index('\\s')] + '\svia\sAPI\r\n')
    telnet.read_until('\n\r')  
    return telnet


def getChannelList(telnet):

    telnet.write('channellist\r\n')
    channellist = telnet.read_until('\n\r')[:-2]
    telnet.read_until('\n\r')
    channels = channellist.split('|')
    list_of_channels = []
    for channel in channels:
        channelinfo = {}
        for token in channel.split(' '):
            info = token.split('=')
            channelinfo[info[0]] = info[1]
        list_of_channels.append(channelinfo)
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
