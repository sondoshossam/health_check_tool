import pandas as pd
import os 
import sys 
import zipfile
import shutil
from datetime import datetime
from firewall_device import FireWallDevice
from email_sender import  EmailSender


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def start_main_task(dataframe):
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_%H_%M")
    for i, server_info in dataframe.iterrows(): 
        name, ip, model = server_info[:3]
        device = FireWallDevice(name , ip , model.lower() , store_path=dt_string)
        device.get_firewall_credential()
        if device.login():
            device.run_all_commands()
            device.logout()
        else:
            print(f"fail to connect to {name}/{ip}")
        break

    zipf = zipfile.ZipFile(f'{dt_string}.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(f'{dt_string}', zipf)
    zipf.close()
    shutil.rmtree(dt_string)
    EmailSender.send(f'{dt_string}.zip')
    os.remove(f'{dt_string}.zip')
        

def is_valid_file(dataframe):
    REQ_FIELDS = ['node name', 'node ip', 'model']
    col_names = [ele.lower() for ele in list(dataframe.columns)]
    is_valid = True
    for ele in REQ_FIELDS:
        if ele not in col_names:
            print(f"the column {ele} is required")
            is_valid = False
            break 
    return is_valid
    

def start_parseing(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print("error occors during file parsing")
        print(e)
    else:
        file_length = len(df)
        print(f"the file contains {file_length} records.")
        if file_length > 0:
            if is_valid_file(df):
                start_main_task(df)
            else:
                print("the file doesn't have apropiate structure")
        else:
            print("you have selected embty file.")

if __name__ == "__main__":
    if len(sys.argv ) > 1:
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print("please select valid path the the IPSec HC ")
            sys.exit(1)
        start_parseing(file_path)
    else:
        print("you have to run the program using\npython3 path_to_ip_file")
