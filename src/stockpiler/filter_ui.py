from tkinter import ttk
from tkinter import *
from menu import menu
from items import master_list, ButtonState, category_mapping
import os
from tooltip import CreateToolTip
import re
import logging
import datetime

class FilterTab():
	def __init__(self,parent_notbook):
		self.tab = ttk.Frame(parent_notbook)
		parent_notbook.add(self.tab, text="Filter")
		self.canvas = Canvas(self.tab)

		def _on_mousewheel(event):
			self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

		self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

		scrollbar = ttk.Scrollbar(self.tab, orient=VERTICAL, command=self.canvas.yview)
		scrollbar.pack(side="right", fill="y")

		self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand=scrollbar.set)
		self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

		self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

		self.frame = ttk.Frame(self.canvas)

		self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="2071p", width="550p")

		self.item_list = master_list

		self.create_buttons()

	def create_buttons(self):
		for widgets in self.frame.winfo_children():
			widgets.destroy()

		if menu.faction[0] == 0:
			Wimg = PhotoImage(file="UI//W0.png")
			WardenButton = ttk.Button(self.frame, image=Wimg, style="EnabledFaction.TButton")
			WardenButton.image = Wimg
		else:
			Wimg = PhotoImage(file="UI//W1.png")
			WardenButton = ttk.Button(self.frame, image=Wimg, style="DisabledFaction.TButton")
			WardenButton.image = Wimg

		def warden_button(btn):		
			if str(btn['style']) == "EnabledFaction.TButton":
				btn.config(style="DisabledFaction.TButton")
				menu.faction[0] = 1
				self.item_list.factionToggle("Warden",ButtonState.DISABLED)
			else:
				btn.config(style="EnabledFaction.TButton")
				menu.faction[0] = 0
				self.item_list.factionToggle("Warden",ButtonState.ENABLED)
			self.refresh_button()
		WardenButton["command"] = warden_button
		WardenButton.grid(row=0, column=0, columnspan=1, pady=5)


		WardenButton_ttp = CreateToolTip(WardenButton, 'Enable/Disable Warden-only Items')
		
		
		if menu.faction[1] == 0:
			Cimg = PhotoImage(file="UI//C0.png")
			ColonialButton = ttk.Button(self.frame, image=Cimg, style="EnabledFaction.TButton")
			ColonialButton.image = Cimg
		else:
			Cimg = PhotoImage(file="UI//C1.png")
			ColonialButton = ttk.Button(self.frame, image=Cimg, style="DisabledFaction.TButton")
			ColonialButton.image = Cimg

		def colonial_button(btn):
			if str(btn['style']) == "EnabledFaction.TButton":
				btn.config(style="DisabledFaction.TButton")
				menu.faction[1] = 1
				self.item_list.factionToggle("Colonial",ButtonState.DISABLED)
			else:
				btn.config(style="EnabledFaction.TButton")
				menu.faction[1] = 0
				self.item_list.factionToggle("Colonial",ButtonState.ENABLED)
			self.refresh_button()

		ColonialButton["command"] = colonial_button
		ColonialButton.grid(row=menu.iconrow, column=1, columnspan=1, pady=5)
		ColonialButton_ttp = CreateToolTip(ColonialButton, 'Enable/Disable Colonial-only Items')


		row = 0
		column = 0
		for i,(category,custom_categories) in enumerate(category_mapping.items()):

			catsep = ttk.Separator(self.frame, orient=HORIZONTAL)
			catsep.grid(row=row, columnspan=8, sticky="ew", pady=10)
			catimg = PhotoImage(file="UI//cat" + str(menu.lastcat) + ".png")
			row+=1

			if menu.category[i][1] == 0:
				catbtn = ttk.Button(self.frame, image=catimg, style="EnabledCategory.TButton")
			else:
				catbtn = ttk.Button(self.frame, image=catimg, style="DisabledCategory.TButton")
			def cat_disable(btn):
				if str(btn['style']) == "EnabledCategory.TButton":
					btn.config(style="DisabledCategory.TButton")
					menu.category[i][1] = 1
					self.item_list.categoryToggle(category,ButtonState.DISABLED)
				else:
					btn.config(style="EnabledCategory.TButton")
					menu.category[i][1] = 0
					self.item_list.categoryToggle(category,ButtonState.ENABLED)

			catbtn["command"] = cat_disable
			catbtn.grid(row=row, column=column, sticky="NSEW", columnspan=8)
			CreateToolTip(catbtn,category)
			
			for custom_category in custom_categories:

				cc_text = ttk.Label(text=custom_category)
				cc_text.grid(row=row, columnspan=2, sticky="ew")
				row+=1

				items_i = self.item_list.filter({"custom_category":custom_category,"stockpile_category":category})
				for item in items_i:
					if hasattr(item,"btn"):
						if column < 8:
							item.btn.grid(row=row, column=column, sticky="W", padx=2, pady=2)
							column += 1
						else:
							row += 1
							column = 0
							item.btn.grid(row=row, column=column, sticky="W", padx=2, pady=2)
							column += 1


		self.quit_button = ttk.Button(self.frame, text="Quit", style="EnabledButton.TButton")

		["command"].grid(row=500, column=0, columnspan=10, sticky="NSEW")

		self.frame.update()


		try:
			print("create_window height for Filter canvas should be roughly:", str(btn.winfo_y()-505))
		except Exception as e:
			print("Exception: ", e)
			print("Might not be any buttons")
			logging.info(str(datetime.datetime.now()) + " No buttons? " + str(e))
		
