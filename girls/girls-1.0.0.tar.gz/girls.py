def queen(girls):
	for each_girl in girls:
		if isinstance(each_girl,list):
			queen(each_girl)
		else:
			print(each_girl)