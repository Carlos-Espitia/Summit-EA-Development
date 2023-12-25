import socket 
import threading

# multiple servers 
# create a event listener

class Server:
    def __init__(self, host="127.0.0.1", port=50000, maxByte=1024): # make this more custom later
        # server information
        self.SERVER = host
        PORT = port
        ADDR = (self.SERVER, PORT)
        self.HEADER = maxByte # amount of bytes
        self.FORMAT = 'utf-8' 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)

    def start(self):
        self.server.listen()
        print(f"[SERVER] Server is listening on {self.SERVER}")
        while True: # always active listeneing for connections
            conn, addr = self.server.accept() # accepts connections and gets their con and address
            # make a thread for each connection and run handle_client on them
            thread = threading.Thread(target=self._handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def _handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_header = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_header:
                msg_length = int(msg_header.strip())
                msg = conn.recv(msg_length).decode(self.FORMAT)
                print(f"[{addr}] {msg}")
            else:
                print("Client disconnected")
                connected = False
        
        conn.close() # close connection
