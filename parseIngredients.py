import search


def get_all_nut(ingredients, weights):
	all_nutrients = []
	for i in ingredients:
		all_nutrients.extend(search.get_nutrients(search.get_food_id(i)))
	aggregate(all_nutrients, weights)


def aggregate(nutdata, weights):
	nutlists = []
	for data, weight in zip(nutdata, weights):
		nutlists.append(change_weight(extract_float(data), weight))
	return nutlists


def change_weight(lst, weight):
	new_list = []
	for el in lst:
		new_list.extend(el * weight)
	return new_list


def extract_float(nut):
	amts = []
	for n in nut:
		for nut_name, amt in n.iteritems():
			amts.extend([float(a) for a in amt.split() if a.isdigit()])
	return amts


def parseIngredient(s):
	lines = []
	nutrition = []
	multipliers = []
	for i in range(25):
		nutrition.append(0)

	ingredients = []
	lines = s.split("\n")
	print "  OUTPUT  "
	for line in lines:
		result = parseSingleIngredient(line)
		if result != None:
			if result[0] != None and result[0] != "None" and type(result[0]) == str:
				tempWords = result[1:]
				ingredient_description = findBest(tempWords)
				ingredients.extend(search.get_food_name(ingredient_description))
			print " "
			multipliers.append(multiplier(result[0]))

			get_all_nut(ingredients, multipliers)




def multiplier(unitWeight):
	result = float(unitWeight[1:])
	if unitWeight[0] == 'v':
		result *= 0.228842
	elif unitWeight[0] == 'q':
		result *= 0.0089
	result *= 100
	return result

#getHits(string) return int; 
#volume to weight 0.228842
#quantities to weight 0.0089
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

globArray = []
length = 0
def permutations(remaining):
	global globArray
	global length
	if remaining == 0:
		returnlist = []
		for i in globArray:
			returnlist.append(i)
		return returnlist

	minIndex = 0
	for i in range(length-1,-1,-1):
		if globArray[i] == 1:
			minIndex = i+1
			break
	if minIndex == length:
		return None

	results = []
	for i in range(minIndex, length):
		globArray[i] = 1
		resultExtend = permutations(remaining-1)
		if resultExtend != None:
			if remaining == 1:
				results.append(resultExtend)
			else:
				results.extend(resultExtend)
		globArray[i] = 0
	return results

def findBest(words): #words is a non-empty list of strings
						#returns a string with words separated by spaces
	global globArray
	global length
	length = len(words)
	for i in range(len(words)):
		globArray.append(0) #0 is unclaimed, 1 is claimed (in input string)

	for i in range(len(words),0,-1):
		min = -1
		best = ""
		possibilities = []
		permute = permutations(i)
		for j in range(len(permute)):
			tempString = ""
			for k in range(len(words)):
				if permute[j][k] == 1:
					tempString += words[k] + " "
			possibilities.append(tempString)

		for j in possibilities:
			hits = search.get_hits(j)
			if hits!=0:
				if min == -1 or hits<min:
					best = j
					min = hits

		if min != -1:
			return best

	return None
