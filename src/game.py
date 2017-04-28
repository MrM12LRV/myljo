
import socket
from time import sleep
import Tkinter
from sys import argv

def recv_char(s):
    try: return s.recv(1)
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
    s.connect((host, 8000))

    player_id = s.recv(1024)

    s.setblocking(0)

    window = Tkinter.Tk()
    c = Tkinter.Canvas(window, width = 400, height = 400)

    class Struct(object): pass
    data = Struct()

    data.p0x = 50; data.p0y = 50; data.p0r = 5
    data.p1x = 100; data.p1y = 100; data.p1r = 5
    data.c = c
    data.serversocket = s

    c.pack()
    c.update()
    window.bind("<Key>", lambda event: keyPressedHandler(event, data))

    def keyPressedHandler(event, data):
        # Update remote
        data.serversocket.send(event.char)
        print event.char
        # Update local
        if player_id == "0":
            if event.char == "w": data.p0y -= 5
            if event.char == "a": data.p0x -= 5
            if event.char == "s": data.p0y += 5
            if event.char == "d": data.p0x += 5
        if player_id == "1":
            if event.char == "w": data.p1y -= 5
            if event.char == "a": data.p1x -= 5
            if event.char == "s": data.p1y += 5
            if event.char == "d": data.p1x += 5

        data.c.delete(Tkinter.ALL)
        data.c.create_rectangle(0,0,400,400, fill="yellow")
        c.create_text(50,10, text="player: " + str(player_id))
        ccreate_rectangle(data.c, data.p0x, data.p0y, data.p0r, fill="blue")
        ccreate_rectangle(data.c, data.p1x, data.p1y, data.p1r, fill="red")


    def checkRecv(data):
        omove = recv_char(data.serversocket)

        if omove != None:
            if player_id == "0":
                if omove == "w": data.p1y -= 5
                if omove == "a": data.p1x -= 5
                if omove == "s": data.p1y += 5
                if omove == "d": data.p1x += 5
            if player_id == "1":
                if omove == "w": data.p0y -= 5
                if omove == "a": data.p0x -= 5
                if omove == "s": data.p0y += 5
                if omove == "d": data.p0x += 5

        data.c.delete(Tkinter.ALL)
        data.c.create_rectangle(0,0,400,400, fill="yellow")
        c.create_text(50,10, text="player: " + str(player_id))
        ccreate_rectangle(data.c, data.p0x, data.p0y, data.p0r, fill="blue")
        ccreate_rectangle(data.c, data.p1x, data.p1y, data.p1r, fill="red")

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