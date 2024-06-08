#!/bin/bash
cd /home/alveslab/Downloads
#git clone https://github.com/plf-uga/xport_rsip.git
python3 /home/alveslab/upload_py/down_gdrive.py
mv /home/alveslab/Downloads/upload_py/mycreds.txt /home/alveslab/upload_py/mycreds.txt
rm -r /home/alveslab/Downloads/upload_py <<< yes