
import socket
from time import sleep
import Tkinter
from sys import argv

def client_thread(clientsocket):
    print "Client: In client thread"
    print dir(clientsocket)

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

    window = Tkinter.Tk()
    c = Tkinter.Canvas(window, width = 100, height = 100)
    c.pack()
    c.update()
    window.bind("<Key>", lambda event: s.send(event.char))

    window.mainloop()

    s.close()


if __name__ == "__main__":
    try:
        run_client()
    except Exception as e:
        print "Client error:", e.message
        s.close()