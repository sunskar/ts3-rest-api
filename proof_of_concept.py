import api


def main():

    HOST = 'host'
    PORT = '10011'
    USER = 'user'
    PASS = 'pass'
    
    tn = api.connectToTelnet(HOST, PORT, USER, PASS)
    list_of_channels = api.getChannelList(tn)
    print api.getChannelByCid(8, list_of_channels)['channel_name']
    for client in api.getClientList(tn):
        if client['client_type'] != '0':
            continue
        print (str(client['client_nickname']) + ' - ' + str(api.getChannelByCid(client['cid'], list_of_channels)['channel_name']))


if __name__ == "__main__":
    main()

