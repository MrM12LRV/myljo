
import socket
import game_util
from time import sleep
import Tkinter

def run():
    print "Hi Myles, you are a(n)" + game_util.add_strings("dank","meme")

    result = game_util.add_numbers(3,5)

    return result

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

    s.connect((socket.gethostname(), 12348))

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