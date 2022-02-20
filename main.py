import numpy as np
import math
from flask import Flask, request, render_template, session, send_file
from werkzeug.utils import secure_filename
import os
import cv2 as cv

import imagedetector as imd
cwd=os.getcwd()
UPLOAD_FOLDER = cwd+'/uploads'

app = Flask(__name__, template_folder='templates')
app.secret_key = "derek"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	# data = {} #within data, have hyperlinks for the saved image along with the name of the html template to be loaded for that image  
	# data['abc'] = 'abcd'
	# for i in data:
	# 	print(i)

	data = [('imagename.png', 'imagename.html')]
	#Dashboard page for a single user
	#Adding a new file/project
	if request.method == 'POST':
		print("POSTING")
		if 'file' not in request.files:
			print('no file')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print('no filename')
			return redirect(request.url)
		filename = secure_filename(file.filename)
		print(app.config['UPLOAD_FOLDER'], type(app.config['UPLOAD_FOLDER']))
		print("name: ",filename)
		print("path:",os.path.join(app.config['UPLOAD_FOLDER']))
		print("new path:",os.path.join(os.getcwd()+'/static/images'))
		file.save(os.path.join(os.path.join(os.getcwd()+'/static/images'), filename))
		file.save(os.path.join(os.path.join(os.getcwd()+'/templates'), filename))

		file_path = '/static/images/' + filename
		"""
		here, have code to create html file
		and append (hyperlink of image, html template) to data   
		"""

		html_file_path = '/static/' + filename[:-4] + '.html'
		session['html_filename'] = filename[:-4] + '.html'

		imd.createHTML(filename, os.path.join(os.getcwd()+'/static/images/' + filename), os.path.join(os.path.join(os.getcwd()+'/templates')))
		imd.createHTML(filename, os.path.join(os.getcwd()+'/static/images/' + filename), os.path.join(os.getcwd()+'/static'))
		
		print("file_path:",file_path)
		# img = cv.imread(file_path)
		# img = cv.resize(img, (60, 60))
		# cv.imwrite(file_path, img)

		return render_template("dashboardtest.html", file_loc=file_path, html_file_loc=html_file_path, data=data) #Return same dashboard template, but with 

	return render_template("dashboardtest.html", data=data)
@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
	file_loc_now = os.getcwd() + '/static/' + session['html_filename']
	print(file_loc_now)
	filename_now = session['html_filename']
	return send_file(file_loc_now, attachment_filename=filename_now, as_attachment=True)
@app.route('/', methods=['GET', 'POST'])
def index():
	#Dashboard page
	return render_template("index.html")
@app.route('/view_page', methods=['GET', 'POST'])
def view_page():
	#Dashboard page

	return render_template(session['html_filename'])
@app.route('/test', methods=['GET', 'POST'])
def test():
	#Dashboard page
	data = [
	# (n, x, y, width, height, type, text )
	('5', '10', '700', '100', 'text', 'My Website'),
	('10', '150', '150', '110', 'button', 'MIT'),
	('200', '150', '200', '105', 'button', 'HHS'),
	('10', '265', '400', '200', 'text', 'Im just tryna be inside of you before you wake up'),
	('500', '150', '205', '330', 'text', 'Derek G. Tejas K. Pradyun K. Samay D.')
	]
	formattedData = []
	i = 1

	round_pixels = 10

	for tup in data:
		tupList = []
		tupList.append(i)
		for j in range(4):
			tupList.append("{}".format(round_pixels * math.ceil(int(tup[j])/round_pixels)))   
		tupList.append(tup[4])
		tupList.append(tup[5])
		formattedData.append(tuple(tupList))
		i+=1
	print(formattedData)

	return render_template("TestCreation.html", data=formattedData)


if __name__ == '__main__':
	app.run()
