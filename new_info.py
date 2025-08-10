#!/usr/bin/env python3
"""
SYSTEM INFORMATION COLLECTOR
Version: 2.0
Author: Your Name
Description: Collects comprehensive hardware/software information from Windows systems
"""

import sys
import subprocess
import argparse
from datetime import datetime
import platform
import json
from typing import Dict, Optional

# ASCII Art Header
HEADER = r"""
  ____ _____ _   _ ____  _____ ___ ___  _   _   ___ _   _ _____ ____  
 / ___|_   _| | | |  _ \|  ___|_ _/ _ \| \ | | |_ _| \ | | ____|  _ \ 
 \___ \ | | | | | | |_) | |_   | | | | |  \| |  | ||  \| |  _| | |_) |
  ___) || | | |_| |  _ <|  _|  | | |_| | |\  |  | || |\  | |___|  _ < 
 |____/ |_|  \___/|_| \_\_|   |___\___/|_| \_| |___|_| \_|_____|_| \_\
"""

class SystemInfoCollector:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.system_info = {
            "metadata": {
                "collection_time": self.timestamp,
                "script_version": "2.0",
                "python_version": platform.python_version(),
                "host_os": platform.system() + " " + platform.release()
            }
        }

    def run_command(self, command: str, powershell: bool = False) -> str:
        """Execute system command and return output"""
        try:
            if powershell:
                result = subprocess.run(["powershell", "-Command", command], 
                                      capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(command, shell=True, 
                                      capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def collect_wmic_info(self) -> Dict[str, str]:
        """Collect information using WMIC commands"""
        return {
            'motherboard': self.run_command('wmic baseboard get product, Manufacturer'),
            'os': self.run_command('wmic os get name'),
            'cpu': self.run_command('wmic cpu get name'),
            'gpu': self.run_command('wmic path win32_videocontroller get name'),
            'ram': self.run_command('wmic memorychip get memorytype,speed,Manufacturer,Capacity'),
            'storage': self.run_command('wmic diskdrive get Model,Size'),
            'network': self.run_command('ipconfig'),
            'mac': self.run_command('getmac'),
            'hostname': self.run_command('hostname'),
            'user': self.run_command('whoami'),
            'printers': self.run_command('wmic printer get name,default')
        }

    def collect_powershell_info(self) -> Dict[str, str]:
        """Collect information using PowerShell commands"""
        return {
            'motherboard': self.run_command('Get-WmiObject Win32_BaseBoard | Select-Object Manufacturer, Product | Format-Table -AutoSize', True),
            'os': self.run_command('Get-WmiObject Win32_OperatingSystem | Select-Object Name | Format-Table -AutoSize', True),
            'cpu': self.run_command('Get-WmiObject Win32_Processor | Select-Object Name | Format-Table -AutoSize', True),
            'gpu': self.run_command('Get-WmiObject Win32_VideoController | Select-Object Name | Format-Table -AutoSize', True),
            'ram': self.run_command('Get-WmiObject Win32_PhysicalMemory | Select-Object MemoryType, Speed, Manufacturer, Capacity | Format-Table -AutoSize', True),
            'storage': self.run_command('Get-WmiObject Win32_DiskDrive | Select-Object Model, Size | Format-Table -AutoSize', True),
            'network': self.run_command('Get-NetIPAddress | Where-Object { $_.AddressFamily -eq "IPv4" -and $_.InterfaceAlias -notlike "*Loopback*" } | Select-Object InterfaceAlias, IPAddress | Format-Table -AutoSize', True),
            'mac': self.run_command('Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Select-Object Name, MacAddress | Format-Table -AutoSize', True),
            'hostname': self.run_command('hostname'),
            'user': self.run_command('whoami'),
            'printers': self.run_command('Get-WmiObject Win32_Printer | Select-Object Name, Default | Format-Table -AutoSize', True)
        }

    def collect_system_info(self):
        """Main collection method with fallback logic"""
        try:
            print("Attempting to collect information using WMIC...")
            wmic_info = self.collect_wmic_info()
            if any("Error" in value for value in wmic_info.values()):
                raise Exception("WMIC collection failed")
            self.system_info.update({"collection_method": "WMIC", "data": wmic_info})
        except:
            print("Falling back to PowerShell collection...")
            ps_info = self.collect_powershell_info()
            self.system_info.update({"collection_method": "PowerShell", "data": ps_info})

    def save_to_file(self, filename: str, output_format: str = "text"):
        """Save collected information to file"""
        try:
            if output_format.lower() == "json":
                with open(f"{filename}.json", 'w') as f:
                    json.dump(self.system_info, f, indent=4)
                print(f"System information saved to {filename}.json")
            else:
                with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
                    f.write(HEADER)
                    f.write(f"\nSYSTEM INFORMATION REPORT\n")
                    f.write(f"Generated on: {self.timestamp}\n")
                    f.write(f"Collection method: {self.system_info.get('collection_method', 'Unknown')}\n")
                    f.write("="*80 + "\n\n")
                    
                    for category, info in self.system_info['data'].items():
                        f.write(f"{category.upper():^80}\n")
                        f.write("="*80 + "\n")
                        f.write(f"{info}\n\n")
                print(f"System information saved to {filename}.txt")
        except Exception as e:
            print(f"Failed to save file: {str(e)}")

def main():
    print(HEADER)
    print("System Information Collector v2.0\n")
    
    parser = argparse.ArgumentParser(description="Collect system hardware/software information")
    parser.add_argument('-n', '--name', help="Output filename (without extension)")
    parser.add_argument('-f', '--format', choices=['text', 'json'], default='text',
                       help="Output format (text or json)")
    args = parser.parse_args()
    
    filename = args.name if args.name else input("Enter output filename: ")
    
    collector = SystemInfoCollector()
    collector.collect_system_info()
    collector.save_to_file(filename, args.format)

if __name__ == "__main__":
    main()