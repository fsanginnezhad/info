import sys
import subprocess


try:
    name = sys.argv[1]
except Exception:
    name = input('enter your name: ')
try:
    addr = sys.argv[2] + f'\\{name}.txt'
except Exception:
    addr = f'.\\{name}.txt'


commands = {
    'MotherBoard': 'wmic baseboard get product, Manufacturer',
    'OS': 'wmic os get name',
    'CPU': 'wmic cpu get name',
    'GPU': 'wmic path win32_videocontroller get name',
    'RAM': 'wmic memorychip get memorytype,speed,Manufacturer,Capacity',
    'Storage': 'wmic diskdrive get Model,Size',
    'IP-Address': 'ipconfig',
    'MAC': 'getmac',
    'HostName': 'hostname',
    'User': 'whoami',
    'Printer': 'wmic printer get name,default'
}

commands_ = {
    'MotherBoard': 'powershell -command "Get-WmiObject Win32_BaseBoard | Select-Object Manufacturer, Product | Format-Table -AutoSize"',
    'OS': 'powershell -command "Get-WmiObject Win32_OperatingSystem | Select-Object Name | Format-Table -AutoSize"',
    'CPU': 'powershell -command "Get-WmiObject Win32_Processor | Select-Object Name | Format-Table -AutoSize"',
    'GPU': 'powershell -command "Get-WmiObject Win32_VideoController | Select-Object Name | Format-Table -AutoSize"',
    'RAM': 'powershell -command "Get-WmiObject Win32_PhysicalMemory | Select-Object MemoryType, Speed, Manufacturer, Capacity | Format-Table -AutoSize"',
    'Storage': 'powershell -command "Get-WmiObject Win32_DiskDrive | Select-Object Model, Size | Format-Table -AutoSize"',
    'IP-Address': 'powershell -command "Get-NetIPAddress | Where-Object { $_.AddressFamily -eq \'IPv4\' -and $_.InterfaceAlias -notlike \'*Loopback*\' } | Select-Object InterfaceAlias, IPAddress | Format-Table -AutoSize"',
    'MAC': 'powershell -command "Get-NetAdapter | Where-Object { $_.Status -eq \'Up\' } | Select-Object Name, MacAddress | Format-Table -AutoSize"',
    'HostName': 'hostname',
    'User': 'whoami',
    'Printer': 'powershell -command "Get-WmiObject Win32_Printer | Select-Object Name, Default | Format-Table -AutoSize"'
}


def info(commands: dict):
    info = open(addr, 'a')
    for i in commands:
        info.write(f'--------------------------------------{i}----------------------------------------\n') # noqa
        info.write(subprocess.check_output(f'{commands[i]}').decode('utf-8'))
    info.close()


try:
    info(commands)
except Exception:
    info(commands_)