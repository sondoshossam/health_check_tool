import json 
import os 
import sys 

CONFIG_FILE_PATH = "config.json"


class ModelLodaer:
    __shared_configurations = {}
    if os.path.isfile(CONFIG_FILE_PATH):
        try:
            file_content = json.load(open(CONFIG_FILE_PATH , "r"))
            __shared_configurations = file_content.copy()
        except:
            print(f"please make sure that the file {CONFIG_FILE_PATH} not courapted")
            sys.exit(1)
    else:
        print(f"please make sure that the file {CONFIG_FILE_PATH} existed")
        sys.exit(1)
    
    @staticmethod
    def get_model_commands(target_model):
        for command in ModelLodaer.__shared_configurations.get(target_model , []):
            yield command.get("cmd", None)
    




