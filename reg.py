import winreg
import os
#HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System

def print_environ():
    for env in os.environ:
        print(env, os.environ[env])

#print_environ()
arch_keys = winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY

aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
for arch_key in arch_keys:
    #key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Uninstall", 0, winreg.KEY_READ | arch_key)
    #aKey = winreg.OpenKey(aReg, "SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Uninstall", 0, winreg.KEY_READ | arch_key)
    aKey = winreg.OpenKey(aReg, r"HARDWARE\\DEVICEMAP\\Scsi", 0, winreg.KEY_READ | arch_key)
    print(winreg.QueryInfoKey(aKey)[1],winreg.QueryInfoKey(aKey)[0])
    #aKey = OpenKey(aReg, aKey)
    for i in range(1024):
        try:
            asubkey_name = winreg.EnumKey(aKey,i)
            print('subkey name', asubkey_name)
            #asubkey=winreg.OpenKey(aKey,'Identifier')
            #print(asubkey)
            #val=winreg.QueryValue(asubkey, "DisplayName")
            #val=winreg.QueryValueEx(asubkey, "DisplayName")
            #print( val)
        except EnvironmentError:
            print('ero0r')
            break


def windows_group_policy_path():
    # we know that we're running under windows at this point so it's safe to do these imports
    from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKeyEx, QueryValueEx, REG_EXPAND_SZ, REG_SZ
    try:
        root = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        policy_key = OpenKeyEx(root, r"SOFTWARE\\Google\\Chrome")
        user_data_dir, type_ = QueryValueEx(policy_key, "UserDataDir")
        if type_ == REG_EXPAND_SZ:
            user_data_dir = os.path.expandvars(user_data_dir)
        elif type_ != REG_SZ:
            return None
    except OSError:
        print('OsError')
        return None
    return os.path.join(user_data_dir, "Default", "Cookies")


#windows_group_policy_path()



def _find_chrome_win(): # + 
    import winreg as reg
    #reg_path = r'SOFTWARE\\Microsoft\Windows\\CurrentVersion\\App Paths\\chrome.exe'
    reg_path =  r"HARDWARE\\DESCRIPTION\\System\\FloatingPointProcessor\\0"
    for install_type in reg.HKEY_CURRENT_USER, reg.HKEY_LOCAL_MACHINE:
        try:
            reg_key = reg.OpenKey(install_type, reg_path, 0, reg.KEY_READ | winreg.KEY_WOW64_32KEY)
            print(1)
            chrome_path = reg.QueryValue(reg_key, None)
            print(2)
            reg_key.Close()
            if not os.path.isfile(chrome_path):
                continue
        except WindowsError:
            chrome_path = None
        else:
            break

    return chrome_path 

#print(_find_chrome_win())


def working_case():
    #keypath=r'SYSTEM\\CurrentControlSet\\Services\\cdrom' #r'SYSTEM\\CurrentControlSet\\Services\\cdrom:AutoRun' (это не синтаксис)
    keypath = r"HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0"
    key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, keypath)
    return  winreg.QueryValueEx(key,'Identifier')[0]

print('ssd/hdd identifier', working_case())



import winreg
import os
def get_scsi_disks_identifiers():
    arch_keys = winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY
    key_path = r'HARDWARE\DEVICEMAP\Scsi'
    aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    scsi_ports = []
    scsi_identifiers = []
    for arch_key in arch_keys:
        aKey = winreg.OpenKey(aReg, key_path, 0, winreg.KEY_READ | arch_key)
        for i in range(1024):
            try:
                scsi_port = winreg.EnumKey(aKey,i)
                scsi_ports.append(scsi_port)
            except EnvironmentError:
                break
        for scsi_port in scsi_ports:
            port_key_path = os.path.join(key_path, scsi_port, r'Scsi Bus 0\Target Id 0\Logical Unit Id 0')
            try:
                key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, port_key_path)
                identifier = winreg.QueryValueEx(key,'Identifier')[0]
                scsi_identifiers.append(identifier)
            except FileNotFoundError:
                pass
    return scsi_identifiers
            
    
print(get_scsi_disks_identifiers())


#HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SQMClient:MachineId
#HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\OneSettings\WSD\SetupPlatform\QueryParameters
#Компьютер\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\OneSettings\WSD\UpdateAgent\QueryParameters