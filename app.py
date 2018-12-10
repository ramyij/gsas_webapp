import os
from flask import Flask, render_template, request, session, jsonify
import functions as fn
from PIL import Image
from flask_session import Session
import json
from time import sleep

app = Flask(__name__)
sess = Session()
# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.secret_key = 'supersecret1234'
app.config['SESSION_TYPE'] = SESSION_TYPE


app.config.from_object(__name__)
sess.init_app(app)
# app.run()


UPLOAD_FOLDER = os.path.join('static','uploads') #'mysite',  add for pythonanywhere hosting
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

RESULTS_FOLDER = os.path.join('static','results')
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)
    session['uploaded_image'] = f
    return render_template('index.html',display_image = f)

@app.route('/results', methods=['GET', 'POST'])
def get_results():
	uploaded_image = session.get('uploaded_image',None)
	# alpha = request.form["sliderGlare"]
	inputs = jsonify(request.form).response[0]
	inputs_dict = json.loads(inputs)
	message = inputs_dict

	
	processed_image, perc_wrinkle = fn.process_image(uploaded_image, threshold_1 = int(inputs_dict.get("background",20)), resize=None, alpha=int(inputs_dict.get('alpha',60)), beta = int(inputs_dict.get('beta',0)))
	message3 = "Percent Wrinkled: %s " % perc_wrinkle

	fn.plot_wrinkle_class(processed_image,uploaded_image)
    
	im = uploaded_image.split('/')[-1].split('.')[0]+'_wrinkle.png'
	f = os.path.join(app.config['RESULTS_FOLDER'], im)
	return render_template('results.html',display_image = f, message3 = message)

