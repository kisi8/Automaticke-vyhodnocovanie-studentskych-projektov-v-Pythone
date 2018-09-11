'''
Author: Juraj Kyseľ (xkysel12)
E-mail: xkysel12@stud.fit.vutbr.cz
File: flask_app.py

This is the main file of flask application
containing complete routing and function calling.
'''

import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import checks
import constants
import ast2xml
import helper
from contextlib import redirect_stdout
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = constants.UPLOAD_FOLDER

def allowed_file(filename):
	'''
	Controling extension of file.

	:param filename: name of the file
	:type filename: string

	:returns: true/false
	:rtype: bool
	'''
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS

@app.route('/proj', methods=['GET', 'POST'])
def upload_file():
	'''
	Main paige of the system where student is submiting file.

	:returns: redirect to page
	:rtype: render template
	'''
	if request.method == 'POST':
		session['filename'] = 'gg'
		# kontrola loginu
		if request.form['fname'] == '':
			flash('Enter your login')
			return redirect(request.url)
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			session['filename'] = secure_filename(file.filename)
			# kontrola loginu
			if not checks.filename_login(session['filename'], request.form['fname']):
				flash('Inccorrect filename or not matching login')
				return redirect(request.url)

			file.save(os.path.join(app.config['UPLOAD_FOLDER'], session['filename']))

			session['login'] = request.form['fname']

			syn = checks.syntax_check(session['filename'])
			if syn != 0:
				flash('File cannot be compiled!')
				flash('%s' % syn)
				os.remove(constants.UPLOAD_FOLDER + '/' + session['filename'])
				return redirect(request.url)

			session['pep'] = checks.pep8_check(constants.UPLOAD_FOLDER + '/' + session['filename'])
			with open('pep.txt', 'w') as f:
				with redirect_stdout(f):
					checks.pep8_check(constants.UPLOAD_FOLDER + '/' + session['filename'])
			helper.pep8_make_html(session['filename'])
			session['pepfile'] = session['filename'] + '-pep.html'
			session['result'] = checks.checks(ast2xml.convert(constants.UPLOAD_FOLDER + '/' + session['filename']),constants.UPLOAD_FOLDER + '/' + session['filename'], session['filename'])

			# logovanie výsledku
			if not helper.is_List_Empty(session['result']):
				with open('/mnt/data/isj-2017-18/public/app/logs/%s.txt' % str(uuid.uuid4()), 'w')  as file:
					file.write(session['filename'])
					for item in session['result']:
						file.write(str(item))

			session['prak'] = helper.count_odporucania(session['result'])

			return redirect(url_for('eval', name=session['login']))
		else:
			flash('Python file required')
			return redirect(request.url)
	return render_template('home.html')

@app.route('/proj/logout', methods=['GET', 'POST'])
def logout():
	'''
	Logout page.

	:returns: redirect to page
	:rtype: render template
	'''
	try:
		os.remove('/mnt/data/isj-2017-18/public/app/templates/%s-pep.html' % session['filename'])
		os.remove('/mnt/data/isj-2017-18/public/app/pep.txt')
		os.remove('/mnt/data/isj-2017-18/public/app/syntax.txt')
		os.remove('/mnt/data/isj-2017-18/public/app/prints.py')
		os.remove('/mnt/data/isj-2017-18/public/app/assert.txt')
		os.remove('/mnt/data/isj-2017-18/public/app/list.txt')
		os.remove('/mnt/data/isj-2017-18/public/app/%s.txt' % session['filename'])
	except FileNotFoundError:
		pass
	session.pop('login', None)
	session.pop('filename', None)
	session.pop('pep', None)
	session.pop('result', None)
	session.pop('prak', None)
	session.pop('pepfile', None)
	return redirect(url_for('upload_file'))

@app.route('/proj/<name>', methods=['GET', 'POST'])
def eval(name):
	'''
	Evaluation page.

	:param name: name of student
	:type filename: string

	:returns: redirect to page
	:rtype: render template
	'''
	try:
		if session['login'] and session['filename']:
			# pep = session['pep'] pridať do returnu
			return render_template('eval.html', name = name, prak = session['prak'], pep = session['pep'])
	except KeyError:
		return redirect(url_for('upload_file'))

@app.route('/proj/<name>/pep8', methods=['GET', 'POST'])
def pep8(name):
	'''
	PEP 8 page.

	:param name: name of student
	:type filename: string

	:returns: redirect to page
	:rtype: render template
	'''
	source = helper.source_code(constants.UPLOAD_FOLDER + '/' + session['filename'])
	return render_template('pep8.html', source = source, pepfile = session['pepfile'])

@app.route('/proj/<name>/praktiky', methods=['GET', 'POST'])
def praktiky(name):
	'''
	Idioms page.

	:param name: name of student
	:type filename: string

	:returns: redirect to page
	:rtype: render template
	'''
	source = helper.source_code(constants.UPLOAD_FOLDER + '/' + session['filename'])
	return render_template('praktiky.html', source = source, result = session['result'])

if __name__ == '__main__':
	app.run()

from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(8090, site)
reactor.run()
