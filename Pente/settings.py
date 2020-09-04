# game options/settings
TITLE = 'Jeu de Pente AI implementation'
SIZE_BOARD = 19
DELTA_PIX = 50
WIDTH = 1500
HEIGHT = (SIZE_BOARD + 1) * DELTA_PIX
SIZE_STONE = 23
CLR_STONE = ['white', 'black']
BOARD = [[ 0 for i in range(SIZE_BOARD)] for i in range(SIZE_BOARD)]
DICTIONARY = {'player': None, 'player_color': None, 'nb_points': None}
CAPTURE_DIC = {'1': 0, '2': 0}
BOARD_FILE = 'board.txt'
SAVED_GAME = 'savedGame.txt'
AUDIO_FILE = 'audio.txt'
THEME_FILE = 'theme.txt'
IMAGE_FOLDER = 'image'
SOUND_FOLDER = 'sound'
GAME_FILES = 'game_files'
