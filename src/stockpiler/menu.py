from tkinter import IntVar, StringVar
class menu(object):
	iconrow = 1
	experimentalResizing = IntVar()
	iconcolumn = 0
	lastcat = 0
	itembuttons = []
	icons = []
	category = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]
	faction = [0, 0]
	topscroll = 0
	BotHost = StringVar()
	BotPassword = StringVar()
	BotGuildID = StringVar()
	CSVExport = IntVar()
	updateBot = IntVar()
	XLSXExport = IntVar()
	ImgExport = IntVar()
	debug = IntVar()
	Set = IntVar()
	Learning = IntVar()
	PickerX = -1
	PickerY = -1
	bindings = list()
	grabshift = IntVar()
	grabctrl = IntVar()
	grabalt = IntVar()
	grabhotkey = StringVar()
	scanshift = IntVar()
	scanctrl = IntVar()
	scanalt = IntVar()
	scanhotkey = StringVar()
	grabhotkeystring = "f2"
	scanhotkeystring = "f3"
	grabmods = "000"
	scanmods = "000"

menu.grabshift.set(0)
menu.grabctrl.set(0)
menu.grabalt.set(0)
menu.scanshift.set(0)
menu.scanctrl.set(0)
menu.scanalt.set(0)
menu.debug.set(0)
menu.experimentalResizing.set(0)