import os
import re
import sys
import requests
from nested_lookup import nested_lookup

# Add slugs from product list here: https://network.pivotal.io/api/v2/products/
# Remember to accept the EULA from the webpage first
products=[
    ]

# Get fresh token
uaa_refresh_token = os.getenv('UAA_API_TOKEN', "Not Set")
response = requests.post('https://network.pivotal.io/api/v2/authentication/access_tokens', data={'refresh_token':uaa_refresh_token})

# Exit if bad token
if not response:
    print("Error: Probably a bad api token. Check your .env file and follow the instructions to see if you've added the correct UAA_API_TOKEN")
    sys.exit()

# Available product slugs
product_slugs = nested_lookup('slug', requests.get('https://network.pivotal.io/api/v2/products/').json())
print(product_slugs)

# Get all products
product_urls=[]
for product in products:
    product_url="https://network.pivotal.io/api/v2/products/" + product + "/releases/latest"
    product_urls.append(product_url)

# Setup headers for file download
headers={}
headers["Authorization"]="Bearer " + response.json()['access_token']

# Download all files in product
for product_url in product_urls:
    r = requests.get(product_url, allow_redirects=True)

    for product_file in r.json()['product_files']:
        directory = os.path.dirname(product_file['aws_object_key']) # Use the aws object key as path
        try:
            os.makedirs(directory, exist_ok=True) # create any directories needed
        except FileExistsError:
            # directory already exists
            pass
        r_downloadfile = requests.get(product_file['_links']['download']['href'], headers=headers) # make get request
        open(product_file['aws_object_key'], 'wb').write(r_downloadfile.content) # write to file