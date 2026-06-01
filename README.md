
# SysMon - System Monitor Dashboard

A real-time web dashboard that monitors your Windows system's CPU, RAM, Disk, Network, and top processes.

## Setup

### 1. Install Python
Make sure Python 3.8+ is installed. Download from https://python.org if needed.

### 2. Install dependencies
Open a terminal (Command Prompt or PowerShell) in this folder and run:

```
pip install -r requirements.txt
```

### 3. Run the app

```
python app.py
```

### 4. Open in browser
Go to: **http://localhost:5000**

The dashboard refreshes automatically every 2 seconds.

## What it shows
- **CPU** — usage %, core count, clock speed
- **Memory** — used/total GB with live bar
- **Disk (C:)** — used/total GB with live bar
- **Network** — total MB sent and received since boot
- **Top Processes** — top 8 processes by CPU usage, with PID and memory %

## Color indicators
- 🟢 Green = normal (under 60%)
- 🟡 Yellow = moderate (60–85%)
- 🔴 Red = high (above 85%)
