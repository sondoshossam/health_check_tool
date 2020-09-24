# Health Check Tool
## Installation 
> To get started...
download and install the requirements by the following commands 
```shell
$ git clone https://github.com/sondoshossam/health_check_tool
$ cd health_check_tool
$ sudo pip3 install -r requirements.txt
```
> To run the program ...
```shell
$ python3 __main__.py path_to_xls_or_csv_file
```
> usage example 
```shell
$ python3 __main__.py Use\ case\ -\ IPSec\ HC\ report.xls
```
## Configure the email list 
you can edit the recipient list  from app_config.py you have just to add the emails as a string seperated by ,
> 
RECIPIENT_LIST = ["sondoshossam53@gmail.com ","example1@whatever.com","anotherexample@whatever.com" ]
