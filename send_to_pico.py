import time
import serial
from spotify_now import get_current_track

# Certifique-se de que o COM6 está correto
ser = serial.Serial("COM5", 115200)

while True:
    track_info = get_current_track()
    if track_info:
        track_name, duration, progress = track_info
        # Certifique-se de que 'encode' está sendo chamado corretamente
        message = f"{track_name[:20]}|{duration}|{progress}\n"
        ser.write(message.encode("utf-8"))  # Aqui você deve chamar 'encode' no objeto 'message'
    
    time.sleep(0.5)
