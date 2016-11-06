from flask import Flask
from flask import request
from flask import render_template
import search
import json
import os
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import parseIngredients
from image_to_text import convert_to_text

UPLOAD_FOLDER = '/Users/RobertPan/Documents/recipe-nutrition-master/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/', methods=['GET','POST'])
def my_index_post():
	try:
		text = request.form['text']
		name = search.get_food_name(text)
		nutrients = json.loads(search.get_nutrients(search.get_food_id(text)))
	except:
		if request.method == 'POST':
			if 'file' not in request.files:
				flash('No file part')
				return redirect(request.url)
			file = request.files['file']
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				flash('No selected file')
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				nutritions = convert_to_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return '''
		<!doctype html>
		<title>Upload new File</title>
		<h1>Upload new File</h1>
		<form action="" method=post enctype=multipart/form-data>
		  <p><input type=file name=file>
			<input type=submit value=Upload>
		</form>
		'''
	return render_template("index.html", name = name, nutrients = nutrients)



def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == "__main__":
	app.run()
