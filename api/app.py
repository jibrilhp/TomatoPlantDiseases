from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap

import os
import model

app = Flask(__name__, template_folder='Template')
Bootstrap(app)

# Initialize Firestore DB
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("bangkit-finalproject-firebase-adminsdk-v8dc7-218c11fe14.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
tomato_ref = db.collection('bangkit_tomato')

"""
Routes
"""
@app.route('/test',methods=['GET'])
def test_firebase():
    try:
        tomato_ref.document('1').set({'s':'s'} )
        return "ok"
    except Exception as e:
        print("err")
        return "hmm " + str(e)

@app.route('/predict',methods=['GET'])
def predict():
    return render_template('predict.html')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            image_path = os.path.join('static', uploaded_file.filename)
            uploaded_file.save(image_path)
            class_name = model.get_prediction(image_path)
            result = {
                'class_name': class_name,
                'image_path': image_path,
            }
            return render_template('result.html', result = result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)
