import socket 
import threading

from API.utils import Utils

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
        self.connections = []
        self.lock = threading.Lock()  # A lock to protect the connections list
        self.DISCONNECTION = "!DISCCONNECTED"
        self.textSeperator = "~"
        self.server.setblocking(False) # Set the server socket to non-blocking mode     

    def loop(self):
        try:
            conn, addr = self.server.accept() # accepts connections and gets their con and address
            # make a thread for each connection and run handle_client on them
            with self.lock:  # Ensure thread-safe modification of the connections list
                self.connections.append(conn)
            thread = threading.Thread(target=self._handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {len(self.connections)}")
        except BlockingIOError:
            # No client is trying to connect right now
            pass  # Do nothing or handle as needed

    def start(self):
        self.server.listen()
        print(f"[SERVER] Server is listening on {self.SERVER}")
        Utils.setInterval(self.loop, 0) # always listening on connections

    def _handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.send("You have connected!".encode(self.FORMAT))

        connected = True

        while connected:
            try:

                # decoding shit
                # print(f"{conn.recv(self.HEADER)} | {conn.recv(self.HEADER).decode(self.FORMAT)} | {conn.recv(self.HEADER).decode(self.FORMAT).strip()}")
                msgCoded = conn.recv(self.HEADER) # use this to check for messages since it takes time to decode
                msg = conn.recv(self.HEADER).decode(self.FORMAT).strip()

                if msg == self.DISCONNECTION: connected = False

                if msgCoded == b'ping\x00': 
                    continue  # Skip further processing for 'ping'
                
                if msg: print(f"[{addr}] {msg}")

                    
            except ConnectionResetError:
                connected = False  # Consider if you want to disconnect or continue trying
                pass
            except ValueError as e:
                # print(f"There was a problem with | {addr} | {e}")
                connected = False  # Consider if you want to disconnect or continue trying
                pass

        with self.lock:
            if conn in self.connections:
                self.connections.remove(conn)

        print("Client disconnected")    
        conn.close() # close connection
    
    def send(self, msg):
        msg = self.textSeperator + msg
        for conn in self.connections[:]:
            try:
                conn.send(msg.encode(self.FORMAT))
            except ConnectionResetError:
                with self.lock:
                    if conn in self.connections:
                        self.connections.remove(conn)
                print(f"Connection was reset by the client during sending.")
            except Exception as e:
                print(f"An error occurred while sending message: {e}")

server = Server()

