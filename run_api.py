import os
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import dill as pickle

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.chaordic_data
user_data = db.user_data
recommendations = db.recommendations

app = Flask(__name__)

@app.route('/chaordic_api', methods=['POST'])
def apicall():
    
    #get json input correctly
    try:
        post_data = request.get_json()
    except Exception as e:
        raise e

    if not post_data:
        return(bad_request())
    else:
        #saves page view info inside mongodb database
        result = user_data.insert_one(post_data)
    
        #get user browser_id for recommendation prediction
        browser_id = post_data['browser_id']
        
        #find recommendation that was previously saved on MongoDB
        browser_recomm = db.recommendations.find({'browser_id':'00000af27a0bb1eed667e6eabdd167fe568ed315'})[0]
        del browser_recomm['_id']
        
        #output response with recommendations
        responses = jsonify(browser_recomm)
        responses.status_code = 200

        return (responses)

#runs api on port 8080
if __name__ == '__main__':
     app.run(port=8080)
