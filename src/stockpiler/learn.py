def Learn(LearnInt, image):
	global counter
	global IconName
	global LastStockpile
	# grab whole screen and prepare for template matching
	# COMMENT OUT THESE TWO LINES IF YOU ARE TESTING A SPECIFIC IMAGE
	TestImage = False

	# WHEN USING OTHER RESOLUTIONS, GRAB THEM HERE
	resx = 1920
	resy = 1080

	try:
		# OKAY, so you'll have to grab the whole screen, detect that thing in the upper left, then use that as a basis
		# for cropping that full screenshot down to just the foxhole window
		screen = np.array(ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True))
		screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

		numbox = cv2.imread('CheckImages//StateOf.png', cv2.IMREAD_GRAYSCALE)
		res = cv2.matchTemplate(screen, numbox, cv2.TM_CCOEFF_NORMED)
		threshold = .95
		if np.amax(res) > threshold:
			stateloc = np.where(res >= threshold)
			if stateloc[0].astype(int) - 35 >= 0:
				statey = stateloc[0].astype(int) - 35
			else:
				statey = 0
			if stateloc[1].astype(int) - 35 >= 0:
				statex = stateloc[1].astype(int) - 35
			else:
				statex = 0
			# If/when it moves to multiple resolutions, these hardcoded sizes will need to be variables
			screen = screen[int(statey):int(statey) + resy, int(statex):int(statex) + resx]
			print("It thinks it found the window position in Learn and is grabbing location: X:", str(statex), " Y:", str(statey))
			if menu.debug.get() == 1:
				cv2.imshow('Grabbed in Learn, found State of War', screen)
				cv2.waitKey(0)
		else:
			print("State of the War not found in Learn.  It may be covered up or you're not on the map.")
			if menu.debug.get() == 1:
				cv2.imshow('Grabbed in Learn, did NOT find State of War', screen)
				cv2.waitKey(0)
	except Exception as e:
		print("Exception: ", e)
		print("Failed to grab the screen in Learn")
		logging.info(str(datetime.datetime.now()) + " Failed Grabbing the screen in Learn " + str(e))

	# UNCOMMENT AND MODIFY LINE BELOW IF YOU ARE TESTING A SPECIFIC IMAGE
	# screen = cv2.cvtColor(np.array(Image.open("test_2021-11-25-110247.png")), cv2.COLOR_RGB2GRAY)
	# TestImage = True

	if LearnInt != "":
		pass
	else:
		screen = LastStockpile

	numbox = cv2.imread('CheckImages//NumBox.png', cv2.IMREAD_GRAYSCALE)
	res = cv2.matchTemplate(screen, numbox, cv2.TM_CCOEFF_NORMED)
	threshold = .99
	if np.amax(res) > threshold:
		numloc = np.where(res >= threshold)
		print("found them here:", numloc)
		print(len(numloc[0]))
		for spot in range(len(numloc[0])):
			# Stockpiles never displayed in upper left under State of the War area
			# State of the War area throws false positives for icons
			if numloc[1][spot] < (resx * .2) and numloc[0][spot] < (resy * .24) and not TestImage:
				pass
			else:
				print("x:", numloc[1][spot], " y:",numloc[0][spot])
				# cv2.imshow('icon', screen[int(numloc[0][spot]+2):int(numloc[0][spot]+36), int(numloc[1][spot]-38):numloc[1][spot]-4])
				# cv2.waitKey(0)
				currenticon = screen[int(numloc[0][spot]+2):int(numloc[0][spot]+36), int(numloc[1][spot]-38):numloc[1][spot]-4]
				print("currenticon:", currenticon.shape)
				if menu.Set.get() == 0:
					folder = "CheckImages//Default//"
				else:
					folder = "CheckImages//Modded//"
				Found = False
				for imagefile in os.listdir(folder):
					checkimage = cv2.imread(folder + imagefile, cv2.IMREAD_GRAYSCALE)
					print("Checking for ", str(imagefile))
					result = cv2.matchTemplate(currenticon, checkimage, cv2.TM_CCOEFF_NORMED)
					threshold = .99
					if np.amax(result) > threshold:
						#print("Found:", imagefile)
						Found = True
						break
				if not Found:
					print("Not found, should launch IconPicker")
					IconCatPicker(currenticon, 0)
					# IconPicker(currenticon)
		SearchImage(1, screen)
		CreateButtons("blah")
	else:
		print("Found no numboxes, which is very strange")
		if menu.debug.get() == 1:
			cv2.imshow("No numboxes?", screen)
			cv2.waitKey(0)