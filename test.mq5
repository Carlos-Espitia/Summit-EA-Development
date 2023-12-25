#property copyright   "Carlos Espitia"
#property version     "1.00"
#property description "description here"
 
 
// make sure to enable and add ip address to mt5
// The path to the config is Tools -> Options -> Expert advisors -> WbRequest (checkbox)
input string Address= "127.0.0.1";
input int    Port   = 50000;


void OnStart() {
  int socket = SocketCreate();
  
  if(socket == INVALID_HANDLE) {
      Print("Failed to create a socket, error ",GetLastError()); 
      return;
  }
  
  if(!SocketConnect(socket,Address,Port,1000)) {
      Print("Connection to ",Address,":",Port," failed, error ",GetLastError()); 
      return;
  }
  
  Print("worked");

  SocketClose(socket);
}