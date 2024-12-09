class SocketHandling {
  private:
    int socket;  // A private member variable

  public:
    // Constructor
    SocketHandling(int initSocket) {
      socket = initSocket;
    }

    bool isConnected() {
      string msg = "ping";
      uchar data[];
      StringToCharArray(msg, data);
      int sent = SocketSend(socket, data, ArraySize(data));

      if(sent <= 0) return false;
      return true;
    }

    // server can send multiple messages so figure out how to make a list of messages
    string recv() {
      char   rsp[];
      string result;

      uint len=SocketIsReadable(socket); // check if server has sent data 
      if(!len) return result;

      result += CharArrayToString(rsp,0,SocketRead(socket,rsp,len,0));

      return result;
    }
};