
import socket
import game

def run_server():
    print "Server: In server."

    serversocket = socket.socket()
    print "Server: Created socket"

    #bind the socket to a public host,
    # and a well-known port
    serversocket.bind((socket.gethostname(), 12348))
    print "Server: binded socket"

    #become a server socket
    serversocket.listen(5)
    print "Server: made socket a server socket"

    while True:
        #accept connections from outside
        print "Server: Waiting for client."
        (clientsocket, address) = serversocket.accept()

        #now do something with the clientsocket
        #in this case, we'll pretend this is a threaded server
        print "Server: clientsocket", clientsocket, "-- address:", address
        clientsocket.send("Hi Client from Server")
        clientsocket.close()



if __name__ == "__main__":
    run_server()