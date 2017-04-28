
import socket
import game
import Tkinter
from draw_util import ccreate_rectangle
from time import sleep

NUM_PLAYERS = 2

def recv_char(socket):
    try: return socket.recv(1)
    except: return None

class Player(object):
    def __init__(self, clientsocket, address, player_id):
        self.clientsocket = clientsocket
        self.address = address
        self.player_id = player_id
    def __str__(self):
        return "Player" + str(self.player_id) + ": { " + \
               "clientsocket = " + str(self.clientsocket) + ", " + \
               "address = " + str(self.address) + " }"
    def __repr__(self):
        return self.__str__()

def waitForPlayers(serversocket):
    players = []
    found_players = 0
    while found_players < NUM_PLAYERS:

        print "Server: Waiting for player " + str(found_players)
        (clientsocket, address) = serversocket.accept()

        player_id = found_players
        players += [Player(clientsocket, address, player_id)]
        clientsocket.send(str(player_id))

        clientsocket.send(str(player_id))
        found_players += 1

    return players[0], players[1]

serversocket = None
p1, p2 = None, None
def run_server():
    global serversocket, p1, p2
    print "Server: In server."

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Server: Created socket"

    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #bind the socket to a public host,
    # and a well-known port
    serversocket.bind((socket.gethostname(), 8000))
    print "Server: binded socket"
    #become a server socket
    serversocket.listen(5)
    print "Server: made socket a server socket"


    p1, p2 = waitForPlayers(serversocket)
    p1.clientsocket.setblocking(0)
    p2.clientsocket.setblocking(0)

    root = Tkinter.Tk()
    c = Tkinter.Canvas(root, width = 400, height = 400)
    c.pack()
    c.create_rectangle(0,0,400,400, fill="yellow")

    class Struct(object): pass
    data = Struct()

    data.p1x = 50; data.p1y = 50; data.p1r = 5
    data.p2x = 100; data.p2y = 100; data.p2r = 5
    data.c = c
    data.p1 = p1
    data.p2 = p2

    def checkRecv(data):
        data.c.delete(Tkinter.ALL)
        data.c.create_rectangle(0,0,400,400, fill="yellow")
        ccreate_rectangle(data.c, data.p1x, data.p1y, data.p1r, fill="blue")
        ccreate_rectangle(data.c, data.p2x, data.p2y, data.p2r, fill="red")

        p1move = recv_char(data.p1.clientsocket)
        p2move = recv_char(data.p2.clientsocket)

        if p1move != None:
            if p1move == "w": data.p1y -= 5
            if p1move == "s": data.p1y += 5
            if p1move == "a": data.p1x -= 5
            if p1move == "d": data.p1x += 5
            print "P1:", p1move
        if p2move != None:
            if p2move == "w": data.p2y -= 5
            if p2move == "s": data.p2y += 5
            if p2move == "a": data.p2x -= 5
            if p2move == "d": data.p2x += 5
            print "P2:", p2move

    def me(data):
        checkRecv(data)
        c.after(100, me, data)
    me(data)
    root.mainloop()

if __name__ == "__main__":
    try:
        run_server()
    except Exception as e:
        serversocket.close()
        p1.clientsocket.close()
        p2.clientsocket.close()
        print "Closed server:", e.message, e.args