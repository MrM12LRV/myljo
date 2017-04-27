
import socket
import game_util

def run():
    print "Hi Myles, you are a(n)" + game_util.add_strings("dank","meme")

    result = game_util.add_numbers(3,5)

    return result

def client_thread(clientsocket):
    print "Client: In client thread"
    print dir(clientsocket)

def run_client():
    print "Client: In client"

    #create an INET, STREAMing socket
    while True:
        try: s = socket.socket()
        except: print "########Exception########"; continue
        break
    print "Client: created socket"
    s.connect((socket.gethostname(), 12348))
    print "Client: connected"
    while True: pass
    print "Client:", s.recv(1024)
    s.close()


if __name__ == "__main__":
    run_client()