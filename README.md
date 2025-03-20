# Real-Time Process Monitoring Dashboard

Hey there! This is a neat little tool I threw together to keep an eye on your system’s processes in real time. It’s got a slick dark-themed UI with charts for CPU and memory usage, plus a table of running processes you can kill if they’re acting up. Built with Flask, SocketIO, and some front-end magic—perfect for OS nerds or anyone who likes watching their computer’s guts tick.

## What It Does
- Shows total CPU and memory usage up top.
- Graphs CPU and memory trends (full-width, stacked vertically).
- Lists all running processes with PID, name, CPU%, memory%, and state.
- Lets you kill processes with a button (if you’ve got the perms).
- Pops up messages for success or errors.

## Tech Stack
- **Backend**: Python (Flask + Flask-SocketIO) with `psutil` for system data.
- **Frontend**: HTML/CSS/JS with Chart.js for graphs and Socket.IO for real-time updates.
- **Look**: Dark purple theme ‘cause light mode hurts my eyes.

## Getting Started

### Prerequisites
- Python 3.x (I used 3.11, but 3.8+ should work).
- Git (if you’re cloning this).
- A terminal and some patience.

### Setup
1. **Clone the Repo**
   ```bash
   git clone https://github.com/BinarySapling/OS_CA.git
   cd OS_CA
   pip install flask flask-socketio psutil
   OS_CA/
Project Structure
    ├── app.py
    ├── templates/
    │   └── index.html
    └── README.md
Run It
  python app.py
Open It Hit http://localhost:5000 in your browser. Boom—dashboard time.
