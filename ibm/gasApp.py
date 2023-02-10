
# NOTE: manually define and pass the array(s) of values to be scored in the next line
import numpy as np
from flask import Flask, request, jsonify, render_template
#import pickle
import requests

app = Flask(__name__)
#model = pickle.load(open('gas.pkl', 'rb'))

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "TYd9HnGIYYRWxH5Mj6WPspwpFfPlsXBsIxemkb5DnMWX"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print(x_test)
    
    payload_scoring = {"input_data": [{"fields": [["year", "month", "day"]], "values": [[2005,7,23]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a13efacb-3c85-4ddf-90b1-2c6f3df02634/predictions?version=2021-10-28&version=2021-10-28', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred= response_scoring.json()
    print(pred)
    
    output = pred['predictions'][0]['values'][0][0]
    print(output)
    #output = str(output)+'$ Dollors'
  
    return render_template('index.html', prediction_text='Gas Price is {} Dollars'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
