import csv
import os
from menu import menu
from tkinter import *
from tkinter import ttk 
import enum
from tooltip import CreateToolTip
import re
import copy

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
        self.modded_check =  "CheckImages//Modded//"+self.id+".png"
        self.check =  "CheckImages//Default//"+self.id+".png"
        self.icon =  "UI//"+self.id+".png"
        self.enabled = "enabled"
        if os.path.exists(self.icon):
            self.img = PhotoImage(self.icon)
            self.btn = ttk.Button(
                self.frame, 
                image=self.img, 
                style="EnabledButton.TButton",
                command=self.toggle
            )
            self.ttp = CreateToolTip(self.btn,re.sub('\'', '', self.name))
            

    def toggle(self):
        # toggle is designed to work only if the category and faction are turned on
        if self.enabled == ButtonState.ENABLED:
            self.enabled = ButtonState.MANUAL_DISABLED
            self.btn.config(style="ManualDisabledButton.TButton")
        if self.enabled == ButtonState.MANUAL_DISABLED:
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
        with open('ItemNumbering.csv', 'rt') as f_input:
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
                item_id = int(rowdata[0])
                enable_status = int(rowdata[0])
                self.data[item_id].enabled = ButtonState(enable_status)

    def filter(self,filter_dict):

        out_data = []
        for d in self.data:
            matched = True
            for k,v in filter_dict:
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

master_list = ItemList()
ItemList.master_data = master_list.data

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
    "Vehicles":[
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