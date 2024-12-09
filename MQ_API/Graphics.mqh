// class Graphics {

//   public:
//     // Constructor
//     Graphics() {}


//     bool create_Hline(
//         const long            chart_ID=0,        // chart's ID 
//         const string          name="HLine",      // line name
//         const int             sub_window=0,      // subwindow index
//         double                price=0,           // line price
//         const color           clr=C'0,204,255',      // line color
//         const ENUM_LINE_STYLE style=STYLE_SOLID, // line style
//         const int             width=1,           // line width
//         const bool            back=false,        // in the background
//         const bool            selection=true,    // highlight to move
//         const bool            editable=true,    // highlight to move

//         const bool            hidden=false,       // hidden in the object list
//         const long            z_order=0)         // priority for mouse click
//         {
//         if(!price) price=SymbolInfoDouble(Symbol(),SYMBOL_BID);
//         if(!ObjectCreate(chart_ID,name,OBJ_HLINE,sub_window,0,price)) {
//             Print(__FUNCTION__,": failed to create a horizontal line! Error code = ",GetLastError());
//             return(false);
//         }
//         ObjectSetInteger(chart_ID,name,OBJPROP_COLOR,clr);
//         ObjectSetInteger(chart_ID,name,OBJPROP_STYLE,style);
//         ObjectSetInteger(chart_ID,name,OBJPROP_WIDTH,width);
//         ObjectSetInteger(chart_ID,name,OBJPROP_BACK,back);
//         ObjectSetInteger(chart_ID,name,OBJPROP_SELECTABLE,selection);
//         ObjectSetInteger(chart_ID,name,OBJPROP_SELECTED,false); 
//         ObjectSetInteger(chart_ID,name,OBJPROP_HIDDEN,hidden);
//         ObjectSetInteger(chart_ID,name,OBJPROP_ZORDER,z_order);
//         return(true);
//     }

// };


//+------------------------------------------------------------------+
//|                                             GraphicalObjectHandler.mqh |
//+------------------------------------------------------------------+
// #include <ChartObjects\ChartObjectsLines.mqh>
// #include <ChartObjects\ChartObjectsMain.mqh>
// #include <Strings\StringUtils.mqh> // Include if you have string utility functions

class GraphicalObjectHandler {
  public:
    void executeCommand(string command) {

        // Extract JSON content from the command
        string jsonContent = StringSubstr(command, StringFind(command, "{"), StringFind(command, "}") - StringFind(command, "{") + 1);
        
        // Parse the JSON-like content (very simplified version)
        string type = ExtractJsonValue(jsonContent, "type");

        Print(type);

        // not all types use these variables, command will not always have all json values, it depends on what type of graphical object is wanted to be used
        // double price = StringToDouble(ExtractJsonValue(jsonContent, "price"));
        // datetime time1 = StringToTime(ExtractJsonValue(params, "time1"));
        // double price1 = StringToDouble(ExtractJsonValue(params, "price1"));
        // datetime time2 = StringToTime(ExtractJsonValue(params, "time2"));
        // double price2 = StringToDouble(ExtractJsonValue(params, "price2"));
        // color clr = StringToColor(ExtractJsonValue(params, "clr"));

        if (type == "HLINE") CreateHorizontalLine(jsonContent);
        // if (type == "RECTANGLE") CreateRectangle(jsonContent);

    }

    bool isGraphicalCommand(string command) {
        return StringFind(command, "[G]") == 0;
    }

  private:

    void CreateHorizontalLine(string jsonContent) {

        long chart_id = StringToInteger(ExtractJsonValue(jsonContent, "chart_id"));
        string name = ExtractJsonValue(jsonContent, "name");
        int sub_window = StringToInteger(ExtractJsonValue(jsonContent, "sub_window"));
        double price = StringToDouble(ExtractJsonValue(jsonContent, "price"));
        color clr = StringToColor(ExtractJsonValue(jsonContent, "clr")); // only works with string colors
        int width = StringToInteger(ExtractJsonValue(jsonContent, "width"));
        bool back = StringToBool(ExtractJsonValue(jsonContent, "back"));
        bool selection = StringToBool(ExtractJsonValue(jsonContent, "selection"));
        bool hidden = StringToBool(ExtractJsonValue(jsonContent, "hidden"));
        bool z_order = StringToLong(ExtractJsonValue(jsonContent, "z_order"));

        if(!price) price=SymbolInfoDouble(Symbol(),SYMBOL_BID);
        if(!ObjectCreate(chart_id,name,OBJ_HLINE,sub_window,0,price)) {
            Print(__FUNCTION__,": failed to create a horizontal line! Error code = ",GetLastError());
        }
        ObjectSetInteger(chart_id,name,OBJPROP_COLOR,clr);
        // ObjectSetInteger(chart_id,name,OBJPROP_STYLE,style);
        ObjectSetInteger(chart_id,name,OBJPROP_WIDTH,width);
        ObjectSetInteger(chart_id,name,OBJPROP_BACK,back);
        ObjectSetInteger(chart_id,name,OBJPROP_SELECTABLE,selection);
        ObjectSetInteger(chart_id,name,OBJPROP_SELECTED,false); 
        ObjectSetInteger(chart_id,name,OBJPROP_HIDDEN,hidden);
        ObjectSetInteger(chart_id,name,OBJPROP_ZORDER,z_order);
    }

    // Simplified method to extract a value from a JSON-like string
    // needs fixing
    // doesnt work wit RGB because it uses ',' | only color text like clrBlack
    string ExtractJsonValue(string json, string key) {
        string value = "";
        int startPos = StringFind(json, "\"" + key + "\"");
        if (startPos >= 0) {
            startPos = StringFind(json, ":", startPos) + 1; // Start of the value
            int endPos = StringFind(json, ",", startPos); // End of the value
            if (endPos < 0) endPos = StringFind(json, "}", startPos); // If it's the last element
            value = StringSubstr(json, startPos, endPos - startPos);
            value = Trim(value); // Assuming a Trim function to remove white spaces and extra quotes
        }
        return value;
    }

    // Add other helper functions as needed
    string Trim(string text) {
        // Trim leading spaces
        while(StringGetCharacter(text, 0) == ' ' || StringGetCharacter(text, 0) == '\"')
            text = StringSubstr(text, 1);

        // Trim trailing spaces
        while(StringGetCharacter(text, StringLen(text)-1) == ' ' || StringGetCharacter(text, StringLen(text)-1) == '\"')
            text = StringSubstr(text, 0, StringLen(text)-1);

        return text;
    }

    bool StringToBool(string str) {
        return (str == "true");
    }

    long StringToLong(string str) {
        return StringToInteger(str);
    }
};
