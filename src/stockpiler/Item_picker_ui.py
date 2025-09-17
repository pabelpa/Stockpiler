from tkinter import ttk
from tkinter import *
import os
import re
import logging
import datetime
from PIL import ImageTk
import cv2

from stockpiler.tooltip import CreateToolTip
from stockpiler.items import ButtonState, category_mapping

class ItemPicker():		
	def __init__(self,main_obj,image):
		self.main_obj = main_obj
		root_x = main_obj.main_widget.winfo_rootx()
		root_y = main_obj.main_widget.winfo_rooty()
		if main_obj.PickerX != -1:
			win_x = main_obj.PickerX
			win_y = main_obj.PickerY
		elif root_x == root_y == -32000:
			win_x = 20
			win_y = 20
		elif root_x < 20:
			win_x = 20
			win_y = 20
		else:
			# This window is so big in its current form that it just needs to be further in the corner
			win_x = root_x - 20
			win_y = root_y - 20

		location = "+" + str(win_x) + "+" + str(win_y)
		window = Toplevel(main_obj.main_widget)
		window.geometry(location)
		frame = ttk.Frame(window)
		window.resizable(False, False)
		frame.pack()
		frame.grid_forget()
		iconrow = iconcolumn = 0

		NewIconLabel = ttk.Label(frame, text="What item is this?")
		NewIconLabel.grid(row=iconrow, column=0, columnspan=8)
		iconrow += 1
		self.image = image
		im = Image.fromarray(image)
		tkimage = ImageTk.PhotoImage(im)
		NewIconImage = ttk.Label(frame, image=tkimage)
		NewIconImage.image = image
		NewIconImage.grid(row=iconrow, column=0)
		
		bigim = im.resize(size=(200, 200), resample=Image.NEAREST)
		tkimagebig = ImageTk.PhotoImage(bigim)
		
		BigIconImage = ttk.Label(frame, image=tkimagebig)
		BigIconImage.image = image
		BigIconImage.grid(row=iconrow, column=1, columnspan=4)
		
		iconrow += 1
		crate_or_ind = IntVar()
		crate = ttk.Radiobutton(frame,text="Crate",variable=crate_or_ind,value=1)
		individual = ttk.Radiobutton(frame,text="Crate",variable=crate_or_ind,value=2)
		self.crate_or_ind = crate_or_ind
		crate.grid(row = iconrow, column=0)
		individual.grid(row = iconrow, column=4)
		iconrow += 1

		def _on_mousewheel(event):
			frame.yview_scroll(int(-1*(event.delta/120)), "units")

		frame.bind_all("<MouseWheel>", _on_mousewheel)

		scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.canvas.yview)
		scrollbar.pack(side="right", fill="y")

		self.item_list = main_obj.master_list

		self.create_buttons()

		file_dir = os.path.dirname(os.path.abspath(__file__))
		root_dir = os.path.dirname(os.path.dirname(file_dir))

		column = 0
		for i,(category,custom_categories) in enumerate(category_mapping.items()):

			catimg = PhotoImage(file=os.path.join(root_dir,"UI","cat" + str(i+1) + ".png"))
			cat_label = ttk.Label(self.frame, image=catimg)
			cat_label.grid(row=iconrow, column=column, sticky="NSEW", columnspan=8)
			cat_label.image = catimg

			row+=1
			
			for custom_category in custom_categories:

				cc_text = ttk.Label(master=self.frame,text=custom_category)
				cc_text.grid(row=row, columnspan=8, sticky="ew")
				row+=1

				items_i = self.item_list.filter({"custom_category":custom_category,"stockpile_category":category})

				for item in items_i:
					if hasattr(item,"img"):
						if column >= 8:
							row += 1
							column = 0
						item_btn = item.make_btn(self.frame)

						if item_btn:
							item_btn.grid(row=row, column=column, sticky="W", padx=2, pady=2)
							item_btn["command"] = lambda : self.item_selected(item)
						column += 1
				row+=1
				column = 0

			catsep = ttk.Separator(self.frame, orient=HORIZONTAL)
			catsep.grid(row=row, columnspan=8, sticky="ew", pady=10)
			row+=1

		self.quit_button = ttk.Button(self.frame, text="Quit", style="EnabledButton.TButton")

		self.quit_button["command"] = self.parent_widget.main_widget.quit()
		self.quit_button.grid(row=500, column=0, columnspan=10, sticky="NSEW")

		self.frame.update()

	def item_selected(self,item):
		self.selected_id = item.id
		if self.crate_or_ind == 1:
			name = str(item.id) + ".png"
		elif self.crate_or_ind == 2:
			name = str(item.id) + "C.png"
		else:
			print("no radio button selected")
		if self.main_obj.Set.get() == 0:
			save = 'CheckImages//Default//' + name
		else:
			save = 'CheckImages//Modded//' + name
		print("save:", save)
		cv2.imwrite(save, self.image)


	def create_cat_func(self, btn,category,i):
		def cat_disable():
			if str(btn['style']) == "EnabledCategory.TButton":
				btn.config(style="DisabledCategory.TButton")
				self.parent_widget.category[i][1] = 1
				self.item_list.categoryToggle(category,ButtonState.DISABLED)
			else:
				btn.config(style="EnabledCategory.TButton")
				self.parent_widget.category[i][1] = 0
				self.item_list.categoryToggle(category,ButtonState.ENABLED)
			self.refresh_buttons()
		return cat_disable