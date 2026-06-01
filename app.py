from flask import Flask, jsonify, render_template
import psutil
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    # RAM
    ram = psutil.virtual_memory()

    # Disk (C: drive on Windows)
    try:
        disk = psutil.disk_usage("C:\\")
    except:
        disk = psutil.disk_usage("/")

    # Network
    net = psutil.net_io_counters()

    # Top 8 processes by CPU
    EXCLUDED = {"system idle process", "idle"}
    procs = []
    for p in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                    key=lambda x: x.info['cpu_percent'] or 0, reverse=True):
        try:
            name = p.info['name'] or ""
            if name.lower() in EXCLUDED:
                continue
            cpu = min(round(p.info['cpu_percent'] or 0, 1), 100.0)
            procs.append({
                "pid":  p.info['pid'],
                "name": name,
                "cpu":  cpu,
                "mem":  round(p.info['memory_percent'] or 0, 1),
            })
            if len(procs) == 8:
                break
        except:
            pass

    return jsonify({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "cpu": {
            "percent": cpu_percent,
            "cores": cpu_count,
            "freq_mhz": round(cpu_freq.current) if cpu_freq else "N/A",
        },
        "ram": {
            "percent": ram.percent,
            "used_gb": round(ram.used / 1e9, 2),
            "total_gb": round(ram.total / 1e9, 2),
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": round(disk.used / 1e9, 1),
            "total_gb": round(disk.total / 1e9, 1),
        },
        "network": {
            "sent_mb": round(net.bytes_sent / 1e6, 1),
            "recv_mb": round(net.bytes_recv / 1e6, 1),
        },
        "processes": procs,
    })

if __name__ == "__main__":
    print("System Monitor running at http://localhost:5000")
    app.run(debug=False, port=5000)from flask import Flask, jsonify, render_template
import psutil
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def stats():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    # RAM
    ram = psutil.virtual_memory()

    # Disk (C: drive on Windows)
    try:
        disk = psutil.disk_usage("C:\\")
    except:
        disk = psutil.disk_usage("/")

    # Network
    net = psutil.net_io_counters()

    # Top 8 processes by CPU
    procs = []
    for p in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                    key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:8]:
        try:
            procs.append({
                "pid":  p.info['pid'],
                "name": p.info['name'],
                "cpu":  round(p.info['cpu_percent'] or 0, 1),
                "mem":  round(p.info['memory_percent'] or 0, 1),
            })
        except:
            pass

    return jsonify({
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "cpu": {
            "percent": cpu_percent,
            "cores": cpu_count,
            "freq_mhz": round(cpu_freq.current) if cpu_freq else "N/A",
        },
        "ram": {
            "percent": ram.percent,
            "used_gb": round(ram.used / 1e9, 2),
            "total_gb": round(ram.total / 1e9, 2),
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": round(disk.used / 1e9, 1),
            "total_gb": round(disk.total / 1e9, 1),
        },
        "network": {
            "sent_mb": round(net.bytes_sent / 1e6, 1),
            "recv_mb": round(net.bytes_recv / 1e6, 1),
        },
        "processes": procs,
    })

if __name__ == "__main__":
    print("System Monitor running at http://localhost:5000")
    app.run(debug=False, port=5000)
