
import socket
import game
import Tkinter
from draw_util import ccreate_rectangle
from time import sleep

def recv_char(s):
    try: return s.recv(1)
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
    while True:

        print "Server: Waiting for player " + str(found_players)
        (clientsocket, address) = serversocket.accept()

        player_id = found_players
        players += [Player(clientsocket, address, player_id)]
        clientsocket.send(str(player_id))

        clientsocket.send(str(player_id))
        found_players += 1

        wait_for_more = raw_input("Wait for more players?[Y/n] ")
        if wait_for_more.lower() == "y":
            continue
        elif wait_for_more.lower() == "n":
            break

    return players

serversocket = None
p1, p2 = None, None
def run_server():
    global serversocket, p1, p2

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(), 8000))
    serversocket.listen(5)

    players = waitForPlayers(serversocket)
    for i in xrange(len(players)):
        players[i].clientsocket.setblocking(0) # non-blocking

    root = Tkinter.Tk()
    c = Tkinter.Canvas(root, width = 100, height = 100)
    c.pack()
    c.create_rectangle(0,0,400,400, fill="black")

    class Struct(object): pass
    data = Struct()
    data.players = players

    def serverRecv(data):
        moves = [None]*len(data.players)
        for i in xrange(len(data.players)):
            moves[i] = recv_char(data.players[i].clientsocket)

        for i in xrange(len(moves)):
            if moves[i] != None:
                for j in xrange(len(moves)):
                    if i != j:
                        data.players[j].clientsocket.send(moves[i])

    def timerCallback(data):
        serverRecv(data)
        c.after(100, timerCallback, data)
    timerCallback(data)

    root.mainloop()

if __name__ == "__main__":
    #try:
    run_server()
    #except Exception as e:
    #    serversocket.close()
    #    #p1.clientsocket.close()
    #    #p2.clientsocket.close()
    #    print "Closed server:", e.message, e.args