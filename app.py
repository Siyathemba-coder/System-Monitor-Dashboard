from flask import Flask, jsonify, render_template, make_response
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
    EXCLUDED = {"system idle process", "idle", "registry"}
    procs = []
    for p in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                    key=lambda x: x.info['cpu_percent'] or 0, reverse=True):
        try:
            name = p.info['name'] or ""
            if name.strip().lower() in EXCLUDED or p.info['pid'] == 0:
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

@app.route("/api/report")
def report():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count   = psutil.cpu_count()
    cpu_freq    = psutil.cpu_freq()
    ram         = psutil.virtual_memory()
    try:
        disk = psutil.disk_usage("C:\\")
    except:
        disk = psutil.disk_usage("/")
    net  = psutil.net_io_counters()
    now  = datetime.datetime.now()

    EXCLUDED = {"system idle process", "idle", "registry"}
    procs = []
    for p in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                    key=lambda x: x.info['cpu_percent'] or 0, reverse=True):
        try:
            name = p.info['name'] or ""
            if name.strip().lower() in EXCLUDED or p.info['pid'] == 0:
                continue
            procs.append({
                "pid":  p.info['pid'],
                "name": name,
                "cpu":  min(round(p.info['cpu_percent'] or 0, 1), 100.0),
                "mem":  round(p.info['memory_percent'] or 0, 1),
            })
            if len(procs) == 10:
                break
        except:
            pass

    def bar(pct, width=20):
        filled = int(pct / 100 * width)
        return "[" + "█" * filled + "░" * (width - filled) + f"] {pct}%"

    lines = [
        "=" * 60,
        "  SYSMON — SYSTEM REPORT",
        f"  Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "[ CPU ]",
        f"  Usage   : {bar(cpu_percent)}",
        f"  Cores   : {cpu_count}",
        f"  Speed   : {round(cpu_freq.current) if cpu_freq else 'N/A'} MHz",
        "",
        "[ MEMORY ]",
        f"  Usage   : {bar(ram.percent)}",
        f"  Used    : {round(ram.used/1e9,2)} GB / {round(ram.total/1e9,2)} GB",
        "",
        "[ DISK  (C:) ]",
        f"  Usage   : {bar(disk.percent)}",
        f"  Used    : {round(disk.used/1e9,1)} GB / {round(disk.total/1e9,1)} GB",
        f"  Free    : {round(disk.free/1e9,1)} GB",
        "",
        "[ NETWORK ]",
        f"  Sent    : {round(net.bytes_sent/1e6,1)} MB",
        f"  Received: {round(net.bytes_recv/1e6,1)} MB",
        "",
        "[ TOP PROCESSES ]",
        f"  {'PROCESS':<30} {'PID':>7}  {'CPU%':>6}  {'MEM%':>6}",
        "  " + "-" * 54,
    ]
    for p in procs:
        lines.append(f"  {p['name']:<30} {p['pid']:>7}  {p['cpu']:>5.1f}%  {p['mem']:>5.1f}%")

    lines += ["", "=" * 60, "  End of Report", "=" * 60]
    content = "\n".join(lines)

    filename = f"sysmon_report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    response = make_response(content)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/plain"
    return response


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
