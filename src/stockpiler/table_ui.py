from tkinter import ttk
from tkinter import *
from menu import menu
from items import master_list, ButtonState, category_mapping
import os
from tooltip import CreateToolTip
import re
import logging
import datetime
from tksheet import Sheet

class TableTab():
    def __init__(self,parent):
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text="Results")
        
        self.canvas = Canvas(self.tab)
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="410p", width="402p")

        TableBottom = ttk.Frame(self.canvas)
        TableBottom.columnconfigure(0, weight=1)
        TableBottom.columnconfigure(1, weight=1)
        TableBottom.columnconfigure(2, weight=1)
        TableBottom.pack(fill='x', side=BOTTOM)

        ResultSheet = Sheet(self.frame, data=fillerdata)
        ResultSheet.enable_bindings()
        ResultSheet.pack(expand=True, fill='both')
        ResultSheet.set_options(table_bg="grey75", header_bg="grey55", index_bg="grey55", top_left_bg="grey15", frame_bg="grey15")