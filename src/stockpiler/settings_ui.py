from menu import menu
from tkinter import ttk
from tkinter import *
from global_hotkeys import *

from tooltip import CreateToolTip
from popup import popup

class SettingsTab():
	def __init__(self,parent_notebook):
		self.tab = ttk.Frame(parent_notebook)
		parent_notebook.add(self.tab, text="Settings")
		self.canvas = Canvas(self.tab)
		self.canvas.pack(side=TOP, fill=BOTH, expand=1)


		self.frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.frame, anchor="nw", height="500p", width="402p")
		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(7, weight=1)

		row = 0
		GrabImageEntryLabel = ttk.Label(self.frame, text="Grab Stockpile Image:")
		GrabImageEntryLabel.grid(row=row, column=0)

		GrabImageEntry = ttk.Entry(self.frame, textvariable=menu.grabhotkey, width=10)
		GrabImageEntry.grid(row=row, column=1)
		GrabImageEntry.delete(0, 'end')
		GrabImageEntry.insert(0, menu.grabhotkeystring)
		GrabImageEntry_ttp = CreateToolTip(GrabImageEntry, 'Available hotkeys are: all letters, numbers, function keys (as f#)'
														', backspace, tab, clear, enter, pause, caps_lock, escape, space, '
														'page_up, page_down, end, home, up, down, left, right, select, print, '
														'print_screen, insert, delete, help, numpad numbers (as numpad_#), '
														'separator_key (pipe key), multiply_key, add_key, subtract_key, '
														'decimal_key, divide_key, num_lock, scroll_lock, and symbols '
														'(+ - ` , . / ; [ ] \')')
		
		GrabShiftCheck = ttk.Checkbutton(self.frame, text="Shift?", variable=menu.grabshift)
		GrabShiftCheck.grid(row=row, column=2)

		GrabCtrlCheck = ttk.Checkbutton(self.frame, text="Ctrl?", variable=menu.grabctrl)
		GrabCtrlCheck.grid(row=row, column=3)

		GrabAltCheck = ttk.Checkbutton(self.frame, text="Alt?", variable=menu.grabalt)
		GrabAltCheck.grid(row=row, column=4)


		row += 1
		ScanEntryLabel = ttk.Label(self.frame, text="Scan Stockpile:")
		ScanEntryLabel.grid(row=row, column=0)

		ScanEntry = ttk.Entry(self.frame, textvariable=menu.scanhotkey, width=10)
		ScanEntry.grid(row=row, column=1)
		ScanEntry.delete(0, 'end')
		ScanEntry.insert(0, menu.scanhotkeystring)
		ScanEntry_ttp = CreateToolTip(ScanEntry, 'Available hotkeys are: all letters, numbers, function keys (as f#)'
														', backspace, tab, clear, enter, pause, caps_lock, escape, space, '
														'page_up, page_down, end, home, up, down, left, right, select, print, '
														'print_screen, insert, delete, help, numpad numbers (as numpad_#), '
														'separator_key (pipe key), multiply_key, add_key, subtract_key, '
														'decimal_key, divide_key, num_lock, scroll_lock, and symbols '
														'(+ - ` , . / ; [ ] \')')
		
		ScanShiftCheck = ttk.Checkbutton(self.frame, text="Shift?", variable=menu.scanshift)
		ScanShiftCheck.grid(row=row, column=2)

		ScanCtrlCheck = ttk.Checkbutton(self.frame, text="Ctrl?", variable=menu.scanctrl)
		ScanCtrlCheck.grid(row=row, column=3)

		ScanAltCheck = ttk.Checkbutton(self.frame, text="Alt?", variable=menu.scanalt)
		ScanAltCheck.grid(row=row, column=4)

		row += 1
		ResetHotkeysButton = ttk.Button(self.frame, text="Reset Hotkeys", command=self.reset_hotkeys)
		ResetHotkeysButton.grid(row=row, column=0, columnspan=8, pady=1)
		ResetHotkeys_ttp = CreateToolTip(ResetHotkeysButton, 'Some combinations may not work, like Ctrl + Shift + F-keys.\n'
															'This button will reset the hotkeys to default.  Remember to '
															'save your settings.')
		row += 1
		self.separator(row)

		row += 1
		SetLabel = ttk.Label(self.frame, text="Icon set?", style="TLabel")
		SetLabel.grid(row=row, column=0)
		DefaultRadio = ttk.Radiobutton(self.frame, text="Default", variable=menu.Set, value=0)
		DefaultRadio.grid(row=row, column=1)
		ModdedRadio = ttk.Radiobutton(self.frame, text="Modded", variable=menu.Set, value=1)
		ModdedRadio.grid(row=row, column=2)

		row += 1
		self.separator(row)

		row += 1
		LearningCheck = ttk.Checkbutton(self.frame, text="Learning Mode?", variable=menu.Learning)
		LearningCheck.grid(row=row, column=0, columnspan=2)
		
		row += 1
		self.separator(row)

		row += 1
		CSVCheck = ttk.Checkbutton(self.frame, text="CSV?", variable=menu.CSVExport)
		CSVCheck.grid(row=row, column=0)
		XLSXCheck = ttk.Checkbutton(self.frame, text="XLSX?", variable=menu.XLSXExport)
		XLSXCheck.grid(row=row, column=1)
		ImgCheck = ttk.Checkbutton(self.frame, text="Image?", variable=menu.ImgExport)
		ImgCheck.grid(row=row, column=2)

		row += 1
		self.separator

		row += 1
		SendBotCheck = ttk.Checkbutton(self.frame, text="Send To Bot?", variable=menu.updateBot)
		SendBotCheck.grid(row=row, column=0, rowspan=2, padx=5)
		SendBotCheck_ttp = CreateToolTip(SendBotCheck, 'Send results to Storeman-Bot Discord Bot?')
		BotHostLabel = ttk.Label(self.frame, text="Bot Host:")
		BotHostLabel.grid(row=row, column=2)
		BotHost = ttk.Entry(self.frame, textvariable=menu.BotHost)
		BotHost.grid(row=row, column=3, columnspan=2)
		BotHost_ttp = CreateToolTip(BotHost, 'Host is http://<your Storeman-Bot server IP>:8090')

		row += 1
		BotPasswordLabel = ttk.Label(self.frame, text="Password:")
		BotPasswordLabel.grid(row=row, column=2)
		BotPassword = ttk.Entry(self.frame, textvariable=menu.BotPassword)
		BotPassword.grid(row=row, column=3, columnspan=2)
		BotPassword.config(show="*")
		BotPassword_ttp = CreateToolTip(BotPassword, 'Password is set with bot using /spsetpassword command in Discord')

		row += 1
		BotGuildIDLabel = ttk.Label(self.frame, text="GuildID:")
		BotGuildIDLabel.grid(row=row, column=2)
		BotGuildIDLabel_ttp = CreateToolTip(BotGuildIDLabel, 'Only use if you are using a multi-server instance.  If you are using a public instance of Storeman Bot, this is your Discord\'s "Guild ID"')
		BotGuildID = ttk.Entry(self.frame, textvariable=menu.BotGuildID)
		BotGuildID.grid(row=row, column=3, columnspan=2)
		BotGuildID_ttp = CreateToolTip(BotGuildID, 'Only use if you are using a multi-server instance.  If you are using a public instance of Storeman Bot, this is your Discord\'s "Guild ID"')

		row += 1
		self.separator()

		row += 1
		ObnoxiousCheck = ttk.Checkbutton(self.frame, text="  Obnoxious\ndebug mode?", variable=menu.debug)
		ObnoxiousCheck.grid(row=row, column=0, rowspan=2, padx=5)
		ObnoxiousCheck = ttk.Checkbutton(self.frame, text="  Experimental Resizing", variable=menu.experimentalResizing)
		ObnoxiousCheck.grid(row=row, column=1, rowspan=2, padx=5)


		save_img = PhotoImage(file="UI/Save.png")
		save_btn = ttk.Button(self.frame, image=save_img, command=self.get_save_settings_func())

		save_btn.image = save_img
		save_btn.grid(row=row, column=0, columnspan=8, pady=5)
		SaveButton_ttp2 = CreateToolTip(save_btn, 'Save Current Filter and Export Settings')


	def separator(self,row):
		setsep = ttk.Separator(self.frame, orient=HORIZONTAL)
		setsep.grid(row=row, columnspan=8, sticky="ew", pady=10)

	def reset_hotkeys(self):
		menu.grabshift.set(0)
		menu.grabctrl.set(0)
		menu.grabalt.set(0)
		menu.grabmods = "000"
		menu.grabhotkey.set("f2")
		menu.grabhotkeystring = "f2"
		menu.scanshift.set(0)
		menu.scanctrl.set(0)
		menu.scanalt.set(0)
		menu.scanmods = "000"
		menu.scanhotkey.set("f3")
		menu.scanhotkeystring = "f3"

	def set_hotkeys(self):
		clear_hotkeys()
		if menu.grabmods[0] == "0":
			grabshift = ""
		else:
			grabshift = "\"shift\","
		if menu.grabmods[1] == "0":
			grabctrl = ""
		else:
			grabctrl = "\"control\","
		if menu.grabmods[2] == "0":
			grabalt = ""
		else:
			grabalt = "\"alt\","
		if menu.scanmods[0] == "0":
			scanshift = ""
		else:
			scanshift = "\"shift\","
		if menu.scanmods[1] == "0":
			scanctrl = ""
		else:
			scanctrl = "\"control\","
		if menu.scanmods[2] == "0":
			scanalt = ""
		else:
			scanalt = "\"alt\","
		bindingsstring = "menu.bindings = [[[" + grabshift + grabctrl + grabalt + "\"" + menu.grabhotkeystring +\
						"\"], None, GrabStockpileImage],[[" + scanshift + scanctrl + scanalt + "\"" + \
						menu.scanhotkeystring + "\"], None, LearnOrNot],]"
		exec(bindingsstring)
		register_hotkeys(menu.bindings)
		start_checking_hotkeys()
		if menu.grabhotkeystring == menu.scanhotkeystring:
			self.popup = popup("DuplicateHotkeys")

	def get_save_settings_func(self):
		def out_func():
			with open("Config.txt", "w") as exportfile:
				exportfile.write(str(menu.CSVExport.get()) + "\n")
				exportfile.write(str(menu.XLSXExport.get()) + "\n")
				exportfile.write(str(menu.ImgExport.get()) + "\n")
				exportfile.write(str(menu.Set.get()) + "\n")
				exportfile.write(str(menu.Learning.get()) + "\n")
				exportfile.write(str(menu.updateBot.get()) + "\n")
				exportfile.write(str(menu.BotHost.get()) + "\n")
				exportfile.write(str(menu.BotPassword.get()) + "\n")
				exportfile.write(str(menu.BotGuildID.get()) + "\n")
				exportfile.write(str(menu.grabhotkey.get()) + "\n")
				exportfile.write(str(menu.scanhotkey.get()) + "\n")
				menu.grabhotkeystring = menu.grabhotkey.get()
				menu.scanhotkeystring = menu.scanhotkey.get()
				exportfile.write(str(menu.grabshift.get()) + str(menu.grabctrl.get()) + str(menu.grabalt.get()) + "\n")
				exportfile.write(str(menu.scanshift.get()) + str(menu.scanctrl.get()) + str(menu.scanalt.get()) + "\n")
				exportfile.write(str(menu.experimentalResizing.get()) + "\n")
			menu.grabmods = str(menu.grabshift.get()) + str(menu.grabctrl.get()) + str(menu.grabalt.get())
			menu.scanmods = str(menu.scanshift.get()) + str(menu.scanctrl.get()) + str(menu.scanalt.get())
			self.set_hotkeys()
		return out_func