# Objectstore
## Intro
There are various methods and protocols available for storing and retrieving data when using an objectstore resource (rather than a local POSIX-compliant file system). This document describes several modules written by AusSRC that streamline API calls to the S3 protocol, as implemented by the Python Boto3 library, as well as a json structure for holding objectstore certificates and keys. The modules are based on a parent class specific for handling FITS datasets, but the basic upload and download will work for any file. These can be used to programatically access an objectstore and are easily used within an existing workflow/pipeline.

## Install
You can clone the code from here to have access to the source. Alternatively you can install via pipas:

    pip3 install ObjStore
