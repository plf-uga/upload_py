import os
import shutil
import datetime
import tarfile
import time
import sys
sys.path.append('/home/alveslab/.local/lib/python3.6/site-packages')
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


#Function to get authentification and upload compressed folders
def upload_to_drive (path):
    try:
        #Get credentials for the cloud
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(f'mycreds.txt')
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")
        drive = GoogleDrive(gauth)
        file_drive = drive.CreateFile({'title': os.path.basename(path)})
        # Set content from the file
        file_drive.SetContentFile(path)
        # Upload the file
        file_drive.Upload()
        print("INFO", f'{path} uploaded successfully!')
        return True
    except Exception as e:
        print("ERROR", f'Error uploading {path}: {str(e)}')
        return False

inp = input('Type the path of file you want to upload: \n')
upload_to_drive (inp)