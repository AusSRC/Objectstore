import boto3
import sys
try:
    import ObjStore
    from ObjStore.get_access_keys import *
except ModuleNotFoundError:
    from get_access_keys import *


# object in the object store that we want - this is relative to the bucket name, defined below
key = f"{sys.argv[1]}"

# objectstore address
endpoint = 'https://projects.pawsey.org.au'      
# objectstore account name
project = 'ja3'                                  
# bucket in the objectstore that holds our object
bucket = "aussrc"                                   
# File holding access id's for objectstore
certfile = "../my_certs.json"                  

(access_id,secret_id,quota) = get_access_keys(certfile,endpoint,project)

client = boto3.client(service_name='s3',aws_access_key_id=access_id,aws_secret_access_key=secret_id, endpoint_url=endpoint)

# Expiry date from now (in sec)
expiry = 8640000 #(10 days)
expiry = 31536000 #(1 year)

url = client.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': key}, ExpiresIn=expiry)

# Which gives:
print(url)


