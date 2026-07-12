# InstaCPR

> A modular Python framework for automating copyright report submissions on Meta platforms.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Instagram%20%7C%20Facebook-purple)
![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ⚠️ Disclaimer

This project is intended **only for educational, research, testing, and legitimate copyright enforcement purposes.**

Users are solely responsible for complying with all applicable laws, platform policies, and Meta's Terms of Service.

The author assumes **no responsibility** for misuse of this software.

---

# Overview

InstaCPR is a modular automation framework built with Python and Selenium that streamlines copyright reporting workflows for Meta platforms.

Instead of using a single monolithic script, the project separates responsibilities into reusable modules including:

- Workflow Engine
- Driver Management
- Retry System
- Logging
- Report Generation
- Temporary Email Integration
- OTP Retrieval
- Platform-specific Actions
- Telegram Progress Updates
- Terminal Interface

The framework was designed to be scalable and easily extendable for future automation features.

---

# Features

- Instagram copyright reporting
- Facebook copyright reporting
- Modular workflow engine
- Automatic temporary email generation
- Automatic OTP retrieval
- Retry system
- Headless browser support
- Proxy support
- JSON report generation
- Screenshot capture on failure
- Telegram progress updates
- Terminal UI
- Structured logging
- Platform abstraction
- Easily extendable architecture

---

# Architecture

```
                User
                  │
                  ▼
          MetaReporter
                  │
                  ▼
             Workflow
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 Driver      MailGen      OTP System
 Manager     Generator
     │
     ▼
 Selenium Browser
     │
     ▼
 Instagram / Facebook
```

---

# Project Structure

```
instaCPR/

│
├── core/
│   ├── config.py
│   ├── driver.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── models.py
│   ├── platforms.py
│   ├── proxy.py
│   ├── queue.py
│   ├── reporter.py
│   └── workflow.py
│
├── utils/
│   ├── actions/
│   │   ├── instagram/
│   │   └── facebook/
│   │
│   ├── mailgen.py
│   ├── otp.py
│   ├── post2user.py
│   └── ...
│
├── reports/
├── logs/
├── screenshots/
│
├── mainTUI.py
├── mainTG.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/laguetechnical/instaCPR.git

cd instaCPR
```

### Linux (One-line Automatic Install)

```bash
git clone https://github.com/laguetechnical/instaCPR.git && cd instaCPR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cat > /usr/local/bin/instacpr << 'EOF'
#!/bin/bash
export PYTHONPATH="/path/to/instaCPR:$PYTHONPATH"
exec $(pwd)/venv/bin/python $$   (pwd)/mainTUI.py "   $$@"
EOF
sudo chmod +x /usr/local/bin/instacpr && deactivate && echo "✅ InstaCPR installed! Run: instacpr"

### Windows

```cmd
.venv\Scripts\activate
```

---

# Requirements

- Python 3.10+
- Google Chrome
- ChromeDriver (handled automatically)
- Internet connection

---

# Dependencies

- Selenium
- webdriver-manager
- requests
- beautifulsoup4
- python-dotenv
- flask
- telethon
- python-telegram-bot
- rich
- tenacity
- pproxy

---

# Running

Terminal Interface

```bash
python mainTUI.py
```

Telegram Bot

```bash
python mainTG.py
```

---

# Workflow

The reporting process follows this sequence:

1. Launch browser
2. Open copyright form
3. Generate temporary email
4. Fill report details
5. Submit initial form
6. Wait for Meta OTP
7. Retrieve OTP automatically
8. Submit OTP
9. Complete report
10. Save report JSON
11. Close browser

---

# Core Components

## MetaReporter

Coordinates the complete reporting process.

Responsibilities:

- Driver creation
- Report building
- Workflow execution
- Progress reporting
- Error handling
- Report saving

---

## Workflow

Responsible for executing every reporting step.

Features:

- Step execution
- Retry logic
- OTP handling
- Progress callbacks
- Exception handling

---

## DriverManager

Handles Selenium lifecycle.

Features:

- Chrome startup
- Headless mode
- Proxy configuration
- Screenshots
- Browser cleanup

---

## Logger

Provides structured logging.

- Progress logs
- Errors
- Exceptions
- Report status

---

## Platform Configuration

Platform-specific actions are separated from the core engine.

```
Instagram
    ↓
Action Mapping

Facebook
    ↓
Action Mapping

Workflow
    ↓
Shared Execution Logic
```

This allows new platforms to be added with minimal code changes.

---

# Reports

Successful runs generate JSON reports.

Example:

```json
{
  "status": "success",
  "platform": "instagram",
  "fullname": "John Doe",
  "target_url": "...",
  "email": "...",
  "duration_seconds": 42
}
```

---

# Headless Mode

Supports Chrome Headless.

```python
MetaReporter(
    headless=True
)
```

---

# Proxy Support

Supports HTTP proxies.

Example:

```python
proxy_config = "http://IP:PORT"
```

---

# Error Handling

The framework automatically handles:

- Selenium exceptions
- Retryable failures
- OTP timeout
- Browser cleanup
- Screenshot capture
- Logging

---

# Screenshots

On failures, browser screenshots are automatically captured for debugging.

---

# Logging

Logs include:

- Progress
- Exceptions
- Retry attempts
- Workflow steps
- Final status

---

# Extending the Framework

New platforms can be added by:

1. Creating action modules
2. Registering them in `platforms.py`
3. Defining workflow mappings

No changes to the workflow engine are required.

---

# Roadmap

- [ ] Web Dashboard
- [ ] Multi-threaded reporting
- [ ] CAPTCHA solving integration
- [ ] Advanced proxy rotation
- [ ] Queue management improvements
- [ ] Docker support
- [ ] CI/CD pipeline
- [ ] Plugin system
- [ ] REST API

---

# Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss your proposed improvements.

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

Built with:

- Python
- Selenium
- Telethon
- Rich
- Flask
- webdriver-manager

---

# Author

**Ahmed Salim**

GitHub:
https://github.com/laguetechnical

---

## Star the Repository ⭐

If you found this project useful, consider giving it a star to support future development.
