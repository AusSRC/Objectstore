import boto3
try:
    import objectstore
    from iobjectstore.get_access_keys import *
except ModuleNotFoundError:
    from get_access_keys import *


# objectstore address
endpoint = 'https://projects.pawsey.org.au'      
# objectstore account name
project = 'ja3'                                  
# bucket in the objectstore that holds our object
bucket = "aussrc"                                   
# object in the object store that we want
key = "flash/pilot2_outputs/SB33616_output_plots_and_ascii.tar.gz"                     
# File holding access id's for objectstore
my_certs_file = "my_certs.json"                  

(access_id,secret_id,quota) = get_access_keys(my_certs_file,endpoint,project)

client = boto3.client(service_name='s3',aws_access_key_id=access_id,aws_secret_access_key=secret_id, endpoint_url=endpoint)

# Expiry date from now (in sec)
expiry = 8640000 #(10 days)
expiry = 31536000 #(1 year)

url = client.generate_presigned_url( ClientMethod='get_object', Params={ 'Bucket': bucket, 'Key': key}, ExpiresIn=expiry)

# Which gives:
print(url)


