import autoit
import time

# Affiche la position du curseur pendant 5 secondes
start_time = time.time()
while time.time() - start_time < 5:
    pos = autoit.mouse_get_pos()
    print(f"Position du curseur : x={pos[0]}, y={pos[1]}", end='\r')
    time.sleep(0.05)

# Déplace la souris de gauche à droite sur l'écran
screen_width = autoit.win_get_pos("[ACTIVE]")[2]
y = autoit.mouse_get_pos()[1]

for x in range(0, screen_width, 10):
    autoit.mouse_move(x, y, speed=1)
    time.sleep(0.01)