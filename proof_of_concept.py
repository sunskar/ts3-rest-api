import ts3_rest_api as tra


def main():

    HOST = 'host'
    PORT = '10011'
    USER = 'user'
    PASS = 'pass'
    
    tn = tra.connectToTelnet(HOST, PORT, USER, PASS)
    list_of_channels = tra.getChannelList(tn)
    print tra.getChannelByCid(8, list_of_channels)['channel_name']
    for client in tra.getClientList(tn):
        if client['client_type'] != '0':
            continue
        print (str(client['client_nickname']) + ' - ' + str(tra.getChannelByCid(client['cid'], list_of_channels)['channel_name']))

if __name__ == "__main__":
    main()

