
import socket
from time import sleep
import Tkinter
from sys import argv

def recv_char(s):
    try: return s.recv(2)
    except: return None

def ccreate_rectangle(canvas, cx, cy, r, fill="white", outline="black"):
    canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, fill=fill, outline=outline)

def run_client():
    global s
    #create an INET, STREAMing socket
    while True:
        try: s = socket.socket()
        except: print "########Exception########"; continue
        break

    host = socket.gethostname() if len(argv) <= 1 else argv[1]
    s.connect(("128.237.162.17", 8000))

    player_id = int(s.recv(1024))

    s.setblocking(0)

    window = Tkinter.Tk()
    c = Tkinter.Canvas(window, width = 400, height = 400)

    class Struct(object):
        def __str__(self): return "("+str(self.x)+","+str(self.y)+","+str(self.r)+")"
        def __repr__(self): return self.__str__()

    data = Struct()

    data.players_pos = [Struct(), Struct(), Struct()]
    for i in xrange(len(data.players_pos)):
        data.players_pos[i].x = 20 * i
        data.players_pos[i].y = 50
        data.players_pos[i].r = 5
    data.c = c
    data.serversocket = s

    c.pack()
    c.update()
    window.bind("<Key>", lambda event: keyPressedHandler(event, data))

    def drawBoard(data):
        colors = ["blue", "red", "green", "black", "white", "purple", "yellow"]
        data.c.delete(Tkinter.ALL)
        data.c.create_rectangle(0,0,400,400, fill="yellow")
        c.create_text(50,10, text="player: " + str(player_id))
        for i in xrange(len(data.players_pos)):
            ccreate_rectangle(data.c,
                              data.players_pos[i].x,
                              data.players_pos[i].y,
                              data.players_pos[i].r, fill=colors[i%len(colors)])

    def keyPressedHandler(event, data):
        # Update remote
        to_send = str(player_id) + event.char
        print to_send
        assert(len(to_send) == 2)
        data.serversocket.send(to_send)

        print event.char
        # Update local
        player_idx = int(player_id)

        if event.char == "w": data.players_pos[player_idx].y -= 5
        if event.char == "a": data.players_pos[player_idx].x -= 5
        if event.char == "s": data.players_pos[player_idx].y += 5
        if event.char == "d": data.players_pos[player_idx].x += 5

        drawBoard(data)




    def checkRecv(data):
        # TODO: change what a message looks like.  We need to know where it
        #   is coming from here.
        recv_data = recv_char(data.serversocket)

        player_idx = int(player_id)
        if recv_data != None and recv_data[0] == player_id: return
        if recv_data != None:
            print player_idx, "is receiving from", recv_data[0]
            print recv_data
            assert(len(recv_data) == 2)
            node_from, omove = recv_data[0], recv_data[1]
            assert("0" <= node_from <= "9")
            node_from = int(node_from)
            if omove == "w": data.players_pos[node_from].y -= 5
            if omove == "a": data.players_pos[node_from].x -= 5
            if omove == "s": data.players_pos[node_from].y += 5
            if omove == "d": data.players_pos[node_from].x += 5



            drawBoard(data)
        print data.players_pos

    def timerCallback(data):
        checkRecv(data)
        c.after(100, timerCallback, data)
    timerCallback(data)

    window.mainloop()

    s.close()


if __name__ == "__main__":
    #try:
    run_client()
    #except Exception as e:
    #    print "Client error:", e.message
    #    s.close()
