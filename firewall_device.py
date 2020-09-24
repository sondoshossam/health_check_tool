import getpass
from pexpect import pxssh
import logging
import os 
from model_loader import ModelLodaer
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('firewall logger')
logger.setLevel(logging.DEBUG)
logger.disabled = True


class FireWallDevice:
    def __init__(self,node_name, ip, model, store_path ="19-9-2020"):
        self.__store_path = store_path
        self.__ip = ip 
        self.__node_name = node_name
        self.__model = model
        self.__login_user_name = ""
        self.__login_password = ""
        self.__connection = None
        if not os.path.isdir(store_path):
            os.makedirs(store_path)
        self.__command_track = {"suc":[], "fail":[]}

    def get_firewall_credential(self):
        print(f"pls enter the credential for {self.__node_name} at {self.__ip}")
        self.__login_user_name = input("user name:")
        self.__login_password =  getpass.getpass()
        logger.debug(f"the user name {self.__login_user_name} and the password {self.__login_password}")

    def login(self) -> bool:
        is_connected = False
        try:                                                            
            self.__connection  = pxssh.pxssh()
            is_connected = self.__connection.login (self.__ip, self.__login_user_name, self.__login_password)
        except Exception as e:
            print(f"failed to connect to {self.__ip}")
            print(e)
        return is_connected
    
    def logout(self):
        if not (self.__connection is None):
            try:
                self.__connection.logout()
            except :
                pass 
        self.__connection = None


    def execute_commande(self , cmd):
        status, responce  = False , ""
        try:
            self.__connection.sendline(cmd) 
            self.__connection.prompt()
            result_bytes = self.__connection.before
            responce = str(result_bytes, "utf8")
            status = True
        except:
            pass 
        return status, responce

    def run_all_commands(self):
        report_file_path = os.path.join(self.__store_path, f"{self.__model}_{self.__node_name}.txt")
        report_file = open(report_file_path, "w")
        report_file.write("#"*40)
        report_file.write(f"\nNode Name:{self.__node_name}\nModel:{self.__model}\nIp:{self.__ip}\n")
        report_file.write("#"*40)
        report_file.write("\n")
        for command in ModelLodaer.get_model_commands(self.__model):
            is_executed, responce = self.execute_commande(command)
            if is_executed:
                report_file.write("#"*40 + "\n")
                report_file.write(f">> {command} \n")
                report_file.write("result:\n")
                report_file.write(responce)
                report_file.write("\n")
                self.__command_track["suc"].append(command)
            else:
                report_file.write("#"*40 + "\n")
                report_file.write(f">> {command} \n")
                report_file.write("result:\n")
                report_file.write("failed to execute the command\n")
                self.__command_track["fail"].append(command)
        report_file.close()

    def get_report(self):
        pass


if __name__ == "__main__":
    f = FireWallDevice("anyname", "192.168.1.6" , "juniper")
    #f.get_firewall_credential()
    if f.login():
        f.run_all_commands()
        f.logout()
    else:
        print("fail")
