import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        output = f"Position du curseur : x={x}, y={y}"
        print('\r' + output + ' ' * 20, end='')  # Ajoute des espaces pour effacer les restes
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nArrêt du programme.")