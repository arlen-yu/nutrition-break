from flask import Flask
from flask import request
from flask import render_template
import search
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_index_post():
	text = request.form['text']
	name = search.get_food_name(text)
	nutrients = json.loads(search.get_nutrients(search.get_food_id(text)))
	return render_template("index.html", name = name, nutrients = nutrients)


if __name__ == "__main__":
	app.run()
