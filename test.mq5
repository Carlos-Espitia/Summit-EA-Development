#property copyright   "Carlos Espitia"
#property version     "1.00"
#property description "description here"

#include "MQ_API/SocketHandling.mqh"
#include "MQ_API/Graphics.mqh"
 
// make sure to enable and add ip address to mt5
// The path to the config is Tools -> Options -> Expert advisors -> WbRequest (checkbox)
input string Address= "127.0.0.1";
input int    Port   = 50000;

string textSeperator = "~";

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

  // class initializations
  SocketHandling sockethandler(socket);
  GraphicalObjectHandler graphics();
  bool connected = true;
  char rsp[];

  // listening for commands from python
  while(sockethandler.isConnected()) {
    Sleep(300);  // Wait a second before the next check | 300 ms best results 

    string recieved = sockethandler.recv();

    if(StringLen(recieved) <= 0) continue; // empty string was received

    // Print(recieved);

    string results[];// An array to get strings
    // had to use StringGetCharacter cuz of weird ushort
    int numStrings=StringSplit(recieved,StringGetCharacter(textSeperator,0),results);
    if(numStrings>0) {
      for(int i=0;i<numStrings;i++) {
        Print("[", i, "] ", results[i]);

        // ChartOpen("UERUSD", )

        if(graphics.isGraphicalCommand(results[i])) graphics.executeCommand(results[i]);

      }
    }
  }


  Print("Socket closed | ", GetLastError());
  SocketClose(socket);
}
