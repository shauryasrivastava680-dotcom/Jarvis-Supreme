import os, platform, psutil, webbrowser, time, socket
try:
    from flask import Flask, render_template_string
    from flask_socketio import SocketIO, emit
except ImportError:
    print("Missing Libraries! Run: pip install flask flask-socketio eventlet")
    os._exit(0)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- JARVIS SUPREME CONFIGURATION ---
SYSTEM_CONFIG = {
    "boss": "Shaurya",
    "access": "hare krisna",
    "emergency": "radhe radhe",
    "edith_status": "Blueprint Loaded",
    "theme": "#00fbff"
}

# --- MASTER DASHBOARD (HTML/JS) ---
# Isme EDITH ka 3D wireframe aur All-Language support integrated hai.
MASTER_HUD = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS: EDITH INTERFACE</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { margin: 0; background: #000; color: #00fbff; font-family: 'Courier New', monospace; overflow: hidden; }
        .screen { height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        #projector-grid { display: none; position: fixed; inset: 0; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; background: black; z-index: 5000; }
        .view { border: 0.5px solid rgba(0,251,255,0.2); display: flex; align-items: center; justify-content: center; transform-origin: center; text-align: center; }
        .view:nth-child(2) { transform: rotate(90deg); } .view:nth-child(3) { transform: rotate(180deg); } .view:nth-child(4) { transform: rotate(270deg); }
        .btn { background: rgba(0,251,255,0.1); border: 1px solid #00fbff; color: #00fbff; padding: 12px 25px; margin: 10px; cursor: pointer; border-radius: 5px; }
        .edith-frame { width: 250px; height: 100px; border: 2px solid #00fbff; border-radius: 50% / 10%; position: relative; animation: rotate3d 5s infinite linear; }
        @keyframes rotate3d { from { transform: rotateY(0deg); } to { transform: rotateY(360deg); } }
        .stats-panel { position: absolute; top: 20px; left: 20px; font-size: 12px; line-height: 1.5; }
    </style>
</head>
<body>
    <div id="auth-layer" class="screen">
        <h1 id="lock-text">BIOMETRIC SCAN REQUIRED</h1>
        <button class="btn" onclick="startAuth()">SAY ACCESS CODE</button>
    </div>

    <div id="projector-grid">
        <div class="view"><div><div class="edith-frame"></div><p>EDITH v1.0<br>SHAURYA</p></div></div>
        <div class="view"><div><div class="edith-frame"></div><p>EDITH v1.0<br>SHAURYA</p></div></div>
        <div class="view"><div><div class="edith-frame"></div><p>EDITH v1.0<br>SHAURYA</p></div></div>
        <div class="view"><div><div class="edith-frame"></div><p>EDITH v1.0<br>SHAURYA</p></div></div>
    </div>

    <div id="main-panel" class="screen" style="display:none;">
        <div class="stats-panel">
            <div>SYSTEM: ONLINE</div>
            <div>SATELLITE: ACTIVE</div>
            <div>NANO-CORE: READY</div>
            <div id="cpu-stat">CPU: 0%</div>
        </div>
        <div class="edith-frame" style="margin-bottom: 30px;"></div>
        <h2>EDITH SUPREME DASHBOARD</h2>
        <div>
            <button class="btn" onclick="toggleProjector()">3D PROJECTOR</button>
            <button class="btn" onclick="triggerNano()">NANO REPAIR</button>
            <button class="btn" onclick="askJarvis()">COMMAND JARVIS</button>
            <button class="btn" onclick="playMusic()">PLAY MUSIC</button>
        </div>
    </div>

    <script>
        const socket = io();
        const synth = window.speechSynthesis;

        function speak(text) {
            const ut = new SpeechSynthesisUtterance(text);
            ut.pitch = 0.85; ut.rate = 1.0;
            synth.speak(ut);
        }

        function startAuth() {
            const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            rec.lang = 'hi-IN';
            rec.start();
            rec.onresult = (e) => {
                const code = e.results[0][0].transcript.toLowerCase();
                socket.emit('verify_shaurya', {code: code});
            };
        }

        socket.on('auth_success', (data) => {
            speak(data.msg);
            document.getElementById('auth-layer').style.display = 'none';
            document.getElementById('main-panel').style.display = 'flex';
        });

        function toggleProjector() {
            const grid = document.getElementById('projector-grid');
            grid.style.display = (grid.style.display === 'none') ? 'grid' : 'none';
            speak("Projecting EDITH blueprints in 3D.");
        }

        function triggerNano() {
            speak("Initiating Nano-repair protocol. Optimizing molecular health.");
            socket.emit('run_nano');
        }

        function playMusic() {
            const song = prompt("Sir, which track should I stream?");
            if(song) socket.emit('music_req', {query: song});
        }

        function askJarvis() {
            const cmd = prompt("Enter command (App name, Weather, or Question):");
            if(cmd) socket.emit('universal_cmd', {cmd: cmd});
        }

        socket.on('jarvis_talk', (data) => speak(data.text));

        // Real-time Health
        setInterval(() => socket.emit('get_health'), 2000);
        socket.on('health_update', (data) => {
            document.getElementById('cpu-stat').innerText = `CPU: ${data.cpu}% | RAM: ${data.ram}%`;
        });
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC ---
@app.route('/')
def home():
    return render_template_string(MASTER_HUD)

@socketio.on('verify_shaurya')
def verify(data):
    code = data['code'].strip()
    if code in [SYSTEM_CONFIG["access"], SYSTEM_CONFIG["emergency"]]:
        emit('auth_success', {'msg': f"Welcome back Shaurya. EDITH is online and ready for deployment."})
    else:
        emit('jarvis_talk', {'text': "Authentication failed. Access denied."})

@socketio.on('get_health')
def health():
    emit('health_update', {'cpu': psutil.cpu_percent(), 'ram': psutil.virtual_memory().percent})

@socketio.on('music_req')
def music(data):
    webbrowser.open(f"https://www.youtube.com/results?search_query={data['query']}")
    emit('jarvis_talk', {'text': f"Streaming {data['query']} for you, Sir."})

@socketio.on('universal_cmd')
def universal(data):
    cmd = data['cmd'].lower()
    if "open" in cmd:
        app_name = cmd.replace("open ", "")
        os.system(f"start {app_name}" if platform.system() == "Windows" else f"open -a {app_name}")
        emit('jarvis_talk', {'text': f"Opening {app_name}."})
    else:
        # Thinking logic
        emit('jarvis_talk', {'text': f"Sir, I have processed your request for {cmd}. Systems are operational."})

@socketio.on('run_nano')
def nano():
    # Simulation for repair
    time.sleep(1)

if __name__ == '__main__':
    # Globally accessible on local network
    print(f"JARVIS IS STARTING...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
