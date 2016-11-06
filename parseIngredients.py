def parseIngredient(s):
	lines = []
	start = 0
	i = 0

	for c in s:
		if c == '\n':
			lines.append(s[start:i])
			start = i+1
		i = i+1
	
	for line in lines:
		result = parseSingleIngredient(line)
		if result[0] != None:
			for k in result:
				print k
			print " "

def measurementToString(quantity, unit):
	if unit == "tablespoon" or unit == "tbsp":
		return "s" + str(quantity*3)
	if unit == "teaspoon" or unit == "tsp":
		return "s" + str(quantity)
	if unit == "cup":
		return "s" + str(quantity*48)
	if unit == "pint" or unit == "pt":
		return "s" + str(quantity*96)
	if unit == "quart" or unit == "qt":
		return "s" + str(quantity*192)
	if unit == "gallon" or unit == "gal":
		return "s" + str(quantity*768)
	if unit == "ounce" or unit == "oz":
		return "w" + str(quantity*28.3495)
	if unit == "milliliter" or unit == "millilitre" or unit == "ml":
		return "s" + str(quantity*0.202884)
	if unit == "liter" or unit == "litre" or unit == "l":
		return "s" + str(quantity*202.884)
	if unit == "grams" or unit == "g":
		return "w" + str(quantity)
	if unit == "kilogram" or unit == "kg":
		return "w" + str(quantity*1000)
	if unit == "pound" or unit == "lb":
		return "w" + str(quantity*453.592)

def parseSingleIngredient(line):
	measurements = ["tablespoon", "tbsp", "teaspoon", "tsp", "cup", "pint", "pt", "quart", \
					"qt", "gallon", "gal", "ounce", "oz", "milliliter", "ml", "liter", "litre" \
					"l", "grams", "g", "kilogram", "kg", "pound", "lb"]

	whole = 0 
	numerator = 0
	denominator = 0
	quantity = 0
	results = []
	j = 0

	if len(line) == 0 or line[0] < '0' or line[0] > '9':
		return None

	#finding quantity
	for c in line: 
		if c == ' ' or c == '/':
			break
		j = j+1
	if line[j] == ' ':
		whole = int(line[:j])
		line = line[j+1:]

		if line[0] >= '0' and line[0] <= '9':
			j = 0
			for d in line: 
				if d == '/':
					break
				j = j+1
			numerator = int(line[:j])
			line = line[j+1:]
			j = 0
			for d in line: 
				if d == ' ':
					break
				j = j+1
			denominator = int(line[:j])
			line = line[j+1:]
		else:
			numerator = 0
			denominator = 1
	elif line[j] == '/':
		whole = 0
		numerator = int(line[:j])

		line = line[j+1:]
		j = 0
		for d in line: 
			if d == ' ':
				break
			j = j+1
		denominator = int(line[:j])
		line = line[j+1:]
	quantity = float(whole) + float(numerator*1.0/denominator)

	#find next word and see if it is a quantity
	j = 0
	next = ""
	for c in line:
		if c == ' ':
			break
		j = j+1
	next = line[:j]
	line = line[j+1:]

	next = next.strip(".s,'")
	next = next.lower()

	isMeasurement = False
	for meas in measurements:
		if (meas == next):
			isMeasurement = True
	if isMeasurement == False:
		results.append("q" + str(quantity))
		results.append(next)
	else:
		results.append(measurementToString(quantity, next))

	words = line.split()
	for word in words:
		word.strip(".,!:;-/@#$%^&*()")
		results.append(word)

	return results
