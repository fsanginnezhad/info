# 🖥️ System Information Collector

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Comprehensive Data Collection**  
  Retrieve detailed specs about CPU, GPU, RAM, storage, and more
- **Dual Collection Engine**  
  Uses both WMIC and PowerShell with automatic fallback
- **Multiple Output Formats**  
  Save as human-readable text or machine-readable JSON
- **Professional Reporting**  
  Beautifully formatted output with timestamps and headers
- **Easy to Use**  
  Simple command-line interface with interactive mode

## 📦 Installation

```bash
git clone https://github.com/yourusername/system-info-collector.git
cd system-info-collector
pip install -r requirements.txt
🚀 Usage
Basic Command
bash
python system_info.py
Advanced Options
Flag	Description	Example
-n	Specify output filename	-n my_system_report
-f	Output format (text or json)	-f json
-h	Show help message	-h
Example Output Files
text
system_report.txt
system_report.json
📋 Collected Information
Category	Details Collected
Motherboard	Manufacturer, Product
CPU	Model name, Specifications
GPU	Graphics card model
RAM	Type, Speed, Capacity, Manufacturer
Storage	Drives, Models, Sizes
OS	Version, Name
Network	IP Addresses, MAC Addresses
User	Current username
Printers	Installed printers, Default printer
🛠️ Technical Details
python
SystemInfoCollector()
├── .collect_wmic_info()       # WMIC-based collection
├── .collect_powershell_info() # PowerShell-based collection
├── .run_command()            # Safe command execution
└── .save_to_file()           # Multi-format output
📜 License
MIT License - Free for personal and commercial use

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

📧 Contact
For support or questions:
📩 fxfix3r@gmail.com
