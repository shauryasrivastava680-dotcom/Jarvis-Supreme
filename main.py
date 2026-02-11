import os, platform, psutil, webbrowser, time
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- JARVIS DASHBOARD (NO LOCK VERSION) ---
MASTER_HUD = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS SUPREME</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { margin: 0; background: #000; color: #00fbff; font-family: 'Segoe UI', sans-serif; overflow-x: hidden; }
        .container { height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
        #projector-grid { display: none; position: fixed; inset: 0; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; background: black; z-index: 9999; }
        .view { border: 0.2px solid rgba(0,251,255,0.1); display: flex; align-items: center; justify-content: center; }
        .view:nth-child(2) { transform: rotate(90deg); } .view:nth-child(3) { transform: rotate(180deg); } .view:nth-child(4) { transform: rotate(270deg); }
        .btn { background: rgba(0,251,255,0.1); border: 1px solid #00fbff; color: #00fbff; padding: 15px 30px; margin: 10px; cursor: pointer; font-weight: bold; width: 200px; text-transform: uppercase; letter-spacing: 2px; }
        .edith-ring { width: 150px; height: 150px; border: 4px double #00fbff; border-radius: 50%; animation: pulse 2s infinite; margin-bottom: 20px; }
        @keyframes pulse { 0% { transform: scale(0.95); opacity: 0.5; } 70% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(0.95); opacity: 0.5; } }
        .status-box { position: absolute; top: 10px; font-size: 10px; color: #00fbff; opacity: 0.7; }
    </style>
</head>
<body>
    <div class="container">
        <div class="status-box">SYSTEM: ONLINE | ENCRYPTION: ACTIVE</div>
        <div class="edith-ring"></div>
        <h1 style="letter-spacing: 5px;">JARVIS SUPER</h1>
        <p style="color: white; opacity: 0.6;">Welcome back, Shaurya.</p>
        
        <button class="btn" onclick="toggleProjector()">3D PROJECTOR</button>
        <button class="btn" onclick="triggerMusic()">PLAY MUSIC</button>
        <button class="btn" onclick="alert('System Optimized, Sir.')">NANO REPAIR</button>
    </div>

    <div id="projector-grid" onclick="this.style.display='none'">
        <div class="view"><div><div class="edith-ring"></div><p>EDITH<br>V1.0</p></div></div>
        <div class="view"><div><div class="edith-ring"></div><p>EDITH<br>V1.0</p></div></div>
        <div class="view"><div><div class="edith-ring"></div><p>EDITH<br>V1.0</p></div></div>
        <div class="view"><div><div class="edith-ring"></div><p>EDITH<br>V1.0</p></div></div>
    </div>

    <script>
        const socket = io();
        const synth = window.speechSynthesis;
        function speak(t) { const u = new SpeechSynthesisUtterance(t); u.pitch=0.8; synth.speak(u); }

        function toggleProjector() {
            document.getElementById('projector-grid').style.display = 'grid';
            speak("Activating 3D Blueprint Projection.");
        }

        function triggerMusic() {
            let song = prompt("Enter Song Name:");
            if(song) socket.emit('music', {query: song});
        }

        window.onload = () => speak("Jarvis is online. Systems ready.");
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(MASTER_HUD)

@socketio.on('music')
def music(data):
    # This will open on the SERVER/PC if it's running
    webbrowser.open(f"https://www.youtube.com/results?search_query={data['query']}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)