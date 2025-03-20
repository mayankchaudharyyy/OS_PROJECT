from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") # let it connect from anywhere for now

# serve up the html page
@app.route('/')
def index():
    return render_template('index.html')

# messy function to grab system stats
def get_system_data():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            # shove process details into a dict
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu': round(proc.info['cpu_percent'], 1),
                'memory': round(proc.info['memory_percent'],1),
                'state': proc.info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass # skip if it fails, whatever

    # get cpu and memory stuff
    total_cpu = round(psutil.cpu_percent(), 1)
    mem = psutil.virtual_memory()
    total_memory_used = round(mem.used / (1024**3), 2) # bytes to GB
    total_memory_total = round(mem.total / 1024 ** 3, 2)
    total_memory = round(mem.percent,1)

    # pack it all up
    return {
        'total_cpu': total_cpu,
        'total_memory': total_memory,
        'total_memory_used': total_memory_used,
        'total_memory_total': total_memory_total,
        'processes': processes
    }

# keep sending updates
def background_task():
    while True:
        data = get_system_data()
        socketio.emit('update', data)
        time.sleep(1) # chill for a sec

# when someone connects
@socketio.on('connect')
def handle_connect():
    socketio.emit('message', {'msg': 'Hey you connected!', 'status': 'success'})
    socketio.start_background_task(background_task) # start the updates

# kill a process when asked
@socketio.on('kill_process')
def handle_kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate() # try to kill nicely
        socketio.emit('message', {'msg': 'Killed process ' + str(pid), 'status': 'success'})
    except psutil.NoSuchProcess:
        socketio.emit('message', {'msg': "Couldn't find " + str(pid), 'status': 'error'})
    except psutil.AccessDenied:
        socketio.emit('message', {'msg': 'No permission to kill ' + str(pid), 'status': 'error'})
    except Exception as e:
        socketio.emit('message', {'msg': 'Oops, error: ' + str(e), 'status': 'error'})

# run this thing
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)