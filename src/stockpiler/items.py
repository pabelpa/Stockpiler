import csv
import os
from tkinter import *
from tkinter import ttk 
import enum
import re
import copy


from stockpiler.tooltip import CreateToolTip

class ButtonState(enum.Enum):
    ENABLED = 0
    MANUAL_DISABLED = 1
    DISABLED = 2
    FACTION_DISABLED = 3

class Item(object):
    headers = [
        "id",
        "i",
        "c",
        "name",
        "nickname",
        "subType",
        "ammo",
        "faction",
        "stockpile_category",
        "custom_category",
        "category_sort",
        "in_category_sort",
        "ind_exists",
        "crate_exists",
        "per_crate",
        "bmats",
        "emats",
        "rmats",
        "hemats",
        "relicmats"
    ]

    def __init__(self,row_data):
        for i,h in enumerate(self.headers):
            self.__setattr__(h,row_data[i])

        file_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(file_dir))
        self.modded_check = os.path.join(root_dir,"CheckImages","Modded",self.id+".png")
        self.check = os.path.join(root_dir,"CheckImages","Default",self.id+".png")
        self.icon = os.path.join(root_dir,"UI",str(self.id)+".png")
 
        self.enabled = ButtonState.ENABLED
        if os.path.exists(self.icon):
            self.img = PhotoImage(file = os.path.abspath(self.icon))

    
    def make_btn(self,frame):
        if os.path.exists(self.icon):
            self.btn = ttk.Button(
                frame, 
                image=self.img, 
                style="EnabledButton.TButton",
                command=lambda: self.toggle()
            )
        else:
            return
        self.btn.image = self.img
        self.ttp = CreateToolTip(self.btn,re.sub('\'', '', self.name))
        return self.btn
            

    def toggle(self):
        # toggle is designed to work only if the category and faction are turned on

        if self.enabled == ButtonState.ENABLED:

            self.enabled = ButtonState.MANUAL_DISABLED
            self.btn.config(style="ManualDisabledButton.TButton")
        elif self.enabled == ButtonState.MANUAL_DISABLED:
            self.enabled = ButtonState.ENABLED
            self.btn.config(style="EnabledButton.TButton")


class ItemList():
    numbers = (('CheckImages//num0.png', "0"), ('CheckImages//num1.png', "1"), ('CheckImages//num2.png', "2"),
			   ('CheckImages//num3.png', "3"), ('CheckImages//num4.png', "4"), ('CheckImages//num5.png', "5"),
			   ('CheckImages//num6.png', "6"), ('CheckImages//num7.png', "7"), ('CheckImages//num8.png', "8"),
			   ('CheckImages//num9.png', "9"), ('CheckImages//numk.png', "k+"))
    stockpilecontents = []
    sortedcontents = []
    slimcontents = []
    ThisStockpileName = ""
    FoundStockpileTypeName = ""
    UIimages = []
    master_data = []
    
	
    def __init__(self):
        self.data = []
        with open('ItemNumberingnew.csv', 'rt') as f_input:
            csv_input = csv.reader(f_input, delimiter=',')
            # Skips first line
            header = next(csv_input)
            # Skips reserved line
            reserved = next(csv_input)
            for rowdata in csv_input:
                item_i = Item(rowdata)
                self.data.append(item_i)


        with open('Filter.csv', 'rt') as f_input:
            csv_input = csv.reader(f_input, delimiter=',')
            # Skips first line
            header = next(csv_input)
            for rowdata in csv_input:
                try:
                    item_id = int(rowdata[0])
                except:
                    continue
                try:
                    enable_status = int(rowdata[1])
                    self.data[item_id].enabled = ButtonState(enable_status)
                except ValueError:
                    self.data[item_id].enabled = ButtonState.DISABLED


    def filter(self,filter_dict):

        out_data = []
        for d in self.data:
            matched = True
            for k,v in filter_dict.items():
                if getattr(d,k)!=v:
                    matched = False
                    break
            if matched:
                out_data.append(d)
        return out_data
    
    def factionToggle(self,faction,state):
        for item in self.data:
            if item.faction == faction:
                item.enabled = state

    def categoryToggle(self,category,state):
        for item in self.data:
            if item.stockpile_category == category:
                item.enabled = state

category_mapping = {
    "Small Arms":[
        "Rifle",
        "Automatic Rifle",
        "Machine Gun",
        "Misc. Small Arms",
        "Light Kinetic Ammo",
        "Heavy Kinetic Ammo",
        "Light Grenade"
    ],
    "Heavy Arms":[
        "20mm Weaponry",
        "AT Weaponry",
        "Mortar Weaponry",
        "30mm Weaponry",
        "Heavy Grenade",
        "Incindiary"
    ],
    "Heavy Ammunition":[
        "Artillery Shells",
        "Tank Munitions",
        "Anti Ship",
        "Rocket Ammunition"
    ],
    "Utility":[
        "Engineering",
        "Intelligence",
        "Demolition",
        "Misc. Equipment"
    ],
    "Medical":[
        "Medical",
    ],
    "Resource":[
        "Materials",
        "Raw Materials",
        "Tech Mats",
        "Fuel",
        "Assembly Materials",
        "Construction Materials",
    ],
    "Uniforms":[
        "Assault Uniforms",
        "Engineering Uniforms",
        "Recon Uniforms",
    ],
    "Vehicle":[
        "Utility",
        "Armor",
        "Light Armor",
        "Heavy Armor",
        "Field Gun",
        "Scout",
        "Rocket",
        "Aquatic",
    ],
    "Shippables":[
        "Logistics",
        "Emplacements",
        "Naval",
        "Large Structure",
        "Ballistic",
    ],
}