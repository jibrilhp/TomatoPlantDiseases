from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from datetime import datetime

import os
import model
import random

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
        now_timestamp = datetime.now()
        tomato_ref.document().set({'name':'pung ' + str(random.randrange(100)),'timestamp':str(datetime.timestamp(now_timestamp))} )
         
        return "ok"
    except Exception as e:
        print("err")
        return "hmm " + str(e)

@app.route('/test2',methods=['GET'])
def read_firebase():
    try:
        query = tomato_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(5)
        
        results = query.stream()
        for doc in results:
            print(doc.get('timestamp'))
            print(doc.get('file_path')) 
            print(doc.id)
        return "ok " 
        
    except Exception as e:
        return "hmm2 " + str(e)

@app.route('/predict',methods=['GET'])
def predict():
    return render_template('predict.html')

@app.route('/mini_encyclopedia/<topics>',methods=['GET']) 
def encyclopedia(topics):
    print(topics)
    return "ok"

@app.route('/report/<id>',methods=['GET'])
def report(id):
    print(id)
    return "ok"

@app.route('/', methods=['GET','POST'])
def index():
    now_timestamp = datetime.now()
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

            filename_data_save =  image_path
            predict_class = class_name 

            tomato_ref.document().set({'predict_class': predict_class,'file_path':filename_data_save,'timestamp':str(datetime.timestamp(now_timestamp))} )
         
            return render_template('result.html', result = result)
    
    query = tomato_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(5)
        
    results = query.stream()
    data_dict_history = {}

    for doc in results:
        data_dict_history[doc.get('timestamp')] = [doc.get('file_path'),doc.get('predict_class'),doc.id]
    
    print(data_dict_history)
    return render_template('index.html', result_dict = data_dict_history)

if __name__ == '__main__':
    app.run(debug = True)
