import os
import requests
import pandas as pd
from flask import Flask, request

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_csv(filepath):
    # Read data from the CSV file
    df = pd.read_csv(filepath)
    df = df.fillna('')  # Replace NaN values with empty strings if necessary

    # Define the endpoint and headers for creating users
    create_user_url = "https://api.aptrinsic.com/v1/users"
    headers = {
        "Authorization": "Bearer bc685332-3d9d-44d0-8c41-5c95f3dce5b3",
        "Content-Type": "application/json"
    }

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        email = row['email']
        identifyId = row['identifyId']

        # Define the payload for creating a new user
        payload = {
            "identifyId": identifyId,
            "email": email,
            "propertyKeys": ["AP-OXQARNCUGSRD-2"]
        }

        # Create the user
        response = requests.post(create_user_url, headers=headers, json=payload)
        print(f"Status Code for {email}: {response.status_code}")
        if response.status_code == 201:
            print(f"Success: User {email} created successfully.")
        else:
            print(f"Failed to create user {email}. Status Code: {response.status_code}")
            print(f"Error Response for {email}:", response.text)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file part is present
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            process_csv(filepath)
            return "File processed successfully. If new users were created, you should see them in Gainsight shortly."
    return '''
    <!doctype html>
    <title>Upload a CSV File</title>
    <h1>Upload a CSV file to create users</h1>
    <p>If a user already exists, they will not be added again. Instead, their existing record may be updated.</p>
    <p>This process adds users to the Marketing web app segment for the purpose only of external emails. Their accounts will not be associated with orgs or existing users. Contact Sam to upload new users to a different segment.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
