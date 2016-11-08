import search
import json

def get_all_nut(ingredients, weights):
	all_nutrients = []
	for i in ingredients:
		all_nutrients.append(search.get_nutrients(search.get_food_id(i)))
	f = sum(aggregate(all_nutrients, weights))

	return "{'Selenium, Se': '"+ str(f[0]) +" ug', 'Phosphorus, P': '"+ str(f[1]) +\
		   " mg', 'Protein': '"+ str(f[2]) +" g', 'Riboflavin': '"+ str(f[3]) + \
		   " mg', 'Fiber, total dietary': '"+ str(f[4]) +" g', 'Potassium, K': '" +\
		   str(f[5]) +" mg', 'Vitamin B-6': '"+ str(f[6]) +" mg', 'Magnesium, Mg': '"+ \
		   str(f[7]) +" mg', 'Vitamin D': '"+ str(f[8]) +" IU', 'Sodium, Na': '"+ \
		   str(f[8]) +" mg', 'Vitamin K (phylloquinone)': '"+ str(f[10]) +" ug', 'Thiamin': '"\
		   + str(f[11]) +" mg', 'Vitamin B-12': '"+ str(f[12]) +" ug', 'Vitamin A, IU': '"\
		   + str(f[13]) +" IU', 'Carbohydrate, by difference': '"+ str(f[14]) +\
		   " g', 'Sugars, total': '"+ str(f[15]) +" g', 'Calcium, Ca': '"+ str(f[16]) +\
		   " mg', 'Total lipid (fat)': '"+ str(f[17]) +" g', 'Iron, Fe': '"+ str(f[18]) +\
		   " mg', 'Niacin': '"+ str(f[19]) +" mg', 'Vitamin C, total ascorbic acid': '"+\
		    str(f[20]) +" mg', 'Energy': '"+ str(f[21]) +" kcal', 'Zinc, Zn': '"+ str(f[22]) +\
		    " mg', 'Folic acid': '"+ str(f[23]) +" ug', 'Cholesterol': '"+ str(f[24]) +" mg'}"

def aggregate(nutdata, weights):
	nutlists = []
	for data, weight in zip(nutdata, weights):
		nutlists.append(change_weight(extract_float(data), weight))
	return nutlists


def change_weight(lst, weight):
	new_list = []
	for el in lst:
		new_list.append(el * weight)
	return new_list


def extract_float(nut):
	amts = []
	j = json.loads(nut.encode('ascii', 'ignore'))
	current = []
	safe_extract("Selenium, Se", j)
	safe_extract("Phosphorus, P", j)
	safe_extract("Protein", j)
	safe_extract("Riboflavin", j)
	safe_extract("Fiber, total dietary", j)
	safe_extract("Potassium, K", j)
	safe_extract("Vitamin B-6", j)
	safe_extract("Magnesium, Mg", j)
	safe_extract("Vitamin D", j)
	safe_extract("Sodium, Na", j)
	safe_extract("Vitamin K (phylloquinone)", j)
	safe_extract("Thiamin", j)
	safe_extract("Vitamin B-12", j)
	safe_extract("Vitamin A, IU", j)
	safe_extract("Carbohydrate, by difference", j)
	safe_extract("Sugars, total", j)
	safe_extract("Calcium, Ca", j)
	safe_extract("Total lipid (fat)", j)
	safe_extract("Iron, Fe", j)
	safe_extract("Niacin", j)
	safe_extract("Vitamin C, total ascorbic acid", j)
	safe_extract("Energy", j)
	safe_extract("Zinc, Zn", j)
	safe_extract("Folic acid", j)
	safe_extract("Cholesterol", j)
	amts.extend(current)
	return amts

def safe_extract(name, j):
	if name in j:
		current.append(float((j[name].split())[0]))
	else:
		current.append(0)


def sum(amts):
	total = []
	for i in range(25):
		total.append(0)

	for i in amts:
		for j in range(25):
			total[j] = total[j] + i[j]
	return total 

def parseIngredient(s):
	lines = []
	nutrition = []
	multipliers = []
	for i in range(25):
		nutrition.append(0)

	ingredients = []
	lines = s.split("\n")

	for line in lines:
		result = parseSingleIngredient(line)
		if result != None:
			if result[0] != None and result[0] != "None" and type(result[0]) == str:
				tempWords = result[1:]
				ingredient_description = findBest(tempWords)
				if ingredient_description != None:
					ingredients.append(search.get_food_name(ingredient_description))

			multipliers.append(multiplier(result[0]))

	return get_all_nut(ingredients, multipliers)

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
