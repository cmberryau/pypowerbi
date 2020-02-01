import json
import os

"""
 There are two ways to specify credentials used by the example scripts:
     1) Directly enter them into this file.
     2) Enter them into a creds.json file in the same directory as this script. (See below for format)
 
 If you are just using the library, it should be fine to just enter the credentials in this file. If you're developing code
 for this library, you'll probably want to use the .json file and add it to your .gitignore so that you don't 
 accidentally commit your login info!
 
 The creds.json file should look like:
 -------------------------------------------------------------------------
 {
  "client_id": "<your client id>",
  "username": "<your username (email)>",
  "password": "<your password>"
 }
 -------------------------------------------------------------------------
"""

# Enter your credentials here. If you're using the creds.json file, leave them as an empty string
client_id = ''
username = ''
password = ''


# If credentials aren't specified in this file, see if there's a "creds.json" file in the current directory and use it
if client_id == '':
    scriptpath = os.path.dirname(os.path.realpath(__file__))
    creds_file_path = os.path.join(scriptpath, 'creds.json')

    if os.path.exists(creds_file_path):
        creds_fh = open(creds_file_path, "r")
        creds = json.load(creds_fh)

        client_id = creds["client_id"]
        username = creds["username"]
        password = creds["password"]
    else:
        raise RuntimeError("Credentials must be specified in Credentials.py or creds.json!")