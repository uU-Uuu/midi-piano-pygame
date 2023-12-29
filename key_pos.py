import pygame

WHITE_KEYS_LEFT = {
    108, 96, 84, 72, 60, 48, 36, 24,
    101, 89, 77, 65, 53, 41, 29, 21
}

WHITE_KEYS_RIGHT = {
    100, 88, 76, 64, 52, 40, 28,
    107, 95, 83, 71, 59, 47, 35, 23
}
WHITE_KEYS_MID = {
    98, 86, 74, 62, 50, 38, 26,
    103, 91, 79, 67, 55, 43, 31,
    105, 93, 81, 69, 57, 45, 33
}
BLACK_KEYS = {
    106, 94, 82, 70, 58, 46, 34, 22,
    104, 92, 80, 68, 56, 44, 32, 20,
    102, 90, 78, 66, 54, 42, 30, 18,
    99, 87, 75, 63, 51, 39, 27,
    97, 85, 73, 61, 49, 37, 25, 13
}

NOTE_WHITE_WIDTH = 23
NOTE_BLACK_WIDTH = 18
NOTE_FIRST = 21
NOTES_TOTAL = 88
NOTES_WHITE_HEIGHT = 150

def notesPos():

    li = [i for i in range(21, 109)]

    list_white_pos = []
    list_white = []
    list_black = []
    x = NOTE_WHITE_WIDTH / 2

    for note in li:
        if note not in BLACK_KEYS:
            x += NOTE_WHITE_WIDTH
            list_white.append(note)
            list_white_pos.append(x)
        else:
            list_black.append(note)

    notes_keys_white = dict(zip(list_white, list_white_pos))

    list_black_pos = []
    for note in list_black:
        for pos in notes_keys_white.keys():
            if note + 1 == pos:
                list_black_pos.append(notes_keys_white[pos] - NOTE_WHITE_WIDTH / 2)
                continue

    notes_keys_black = dict(zip(list_black, list_black_pos))
            
    dict_notes_bl_wh = {**notes_keys_black, **notes_keys_white}

    return dict(sorted(dict_notes_bl_wh.items()))

DICT_NOTES_POS = {21: 34.5, 22: 46.0, 23: 57.5, 24: 80.5, 25: 92.0, 26: 103.5, 27: 115.0, 28: 126.5, 29: 149.5, 30: 161.0, 
                  31: 172.5, 32: 184.0, 33: 195.5, 34: 207.0, 35: 218.5, 36: 241.5, 37: 253.0, 38: 264.5, 39: 276.0, 40: 287.5, 
                  41: 310.5, 42: 322.0, 43: 333.5, 44: 345.0, 45: 356.5, 46: 368.0, 47: 379.5, 48: 402.5, 49: 414.0, 50: 425.5, 
                  51: 437.0, 52: 448.5, 53: 471.5, 54: 483.0, 55: 494.5, 56: 506.0, 57: 517.5, 58: 529.0, 59: 540.5, 60: 563.5, 
                  61: 575.0, 62: 586.5, 63: 598.0, 64: 609.5, 65: 632.5, 66: 644.0, 67: 655.5, 68: 667.0, 69: 678.5, 70: 690.0, 
                  71: 701.5, 72: 724.5, 73: 736.0, 74: 747.5, 75: 759.0, 76: 770.5, 77: 793.5, 78: 805.0, 79: 816.5, 80: 828.0, 
                  81: 839.5, 82: 851.0, 83: 862.5, 84: 885.5, 85: 897.0, 86: 908.5, 87: 920.0, 88: 931.5, 89: 954.5, 90: 966.0, 
                  91: 977.5, 92: 989.0, 93: 1000.5, 94: 1012.0, 95: 1023.5, 96: 1046.5, 97: 1058.0, 98: 1069.5, 99: 1081.0, 100: 1092.5, 
                  101: 1115.5, 102: 1127.0, 103: 1138.5, 104: 1150.0, 105: 1161.5, 106: 1173.0, 107: 1184.5, 108: 1207.5}


def rectNotes():
    list_rect = []
    for key, pos in DICT_NOTES_POS.items():
        height = NOTES_WHITE_HEIGHT * 0.6  if key in BLACK_KEYS else NOTES_WHITE_HEIGHT * 0.4 
        height_coef = 0 if key in BLACK_KEYS else 100
        rect = pygame.Rect(pos - NOTE_WHITE_WIDTH/2, 675 + height_coef, NOTE_WHITE_WIDTH, height)
        list_rect.append(rect)
    return dict(zip([i for i in range(21, 109)], list_rect))


DICT_RECT = rectNotes()

