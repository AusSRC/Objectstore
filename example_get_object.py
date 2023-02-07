#
#   Example of using ObjStore and S3Object.py to get an object on Acacia (objectstore)
#
#   - GWHG @ CSIRO, Feb 2023 

import os
import sys
import json
try:
    import objectstore
    import objectstore.S3Object as S3
    import objectstore.URLObject as URL
    from objectstore.get_access_keys import *
except ModuleNotFoundError:
    import S3Object as S3
    import URLObject as URL
    from get_access_keys import *

USEURL = False
obj = None
my_object = None

# Required variables for storage to Acacia objectstore
certfile = "certs.json"
endpoint = "https://projects.pawsey.org.au"
project = "ja3"


if not USEURL:
    bucket = "test-bucket"
    key = "pyvenv.cfg"
    localpath = "./test.cfg"
    (access_id,secret_id,quota) = get_access_keys(certfile,endpoint,project)

    obj = S3.S3Object(bucket,key,access_id,secret_id,endpoint)
    my_object = obj.getObject()
else:
    bucket = "aussrc"
    key = "flash/setonix_scripts.tar.gz"
    localpath = "./test.tar.gz"
    url = get_download_URL(certfile,endpoint,project,bucket,key)

    obj = URL.UrlObject(url)
    my_object = obj.download_via_URL()

with open(localpath, "wb") as f:
    f.write(my_object) 




