from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get URI from .env
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['food_donation']
collection = db['donations']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        donation = {
            'name': request.form['name'],
            'food': request.form['food'],
            'quantity': request.form['quantity'],
            'location': request.form['location'],
            'status': 'Available'
        }
        collection.insert_one(donation)
        return redirect(url_for('donations'))
    return render_template('donate.html')

@app.route('/receive', methods=['GET', 'POST'])
def receive():
    if request.method == 'POST':
        donation_id = request.form['donation_id']
        collection.update_one({'_id': ObjectId(donation_id)}, {'$set': {'status': 'Received'}})
        return redirect(url_for('donations'))
    donations = collection.find()
    return render_template('receive.html', donations=donations)

@app.route('/donations')
def donations():
    donations = collection.find()
    return render_template('donations.html', donations=donations)

if __name__ == '__main__':
    app.run(debug=True)
