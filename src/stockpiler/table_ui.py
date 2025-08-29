from tkinter import ttk
from tkinter import *
import os
import re
import logging
import datetime
from tksheet import Sheet

from stockpiler.items import ButtonState, category_mapping
from stockpiler.tooltip import CreateToolTip

class TableTab():
    def __init__(self,main_widget):
        parent_notebook = main_widget.notebook
        self.parent_widget = main_widget
        self.tab = ttk.Frame(parent_notebook)
        parent_notebook.add(self.tab, text="Results")
        
        self.canvas = Canvas(self.tab)
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)
        
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="1000p", width="402p")

        TableBottom = ttk.Frame(self.canvas)
        TableBottom.columnconfigure(0, weight=1)
        TableBottom.columnconfigure(1, weight=1)
        TableBottom.columnconfigure(2, weight=1)
        TableBottom.pack(fill='x', side=BOTTOM)
        self.print_table(0)

    def print_table(self,data):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(file_dir))
        row = 0
        column = 0
        for i,(category,custom_categories) in enumerate(category_mapping.items()):

            catimg = PhotoImage(file=os.path.join(root_dir,"UI","cat" + str(i+1) + ".png"))
            cat_label = ttk.Label(self.frame, image=catimg,text=category)
            cat_label.grid(row=row, column=column, sticky="NSEW", columnspan=8)
            cat_label.image = catimg
            row+=1
			
            for custom_category in custom_categories:

                cc_text = ttk.Label(master=self.frame,text=custom_category)
                cc_text.grid(row=row, columnspan=8, sticky="ew")
                row+=1
                ResultSheet = Sheet(self.frame, data=())
                ResultSheet.enable_bindings()
                ResultSheet.grid(row=row, columnspan=8, sticky="ew")
                ResultSheet.set_options(table_bg="grey75", header_bg="grey55", index_bg="grey55", top_left_bg="grey15", frame_bg="grey15")
                row+=1
				
            #     items_i = self.item_list.filter({"custom_category":custom_category,"stockpile_category":category})
            #     print(items_i)
			# 	found_items = []
			# 	for item in items_i:
			# 		if item in data:
			# 			found_items.append(d)
			# 		if hasattr(item,"img"):
			# 			if column < 8:
			# 				item_btn = item.make_btn(self.frame)
			# 				if item_btn:
			# 					item_btn.grid(row=row, column=column, sticky="W", padx=2, pady=2)
			# 				column += 1
			# 			else:
			# 				row += 1
			# 				column = 0
			# 				item_btn = item.make_btn(self.frame)
			# 				if item_btn:
			# 					item_btn.grid(row=row, column=column, sticky="W", padx=2, pady=2)
			# 				column += 1
			# 	row+=1
			# 	column = 0

            catsep = ttk.Separator(self.frame, orient=HORIZONTAL)
            catsep.grid(row=row, columnspan=8, sticky="ew", pady=10)
            row+=1
        # small_arms_res = ttk.Frame(self.canvas)
        # small_arms_res.pack(fill='x')
        # sa_icon = ttk
        # sa_title = ttk.Label(master=small_arms_res,text="Small Arms").pack(side=LEFT)


