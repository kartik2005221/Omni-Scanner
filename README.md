# 🔍 Omni-Scanner: Simple & Powerful Network Scanner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%20%7C%20Windows-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0-orange?label=Version%20\(readme\))
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/kartik2005221/omni-scanner?label=Version%20\(github\)\&sort=semver)

**Discover devices. Understand your network. Stay secure.**

Omni-Scanner is a Python-based, easy-to-use network scanner that helps you detect devices, analyze network paths, and run advanced scans. Designed for ethical hacking, learning, and securing your own network.

---

## 🚀 Features

* 🕵️ **Device Discovery** — Find devices on your local network with ARP scans
* 📡 **Custom Ping Options** — Perform simple or flood pings, and check latency
* 🗺️ **Traceroute** — Visualize the route your packets take
* 🔦 **Advanced Scanning** — Integrates with Nmap for OS detection and stealth scanning

---

## ⚙️ Installation

### Prerequisites

* Python 3.8+
* `nmap` installed — [Get Nmap](https://nmap.org/download.html)
* **Linux/macOS:** `arp-scan` via your package manager
* **Windows:** [Npcap](https://npcap.com/) required for low-level scans

### Setup Steps

1. Clone the project:

   ```bash
   git clone https://github.com/kartik2005221/Omni-Scanner.git
   cd Omni-Scanner
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the scanner:

   ```bash
   sudo python3 main.py
   ```

   OR (on Windows):

   ```bash
   python main.py
   ```

> 💡 **Having issues?** Double-check the requirements or [open an issue](https://github.com/kartik2005221/Omni-Scanner/issues).

---

## 🖥️ Screenshots

**Interactive Menu**
![Menu Demo](/Medias/screenshot.png)

---

## 🧪 Testing

Omni-Scanner now includes a test suite to ensure code quality and reliability.

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests.test_scan_builders -v
python -m unittest tests.test_input_validators -v
```

### Test Coverage

The test suite covers:
* **Command Builders** — Validates correct command construction for ping, traceroute, ARP, and Nmap scans
* **Input Validators** — Tests port parsing, packet size validation, timeout validation, and IP normalization
* **Edge Cases** — Ensures proper handling of invalid inputs and boundary conditions

All core utility functions are tested to maintain code quality during refactoring and feature additions.

---

## 🛠️ Development

### Project Structure

```
Omni-Scanner/
├── OS_scripts/          # Platform-specific menu implementations
│   ├── linux.py         # Linux menu and commands
│   └── windows.py       # Windows menu and commands
├── utils/               # Utility modules
│   ├── scan_builders.py        # Pure command construction functions
│   ├── input_validators.py    # Enhanced input validation
│   ├── menu_utils.py          # Menu and validation helpers
│   ├── common_utils.py        # Common utilities
│   └── administrative_utils.py # Sudo/admin management
├── tests/               # Unit test suite
│   ├── test_scan_builders.py
│   └── test_input_validators.py
└── main.py             # Application entry point
```

### Code Quality

The codebase follows these principles:
* **Separation of Concerns** — Command building separated from UI and execution
* **Input Validation** — Uses Python's `ipaddress` module for robust IP validation
* **Enhanced Docstrings** — Comprehensive documentation for all public functions
* **Testability** — Pure functions enable easy unit testing without I/O dependencies

---

## ⚠️ Responsible Use

This tool is for **educational and authorized use only**.

✅ Only scan networks you own or have clear permission to test.

⛔ Never use this tool for illegal activities — misuse is strictly prohibited.

*Omni-Scanner is meant to promote security awareness, not exploitation.*

---

## 🤝 Contributing

Contributions are welcome!

* Found a bug? [Open an issue](https://github.com/kartik2005221/Omni-Scanner/issues) with the "Bug" label
* Got a feature idea? Suggest it under "Enhancement"
* Want to code? Fork the repo, make your changes, and submit a pull request

---

## ☕ Support My Work

If this tool helped you, consider supporting:

* **UPI (India):** [kartik2005221@upi](/Medias/QR_1744889718.png)
* **PayPal:** [paypal.me/kartik2005221](https://paypal.me/kartik2005221)

*Your support helps me keep building open-source tools like this!*

---

## 📜 License

Released under the **MIT License** — see [LICENSE](LICENSE) for full details.

---

## 📬 Contact

[![Email](https://img.shields.io/badge/proton%20mail-6D4AFF?style=for-the-badge\&logo=protonmail\&logoColor=white)](mailto:kartik2005221@proton.me)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/kartik2005221)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/kartik2005221/)

---

**Made with ❤️, Python, and a bit of curiosity.**

*Secure networks. Learn continuously. Stay ethical.*
