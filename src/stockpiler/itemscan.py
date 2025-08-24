def ItemScan(screen, garbage):
	global LastStockpile
	global bestTextScale
	global bestIconScale

	resC = None
	res = None
	if menu.Set.get() == 0:
		findshirtC = cv2.imread('CheckImages//Default//86C.png', cv2.IMREAD_GRAYSCALE)
		findshirt = cv2.imread('CheckImages//Default//86.png', cv2.IMREAD_GRAYSCALE)

		if (menu.experimentalResizing.get() == 1):
			if (bestIconScale == None):
				if (foxhole_height == 1080):
					bestIconScale = 1.0
					print("Best scale for ITEM ICONS is: " + str(bestIconScale))
				else:
					best_score, bestIconScale, resC = matchTemplateBestScale(screen, findshirtC, numtimes=20)
					print("Best scale for ITEM ICONS is: " + str(bestIconScale) + " with a score of: " + str(best_score))
			else:
				print("Best scale for ITEM ICONS is: " + str(bestIconScale))
			findshirtC = cv2.resize(findshirtC, (int(findshirtC.shape[1]*bestIconScale), int(findshirtC.shape[0]*bestIconScale)))
			findshirt = cv2.resize(findshirt, (int(findshirt.shape[1]*bestIconScale), int(findshirt.shape[0]*bestIconScale)))

			
	else:
		try:
			findshirtC = cv2.imread('CheckImages//Modded//86C.png', cv2.IMREAD_GRAYSCALE)
		except Exception as e:
			print("Exception: ", e)
			print("You don't have the Shirt crate yet in ItemScan")
			logging.info(str(datetime.datetime.now()) + " Failed loading modded shirt crate icon in ItemScan " + str(e))
		try:
			findshirt = cv2.imread('CheckImages//Modded//86.png', cv2.IMREAD_GRAYSCALE)
		except Exception as e:
			print("Exception: ", e)
			print("You don't have the individual Shirt yet in ItemScan")
			logging.info(str(datetime.datetime.now()) + " Failed loading modded individual shirt icon in ItemScan " + str(e))
	try:
		if (resC == None): resC = cv2.matchTemplate(screen, findshirtC, cv2.TM_CCOEFF_NORMED)
	except Exception as e:
		print("Exception: ", e)
		print("Looks like you're missing the shirt crate in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Maybe missing shirt crate icon in ItemScan " + str(e))
	try:
		res = cv2.matchTemplate(screen, findshirt, cv2.TM_CCOEFF_NORMED)
	except Exception as e:
		print("Exception: ", e)
		print("Looks like you're missing the individual shirts in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Maybe missing individual shirt icon in ItemScan " + str(e))
	threshold = .9
	FoundShirt = False
	try:
		if np.amax(res) > threshold:
			print("Found Shirts")
			y, x = np.unravel_index(res.argmax(), res.shape)
			FoundShirt = True
	except Exception as e:
		print("Exception: ", e)
		print("Don't have the individual shirts icon or not looking at a stockpile in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Don't have the individual shirts icon or not looking at a stockpile in ItemScan " + str(e))
	try:
		if np.amax(resC) > threshold:
			print("Found Shirt Crate")
			#print(np.amax(resC))
			y, x = np.unravel_index(resC.argmax(), resC.shape)
			FoundShirt = True
	except Exception as e:
		print("Exception: ", e)
		print("Don't have the shirt crate icon or not looking at a stockpile in ItemScan")
		logging.info(str(datetime.datetime.now()) + " Don't have the shirt crate icon or not looking at a stockpile in ItemScan " + str(e))
	if not FoundShirt:
		print("Found nothing.  Either don't have shirt icon(s) or not looking at a stockpile in ItemScan")
		y = 0
		x = 0

	# COMMENT OUT IF TESTING A SPECIFIC IMAGE
	if y == x == 0:
		stockpile = screen
	else:
		stockpile = screen[y - 32:1080, x - 11:x + 589]

	if menu.debug.get() == 1:
		cv2.imshow('Stockpile in this image in ItemScan?', stockpile)
		cv2.waitKey(0)
	# UNCOMMENT IF TESTING A SPECIFIC IMAGE
	# stockpile = screen

	# Grab this just in case you need to rerun the scan from Results tab
	# LastStockpile = stockpile
	LastStockpile = screen

	# Image clips for each type of stockpile should be in this array below
	StockpileTypes = (('CheckImages//Seaport.png', 'Seaport', 0), ('Checkimages//StorageDepot.png', 'Storage Depot', 1),
					  ('Checkimages//Outpost.png', 'Outpost', 2), ('Checkimages//Townbase.png', 'Town Base', 3),
					  ('Checkimages//RelicBase.png', 'Relic Base', 4),
					  ('Checkimages//BunkerBase.png', 'Bunker Base', 5),
					  ('Checkimages//Encampment.png', 'Encampment', 6),
					  ('Checkimages//SafeHouse.png', 'Safe House', 7))
	# Check cropped stockpile image for each location type image
	FoundStockpileType = None
	FoundStockpileTypeName = None
	highestScore = 0
	y = 0
	x = 0
	for image in StockpileTypes:
		try:
			findtype = cv2.imread(image[0], cv2.IMREAD_GRAYSCALE)
			if menu.debug.get() == 1:
				cv2.imshow("Looking for this", findtype)
				cv2.waitKey(0)
			if (menu.experimentalResizing.get() == 1): findtype = cv2.resize(findtype, (int(findtype.shape[1]*bestTextScale), int(findtype.shape[0]*bestTextScale)))
			res = cv2.matchTemplate(stockpile, findtype, cv2.TM_CCOEFF_NORMED)
			# Threshold is a bit lower for types as they are slightly see-thru
			typethreshold = .65
			score = np.amax(res)
			#print("Checking:", image[1])
			#print(score)
			if (score > typethreshold and score > highestScore):
				highestScore = score
				y, x = np.unravel_index(res.argmax(), res.shape)
				FoundStockpileType = image[2]
				FoundStockpileTypeName = image[1]
			
		except Exception as e:
			print("Exception: ", e)
			print("Probably not looking at a stockpile or don't have the game open.  Looked for: ", str(image))
			FoundStockpileType = None
			ThisStockpileName = None
			logging.info(str(datetime.datetime.now()) + " Probably not looking at a stockpile or don't have the game open.")
			logging.info(str(datetime.datetime.now()) + " Looked for: ", str(image) + str(e))
			pass
	
	if (FoundStockpileType != None):
		if FoundStockpileTypeName == "Seaport" or FoundStockpileTypeName == "Storage Depot":
			findtab = cv2.imread('CheckImages//Tab.png', cv2.IMREAD_GRAYSCALE)
			if (menu.experimentalResizing.get() == 1): findtab = cv2.resize(findtab, (int(findtab.shape[1]*bestTextScale), int(findtab.shape[0]*bestTextScale)))
			res = cv2.matchTemplate(stockpile, findtab, cv2.TM_CCOEFF_NORMED)
			tabthreshold = .6
			cv2.imwrite('stockpile.jpg', stockpile)
			if np.amax(res) > tabthreshold:
				print("Found the Tab")
				y, x = np.unravel_index(res.argmax(), res.shape)
				# Seaports and Storage Depots have the potential to have named stockpiles, so grab the name
				#print("bestTextScale:" + str(bestTextScale))
				stockpilename = stockpile[int(y - 5*bestTextScale):int(y + 17*bestTextScale), int(x - 150*bestTextScale):int(x - 8*bestTextScale)]
				# Make a list of all current stockpile name images
				currentstockpiles = glob.glob("Stockpiles/*.png")
				# print(currentstockpiles)
				found = 0
				for image in currentstockpiles:
					stockpilelabel = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
					if not image.endswith("image.png"):
						res = cv2.matchTemplate(stockpilename, stockpilelabel, cv2.TM_CCOEFF_NORMED)
						threshold = .97
						flag = False
						if np.amax(res) > threshold:
							# Named stockpile is one already seen
							found = 1
							ThisStockpileName = (image[11:(len(image) - 4)])
				if found != 1:
					newstockpopup(stockpilename)
					PopupWindow.wait_window()
					if NewStockpileName == "" or NewStockpileName.lower() == "public":
						popup("BlankName")
						ThisStockpileName = "TheyLeftTheStockpileNameBlank"
					else:
						# NewStockpileFilename = 'Stockpiles//' + NewStockpileName + '.png'
						# It's a new stockpile, so save an images of the name as well as the cropped stockpile itself
						cv2.imwrite('Stockpiles//' + NewStockpileName + '.png', stockpilename)
						if menu.ImgExport.get() == 1:
							cv2.imwrite('Stockpiles//' + NewStockpileName + ' image.png', stockpile)
						ThisStockpileName = NewStockpileName
			else:
				# It's not a named stockpile, so just call it by the type of location (Bunker Base, Encampment, etc)
				print("Didn't find the Tab, so it looks like it's not a named stockpile")
				ThisStockpileName = FoundStockpileTypeName
		else:
			# It's not a named stockpile, so just call it by the type of location (Bunker Base, Encampment, etc)
			print("Not a named stockpile, it's a Bunker Base, Encampment, something like that")
			ThisStockpileName = FoundStockpileTypeName
		# StockpileName = StockpileNameEntry.get()
		# cv2.imwrite('Stockpiles//' + StockpileName + '.png', stockpilename)
	else:
		# print("Didn't find",image[1])
		print("Doesn't look like any known stockpile type")
		FoundStockpileType = "None"
		ThisStockpileName = "None"
		pass

	# These stockpile types allow for crates (ie: Seaport)
	CrateList = [0, 1]
	# These stockpile types only allow individual items (ie: Bunker Base)
	SingleList = [2, 3, 4, 5, 6, 7]

	start = datetime.datetime.now()

	print(ThisStockpileName)
	if ThisStockpileName == "TheyLeftTheStockpileNameBlank":
		pass
	else:
		if menu.Set.get() == 0:
			folder = "CheckImages//Default//"
		else:
			folder = "CheckImages//Modded//"
		if ThisStockpileName != "None":
			if menu.ImgExport.get() == 1:
				cv2.imwrite('Stockpiles//' + ThisStockpileName + ' image.png', stockpile)
			if FoundStockpileType in CrateList:
				print("Crate Type")
				# Grab all the crate CheckImages
				#print(item)
				#print(items.data[1])
				StockpileImages = [(str(item[0]), folder + str(item[0]) + "C.png", (item[3] + " Crate"), item[8], item[12]) for item in items.data if str(item[19]) == "0"]
				#print(StockpileImages)
				# Grab all the individual vehicles and shippables, make sure the two if's are the right category.  Was incorrectly set to 7 (uniforms) and 8 (vehicles) instead of 8 (vecicles) and 9 (shippables)
				StockpileImagesAppend = [(str(item[0]), folder + str(item[0]) + ".png", item[3], item[8], item[11]) for item in items.data if (str(item[9]) == "8" and str(item[19]) == "0") or (str(item[9]) == "9" and str(item[19]) == "0")]
				StockpileImages.extend(StockpileImagesAppend)
				#print(StockpileImages)
				#print("Checking for:", StockpileImages)
			elif FoundStockpileType in SingleList:
				print("Single Type")
				# Grab all the individual items
				# for item in range(len(items.data)):
				# 	print(item)
				StockpileImages = [(str(item[0]), folder + str(item[0]) + ".png", item[3], item[8], item[11]) for item in items.data]
				#print("Checking for:", StockpileImages)
			else:
				print("No idea what type...")


			stockpilecontents = []
			checked = 0
			#print("StockpileImages", StockpileImages)
			numbers = {}
			for number in items.numbers:
				findnum = cv2.imread(number[0], cv2.IMREAD_GRAYSCALE)
				if (menu.experimentalResizing.get() == 1 and bestIconScale != 1.0):
					findnum = cv2.resize(findnum, (int(findnum.shape[1] * bestIconScale), int(findnum.shape[0] * bestIconScale)))
				numbers[number[1]] = findnum
			
			threshold = .98 if (menu.experimentalResizing.get() == 1 and foxhole_height != 1080) else .99   
			for image in StockpileImages:
				checked += 1
				if str(image[4]) == '1':
					if os.path.exists(image[1]):
						try:
							findimage = cv2.imread(image[1], cv2.IMREAD_GRAYSCALE)
							if (menu.experimentalResizing.get() == 1 and bestIconScale != 1.0): findimage = cv2.resize(findimage, (int(findimage.shape[1] * bestIconScale), int(findimage.shape[0] * bestIconScale)), interpolation=cv2.INTER_LANCZOS4)
							
							res = cv2.matchTemplate(stockpile, findimage, cv2.TM_CCOEFF_NORMED)
							
							#if (image[0] == "46"):
							#	print("Item" + repr(np.amax(res)))
							#elif (image[0] == "92"):
							#	print("Item" + repr(np.amax(res)))
							#elif (image[0] == "279"):
							#	print("Item" + repr(np.amax(res)))
							
							flag = False
							if np.amax(res) > threshold:
								#print(image[1] + ": " + str(np.amax(res)))
								flag = True
								y, x = np.unravel_index(res.argmax(), res.shape)
								# Found a thing, now find amount
								numberlist = []
								numberarea = stockpile[int(y+8*bestTextScale):int(y+28*bestTextScale), int(x+45*bestTextScale):int(x+87*bestTextScale)]
								for number in items.numbers:
									# Clip the area where the stock number will be
									
									resnum = cv2.matchTemplate(numberarea, numbers[number[1]], cv2.TM_CCOEFF_NORMED)
									threshold = .9
									numloc = np.where(resnum >= threshold)
									# It only looks for up to 3 of each number for each item, since after that it would be a "k+" scenario, which never happens in stockpiles
									# This will need to be changed to allow for more digits whenever it does in-person looks at BB stockpiles and such, where it will show up to 5 digits
									if len(numloc[1]) > 0:
										numberlist.append(tuple([numloc[1][0],number[1]]))
									if len(numloc[1]) > 1:
										numberlist.append(tuple([numloc[1][1],number[1]]))
									if len(numloc[1]) > 2:
										numberlist.append(tuple([numloc[1][2],number[1]]))
									# Sort the list of numbers by position closest to the left, putting the numbers in order by extension
									numberlist.sort(key=lambda y: y[0])

								# If the number ends in a K, it just adds 000 since you don't know if that's 1001 or 1999
								# k+ never happens in stockpiles, so this only affects town halls, bunker bases, etc
								quantity = 0
								if len(numberlist) == 1:
									quantity = int(str(numberlist[0][1]))
								elif len(numberlist) == 2:
									if numberlist[1][1] == "k+":
										quantity = int(str(numberlist[0][1]) + "000")
									else:
										quantity = int(str(numberlist[0][1]) + (str(numberlist[1][1])))
								elif len(numberlist) == 3:
									if numberlist[2][1] == "k+":
										quantity = int(str(numberlist[0][1]) + (str(numberlist[1][1])) + "000")
									else:
										quantity = int(str(numberlist[0][1]) + (str(numberlist[1][1])) + str(numberlist[2][1]))
								elif len(numberlist) == 4:
									if numberlist[3][1] == "k+":
										quantity = int(str(numberlist[0][1]) + (str(numberlist[1][1])) + str(numberlist[2][1]) + "000")
									else:
										quantity = int(str(numberlist[0][1]) + (str(numberlist[1][1])) + str(numberlist[2][1]) + str(numberlist[3][1]))
								# place shirts first, since they're always at the top of every stockpile
								if image[0] == "86":
									itemsort = 0
								# bunker supplies next
								elif image[0] == "93":
									itemsort = 1
								# garrison supplies last
								elif image[0] == "90":
									itemsort = 2
								elif image[3] != "Vehicle" and image[3] != "Shippables":
									itemsort = 5
								elif image[3] == "Vehicle":
									itemsort = 10
								else:
									itemsort = 15
								if image[1][(len(image[1])-5):(len(image[1])-4)] == "C":
									stockpilecontents.append(list((image[0], image[2], quantity, itemsort, 1)))
								else:
									stockpilecontents.append(list((image[0], image[2], quantity, itemsort, 0)))
						except Exception as e:
							print("Exception: ", e)
							if menu.debug.get() == 1:
								print("Failed while looking for: ", str(image[2]))
								logging.info(str(datetime.datetime.now()) + "Failed while looking for (missing?): ", str(image[2]) + str(e))
							pass
					else:
						if menu.debug.get() == 1:
							print("File missing:",str(image[1]), str(image[2]))
				else:
					if menu.debug.get() == 1:
						print("Skipping icon: ", str(image[2]), "because ItemNumbering.csv lists it as impossible/never displayed in stockpile images (like pistol ammo and crates of warheads)", image[4])
					pass

			items.sortedcontents = list(sorted(stockpilecontents, key=lambda x: (x[3], x[4], -x[2])))
			# Here's where we sort stockpilecontents by category, then number, so they spit out the same as screenshot
			# Everything but vehicles and shippables first, then single vehicle, then crates of vehicles, then single shippables, then crates of shippables
			if ThisStockpileName in ("Seaport","Storage Depot","Outpost","Town Base","Relic Base","Bunker Base","Encampment","Safe House"):
				ThisStockpileName = "Public"

			if menu.CSVExport.get() == 1:
				stockpilefile = open("Stockpiles//" + ThisStockpileName + ".csv", 'w')
				stockpilefile.write(ThisStockpileName + ",\n")
				stockpilefile.write(FoundStockpileTypeName + ",\n")
				stockpilefile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ",\n")
				stockpilefile.close()

				# Writing to both csv and xlsx, only the quantity and name is written
				# If more elements from items.data are added to stockpilecontents, they could be added to these exports as fields
				with open("Stockpiles//" + ThisStockpileName + ".csv", 'a') as fp:
					# fp.write('\n'.join('{},{},{}'.format(x[0],x[1],x[2]) for x in stockpilecontents))
					############### THIS ONE DOES IN REGULAR ORDER ############
					# fp.write('\n'.join('{},{}'.format(x[1],x[2]) for x in stockpilecontents))
					############### THIS ONE DOES IN SORTED ORDER #############
					fp.write('\n'.join('{},{}'.format(x[1], x[2]) for x in items.sortedcontents))
				fp.close()


			if menu.updateBot.get() == 1 and ThisStockpileName != "Public":
				requestObj = {
					"password": menu.BotPassword.get(),
					"name": ThisStockpileName,
					"guildID": menu.BotGuildID.get()
				}
				data = []
				for x in items.sortedcontents:
					data.append([x[1], x[2]])
				requestObj["data"] = data

				# print("Bot Data", data)

				try:
					r = requests.post(menu.BotHost.get(), json=requestObj, timeout=10)
					response = r.json()
					
					print("=============== [Storeman Bot Link: Sending to Server] ===============")
					storemanBotPrefix = "[Storeman Bot Link]: "
					if (response["success"]): print(storemanBotPrefix + "Scan of " + ThisStockpileName + " has been received by the server successfully. Your logisitics channel will be updated shortly if you have set one (you can use /spstatus on your server for instant updates")
					elif (response["error"] == "empty-stockpile-name"): print(storemanBotPrefix + "Stockpile name is invalid. Perhaps the stockpile name was not detected or empty.")
					elif (response["error"] == "invalid-password"): print(storemanBotPrefix + "Invalid password, check that the Bot Password is correct.")
					elif (response["error"] == "invalid-guild-id"): print(storemanBotPrefix + "The Guild ID entered was not found on the Storeman Bot server. Please check that it is correct.")
					else: print(storemanBotPrefix + "An unhandled error occured: " + response["error"])

					print("=============== [Storeman Bot Link: End of Request] ===============")
				except Exception as e:
					print("There was an error connecting to the Bot")
					print("Exception: ", e)


			if menu.XLSXExport.get() == 1:
				workbook = xlsxwriter.Workbook("Stockpiles//" + ThisStockpileName + ".xlsx")
				worksheet = workbook.add_worksheet()
				worksheet.write(0, 0, ThisStockpileName)
				worksheet.write(1, 0, FoundStockpileTypeName)
				worksheet.write(2, 0, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
				row = 3
				for col, data in enumerate(items.sortedcontents):
					# print("col", col, " data", data)
					worksheet.write(row + col, 0, data[1])
					worksheet.write(row + col, 1, data[2])
				workbook.close()
			print(datetime.datetime.now()-start)
			print("Items Checked:",checked)
			items.slimcontents = items.sortedcontents
			for sublist in items.slimcontents:
				del sublist[3:5]
			ResultSheet.set_sheet_data(data=items.slimcontents)
		else:
			popup("NoStockpile")