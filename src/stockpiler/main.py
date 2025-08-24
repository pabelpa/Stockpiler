from tkinter import *
from tkinter import ttk
import logging
import datetime
import os
from menu import menu

from filter_ui import add_filter_tab
Version = "0.0.1"

StockpilerWindow = Tk()
StockpilerWindow.title('Stockpiler ' + Version)

# Window width is based on generated UI.  If buttons change, width should change here.
StockpilerWindow.geometry("537x600")

# Width locked since button array doesn't adjust dynamically
StockpilerWindow.resizable(width=False, height=False)
StockpilerWindow.iconbitmap(default='Bmat.ico')

if os.path.exists("Config.txt"):
	with open("Config.txt") as file:
		content = file.readlines()
	content = [x.strip() for x in content]
	try:
		print("Attempting to load from Config.txt")
		logging.info(str(datetime.datetime.now()) + ' Attempting to load from config.txt')
		menu.CSVExport.set(int(content[0]))
		menu.XLSXExport.set(int(content[1]))
		menu.ImgExport.set(int(content[2]))
		menu.Set.set(int(content[3]))
		menu.Learning.set(int(content[4]))
		menu.updateBot.set(int(content[5]))
		menu.BotHost.set(content[6])
		menu.BotPassword.set(content[7])
		menu.BotGuildID.set(content[8])
		if (len(content) >= 13): menu.experimentalResizing.set(content[13])
	except Exception as e:
		print("Exception: ", e)
		logging.info(str(datetime.datetime.now()) + ' Loading from config.txt failed, setting defaults')
		menu.CSVExport.set(0)
		menu.XLSXExport.set(0)
		menu.ImgExport.set(1)
		menu.Set.set(0)
		menu.Learning.set(0)
	try:
		print("Attempting to load hotkeys from config.txt")
		logging.info(str(datetime.datetime.now()) + ' Attempting to load from hotkeys from config.txt')
		menu.grabhotkey.set(content[9])
		menu.scanhotkey.set(content[10])
		menu.grabhotkeystring = menu.grabhotkey.get()
		menu.scanhotkeystring = menu.scanhotkey.get()
		menu.grabshift.set(content[11][0])
		menu.grabctrl.set(content[11][1])
		menu.grabalt.set(content[11][2])
		menu.grabmods = str(menu.grabshift.get()) + str(menu.grabctrl.get()) + str(menu.grabalt.get())
		menu.scanshift.set(content[12][0])
		menu.scanctrl.set(content[12][1])
		menu.scanalt.set(content[12][2])
		menu.scanmods = str(menu.scanshift.get()) + str(menu.scanctrl.get()) + str(menu.scanalt.get())
	except Exception as e:
		print("Exception: ", e)
		print("Failed to load hotkeys from config.txt, setting them to defaults of f2, f3")
		logging.info(str(datetime.datetime.now()) + ' No custom hotkeys in config.txt, setting defaults of f2, f3')
		menu.grabhotkey.set("f2")
		menu.scanhotkey.set("f3")
		menu.grabhotkeystring = menu.grabhotkey.get()
		menu.scanhotkeystring = menu.scanhotkey.get()
		menu.grabshift.set(0)
		menu.grabctrl.set(0)
		menu.grabalt.set(0)
		menu.grabmods = "000"
		menu.scanshift.set(0)
		menu.scanctrl.set(0)
		menu.scanalt.set(0)
		menu.scanmods = "000"
else:
	menu.CSVExport.set(0)
	menu.XLSXExport.set(0)
	menu.ImgExport.set(1)
	menu.Set.set(0)
	menu.Learning.set(0)

OuterFrame = ttk.Frame(StockpilerWindow)
OuterFrame.pack(fill=BOTH, expand=1)
TabControl = ttk.Notebook(OuterFrame)

add_filter_tab(TabControl)
CreateButtons("")

SetHotkeys("")

StockpilerWindow.mainloop()