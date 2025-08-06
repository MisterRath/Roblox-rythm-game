from PIL import ImageGrab
import time

initial_pos = (1280, 720)
area = (867, 308, 1694, 1133)
offset1 = 1280 -1142
offset2 = 720 - 582
#create move with 4 elements being the 4 corners of the square using intial_pos and offset1 and offset2
move = [
    (initial_pos[0] - offset1, initial_pos[1] - offset2),  # haut gauche pour carré 1,2,4 et 5
    (initial_pos[0] + offset1, initial_pos[1] - offset2),  # haut droit  pour carré 2,3,5 et 6
    (initial_pos[0] - offset1, initial_pos[1] + offset2),  # bas gauche pour carré 4,5,7 et 8
    (initial_pos[0] + offset1, initial_pos[1] + offset2)   # bas droit pour carré 5,6,8 et 9
]
couples = [
    [(910, 350), (1111, 350), (910, 552), (1111, 552)],      # carré 1
    [(1172, 350), (1386, 350), (1172, 552), (1386, 552)],    # carré 2
    [(1447, 350), (1661, 350), (1447, 552), (1661, 552)],    # carré 3
    [(920, 613), (1111, 613), (920, 827), (1111, 827)],      # carré 4
    [(1172, 613), (1386, 613), (1172, 827), (1386, 827)],    # carré 5
    [(1447, 613), (1661, 613), (1447, 827), (1661, 827)],    # carré 6
    [(910, 888), (1111, 888), (910, 1102), (1111, 1102)],    # carré 7
    [(1172, 888), (1386, 888), (1172, 1102), (1386, 1102)],  # carré 8
    [(1447, 888), (1630, 888), (1447, 1069), (1630, 1069)],  # carré 9
]

def is_not_dark(color, threshold=30):
    # Calcul de la luminance perçue (méthode standard)
    r, g, b = color[:3]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return luminance > threshold

def all_corners_luminous(pixels, coords, threshold=30):
    # Vérifie que tous les coins sont lumineux
    return all(is_not_dark(pixels[x, y], threshold) for x, y in coords)

try:
    while True:
        img = ImageGrab.grab()
        pixels = img.load()
        luminous_couples = [
            f"Square {idx+1}"
            for idx, couple in enumerate(couples)
            if all_corners_luminous(pixels, couple)
        ]
        if luminous_couples:
            print('\r' + ' | '.join(luminous_couples) + ' ' * 40, end='')
        else:
            print('\rNo luminous square' + ' ' * 100, end='')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nArrêt du script.")