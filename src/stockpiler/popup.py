from tkinter import *
from tkinter import ttk
class popup():

    messages = {
        "NoFox":"Foxhole isn't running.\nLaunch Foxhole and retry.",
        "NoStockpile": "Didn't detect stockpile.\nHover over a stockpile on the map and retry.",
        "blank_name": "You must type in the name (which cannot be Public).\nThis field cannot be left blank.\nYou'll need to rescan it.",
        "duplicate_hotkeys": "Warning: If your hotkeys are identical or overlap (ie: F2 and Shift + F2)\nthen it\'s possible that the hotkey will only grab a stockpile image and will not scan."
    }
    def __init__(self,parent,message_type):
        root_x = parent.winfo_rootx()
        root_y = parent.winfo_rooty() 
        if root_x == root_y == -32000:
            win_x = 100
            win_y = 100
        else:
            win_x = root_x - 20
            win_y = root_y + 125

        location = "+" + str(win_x) + "+" + str(win_y)

        PopupWindow = Toplevel(parent)
        PopupWindow.geometry(location)
        PopupWindow.resizable(False, False)
        PopupWindow.grab_set()
        PopupWindow.focus_force()

        self.popup_window = PopupWindow
        def destroy_self(event):
            self.popup_window.destroy()

        PopupWindow.bind('<Return>',destroy_self)

        PopupFrame = ttk.Frame(PopupWindow)
        PopupFrame.pack()

        label = ttk.Label(PopupFrame, text=self.messages[message_type], style="TLabel")
        label.grid(row=2, column=0)

        OKButton = ttk.Button(PopupFrame, text="OK", command=destroy_self)
        OKButton.grid(row=10, column=0, sticky="NSEW")
