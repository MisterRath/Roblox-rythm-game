import time
import numpy as np
import pydirectinput
import keyboard
import dxcam
import threading

# === PARAMÈTRES ===
area = (867, 308, 1694, 1133)
offset = 370
width, height = area[2] - area[0], area[3] - area[1]

move = [(12, 7), (24, 7), (12, 14), (24, 14)]

couples = [
    [(910, 720-offset), (933, 720-offset)],
    [(1170, 720-offset), (1370, 720-offset)],
    [(1555, 720-offset), (1600, 720-offset)],
    [(1280-offset, 613), (904, 720)],
    [(1172, 1), (1386, 3), (1172, 123), (1386, 827)],
    [(1280+offset, 613), (1280+offset, 720)],
    [(910, 720+offset), (933, 720+offset)],
    [(1170, 720+offset), (1370, 720+offset)],
    [(1555, 720+offset), (1600, 720+offset)],
]

carre_to_move = {
    0: [0], 1: [0, 1], 2: [1], 3: [0, 2], 4: [0, 1, 2, 3],
    5: [1, 3], 6: [2], 7: [2, 3], 8: [3],
}

# === COORDONNÉES RELATIVES ===
couples_rel = [[(x - area[0], y - area[1]) for (x, y) in couple] for couple in couples]

# === FLAGS ===
mouse_enabled = False
SHOW_DEBUG = False  # Désactive les print() pour plus de Hz
THRESHOLD = 50

# === INIT CAMERA ===
camera = dxcam.create(output_color="GRAY")
camera.start(region=area, target_fps=0)

# === FILES & FPS ===
queue_detected = []
frame_lock = threading.Lock()
latest_frame = None

# === THREAD DE CAPTURE ===
def capture_thread():
    global latest_frame
    while True:
        frame = camera.get_latest_frame()
        if frame is not None:
            with frame_lock:
                latest_frame = frame

threading.Thread(target=capture_thread, daemon=True).start()

# === LOOP PRINCIPALE (DETECTION + ACTION) ===
loop_count = 0
last_time = time.time()
frequency = 0

try:
    while True:
        loop_count += 1
        now = time.time()
        if now - last_time >= 1:
            frequency = loop_count
            loop_count = 0
            last_time = now

        # Toggle souris
        if keyboard.is_pressed('q'):
            mouse_enabled = not mouse_enabled
            if mouse_enabled:
                pydirectinput.moveTo(0, 0)
                pydirectinput.moveTo(1, 1)
            print(f"\nSouris {'activée' if mouse_enabled else 'désactivée'} (touche 'q').")
            while keyboard.is_pressed('q'):
                time.sleep(0.05)

        with frame_lock:
            frame = latest_frame.copy() if latest_frame is not None else None

        if frame is None:
            continue

        # === DÉTECTION ULTRA-RAPIDE ===
        current_detected = []
        for idx, couple in enumerate(couples_rel):
            if all(frame[y, x] > THRESHOLD for (x, y) in couple):
                current_detected.append(idx)

        for idx in current_detected:
            if idx not in queue_detected:
                queue_detected.append(idx)
        queue_detected = [idx for idx in queue_detected if idx in current_detected]

        if queue_detected:
            detected = queue_detected[0]
            move_idx = carre_to_move[detected][0]
            x, y = move[move_idx]
            if mouse_enabled:
                pydirectinput.moveTo(x, y)

        # === DEBUG (optionnel) ===
        if SHOW_DEBUG and loop_count % 20 == 0:
            print(f"\rFPS: {frequency} | File: {queue_detected}", end='')

except KeyboardInterrupt:
    print("\nArrêt du script.")
    camera.stop()
