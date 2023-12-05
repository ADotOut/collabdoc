import os
import random
import string

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACd317c89ef46c67dc6ad99af7935c74c2'
    TWILIO_SYNC_SERVICE_SID = 'ISf3878c4a038e83c28bba88e3cf92525c'
    TWILIO_API_KEY = 'SKb0312704fca9e4d13f6cf4549aadbf03'
    TWILIO_API_SECRET = 'LLEuQrfFbqLYH9tc4jTm6Uz1e4HkY4H7'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text = request.form['text']
    # Make directory if not exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')    
    filepath = f'downloads/{"".join(random.choices(string.ascii_letters + string.digits, k=10))}.txt' 
    with open(filepath, 'w') as f:
        f.write(text)

    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
