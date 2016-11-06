import sqlite3
import json
import sys

conn = sqlite3.connect('nutrients.db')
c = conn.cursor()

def get_nutrients(id):
	c.execute("""
	  SELECT
	    name,
	    units,
	    amount
	  FROM nutrition
	  JOIN nutrient
	  JOIN common_nutrient
	  ON nutrition.food_id = ?
	  AND nutrition.nutrient_id = nutrient.id
	  AND nutrient.id = common_nutrient.id
	""", (id,))
	vals = {}
	for row in c:
	  vals[row[0]] = str(row[2]) + ' ' + row[1]

	return json.dumps(vals, sort_keys=True, indent=4)
	
def get_food_id(text):
	search_clause = '%' + text + '%'
	c.execute('SELECT id, long_desc FROM food WHERE long_desc LIKE ?', (search_clause,))
	try:
		item = get_simplest(c.fetchall())
	except IndexError:
		return "Not found!"
	return item[0]

def get_food_name(text):
	search_clause = '%' + text + '%'
	c.execute('SELECT id, long_desc FROM food WHERE long_desc LIKE ?', (search_clause,))
	try:
		item = get_simplest(c.fetchall())
	except IndexError:
		return "Not found!"
	return item[1]


def get_simplest(dlst):
	x = len(dlst[0][1])
	xk = 0
	for i in range(0, len(dlst)):
		if x < len(dlst[i][1]):
			pass
		else:
			x = len(dlst[i][1])
			xk = i
	return dlst[xk]
