# 🔍 Omni-Scanner: The Ethical Network Reconnaissance Toolkit 🔍

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)

**Discover. Analyze. Secure.**  
A Python-powered network scanning suite for ethical hackers, sysadmins, and security enthusiasts.

---

## 🚀 Features

- 🕵️ **Network Discovery**: ARP scanning for local device detection
- 📡 **Ping Customization**: Simple ping, flood ping, and adaptive latency checks
- 🗺️ **Traceroute**: Visualize network paths to targets
- 🔦 **Advanced Scans**: Nmap integration for OS detection, service fingerprinting, and stealth scans
- 📊 **User-Friendly**: Clean terminal tables, colored output, and progress tracking

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- `nmap` installed ([Download here](https://nmap.org/download.html))
- **Linux/macOS**: `arp-scan` (install via package manager)
- **Windows**: [Npcap](https://npcap.com/) for raw packet support

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Omni-Scanner.git
   cd Omni-Scanner
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the scanner (Linux/macOS):
   ```bash
   sudo python3 main.py
   ```

---

## 🖥️ Usage

```bash
# Basic ARP scan (Linux/macOS)
sudo python3 main.py --arp --range 192.168.1.1/24

# Advanced Nmap scan (All platforms)
python3 main.py --nmap -t 80,443 -i 10.0.0.5
```

**Interactive Menu**  
![Menu Demo](image link)

---

## ⚠️ Legal & Ethical Disclaimer

**BEFORE RUNNING THIS TOOL**:
1. Obtain **written permission** for any network you don't own.
2. Do **NOT** scan public/critical infrastructure.
3. Usage for illegal purposes is strictly prohibited.

By using Omni-Scanner, you agree to:
- Comply with all local/global laws (e.g., Computer Fraud and Abuse Act)
- Assume full responsibility for your actions

---

## 🤝 Contributing

We welcome contributions! Here's how:
1. 🐛 **Report Bugs**: Open an issue with "Bug" label
2. 💡 **Suggest Features**: Use "Enhancement" label
3. 👩💻 **Code Contributions**:
    - Fork the repo
    - Create a feature branch (`git checkout -b feature/amazing-feature`)
    - Submit a pull request

---

## ☕ Support My Work

**Fuel My Code ☢️**  
If this tool saved you time or helped secure your network:

- **UPI (India)**: coming soon
- **PayPal**: [paypal.me/kartik2005221](https://paypal.me/kartik2005221)

*Every contribution helps me stay caffeinated while patching vulnerabilities!*

---

## 📜 License

Distributed under **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📬 Contact

**Your Name**
- ✉️ Email: [kartik2005221@proton.me](mailto:kartik2005221@proton.me)
- 💻 GitHub: [@kartik2005221](https://github.com/kartik2005221)
- 🐦 Twitter: [@kartik2005221](https://twitter.com/kartik2005221)
- 🔗 LinkedIn: [/in/kartik2005221](https://linkedin.com/in/kartik2005221)

---

**Made with ❤️ and `sudo` privileges**  
*Ethical hacking starts with responsibility.*