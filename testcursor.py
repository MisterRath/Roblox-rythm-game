import pydirectinput
import time

time.sleep(2)

# Positionne la souris à différents endroits
positions = [(0, 0),(1, 1), (12, 7), (12, 14), (24, 7), (24, 14)]

for x, y in positions:
    pydirectinput.moveTo(x, y)
    time.sleep(1)
