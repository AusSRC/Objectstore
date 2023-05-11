#
#   Example of using ObjStore and S3Object.py to store a large file on Acacia (objectstore)
#
#   - GWHG @ CSIRO, Oct 2022 

import os
import sys
import json
from astropy.io import fits

try:
    import ObjStore
    import ObjStore.S3Object as S3
    import ObjStore.URLObject as URL
    from ObjStore.FITSheader import *
    from ObjStore.get_access_keys import *
except ModuleNotFoundError:
    import S3Object as S3
    import URLObject as URL
    from FITSheader import *
    from get_access_keys import *
# Required variables for storage to Acacia objectstore
endpoint = "https://projects.pawsey.org.au"
project = "ja3"
bucket = "aussrc"
certfile = "../my_certs.json"

USEURL = False
obj = None

    # The path to the directory holding the file we want to upload is defined in the local filesystem by 'localpath':
localpath = "/home/ger063/src/acacia"
    #
    # 'keyname' is the same as the filename on the local system
keyname = "sofia_test_datacube.fits"
    #
    # The object it will become on the objectstore is:
    #       project + '/' + bucket + '/' + storepath + '/' + keyname
    #
    # The 'storepath' complication is added because you can't have buckets within buckets,
    # but you often want to mimic that construct. So 'storepath' is just a string made to look
    # like a subdirectory path, eg "myPretendDirectory/myPretendSubdirectory"
storepath = "flash/example_data"
storepath = ""

    # Create an S3 object name:
if storepath:
    objname = storepath+'/'+keyname
else:
    objname = keyname

    # Get the FITS header from file
    hdr = FITSheaderFromFile(localpath+'/'+keyname)
    hdrdict = hdr.convert2dict()
    # Add data type to header
    hdrdict["ContentType"] = "binary/octet-stream"

    # Get the project access keys from the json certs file, assuming you have them:
if not USEURL:
    (access_id,secret_id,quota) = get_access_keys(certfile,endpoint,project)
    # Upload using the Boto3 S3 API and access/secret id's
    # Create an instance of the object class:
    obj = S3.S3Object(bucket,objname,access_id,secret_id,endpoint)
    # You can set defaults like this (but the normal defaults are fastest for most uses):
    #obj.setConfig(file_thresholdsize, file_chunksize, num_threads)

    # Upload to store - files larger than 5G will be 'chunked' - for batch jobs, set progress=False
    obj.uploadFile(localpath,keyname,ExtraArgs=hdrdict,progress=True)
else:
    # Alternative upload using an upload dictionary with a presigned URL.
    obj = URL.UrlObject()
    # Note that in general, the upload dict will be provided to you. But IF you have access and secret details
    # for the project/bucket, you can generate one with:
    #
    # upload_dict = obj.create_presigned_url_upload(certfile,endpoint,project,bucket,objname,expiry)
    #
    # Example dict (not real id's, so won't work!!):
    #
    # {'url': 'https://projects.pawsey.org.au/aussrc', 'fields': {'key': 'flash/example_data/spectral_plots_gt_03.tar.gz', 'AWSAccessKeyId': 'c41d289fe7ecdeab391c045fcebc8c39', 'policy': 'F0aW9uIjogeyJleHBpcmIjIwMjMtMDUtMDVUMDQ6NTM6NDJaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAiYXVzc3JjIn0sIHsia2V5IjogImZsYXNoL2V4YW1wbGVfZGF0YS9zcGVjdHJhbF9wbG90c19ndF8wMy50YXIuZ3oifV19', 'signature': 'FRhpyXnvwrMZGgvETCnN0Q04TQk='}}
    #
    # NOTE you must have the correct IAM permissions on the bucket for writing.
    # You can then give this dict to a user to upload an object to your bucket (without having to
    # provide them with your access details). The user should put it in their certs file.
    #
    # Otherwise, if the upload entry is already in your certfile:
    upload_dict = get_upload_URL(certfile,endpoint,project,bucket,objname)
    obj.upload_via_URL(localpath+"/"+keyname,upload_dict)


