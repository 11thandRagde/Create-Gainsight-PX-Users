import requests

# Define the endpoint and headers
url = "https://api.aptrinsic.com/v1/users"
headers = {
    "Authorization": "Bearer bc685332-3d9d-44d0-8c41-5c95f3dce5b3",
    "Content-Type": "application/json"
}

# Define the payload
payload = {
    "identifyId": "sam+dromo1@inflcr.com",
    "email": "sam+dromo1@inflcr.com",
    "propertyKeys": ["AP-CQ7AHGCXYGO4-2"]
    # current key is for influencer web app
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())
