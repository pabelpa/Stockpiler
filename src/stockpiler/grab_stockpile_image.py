# Function used simply for grabbing cropped stockpile images
# Helpful for grabbing test images for assembling missing icons or new sets of icons (for modded icons)
def GrabStockpileImage():
	global counter
	global bestTextScale
	global bestIconScale
	global foxhole_height
	global foxhole_width
	global width_ratio
	global height_ratio
	# OKAY, so you'll have to grab the whole screen, detect that thing in the upper left, then use that as a basis
	# for cropping that full screenshot down to just the foxhole window

	threshold = .95

	if (menu.experimentalResizing.get() == 1):
		print("==============EXPERIMENTAL RESIZING==============")
		window = gw.getWindowsWithTitle("War")
		if (len(window) > 0):
			foxhole_height = window[0].height - 39
			foxhole_width = window[0].width - 16
		else:
			print("[Warning: !!!] Foxhole window not detected")
		print(f"Foxhole screen size is: {foxhole_width}x{foxhole_height}")
		width_ratio = foxhole_width / 1920 
		height_ratio = foxhole_height / 1080
		print(f"Screen Ratio to original 1920x1080: {width_ratio}x{height_ratio}")
				
	screen = np.array(ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True))
	screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

	numbox = cv2.imread('CheckImages//StateOf.png', cv2.IMREAD_GRAYSCALE)
	
	best_score = None
	res = None

	if (menu.experimentalResizing.get() == 1):
		if (foxhole_height == 1080): bestTextScale = 1.0
		elif (not bestTextScale):
			best_score, bestTextScale, res = matchTemplateBestScale(screen, numbox, numtimes=20)
	else:
		bestTextScale = 1.0
	
	if (not best_score):
		if (menu.experimentalResizing.get() == 1): numbox = cv2.resize(numbox, (int(numbox.shape[1]*bestTextScale), int(numbox.shape[0]*bestTextScale)))
		
		res = cv2.matchTemplate(screen, numbox, cv2.TM_CCOEFF_NORMED)
		best_score = np.amax(res)
	
	print("Best scale for TEXT is: " + str(bestTextScale) + " with a score of: " + str(best_score))
	
	threshold = .7
	if best_score > threshold:
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		statex, statey = max_loc
		margin_ratioed = 35 * height_ratio
		if statey - margin_ratioed >= 0:
			statey = statey - margin_ratioed
		else:
			statey = 0
		if statex - margin_ratioed >= 0:
			statex = statex - margin_ratioed
		else:
			statex = 0

		screen = screen[int(statey):int(statey + (1079 * height_ratio)), int(statex):int(statex + (1919 * width_ratio))]
		if menu.debug.get() == 1:
			cv2.imshow("Grabbed in image GrabStockpileImage", screen)
			cv2.waitKey(0)
		if menu.Set.get() == 0:
			findshirtC = cv2.imread('CheckImages//Default//86C.png', cv2.IMREAD_GRAYSCALE)
			findshirt = cv2.imread('CheckImages//Default//86.png', cv2.IMREAD_GRAYSCALE)
		else:
			findshirtC = cv2.imread('CheckImages//Modded//86C.png', cv2.IMREAD_GRAYSCALE)
			findshirt = cv2.imread('CheckImages//Modded//86.png', cv2.IMREAD_GRAYSCALE)

		# Shirts are always in the same spot in every stockpile, but might be single or crates
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
		try:
			resC = cv2.matchTemplate(screen, findshirtC, cv2.TM_CCOEFF_NORMED)
		except Exception as e:
			print("Exception: ", e)
			print("Maybe you don't have the shirt crate")
			logging.info(str(datetime.datetime.now()) + " Exception loading shirt crate icon in GrabStockpileImage " + str(e))
		try:
			res = cv2.matchTemplate(screen, findshirt, cv2.TM_CCOEFF_NORMED)
		except Exception as e:
			print("Exception: ", e)
			print("Maybe you don't have the individual shirt")
			logging.info(str(datetime.datetime.now()) + " Exception loading individual shirt icon in GrabStockpileImage " + str(e))
		threshold = .99
		FoundShirt = False
		try:
			if np.amax(res) > threshold:
				print("Found Shirts")
				y, x = np.unravel_index(res.argmax(), res.shape)
				FoundShirt = True
		except Exception as e:
			print("Exception: ", e)
			print("Don't have the individual shirts icon or not looking at a stockpile")
			logging.info(str(datetime.datetime.now()) + " Exception finding individual shirt icon in GrabStockpileImage " + str(e))
		try:
			if np.amax(resC) > threshold:
				print("Found Shirt Crate")
				y, x = np.unravel_index(resC.argmax(), resC.shape)
				FoundShirt = True
		except Exception as e:
			print("Exception: ", e)
			print("Don't have the shirt crate icon or not looking at a stockpile")
			logging.info(str(datetime.datetime.now()) + " Exception finding shirt crate icon in GrabStockpileImage " + str(e))
		if not FoundShirt:
			print("Found nothing.  Either don't have shirt icon(s) or not looking at a stockpile")
			y = 0
			x = 0
		# If no stockpile was found, don't bother taking a screenshot, else crop based on where shirts were found
		if x == 0 and y == 0:
			print("Both 0's")
			pass
		else:
			stockpile = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
			stockpile = stockpile[int(y) - 32:int(y) + 1080, int(x) - 11:int(x) + 589]
			imagename = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
			fullimagename = 'test_' + imagename + '.png'
			cv2.imwrite(fullimagename, stockpile)
			logging.info(str(datetime.datetime.now()) + " Saved image with GrabStockpileImage named " + fullimagename)
	else:
		print("No State of the War detected in top left corner.  Either it is covered by something (Stockpiler maybe?)"
			  " or the map is not open")