
"""
Created on Fri Apr 8 16:17:01 2024

@author: Alves Lab 
"""
import os
import shutil
import datetime
import tarfile
import time
import sys
sys.path.append('/home/alveslab/.local/lib/python3.6/site-packages')
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


#Define the directory with the Google Drive credentials
dir = '/home/alveslab/upload_py'

# Function to compress a folder
def compress_folder(folder_path, folder_name):
    with tarfile.open(f'{folder_name}.tar.gz', "w:gz") as tar:
        for file in os.listdir(folder_path):
            tar.add(os.path.join(folder_path, os.path.basename(file)))

#Function to get authentification and upload compressed folders
def upload_to_drive (path):
    try:
        #Get credentials for the cloud
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(os.path.join(dir,'mycreds.txt'))
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
            gauth.SaveCredentialsFile(os.path.join(dir,'mycreds.txt'))
        else:
            # Initialize the saved creds
            gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile(os.path.join(dir, 'mycreds.txt'))
        drive = GoogleDrive(gauth)
        file_drive = drive.CreateFile({'title': os.path.basename(path)})
        # Set content from the file
        file_drive.SetContentFile(path)
        # Upload the file
        file_drive.Upload()
        write_log("INFO", f'{path} uploaded successfully!', verbose = 1)
        return True
    except Exception as e:
        write_log("ERROR", f'Error uploading {path}: {str(e)}', verbose=1)
        return False

           
# Function to delete a folder
def delete_folder(folder_path):
    shutil.rmtree(folder_path)

def write_log(info, message, verbose):
    current_timestamp = time.time()   
    # Convert the timestamp to the desired format
    current_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(current_timestamp))
    cout = f'{info} {current_time} : {message}  \n'
    with open('output.log', 'a') as file:
        if verbose == 1:
            print(cout)
        file.write(cout)  

# Main function
def main(directory_path, del_folder):    
    today = datetime.date.today()    
    for folder_name in os.listdir(directory_path):
        try: 
            folder_path = os.path.join(directory_path, folder_name)
            os.chdir(directory_path)
            if os.path.isdir(folder_path):            
                folder_creation_date = datetime.date.fromtimestamp(os.path.getctime(folder_path))
                if folder_creation_date == today:
                    write_log("INFO", f'{folder_name} not created on {today}, files will be moved to the cloud!', verbose = 1)
                    compress_folder(folder_path, folder_name)                   
                    path = f'{directory_path}/{folder_name}.tar.gz'                
                    sucess = upload_to_drive(path)                     
                    if sucess and del_folder == True:
                        delete_folder(folder_path)
		    #if sucess!=True:
			#write_log("ERROR", f'unable to upload {folder_name}!', verbose = 1)
                    os.remove(path)
            else:
                pass            
        except:            
            write_log("ERROR", f'unable to upload {folder_name}!', verbose = 1)
            pass            
            

# Define here the working directory (Folder with images to be saved)
directory_path = '/home/alveslab/Img_MP'
main(directory_path, del_folder = False)  
