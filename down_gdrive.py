import sys
sys.path.append('/home/alveslab/.local/lib/python3.6/site-packages')
import gdown
gdown.download_folder("current_url", quiet=True)
