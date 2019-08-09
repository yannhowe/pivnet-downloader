import os
import re
import sys
from pathlib import Path
import requests
from nested_lookup import nested_lookup
from minio import Minio
from minio.error import ResponseError, NoSuchKey

# Add slugs from product list here: https://network.pivotal.io/api/v2/products/
# Remember to accept the EULA from the webpage first
if os.getenv('DRYRUN') == "False":
    dryrun = False
else:
    dryrun = True
download_destination = os.getenv('DOWNLOAD_DESTINATION', "local")
products=[
    'p-bosh-backup-and-restore',
    'pivotal-container-service',
    'ops-manager',
    ]
exclude_these_strings = [
    'light-bosh-stemcell-', 
    'azure', 
    'openstack', 
    'vcloud', 
    '.txt', 
    'for GCP', 
    'for Openstack', 
    'for AWS', 
    'for Azure', 
    '-aws-', 
    '-gcp-',
    ]

minioClient = Minio(os.getenv('MINIO_HOST', "localhost"),
                    access_key=os.getenv('MINIO_ACCESS_KEY', "Not Set"),
                    secret_key=os.getenv('MINIO_SECRET_KEY', "Not Set"),
                    secure=False,)
pivnet_bucket = os.getenv('PIVNET_BUCKET_NAME', "pivnet-downloader")

try:
    if not minioClient.bucket_exists(pivnet_bucket):
        try:
            minioClient.make_bucket(pivnet_bucket)
        except ResponseError as err:
            print(err)
except ResponseError as err:
    print(err)

# Get fresh token
uaa_refresh_token = os.getenv('UAA_API_TOKEN', "Not Set")
response = requests.post('https://network.pivotal.io/api/v2/authentication/access_tokens', data={'refresh_token':uaa_refresh_token})

# Exit if bad token
if not response:
    print("Error: Probably a bad api token. Check your .env file and follow the instructions to see if you've added the correct UAA_API_TOKEN")
    sys.exit()

# Available product slugs
product_slugs = nested_lookup('slug', requests.get('https://network.pivotal.io/api/v2/products/').json())
print("available products:")
print(product_slugs)

# Get products
product_urls=[]
stemcell_urls=[]

# Get stemcells-ubuntu-xenial 250.*
stemcells_ubuntu_xenial_release_list = requests.get("https://network.pivotal.io/api/v2/products/stemcells-ubuntu-xenial/releases", allow_redirects=True).json()
for release in stemcells_ubuntu_xenial_release_list["releases"]:
    if "250" in release["version"]:
        stemcell_urls.append(release["_links"]["product_files"]["href"])

try:
    product_urls.append(stemcell_urls[0])
except IndexError:
    print("IndexError: empty list %s" % "stemcell_urls")

# Get other products
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
        if any(exclusions in product_file['aws_object_key'] for exclusions in exclude_these_strings):
            print("excluding %s" % product_file['aws_object_key'])
        else:
            directory = os.path.dirname(product_file['aws_object_key']) # Use the aws object key as path
            try:
                os.makedirs(directory, exist_ok=True) # create any directories needed
            except FileExistsError:
                print("directory already exists %s" % product_file['aws_object_key'])
            if dryrun:
                print("dryrun - downloading %s" % product_file['aws_object_key'])
            else: # Download files
                if download_destination == "minio": # Check MinIO to see if already downloaded
                    try:
                        minioClient.stat_object(pivnet_bucket, product_file['aws_object_key'])
                        object_exists = True
                    except ResponseError as err:
                        print(err)
                        object_exists = False
                    except NoSuchKey as err:
                        print(err)
                        object_exists = False

                if object_exists:
                    print("object exists in bucket %s - %s" % (pivnet_bucket, product_file['aws_object_key']))
                    # Delete from local filesystem
                    print("deleting file %s" % product_file['aws_object_key'])
                    try:
                        os.remove(product_file['aws_object_key'])
                    except FileNotFoundError as err:
                        print("file not found while deleting %s" % product_file['aws_object_key'])
                else: # Doesn't exist in MinIO
                    if Path(product_file['aws_object_key']).is_file(): # Check if file already exists
                        print("already downloaded %s" % product_file['aws_object_key'])
                    else:
                        print("downloading %s" % product_file['aws_object_key'])
                        r_downloadfile = requests.get(product_file['_links']['download']['href'], headers=headers) # make get request
                        open(product_file['aws_object_key'], 'wb').write(r_downloadfile.content) # write to file

                if not object_exists and download_destination == "minio": # Upload to Minio
                    print("uploading to bucket %s - %s" % (pivnet_bucket, product_file['aws_object_key']))
                    try:
                        print(minioClient.fput_object(pivnet_bucket, product_file['aws_object_key'], product_file['aws_object_key']))
                    except ResponseError as err:
                        print(err)
                    # Delete from local filesystem
                    print("deleting file %s" % product_file['aws_object_key'])
                    try:
                        os.remove(product_file['aws_object_key'])
                    except FileNotFoundError as err:
                        print("file not found while deleting %s" % product_file['aws_object_key'])