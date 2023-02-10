import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('gas.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    
    prediction = model.predict(x_test)
    print(prediction)
    pred=prediction[[0]]
    #output = np.round(pred[0],3)
    #output = str(output)+'$ Dollors'
  
    return render_template('index.html', prediction_text='Gas Price is {} Dollors'.format(pred))

if __name__ == "__main__":
    app.run(debug=True)
