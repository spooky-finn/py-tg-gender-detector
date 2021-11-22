import json
from datetime import datetime
from cryptography.fernet import Fernet

from cfg.cfg import *
from src.get_hardware import getHardwareData

def writeLine(pathtofile, lineN, payload):
    writeMode='w+'
    readMode='r+'
    
    if type(payload) == bytes:
      writeMode='wb'
      readMode='rb'
      
    with open(pathtofile, readMode) as f:
      document = f.readlines()
      if writeMode == 'wb':
        document[int(lineN)-1] = payload + '\n'.encode()
      else:
        document[int(lineN)-1] = payload + "\n"
      
      f = open(pathtofile, writeMode)
      for line in document:
          f.write(line)
    
    
    
def checkLicense(path_to_license):
    
    fernet = Fernet(cryptography_secret_key)
     
    # Trial license expired check
    if (str(datetime.now()).split('.')[0] > str(datetime.strptime(licenseExpiredAt, "%Y-%m-%d %H:%M:%S"))):
        print("Free license expired \n", '-'*100)
        return False 
    
    def getLineByNumber(lineN, bytes=False):
      readMode = 'r+'
      if bytes == True:
        readMode = 'rb'
      with open(path_to_license, readMode) as licenceFile:
        for i, line in enumerate(licenceFile): 
          if i == (lineN-1):
            return line.strip()
    
    key = getLineByNumber(1)
    currentHardware = str(getHardwareData())
    # Сначала проверяется есть ли ключ активации в файле лицензии, если он там есть
    # то мы разрешаем активировать программу.
    # Активация заключается в создании зашифрованного Hardware uuid, ключ активации лицензии при этом удалится
    # При следующих запусках проверяется текущий hardware uuuid с записанным в файле.
    if (key == license_uuid_secret_key):
        print("Activation complited")
        print('-' * 50)
        
        currentHardwareToken = fernet.encrypt(currentHardware.encode())
      
        writeLine(path_to_license, 1, currentHardwareToken)
        
        return True 
    else: 
        print('Activation key not found')
        TrustedHardwareToken = getLineByNumber(1, bytes=True)
        
        trustedHardware = fernet.decrypt(TrustedHardwareToken).decode()
        
        if currentHardware == trustedHardware:
            return True
        else:
            print('Hardware authorizatin failed')
    return False