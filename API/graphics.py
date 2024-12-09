import json
from API.socket import server

class Graphics:

    def plot_Hline(
        chart_id=0, # might change
        name="HLine", 
        sub_window=0, 
        price=0, 
        clr="clrBlue", 
        # style="STYLE_SOLID", 
        width=1, 
        back=False, 
        selection=True, 
        editable=False, 
        hidden=False, 
        z_order=0 ):

        # check if server up
        # if server is None:
        #     print("server was not initialized to plot graphics!") 
        #     return

        jsonInfo = {
            "type": "HLINE",
            "chart_id": chart_id,
            "name": name,
            "sub_window": sub_window,
            "price": price,
            "clr": clr,
            # "style": style,
            "width": width,
            "back": back,
            "selection": selection,
            "editable": editable,
            "hidden": hidden,
            "z_order": z_order
        }

        # Convert the dictionary to a JSON string
        server.send("[G] " + json.dumps(jsonInfo))


# Graphics.hLineJson(price=1.10000)
# # Example usage
# json_command = hLineJson(price=1.10000)
# print(json_command)
