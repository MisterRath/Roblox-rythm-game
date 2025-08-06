from PIL import ImageGrab
import time
import pydirectinput
import keyboard

initial_pos = (1280, 720)
area = (867, 308, 1694, 1133)
freq = 1/240  # Fréquence de capture d'image
offset = (376,376 )  # Décalage pour la capture d'image
# move : 4 coins principaux, chaque coin est associé à certains carrés (voir commentaires)
move = [ (12, 7), (24, 7), (12, 14), (24, 14)]

couples = [
    [(910, 344), (933, 344)],      # carré 1
    [(1170, 344), (1370, 344)],    # carré 2
    [(1555, 344), (1600, 344)],    # carré 3
    [(904, 613), (904, 720)],      # carré 4
    [(1172, 1), (1386, 3), (1172, 123), (1386, 827)],    # carré 5
    [(1280+376, 613), (1280+376, 720)],    # carré 6
    [(910, 720+376), (933, 720+376)],    # carré 7
    [(1170, 720+376), (1370, 720+376)],  # carré 8
    [(1555, 720+376), (1600, 720+376)],  # carré 9
]

# Association des carrés à leur(s) move(s)
carre_to_move = {
    0: [0],           # carré 1 → haut gauche
    1: [0, 1],        # carré 2 → haut gauche, haut droit
    2: [1],           # carré 3 → haut droit
    3: [0, 2],        # carré 4 → haut gauche, bas gauche
    4: [0, 1, 2, 3],  # carré 5 → tous les coins
    5: [1, 3],        # carré 6 → haut droit, bas droit
    6: [2],           # carré 7 → bas gauche
    7: [2, 3],        # carré 8 → bas gauche, bas droit
    8: [3],           # carré 9 → bas droit
}

def is_not_dark(color, threshold=10):
    r, g, b = color[:3]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return luminance > threshold

def all_corners_luminous(pixels, coords, threshold=30):
    return all(is_not_dark(pixels[x, y], threshold) for x, y in coords)

mouse_enabled = False
print("Appuie sur 'q' pour activer/désactiver le déplacement de la souris.")

queue_detected = []

try:
    while True:
        if keyboard.is_pressed('q'):
            mouse_enabled = not mouse_enabled
            if mouse_enabled:
                pydirectinput.moveTo(0, 0)
                pydirectinput.moveTo(1, 1)
            print(f"\nDéplacement souris {'activé' if mouse_enabled else 'désactivé'} (touche 'q').")
            while keyboard.is_pressed('q'):
                time.sleep(freq)
        img = ImageGrab.grab()
        pixels = img.load()
        current_detected = []
        for idx, couple in enumerate(couples):
            if all_corners_luminous(pixels, couple):
                current_detected.append(idx)

        # Ajouter les nouveaux carrés détectés à la file
        for idx in current_detected:
            if idx not in queue_detected:
                queue_detected.append(idx)

        # Retirer les carrés qui ne sont plus détectés
        queue_detected = [idx for idx in queue_detected if idx in current_detected]

        if queue_detected:
            detected = queue_detected[0]
            move_idx = carre_to_move[detected][0]
            x, y = move[move_idx]
            if mouse_enabled:
                pydirectinput.moveTo(x, y)
            print(f"\rCarré détecté (file) : {detected+1} | Déplacement souris vers : {x}, {y} | Mouse {'ON' if mouse_enabled else 'OFF'}      ", end='')
        else:
            print(f'\rNo luminous square detected | Mouse {"ON" if mouse_enabled else "OFF"}' + ' ' * 40, end='')

        time.sleep(freq)
except KeyboardInterrupt:
    print("\nArrêt du script.")