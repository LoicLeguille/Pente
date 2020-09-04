# python packages needed
from tkinter import *
import subprocess
import sys
import copy
from AI import *
from settings import *
import settings
from os import path
try:
    import pygame as pg
    from PIL import Image
    from PIL import ImageTk
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    import pygame as pg
    from PIL import Image
    from PIL import ImageTk

class Game(Canvas):
    def __init__(self, root):
        # initiate game window, etc
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        pg.mixer.init()
        self.parent = root
        self.parent.title(settings.TITLE)
        self.parent.resizable(0, 0)
        self.parent.geometry('+20+30')
        self.SW = self.parent.winfo_screenwidth()
        self.SH = self.parent.winfo_screenheight()
        self.english = True
        self.game_over = False
        self.AI_opp = False
        self.T = 'Theme_en'
        Canvas.__init__(self, self.parent, width = settings.WIDTH / 2048 * self.SW, height = settings.HEIGHT / 1152 * self.SH, highlightthickness = 0)
        self.size_board = settings.SIZE_BOARD
        self.size_stone = settings.SIZE_STONE / 2048 * self.SW
        self.color_stone = copy.deepcopy(settings.CLR_STONE)
        self.stone_number = 0
        self.dictionary = copy.deepcopy(settings.DICTIONARY)
        self.capture_dic = copy.deepcopy(settings.CAPTURE_DIC)
        self.last_piece_pos = [9, 9]
        self.capture_count = [0, 0]
        self.state = False
        self.delta = settings.DELTA_PIX
        self.coord_mid = (self.size_board // 2 + 1) * self.delta
        self.load_data()
        self.draw_board()
        self.button_layout()
        self.draw_text()
        self.delta = int(self.delta / 2048 * self.SW)
        self.coord_mid = (self.size_board // 2 + 1) * self.delta
        self.parent.bind('<KeyRelease-F11>', self.button_event)
        self.bind('<Button-1>', self.add_stones)
        self.AI = AI()
        if self.music:
            pg.mixer.music.play(loops = -1)

    def load_data(self):
        # load music, sound, images
        self.dir = path.dirname(__file__)
        self.click = pg.mixer.Sound(path.join(self.dir, settings.SOUND_FOLDER, 'click.ogg'))
        self.peaceatlast = pg.mixer.music.load(path.join(self.dir, settings.SOUND_FOLDER, 'peaceatlast_piano.ogg'))
        # load images
        Bg = PhotoImage(file = path.join(self.dir, settings.IMAGE_FOLDER, 'Bg.png'))
        self.Bg_image = Bg
        Pause_bg = PhotoImage(file = path.join(self.dir, settings.IMAGE_FOLDER, 'Pause_bg.png'))
        self.Pause_bg = Pause_bg
        Player_btn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Player_btn.png'))
        Player_btn = Player_btn.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Player_btn = ImageTk.PhotoImage(Player_btn)
        Player_btn1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Player_btn1.png'))
        Player_btn1 = Player_btn1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Player_btn1 = ImageTk.PhotoImage(Player_btn1)
        Player_btn2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Player_btn2.png'))
        Player_btn2 = Player_btn2.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Player_btn2 = ImageTk.PhotoImage(Player_btn2)
        Player_btn3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Player_btn3.png'))
        Player_btn3 = Player_btn3.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Player_btn3 = ImageTk.PhotoImage(Player_btn3)
        Player_btn4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Player_btn4.png'))
        Player_btn4 = Player_btn4.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Player_btn4 = ImageTk.PhotoImage(Player_btn4)
        Joueur_btn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Joueur_btn.png'))
        Joueur_btn = Joueur_btn.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Joueur_btn = ImageTk.PhotoImage(Joueur_btn)
        Joueur_btn1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Joueur_btn1.png'))
        Joueur_btn1 = Joueur_btn1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Joueur_btn1 = ImageTk.PhotoImage(Joueur_btn1)
        Joueur_btn2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Joueur_btn2.png'))
        Joueur_btn2 = Joueur_btn2.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Joueur_btn2 = ImageTk.PhotoImage(Joueur_btn2)
        Joueur_btn3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Joueur_btn3.png'))
        Joueur_btn3 = Joueur_btn3.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Joueur_btn3 = ImageTk.PhotoImage(Joueur_btn3)
        Joueur_btn4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Joueur_btn4.png'))
        Joueur_btn4 = Joueur_btn4.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Joueur_btn4 = ImageTk.PhotoImage(Joueur_btn4)
        AI_btn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'AI_btn.png'))
        AI_btn = AI_btn.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.AI_btn = ImageTk.PhotoImage(AI_btn)
        AI_btn1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'AI_btn1.png'))
        AI_btn1 = AI_btn1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.AI_btn1 = ImageTk.PhotoImage(AI_btn1)
        AI_btn2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'AI_btn2.png'))
        AI_btn2 = AI_btn2.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.AI_btn2 = ImageTk.PhotoImage(AI_btn2)
        AI_btn3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'AI_btn3.png'))
        AI_btn3 = AI_btn3.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.AI_btn3 = ImageTk.PhotoImage(AI_btn3)
        AI_btn4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'AI_btn4.png'))
        AI_btn4 = AI_btn4.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.AI_btn4 = ImageTk.PhotoImage(AI_btn4)
        IA_btn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'IA_btn.png'))
        IA_btn = IA_btn.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.IA_btn = ImageTk.PhotoImage(IA_btn)
        IA_btn1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'IA_btn1.png'))
        IA_btn1 = IA_btn1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.IA_btn1 = ImageTk.PhotoImage(IA_btn1)
        IA_btn2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'IA_btn2.png'))
        IA_btn2 = IA_btn2.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.IA_btn2 = ImageTk.PhotoImage(IA_btn2)
        IA_btn3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'IA_btn3.png'))
        IA_btn3 = IA_btn3.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.IA_btn3 = ImageTk.PhotoImage(IA_btn3)
        IA_btn4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'IA_btn4.png'))
        IA_btn4 = IA_btn4.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.IA_btn4 = ImageTk.PhotoImage(IA_btn4)
        English = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'English.png'))
        English = English.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.English = ImageTk.PhotoImage(English)
        English1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'English1.png'))
        English1 = English1.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.English1 = ImageTk.PhotoImage(English1)
        English2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'English2.png'))
        English2 = English2.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.English2 = ImageTk.PhotoImage(English2)
        English3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'English3.png'))
        English3 = English3.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.English3 = ImageTk.PhotoImage(English3)
        English4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'English4.png'))
        English4 = English4.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.English4 = ImageTk.PhotoImage(English4)
        Francais = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Français.png'))
        Francais = Francais.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Francais = ImageTk.PhotoImage(Francais)
        Francais1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Français1.png'))
        Francais1 = Francais1.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Francais1 = ImageTk.PhotoImage(Francais1)
        Francais2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Français2.png'))
        Francais2 = Francais2.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Francais2 = ImageTk.PhotoImage(Francais2)
        Francais3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Français3.png'))
        Francais3 = Francais3.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Francais3 = ImageTk.PhotoImage(Francais3)
        Francais4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Français4.png'))
        Francais4 = Francais4.resize((int(49 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Francais4 = ImageTk.PhotoImage(Francais4)
        Resume = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Resume.png'))
        Resume = Resume.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Resume = ImageTk.PhotoImage(Resume)
        Resume1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Resume1.png'))
        Resume1 = Resume1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Resume1 = ImageTk.PhotoImage(Resume1)
        Resume2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Resume2.png'))
        Resume2 = Resume2.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Resume2 = ImageTk.PhotoImage(Resume2)
        Resume3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Resume3.png'))
        Resume3 = Resume3.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Resume3 = ImageTk.PhotoImage(Resume3)
        Resume4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Resume4.png'))
        Resume4 = Resume4.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Resume4 = ImageTk.PhotoImage(Resume4)
        Continuer = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Continuer.png'))
        Continuer = Continuer.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Continuer = ImageTk.PhotoImage(Continuer)
        Continuer1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Continuer1.png'))
        Continuer1 = Continuer1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Continuer1 = ImageTk.PhotoImage(Continuer1)
        Continuer2 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Continuer2.png'))
        Continuer2 = Continuer2.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Continuer2 = ImageTk.PhotoImage(Continuer2)
        Continuer3 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Continuer3.png'))
        Continuer3 = Continuer3.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Continuer3 = ImageTk.PhotoImage(Continuer3)
        Continuer4 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Continuer4.png'))
        Continuer4 = Continuer4.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Continuer4 = ImageTk.PhotoImage(Continuer4)
        Menu_btn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Menu_btn.png'))
        Menu_btn = Menu_btn.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Menu_btn = ImageTk.PhotoImage(Menu_btn)
        Theme_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme_en.png'))
        Theme_en = Theme_en.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme_en = ImageTk.PhotoImage(Theme_en)
        Theme_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme_fr.png'))
        Theme_fr = Theme_fr.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme_fr = ImageTk.PhotoImage(Theme_fr)
        Theme1 = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme1.png'))
        Theme1 = Theme1.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme1 = ImageTk.PhotoImage(Theme1)
        Theme1_bd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme1_bd.png'))
        Theme1_bd = Theme1_bd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme1_bd = ImageTk.PhotoImage(Theme1_bd)
        Theme2_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme2_en.png'))
        Theme2_en = Theme2_en.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme2_en = ImageTk.PhotoImage(Theme2_en)
        Theme2_enbd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme2_enbd.png'))
        Theme2_enbd = Theme2_enbd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme2_enbd = ImageTk.PhotoImage(Theme2_enbd)
        Theme2_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme2_fr.png'))
        Theme2_fr = Theme2_fr.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme2_fr = ImageTk.PhotoImage(Theme2_fr)
        Theme2_frbd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme2_frbd.png'))
        Theme2_frbd = Theme2_frbd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme2_frbd = ImageTk.PhotoImage(Theme2_frbd)
        Theme3_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme3_en.png'))
        Theme3_en = Theme3_en.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme3_en = ImageTk.PhotoImage(Theme3_en)
        Theme3_enbd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme3_enbd.png'))
        Theme3_enbd = Theme3_enbd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme3_enbd = ImageTk.PhotoImage(Theme3_enbd)
        Theme3_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme3_fr.png'))
        Theme3_fr = Theme3_fr.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme3_fr = ImageTk.PhotoImage(Theme3_fr)
        Theme3_frbd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme3_frbd.png'))
        Theme3_frbd = Theme3_frbd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme3_frbd = ImageTk.PhotoImage(Theme3_frbd)
        Theme4_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme4_en.png'))
        Theme4_en = Theme4_en.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme4_en = ImageTk.PhotoImage(Theme4_en)
        Theme4_enbd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme4_enbd.png'))
        Theme4_enbd = Theme4_enbd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme4_enbd = ImageTk.PhotoImage(Theme4_enbd)
        Theme4_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme4_fr.png'))
        Theme4_fr = Theme4_fr.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme4_fr = ImageTk.PhotoImage(Theme4_fr)
        Theme4_frbd = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Theme4_frbd.png'))
        Theme4_frbd = Theme4_frbd.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Theme4_frbd = ImageTk.PhotoImage(Theme4_frbd)
        Back = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Back.png'))
        Back = Back.resize((int(50 / 2048 * self.SW), int(48 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Back = ImageTk.PhotoImage(Back)
        Fullscreen = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Fullscreen.png'))
        Fullscreen = Fullscreen.resize((int(50 / 2048 * self.SW), int(48 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Fullscreen = ImageTk.PhotoImage(Fullscreen)
        MusicOff = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'MusicOff.png'))
        MusicOff = MusicOff.resize((int(47 / 2048 * self.SW), int(47 / 1152 * self.SH)), Image.ANTIALIAS)
        self.MusicOff = ImageTk.PhotoImage(MusicOff)
        MusicOn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'MusicOn.png'))
        MusicOn = MusicOn.resize((int(47 / 2048 * self.SW), int(47 / 1152 * self.SH)), Image.ANTIALIAS)
        self.MusicOn = ImageTk.PhotoImage(MusicOn)
        SoundOff = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'SoundOff.png'))
        SoundOff = SoundOff.resize((int(47 / 2048 * self.SW), int(47 / 1152 * self.SH)), Image.ANTIALIAS)
        self.SoundOff = ImageTk.PhotoImage(SoundOff)
        SoundOn = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'SoundOn.png'))
        SoundOn = SoundOn.resize((int(47 / 2048 * self.SW), int(47 / 1152 * self.SH)), Image.ANTIALIAS)
        self.SoundOn = ImageTk.PhotoImage(SoundOn)
        Pause = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Pause.png'))
        Pause = Pause.resize((int(110 / 2048 * self.SW), int(48 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Pause = ImageTk.PhotoImage(Pause)
        Rules_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_en.png'))
        Rules_en = Rules_en.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_en = ImageTk.PhotoImage(Rules_en)
        Rules_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_fr.png'))
        Rules_fr = Rules_fr.resize((int(190 / 2048 * self.SW), int(49 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_fr = ImageTk.PhotoImage(Rules_fr)
        Rules_img1_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_img1_fr.png'))
        Rules_img1_fr = Rules_img1_fr.resize((int(1434 / 2048 * self.SW), int(788 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_img1_fr = ImageTk.PhotoImage(Rules_img1_fr)
        Rules_img2_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_img2_fr.png'))
        Rules_img2_fr = Rules_img2_fr.resize((int(1435 / 2048 * self.SW), int(655 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_img2_fr = ImageTk.PhotoImage(Rules_img2_fr)
        Rules_img3_fr = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_img3_fr.png'))
        Rules_img3_fr = Rules_img3_fr.resize((int(1437 / 2048 * self.SW), int(703 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_img3_fr = ImageTk.PhotoImage(Rules_img3_fr)
        Rules_img1_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_img1_en.png'))
        Rules_img1_en = Rules_img1_en.resize((int(1434 / 2048 * self.SW), int(788 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_img1_en = ImageTk.PhotoImage(Rules_img1_en)
        Rules_img2_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_img2_en.png'))
        Rules_img2_en = Rules_img2_en.resize((int(1435 / 2048 * self.SW), int(655 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_img2_en = ImageTk.PhotoImage(Rules_img2_en)
        Rules_img3_en = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Rules_img3_en.png'))
        Rules_img3_en = Rules_img3_en.resize((int(1437 / 2048 * self.SW), int(703 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Rules_img3_en = ImageTk.PhotoImage(Rules_img3_en)
        Save = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Save.png'))
        Save = Save.resize((int(50 / 2048 * self.SW), int(48 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Save = ImageTk.PhotoImage(Save)
        Exit = Image.open(path.join(self.dir, settings.IMAGE_FOLDER, 'Exit.png'))
        Exit = Exit.resize((int(50 / 2048 * self.SW), int(48 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Exit = ImageTk.PhotoImage(Exit)
        # load game files
        try:
            with open(path.join(self.dir, settings.GAME_FILES, settings.BOARD_FILE), 'r') as f:
                self.board = []
                for line in f:
                    self.board.append(list(map(int, line[1:-2].split(','))))
        except:
            self.board = copy.deepcopy(settings.BOARD)
        try:
            with open(path.join(self.dir, settings.GAME_FILES, settings.AUDIO_FILE), 'r') as f:
                r = f.readlines()
                if r[1] == 'self.MusicOff':
                    self.Music = self.MusicOff
                    self.music = False
                if r[1] == 'self.MusicOn':
                    self.Music = self.MusicOn
                    self.music = True
                if r[0] == 'self.SoundOff\n':
                    self.Sound = self.SoundOff
                    self.sound = False
                if r[0] == 'self.SoundOn\n':
                    self.Sound = self.SoundOn
                    self.sound = True
        except:
            self.Music = self.MusicOn
            self.music = True
            self.Sound = self.SoundOn
            self.sound = False
        try:
            with open(path.join(self.dir, settings.GAME_FILES, settings.THEME_FILE), 'r') as f:
                r = f.readlines()
                if r[0] == 'English\n':
                    self.saved_language = str(self.English)
                else: self.saved_language = str(self.Francais)
                self.T = r[1]
        except:
            self.T = 'Theme_en'
            self.saved_language = str(self.English)

    def draw_board(self):
        # draw board, background image
        dim = (self.size_board + 1) * self.delta
        self.create_image(0, 0, image = self.Bg_image, anchor = NW)
        self.create_rectangle(self.delta * .5 / 2048 * self.SW, self.delta * .5 / 1152 * self.SH, (self.size_board + .5) * self.delta / 2048 * self.SW,
                             (self.size_board + .5) * self.delta / 1152 * self.SH, outline = 'forestgreen', fill = 'forestgreen')
        self.create_rectangle(self.delta / 2048 * self.SW, self.delta / 1152 * self.SH, self.size_board * self.delta / 2048 * self.SW, self.size_board * self.delta / 1152 * self.SH,
                              width = 5, outline = 'white')
        self.create_rectangle((self.coord_mid - 2.5 * self.delta) / 2048 * self.SW, (self.coord_mid - 2.5 * self.delta) / 1152 * self.SH,
                              (self.coord_mid + 2.5 * self.delta) / 2048 * self.SW, (self.coord_mid + 2.5 * self.delta) / 1152 * self.SH, outline = 'green3', fill = 'green3')
        for x in range(1, self.size_board):
            self.create_line((x + .5) * self.delta / 2048 * self.SW, self.delta / 1152 * self.SH, (x + .5) * self.delta / 2048 * self.SW, (dim - self.delta) / 1152 * self.SH, fill = 'springgreen2')
        for y in range(1, self.size_board):
            self.create_line(self.delta / 2048 * self.SW, (y + .5) * self.delta / 1152 * self.SH, (dim - self.delta) / 2048 * self.SW, (y + .5) * self.delta / 1152 * self.SH, fill = 'springgreen2')
        for x in range(2, self.size_board):
            self.create_line(x * self.delta / 2048 * self.SW, self.delta / 1152 * self.SH, x * self.delta / 2048 * self.SW, (dim - self.delta) / 1152 * self.SH, width = 2, fill = 'white')
        for y in range(2, self.size_board):
            self.create_line(self.delta / 2048 * self.SW, y * self.delta / 1152 * self.SH, (dim - self.delta) / 2048 * self.SW, y * self.delta / 1152 * self.SH, width = 2, fill = 'white')
        self.create_oval((self.coord_mid - 7) / 2048 * self.SW, (self.coord_mid - 7) / 1152 * self.SH, (self.coord_mid + 7) / 2048 * self.SW, (self.coord_mid + 7) / 1152 * self.SH,
                         width = 2, fill = 'black', outline = 'gray')

    def button_event(self, btn):
        # do smth depending on the button
        try: key_pressed = btn.keysym
        except: key_pressed = None
        if self.sound and not key_pressed:
            self.click.play()
        # rules window
        if btn == str(self.Rules_en) or btn == str(self.Rules_fr):
            if self.english: content = None
            else: content = None
            rules = Toplevel(self.parent)
            rules.overrideredirect(True)
            rules.resizable(0, 0)
            content = f'+{int(250 / 2048 * self.SW)}+{int(150 / 1152 * self.SH)}'
            rules.geometry(content)
            scroll_y = Scrollbar(rules, orient = VERTICAL)
            scroll_y.pack(side = RIGHT, fill = 'y')
            canvas = Canvas(rules, width = int(1470 / 2048 * self.SW), height = int(650 / 1152 * self.SH), scrollregion = (0, 0, 0, 2225 / 1152 * self.SH), yscrollcommand = scroll_y.set, highlightthickness = 0)
            scroll_y.config(command = canvas.yview)
            def scroll(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
            canvas.pack()
            canvas.create_image(0, 0, image = self.Pause_bg, anchor = NW)
            canvas.create_image(0, 1000 / 1152 * self.SH, image = self.Pause_bg, anchor = NW)
            if self.english: content, content1, content2 = self.Rules_img1_en, self.Rules_img2_en, self.Rules_img3_en
            else: content, content1, content2 = self.Rules_img1_fr, self.Rules_img2_fr, self.Rules_img3_fr
            canvas.create_image(735 /  2048 * self.SW, 410 / 1152 * self.SH, image = content, anchor = 'center')
            canvas.create_image(735 /  2048 * self.SW, 1154 / 1152 * self.SH, image = content1, anchor = 'center')
            canvas.create_image(735 /  2048 * self.SW, 1854 / 1152 * self.SH, image = content2, anchor = 'center')
            canvas.bind('<MouseWheel>', scroll)
            exit_btn = Button(rules, image = self.Exit, bd = 0, command = rules.destroy)
            exit_btn.place(x = 1470 / 2048 * self.SW, y = 0, anchor = NE)
        # pause window
        if btn == str(self.Pause):
            self.pause = Toplevel(self.parent)
            self.pause.grab_set()
            self.pause.focus_force()
            self.pause.overrideredirect(True)
            self.pause.resizable(0, 0)
            content = f'+{int(500 / 2048 * self.SW)}+{int(300 / 1152 * self.SH)}'
            self.pause.geometry(content)
            canvas = Canvas(self.pause, width = int(500 / 2048 * self.SW), height = int(300 / 1152 * self.SH), highlightthickness = 0)
            canvas.pack()
            canvas.create_image(0, 0, image = self.Pause_bg, anchor = NW)
            canvas.create_text(100 / 2052 * self.SW, 30 / 1152 * self.SH, text = 'PAUSE', font = ('Japanese Robot', round(20 / 2048 * self.SW)), fill = 'white')
            self.save_btn = Button(self.pause, bd = 0, image = self.Save)
            self.save_btn.place(x = 150 / 2052 * self.SW, y = 120 / 1152 * self.SH, anchor = 'center')
            self.save_btn.config(command = lambda: self.button_event(self.save_btn.cget('image')))
            self.music_pausebtn = Button(self.pause, bd = 0, image = self.Music)
            self.music_pausebtn.place(x = 250 / 2052 * self.SW, y = 120 / 1152 * self.SH, anchor = 'center')
            self.music_pausebtn.config(command = lambda: self.button_event(self.music_pausebtn.cget('image')))
            self.sound_pausebtn = Button(self.pause, bd = 0, image = self.Sound)
            self.sound_pausebtn.place(x = 350 / 2052 * self.SW, y = 120 / 1152 * self.SH, anchor = 'center')
            self.sound_pausebtn.config(command = lambda: self.button_event(self.sound_pausebtn.cget('image')))
            self.menu_btn = Button(self.pause, bd = 0, image = self.Menu_btn)
            self.menu_btn.place(x = 250 / 2048 * self.SW, y = 220 / 1152 * self.SH, anchor = 'center')
            self.menu_btn.config(command = lambda: self.button_event(self.menu_btn.cget('image')))
            exit_btn = Button(self.pause, image = self.Exit, bd = 0, command = self.pause.destroy)
            exit_btn.place(x = 500 / 2048 * self.SW, y = 0, anchor = NE)
        # menu window
        if btn == str(self.Menu_btn):
            try:
                self.menu.deiconify()
                self.pause.destroy()
                self.parent.withdraw()
                self.menu.focus_force()
                self.button_event(str(self.Back))
                self.AI_opp = False
            except:
                try: self.pause.destroy()
                except: pass
                self.parent.withdraw()
                self.menu = Toplevel(self.parent)
                self.menu.overrideredirect(True)
                self.menu.resizable(0, 0)
                self.menu.geometry('+300+100')
                canvas = Canvas(self.menu, width = 1000 / 2048 * self.SW, height = 700 / 1152 * self.SH, highlightthickness = 0)
                canvas.pack()
                canvas.create_image(0, 0, image = self.Pause_bg, anchor = NW)
                canvas.create_text((1000//2) / 2048 * self.SW, 100 / 1152 * self.SH, text = 'PENTE', font = ('Japanese Robot', round(100 / 2048 * self.SW)), fill = 'white')
                canvas.create_text(600 / 2048 * self.SW, 200 / 1152 * self.SH, text = 'Theme:', font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fill = 'white')
                if self.english: content1, content2, content3, content4, content5 = self.Player_btn, self.AI_btn, self.English1, self.Francais, self.Resume
                else: content1, content2, content3, content4, content5 = self.Joueur_btn, self.IA_btn, self.English, self.Francais1, self.Continuer
                self.joueur_btn = Button(self.menu, bd = 0, image = content1)
                self.joueur_btn.place(x = 310 / 2048 * self.SW, y = 300 / 1152 * self.SH, anchor = 'center')
                self.joueur_btn.config(command = lambda: self.button_event(self.joueur_btn.cget('image')))
                self.ia_btn = Button(self.menu, bd = 0, image = content2)
                self.ia_btn.place(x = 310 / 2048 * self.SW, y = 380 / 1152 * self.SH, anchor = 'center')
                self.ia_btn.config(command = lambda: self.button_event(self.ia_btn.cget('image')))
                self.resume = Button(self.menu, bd = 0, image = content5)
                self.resume.place(x = 310 / 2048 * self.SW, y = 460 / 1152 * self.SH, anchor = 'center')
                self.resume.config(command = lambda: self.button_event(self.resume.cget('image')))
                self.en = Button(self.menu, bd = 0, image = content3)
                self.en.place(x = 0, y = 700 / 1152 * self.SH, anchor = SW)
                self.en.config(command = lambda: self.button_event(self.en.cget('image')))
                self.fr = Button(self.menu, bd = 0, image = content4)
                self.fr.place(x = 49 / 2048 * self.SW, y = 700 / 1152 * self.SH, anchor = SW)
                self.fr.config(command = lambda: self.button_event(self.fr.cget('image')))
                if self.english:
                    self.theme = Button(self.menu, image = self.Theme_en, bd = 0)
                    self.theme.place(x = 750 / 2048 * self.SW, y = 260 / 1152 * self.SH, anchor = 'center')
                    self.theme.config(command = lambda: self.button_event(self.theme.cget('image')))
                    self.theme1 = Button(self.menu, image = self.Theme1, bd = 0)
                    self.theme1.place(x = 750 / 2048 * self.SW, y = 340 / 1152 * self.SH, anchor = 'center')
                    self.theme1.config(command = lambda: self.button_event(self.theme1.cget('image')))
                    self.theme2 = Button(self.menu, image = self.Theme2_en, bd = 0)
                    self.theme2.place(x = 750 / 2048 * self.SW, y = 420 / 1152 * self.SH, anchor = 'center')
                    self.theme2.config(command = lambda: self.button_event(self.theme2.cget('image')))
                    self.theme3 = Button(self.menu, image = self.Theme3_en, bd = 0)
                    self.theme3.place(x = 750 / 2048 * self.SW, y = 500 / 1152 * self.SH, anchor = 'center')
                    self.theme3.config(command = lambda: self.button_event(self.theme3.cget('image')))
                    self.theme4 = Button(self.menu, image = self.Theme4_en, bd = 0)
                    self.theme4.place(x = 750 / 2048 * self.SW, y = 580 / 1152 * self.SH, anchor = 'center')
                    self.theme4.config(command = lambda: self.button_event(self.theme4.cget('image')))
                else:
                    self.theme = Button(self.menu, image = self.Theme_fr, bd = 0)
                    self.theme.place(x = 300 / 2048 * self.SW, y = 500 / 1152 * self.SH, anchor = 'center')
                    self.theme.config(command = lambda: self.button_event(self.theme.cget('image')))
                    self.theme1 = Button(self.menu, image = self.Theme1, bd = 0)
                    self.theme1.place(x = 500 / 2048 * self.SW, y = 500 / 1152 * self.SH, anchor = 'center')
                    self.theme1.config(command = lambda: self.button_event(self.theme1.cget('image')))
                    self.theme2 = Button(self.menu, image = self.Theme2_fr, bd = 0)
                    self.theme2.place(x = 700 / 2048 * self.SW, y = 500 / 1152 * self.SH, anchor = 'center')
                    self.theme2.config(command = lambda: self.button_event(self.theme2.cget('image')))
                    self.theme3 = Button(self.menu, image = self.Theme3_fr, bd = 0)
                    self.theme3.place(x = 400 / 2048 * self.SW, y = 570 / 1152 * self.SH, anchor = 'center')
                    self.theme3.config(command = lambda: self.button_event(self.theme3.cget('image')))
                    self.theme4 = Button(self.menu, image = self.Theme4_fr, bd = 0)
                    self.theme4.place(x = 600 / 2048 * self.SW, y = 570 / 1152 * self.SH, anchor = 'center')
                    self.theme4.config(command = lambda: self.button_event(self.theme4.cget('image')))
                exit_btn = Button(self.menu, image = self.Exit, bd = 0, command = self.parent.destroy)
                exit_btn.place(x = 1000 / 2048 * self.SW, y = 0, anchor = NE)
                self.button_event(self.T)
                self.button_event(self.saved_language)
                self.menu.mainloop()
        # play against another player localy
        if btn == str(self.Player_btn) or btn == str(self.Player_btn1) or \
           btn == str(self.Player_btn2) or btn == str(self.Player_btn3) or btn == str(self.Player_btn4):
            self.menu.withdraw()
            self.parent.deiconify()
            self.parent.focus_force()
            self.parent.grab_set()
            self.board = copy.deepcopy(settings.BOARD)
            self.button_event(str(self.Back))
            self.draw_text()
        if btn == str(self.Joueur_btn) or btn == str(self.Joueur_btn1) or \
           btn == str(self.Joueur_btn2) or btn == str(self.Joueur_btn3) or btn == str(self.Joueur_btn4):
            self.button_event(str(self.Player_btn))
        # play against an AI
        if btn == str(self.AI_btn) or btn == str(self.AI_btn1) or \
           btn == str(self.AI_btn2) or btn == str(self.AI_btn3) or btn == str(self.AI_btn3):
            self.AI_opp = True
            self.button_event(str(self.Player_btn))
        if btn == str(self.IA_btn) or btn == str(self.IA_btn1) or \
           btn == str(self.IA_btn2) or btn == str(self.IA_btn3) or btn == str(self.IA_btn3):
            self.button_event(str(self.AI_btn))
        # resume saved game
        if btn == str(self.Resume) or btn == str(self.Resume1) or \
           btn == str(self.Resume2) or btn == str(self.Resume3) or btn == str(self.Resume4):
            try:
                with open(path.join(self.dir, settings.GAME_FILES, settings.BOARD_FILE), 'r') as f:
                    self.board = []
                    for line in f:
                        self.board.append(list(map(int, line[1:-2].split(','))))
                with open(path.join(self.dir, settings.GAME_FILES, settings.SAVED_GAME), 'r') as f:
                    r = f.readlines()
                    self.last_piece_pos[0] = int(r[0][:-1])
                    self.last_piece_pos[1] = int(r[1][:-1])
                    self.capture_count[0] = int(r[2][:-1])
                    self.capture_count[1] = int(r[3])

            except:
                self.board = copy.deepcopy(settings.BOARD)
            for m in range(len(self.board)):
                for n in range(len(self.board[m])):
                    if self.board[m][n] != 0:
                        self.stone_number += 1
            if settings.CLR_STONE != self.color_stone:
                self.color_stone.reverse()
                self.stone_number += 1
            for m in range(len((self.board))):
                for n in range(len(self.board[m])):
                    if self.board[m][n] == 1:
                        id = self.create_oval((n + 1) * self.delta - self.size_stone, (m + 1) * self.delta - self.size_stone,
                             (n + 1) * self.delta + self.size_stone, (m + 1) * self.delta + self.size_stone, width = 0, fill = self.color_stone[0])
                        self.dictionary[(n, m)] = str(id)
                    if self.board[m][n] == 2:
                        id = self.create_oval((n + 1) * self.delta - self.size_stone, (m + 1) * self.delta - self.size_stone,
                             (n + 1) * self.delta + self.size_stone, (m + 1) * self.delta + self.size_stone, width = 0, fill = self.color_stone[1])
                        self.dictionary[(n, m)] = str(id)
            self.menu.withdraw()
            self.parent.deiconify()
            self.parent.focus_force()
            self.parent.grab_set()
            self.capture_dic['1'], self.capture_dic['2'] = self.capture_count[0], self.capture_count[1]
            if len(self.dictionary) > 3:
                self.check_win(self.last_piece_pos[1], self.last_piece_pos[0])
            self.draw_text()
        if btn == str(self.Continuer) or btn == str(self.Continuer1) or \
           btn == str(self.Continuer2) or btn == str(self.Continuer3) or btn == str(self.Continuer4):
            self.button_event(str(self.Resume))
        # change theme
        if btn == str(self.Theme_en) or btn == 'Theme_en':
            settings.CLR_STONE = ['white', 'black']
            self.color_stone = ['white', 'black']
            self.en.config(image = self.English1)
            self.joueur_btn.config(image = self.Player_btn)
            self.ia_btn.config(image = self.AI_btn)
            self.resume.config(image = self.Resume)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_en)
            self.theme3.config(image = self.Theme3_en)
            self.theme4.config(image = self.Theme4_en)
            self.T = 'Theme_en'
        if btn == str(self.Theme_fr) or btn == 'Theme_fr':
            settings.CLR_STONE = ['white', 'black']
            self.color_stone = ['white', 'black']
            self.fr.config(image = self.Francais1)
            self.joueur_btn.config(image = self.Joueur_btn)
            self.ia_btn.config(image = self.IA_btn)
            self.resume.config(image = self.Continuer)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_fr)
            self.theme3.config(image = self.Theme3_fr)
            self.theme4.config(image = self.Theme4_fr)
            self.T = 'Theme_fr'
        if btn == str(self.Theme1) or btn == 'Theme1':
            settings.CLR_STONE = ['orange2', 'orange red']
            self.color_stone = ['orange2', 'orange red']
            self.T = 'Theme1'
            if self.english:
                self.en.config(image = self.English1)
                self.joueur_btn.config(image = self.Player_btn1)
                self.ia_btn.config(image = self.AI_btn1)
                self.resume.config(image = self.Resume1)
                self.theme1.config(image = self.Theme1_bd)
                self.theme2.config(image = self.Theme2_en)
                self.theme3.config(image = self.Theme3_en)
                self.theme4.config(image = self.Theme4_en)
            else:
                self.fr.config(image = self.Francais1)
                self.joueur_btn.config(image = self.Joueur_btn1)
                self.ia_btn.config(image = self.IA_btn1)
                self.resume.config(image = self.Continuer1)
                self.theme1.config(image = self.Theme1_bd)
                self.theme2.config(image = self.Theme2_fr)
                self.theme3.config(image = self.Theme3_fr)
                self.theme4.config(image = self.Theme4_fr)
        if btn == str(self.Theme2_en) or btn == 'Theme2_en':
            settings.CLR_STONE = ['cyan', 'medium blue']
            self.color_stone = ['cyan', 'medium blue']
            self.en.config(image = self.English2)
            self.joueur_btn.config(image = self.Player_btn2)
            self.ia_btn.config(image = self.AI_btn2)
            self.resume.config(image = self.Resume2)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_enbd)
            self.theme3.config(image = self.Theme3_en)
            self.theme4.config(image = self.Theme4_en)
            self.T = 'Theme2_en'
        if btn == str(self.Theme2_fr) or btn == 'Theme2_fr':
            settings.CLR_STONE = ['cyan', 'medium blue']
            self.color_stone = ['cyan', 'medium blue']
            self.fr.config(image = self.Francais2)
            self.joueur_btn.config(image = self.Joueur_btn2)
            self.ia_btn.config(image = self.IA_btn2)
            self.resume.config(image = self.Continuer2)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_frbd)
            self.theme3.config(image = self.Theme3_fr)
            self.theme4.config(image = self.Theme4_fr)
            self.T = 'Theme2_fr'
        if btn == str(self.Theme3_en) or btn == 'Theme3_en':
            settings.CLR_STONE = ['OliveDrab1', 'dark green']
            self.color_stone = ['OliveDrab1', 'dark green']
            self.en.config(image = self.English3)
            self.joueur_btn.config(image = self.Player_btn3)
            self.ia_btn.config(image = self.AI_btn3)
            self.resume.config(image = self.Resume3)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_en)
            self.theme3.config(image = self.Theme3_enbd)
            self.theme4.config(image = self.Theme4_en)
            self.T = 'Theme3_en'
        if btn == str(self.Theme3_fr) or btn == 'Theme3_fr':
            settings.CLR_STONE = ['OliveDrab1', 'dark green']
            self.color_stone = ['OliveDrab1', 'dark green']
            self.fr.config(image = self.Francais3)
            self.joueur_btn.config(image = self.Joueur_btn3)
            self.ia_btn.config(image = self.IA_btn3)
            self.resume.config(image = self.Continuer3)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_fr)
            self.theme3.config(image = self.Theme3_frbd)
            self.theme4.config(image = self.Theme4_fr)
            self.T = 'Theme3_fr'
        if btn == str(self.Theme4_en) or btn == 'Theme4_en':
            settings.CLR_STONE = ['yellow', 'DarkGoldenrod1']
            self.color_stone = ['yellow', 'DarkGoldenrod1']
            self.en.config(image = self.English4)
            self.joueur_btn.config(image = self.Player_btn4)
            self.ia_btn.config(image = self.AI_btn4)
            self.resume.config(image = self.Resume4)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_en)
            self.theme3.config(image = self.Theme3_en)
            self.theme4.config(image = self.Theme4_enbd)
            self.T = 'Theme4_en'
        if btn == str(self.Theme4_fr) or btn == 'Theme4_fr':
            settings.CLR_STONE = ['yellow', 'DarkGoldenrod1']
            self.color_stone = ['yellow', 'DarkGoldenrod1']
            self.fr.config(image = self.Francais4)
            self.joueur_btn.config(image = self.Joueur_btn4)
            self.ia_btn.config(image = self.IA_btn4)
            self.resume.config(image = self.Continuer4)
            self.theme1.config(image = self.Theme1)
            self.theme2.config(image = self.Theme2_fr)
            self.theme3.config(image = self.Theme3_fr)
            self.theme4.config(image = self.Theme4_frbd)
            self.T = 'Theme4_fr'
        # change language to english
        if btn == str(self.English):
            self.english = True
            self.fr.config(image = self.Francais)
            self.draw_text()
            self.black_btn.config(text = 'Play as black')
            self.white_btn.config(text = 'Play as white')
            self.rules_btn.config(image = self.Rules_en)
            if self.T == 'Theme_en' or self.T == 'Theme_fr':
                self.en.config(image = self.English1)
                self.joueur_btn.config(image = self.Player_btn)
                self.ia_btn.config(image = self.AI_btn)
                self.resume.config(image = self.Resume)
                self.theme.config(image = self.Theme_en)
                self.theme2.config(image = self.Theme2_en)
                self.theme3.config(image = self.Theme3_en)
                self.theme4.config(image = self.Theme4_en)
            if self.T == 'Theme1':
                self.en.config(image = self.English1)
                self.joueur_btn.config(image = self.Player_btn1)
                self.ia_btn.config(image = self.AI_btn1)
                self.resume.config(image = self.Resume1)
                self.theme.config(image = self.Theme_en)
                self.theme2.config(image = self.Theme2_en)
                self.theme3.config(image = self.Theme3_en)
                self.theme4.config(image = self.Theme4_en)
            if self.T == 'Theme2_en' or self.T == 'Theme2_fr':
                self.en.config(image = self.English2)
                self.joueur_btn.config(image = self.Player_btn2)
                self.ia_btn.config(image = self.AI_btn2)
                self.resume.config(image = self.Resume2)
                self.theme.config(image = self.Theme_en)
                self.theme2.config(image = self.Theme2_enbd)
                self.theme3.config(image = self.Theme3_en)
                self.theme4.config(image = self.Theme4_en)
            if self.T == 'Theme3_en' or self.T == 'Theme3_fr':
                self.en.config(image = self.English3)
                self.joueur_btn.config(image = self.Player_btn3)
                self.ia_btn.config(image = self.AI_btn3)
                self.resume.config(image = self.Resume3)
                self.theme.config(image = self.Theme_en)
                self.theme2.config(image = self.Theme2_en)
                self.theme3.config(image = self.Theme3_enbd)
                self.theme4.config(image = self.Theme4_en)
            if self.T == 'Theme4_en' or self.T == 'Theme4_fr':
                self.en.config(image = self.English4)
                self.joueur_btn.config(image = self.Player_btn4)
                self.ia_btn.config(image = self.AI_btn4)
                self.resume.config(image = self.Resume4)
                self.theme.config(image = self.Theme_en)
                self.theme2.config(image = self.Theme2_en)
                self.theme3.config(image = self.Theme3_en)
                self.theme4.config(image = self.Theme4_enbd)
        # change language to french
        if btn == str(self.Francais):
            self.english = False
            self.en.config(image = self.English)
            self.draw_text()
            self.black_btn.config(text = 'Jouer en noir')
            self.white_btn.config(text = 'Jouer en blanc')
            self.rules_btn.config(image = self.Rules_fr)
            if self.T == 'Theme_en' or self.T == 'Theme_fr':
                self.fr.config(image = self.Francais1)
                self.joueur_btn.config(image = self.Joueur_btn)
                self.ia_btn.config(image = self.IA_btn)
                self.resume.config(image = self.Continuer)
                self.theme.config(image = self.Theme_fr)
                self.theme1.config(image = self.Theme1)
                self.theme2.config(image = self.Theme2_fr)
                self.theme3.config(image = self.Theme3_fr)
                self.theme4.config(image = self.Theme4_fr)
            if self.T == 'Theme1':
                self.fr.config(image = self.Francais1)
                self.joueur_btn.config(image = self.Joueur_btn1)
                self.ia_btn.config(image = self.IA_btn1)
                self.resume.config(image = self.Continuer1)
                self.theme.config(image = self.Theme_fr)
                self.theme1.config(image = self.Theme1_bd)
                self.theme2.config(image = self.Theme2_fr)
                self.theme3.config(image = self.Theme3_fr)
                self.theme4.config(image = self.Theme4_fr)
            if self.T == 'Theme2_en' or self.T == 'Theme2_fr':
                self.fr.config(image = self.Francais2)
                self.joueur_btn.config(image = self.Joueur_btn2)
                self.ia_btn.config(image = self.IA_btn2)
                self.resume.config(image = self.Continuer2)
                self.theme.config(image = self.Theme_fr)
                self.theme1.config(image = self.Theme1)
                self.theme2.config(image = self.Theme2_frbd)
                self.theme3.config(image = self.Theme3_fr)
                self.theme4.config(image = self.Theme4_fr)
            if self.T == 'Theme3_en' or self.T == 'Theme3_fr':
                self.fr.config(image = self.Francais3)
                self.joueur_btn.config(image = self.Joueur_btn3)
                self.ia_btn.config(image = self.IA_btn3)
                self.resume.config(image = self.Continuer3)
                self.theme.config(image = self.Theme_fr)
                self.theme1.config(image = self.Theme1)
                self.theme2.config(image = self.Theme2_fr)
                self.theme3.config(image = self.Theme3_frbd)
                self.theme4.config(image = self.Theme4_fr)
            if self.T == 'Theme4_en' or self.T == 'Theme4_fr':
                self.fr.config(image = self.Francais4)
                self.joueur_btn.config(image = self.Joueur_btn4)
                self.ia_btn.config(image = self.IA_btn4)
                self.resume.config(image = self.Continuer4)
                self.theme.config(image = self.Theme_fr)
                self.theme1.config(image = self.Theme1)
                self.theme2.config(image = self.Theme2_fr)
                self.theme3.config(image = self.Theme3_fr)
                self.theme4.config(image = self.Theme4_frbd)
        # first player play as black
        if btn == 'Jouer en noir' or btn == 'Play as black':
            if self.color_stone[0] == settings.CLR_STONE[0]:
                self.color_stone.reverse()
            self.button_event(str(self.Back))
        # first player play-  as white
        if btn == 'Jouer en blanc' or btn == 'Play as white':
            if self.color_stone[0] == settings.CLR_STONE[1]:
                self.color_stone.reverse()
            self.button_event(str(self.Back))
        # play music on the background
        if btn == str(self.MusicOn):
            self.Music = self.MusicOff
            self.music_btn.config(image = self.Music)
            try: self.music_pausebtn.config(image = self.Music)
            except: pass
            self.music = False
            pg.mixer.music.fadeout(500)
        # mute the music
        if btn == str(self.MusicOff):
            self.Music = self.MusicOn
            self.music_btn.config(image = self.Music)
            try: self.music_pausebtn.config(image = self.Music)
            except: pass
            self.music = True
            pg.mixer.music.play(loops = -1)
        # play sound on button clicked
        if btn == str(self.SoundOn):
            self.Sound = self.SoundOff
            self.sound_btn.config(image = self.Sound)
            try: self.sound_pausebtn.config(image = self.Sound)
            except: pass
            self.sound = False
        # mute buttons sound
        if btn == str(self.SoundOff):
            self.Sound = self.SoundOn
            self.sound_btn.config(image = self.Sound)
            try: self.sound_pausebtn.config(image = self.Sound)
            except: pass
            self.sound = True
        # erase pawns
        if btn == str(self.Back):
            self.bind('<Button-1>', self.add_stones)
            self.game_over = False
            for m in self.dictionary:
                self.delete(self.dictionary[m])
            self.stone_number = 0
            self.board = copy.deepcopy(settings.BOARD)
            self.dictionary = copy.deepcopy(settings.DICTIONARY)
            self.capture_dic = copy.deepcopy(settings.CAPTURE_DIC)
            self.capture_count =  [0, 0]
            self.last_piece_pos = [9, 9]
            self.draw_text()
        # toggle fullscreen
        if btn == str(self.Fullscreen) or key_pressed == 'F11':
            if self.state:
                self.parent.attributes('-fullscreen', False)
                self.state = not self.state
            else:
                self.parent.attributes('-fullscreen', True)
                self.state = not self.state
        # save the game
        if btn == str(self.Save):
            with open(path.join(self.dir, settings.GAME_FILES, settings.BOARD_FILE), 'w') as f:
                for i  in range(len(self.board)):
                    f.write(str(self.board[i]) + '\n')
            with open(path.join(self.dir, settings.GAME_FILES, settings.SAVED_GAME), 'w') as f:
                f.write(str(self.last_piece_pos[0]) + '\n')
                f.write(str(self.last_piece_pos[1]) + '\n')
                f.write(str(self.capture_count[0]) + '\n')
                f.write(str(self.capture_count[1]))
        # save sound and music settings
        with open(path.join(self.dir, settings.GAME_FILES, settings.AUDIO_FILE), 'w') as f:
            if self.sound and self.music:
                f.write('self.SoundOn' + '\n' + 'self.MusicOn')
            if not self.sound and self.music:
                f.write('self.SoundOff' + '\n' + 'self.MusicOn')
            if self.sound and not self.music:
                f.write('self.SoundOn' + '\n' + 'self.MusicOff')
            if not self.sound and not self.music:
                f.write('self.SoundOff' + '\n' + 'self.MusicOff')
        # save language and theme
        with open(path.join(self.dir, settings.GAME_FILES, settings.THEME_FILE), 'w') as f:
            if self.english: f.write('English' + '\n')
            else: f.write('Francais' + '\n')
            f.write(str(self.T))

    def button_layout(self):
        # add game buttons
        if self.english: content1, content2, content3 = 'Play as black', 'Play as white', self.Rules_en
        else: content1, content2, content3 = 'Jouer en noir', 'Jouer en blanc', self.Rules_fr
        self.black_btn = Button(self, text = content1, font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fg = 'white', bg = 'gray30', bd = 1, width = 20)
        self.black_btn.place(x = 1250 / 2048 * self.SW, y = 250 / 1152 * self.SH, anchor = 'center')
        self.black_btn.config(command = lambda: self.button_event(self.black_btn.cget('text')))
        self.white_btn = Button(self, text = content2, font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fg = 'black', bg ='white', bd = 1, width = 20,
                                activebackground = 'gray30', activeforeground = 'white')
        self.white_btn.place(x = 1250 / 2048 * self.SW, y = 320 / 1152 * self.SH, anchor = 'center')
        self.white_btn.config(command = lambda: self.button_event(self.white_btn.cget('text')))
        self.pause_btn = Button(self, bd = 0, image = self.Pause)
        self.pause_btn.place(x = 1200 / 2048 * self.SW, y = 700 / 1152 * self.SH, anchor = 'center')
        self.pause_btn.config(command = lambda: self.button_event(self.pause_btn.cget('image')))
        self.back_btn = Button(self, bd = 0, image = self.Back)
        self.back_btn.place(x = 1325 / 2048 * self.SW, y = 700 / 1152 * self.SH, anchor = 'center')
        self.back_btn.config(command = lambda: self.button_event(self.back_btn.cget('image')))
        self.music_btn = Button(self, bd = 0, image = self.Music)
        self.music_btn.place(x = 1150 / 2048 * self.SW, y = 800 / 1152 * self.SH, anchor = 'center')
        self.music_btn.config(command = lambda: self.button_event(self.music_btn.cget('image')))
        self.sound_btn = Button(self, bd = 0, image = self.Sound)
        self.sound_btn.place(x = 1250 / 2048 * self.SW, y = 800 / 1152 * self.SH, anchor = 'center')
        self.sound_btn.config(command = lambda: self.button_event(self.sound_btn.cget('image')))
        self.fullscreen_btn = Button(self, bd = 0, image = self.Fullscreen)
        self.fullscreen_btn.place(x = 1350 / 2048 * self.SW, y = 800 / 1152 * self.SH, anchor = 'center')
        self.fullscreen_btn.config(command = lambda: self.button_event(self.fullscreen_btn.cget('image')))
        self.rules_btn = Button(self, bd = 0, image = content3)
        self.rules_btn.place(x = 1250 / 2048 * self.SW, y = 900 / 1152 * self.SH, anchor = 'center')
        self.rules_btn.config(command = lambda: self.button_event(self.rules_btn.cget('image')))

    def draw_text(self):
        # add game text
        self.create_text(1250 / 2048 * self.SW, 100 / 1152 * self.SH, text = 'PENTE', font = ('Japanese Robot', round(60 / 2048 * self.SW)), fill = 'white')
        if self.english: content = 'Player:'
        else: content = 'Joueur:'
        try: self.delete(self.dictionary['player'])
        except: pass
        self.dictionary['player'] = self.create_text(1200 / 2048 * self.SW, 400 / 1152 * self.SH, text = content, font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fill = 'white')
        self.dictionary['player_color'] = self.create_oval((1280 - self.size_stone) / 2048 * self.SW, (400 - self.size_stone) / 1152 * self.SH,
            (1280 + self.size_stone) / 2048 * self.SW, (400 + self.size_stone) / 1152 * self.SH, width = 0, fill = self.color_stone[self.stone_number % 2])
        if self.english: content = f"whites ({self.capture_dic['1']}) vs blacks ({self.capture_dic['2']})"
        else : content = f"blancs ({self.capture_dic['1']}) vs noirs ({self.capture_dic['2']})"
        try: self.delete(self.dictionary['nb_points'])
        except: pass
        self.dictionary['nb_points'] = self.create_text(1250 / 2048 * self.SW, 500 / 1152 * self.SH, text = content, font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fill = 'white')

    def getCoordJeu(self, pos):
        # pixel coord to game coord
        x = round(pos[0] / self.delta) * self.delta
        y = round(pos[1] / self.delta) * self.delta
        return x, y

    def get_smaller_board(self, board):
        # get a smaller board for the minimax algorithm
        (diff_x, diff_y) = (9, 9)
        distance = 0
        for m in range(len(self.board)):
            for n in range(len(self.board[m])):
                if self.board[n][m] != 0 and ((m - 9) ** 2 + (n - 9) ** 2) ** .5 > distance:
                    (diff_x, diff_y) = (m, n)
                    distance = ((m - 9) ** 2 + (n - 9) ** 2) ** .5
        self.diff = max(abs(diff_x - 9), abs(diff_y - 9))
        if self.diff % 2 == 0: self.diff += 3
        else: self.diff += 2
        self.diff = self.diff * 2 + 1
        board = [[0 for i in range(self.diff)] for i in range(self.diff)]
        for m in range(9 - self.diff // 2, 9 + self.diff // 2):
            for n in range(9 - self.diff // 2, 9 + self.diff // 2):
                board[n - (9 - self.diff // 2)][m - (9 - self.diff // 2)] = self.board[n][m]
        return board

    def add_stones(self, event):
        # add stones to the board
        pos = event.x, event.y
        x, y = self.getCoordJeu(pos)
        if self.is_valid_move(x, y):
            if self.sound: self.click.play()
            id = self.create_oval(x - self.size_stone, y - self.size_stone, x + self.size_stone, y + self.size_stone,
                 width = 0, fill = self.color_stone[(self.stone_number - 1) % 2])
            self.dictionary[(x // self.delta - 1, y // self.delta - 1)] = str(id)
            self.last_piece_pos = [x // self.delta - 1, y // self.delta - 1]
            if self.color_stone[(self.stone_number - 1) % 2] == settings.CLR_STONE[0]:
                self.board[y // self.delta - 1][x // self.delta - 1] = 1
            else:
                self.board[y // self.delta - 1][x // self.delta - 1] = 2
            self.check_win(y // self.delta - 1, x // self.delta - 1)
            self.capture_count = [self.capture_dic['1'], self.capture_dic['2']]
            self.draw_text()
            if self.AI_opp and not self.game_over: self.add_AI_stones()

    def add_AI_stones(self):
        self.unbind('<Button-1>')
        pos, minimax_score = self.AI.minimax(self.get_smaller_board(self.board), 2, -math.inf, math.inf, True)
        x, y = pos[0] + (self.size_board - self.diff) // 2, pos[1] + (self.size_board - self.diff) // 2
        x, y = (x + 1) * self.delta, (y + 1) * self.delta
        if self.is_valid_move(x, y):
            id = self.create_oval(x - self.size_stone, y - self.size_stone, x + self.size_stone, y + self.size_stone,
                 width = 0, fill = self.color_stone[(self.stone_number - 1) % 2])
            self.dictionary[(x // self.delta - 1, y // self.delta - 1)] = str(id)
            self.last_piece_pos = [x // self.delta - 1, y // self.delta - 1]
            if self.color_stone[(self.stone_number - 1) % 2] == settings.CLR_STONE[0]:
                self.board[y // self.delta - 1][x // self.delta - 1] = 1
            else:
                self.board[y // self.delta - 1][x // self.delta - 1] = 2
            self.check_win(y // self.delta - 1, x // self.delta - 1)
            self.capture_count = [self.capture_dic['1'], self.capture_dic['2']]
            self.draw_text()
            self.bind('<Button-1>', self.add_stones)

    def is_valid_move(self, x, y):
        # check if stone position is valid
        self.stone_number = 1
        for m in range(len(self.board)):
            for n in range(len(self.board[m])):
                if self.board[m][n] != 0:
                    self.stone_number += 1
        # check if stone is in board size
        if not x in range(1, (self.size_board + 1) * self.delta) or not y in range(1, (self.size_board + 1) * self.delta):
            return False
        # check if first stone in center
        if self.stone_number == 1 and not (x, y) == ((self.size_board // 2 + 1) * self.delta, (self.size_board // 2 +1) * self.delta):
            return False
        # check if 3rd stone outside of square
        if self.stone_number == 3 and self.coord_mid - 2.5 * self.delta < x < self.coord_mid + 2.5 * self.delta and self.coord_mid - 2.5 * self.delta < y < self.coord_mid + 2.5 * self.delta:
            return False
        # check if placement on another stone
        if self.board[y // self.delta - 1][x // self.delta - 1] != 0:
            return False
        else: return True

    def check_win(self, x, y):
        # check win method
        checks = [self.check_capture_horizontal(x, y), self.check_capture_vertical(x, y), self.check_capture_diagonal(x, y),
                  self.check_alignment_horizontal(x, y), self.check_alignment_vertical(x, y), self.check_alignment_diagonal(x, y)]
        if any(checks):
            self.game_over = True
            self.unbind('<Button-1>')
            if self.english:
                if self.color_stone[(self.stone_number - 1) % 2] == settings.CLR_STONE[0]:
                    content = 'whites win'
                else: content = 'blacks win'
            else:
                if self.color_stone[(self.stone_number - 1) % 2] == settings.CLR_STONE[0]:
                    content = 'les blancs gagnent'
                else: content = 'les noirs gagnent'
            id = self.create_text(1250 / 2048 * self.SW, 600 / 1152 * self.SH, text = content, font = ('Korean Calligraphy', round(30 / 2048 * self.SW)), fill = 'red')
            self.dictionary['win_msg'] = str(id)
        elif self.stone_number == self.size_board ** 2:
            self.game_over = True
            if self.english:
                content = 'Draw !'
            else:
                content = 'Egalite !'
            id = self.create_text(1250 / 2048 * self.SW, 600 / 1152 * self.SH, text = content, font = ('Korean Calligraphy', round(30 / 2048 * self.SW)), fill = 'red')
            self.dictionary['win_msg'] = str(id)

    def check_capture_horizontal(self, x, y):
        # check capture horizontal
        checker = self.board[x][y]
        if y + 3 < len(self.board) and checker == self.board[x][y + 3]:
            if checker != self.board[x][y + 1] and checker != self.board[x][y + 2]:
                if (y + 1, x) in self.dictionary and (y + 2, x) in self.dictionary:
                    self.delete(self.dictionary[(y + 1, x)])
                    self.delete(self.dictionary[(y + 2, x)])
                    del self.dictionary[(y + 1, x)]
                    del self.dictionary[(y + 2, x)]
                    self.board[x][y + 1] = 0
                    self.board[x][y + 2] = 0
                    self.capture_dic[str(checker)] += 1
        if y - 3 < len(self.board) and checker == self.board[x][y - 3]:
            if checker != self.board[x][y - 1] and checker != self.board[x][y - 2]:
                if (y - 1, x) in self.dictionary and (y - 2, x) in self.dictionary:
                    self.delete(self.dictionary[(y - 1, x)])
                    self.delete(self.dictionary[(y - 2, x)])
                    del self.dictionary[(y - 1, x)]
                    del self.dictionary[(y - 2, x)]
                    self.board[x][y - 1] = 0
                    self.board[x][y - 2] = 0
                    self.capture_dic[str(checker)] += 1
        return self.capture_dic[str(checker)] >= 5

    def check_capture_vertical(self, x, y):
        # check capture vertical
        checker = self.board[x][y]
        if x + 3 < len(self.board) and checker == self.board[x + 3][y]:
            if checker != self.board[x + 1][y] and checker != self.board[x + 2][y]:
                if (y, x + 1) in self.dictionary and (y, x + 2) in self.dictionary:
                    self.delete(self.dictionary[(y, x + 1)])
                    self.delete(self.dictionary[(y, x + 2)])
                    del self.dictionary[(y, x + 1)]
                    del self.dictionary[(y, x + 2)]
                    self.board[x + 1][y] = 0
                    self.board[x + 2][y] = 0
                    self.capture_dic[str(checker)] += 1
        if x - 3 < len(self.board) and checker == self.board[x - 3][y]:
            if checker != self.board[x - 1][y] and checker != self.board[x - 2][y]:
                if (y, x - 1) in self.dictionary and (y, x - 2) in self.dictionary:
                    self.delete(self.dictionary[(y, x - 1)])
                    self.delete(self.dictionary[(y, x - 2)])
                    del self.dictionary[(y, x - 1)]
                    del self.dictionary[(y, x - 2)]
                    self.board[x - 1][y] = 0
                    self.board[x - 2][y] = 0
                    self.capture_dic[str(checker)] += 1
        return self.capture_dic[str(checker)] >= 5

    def check_capture_diagonal(self, x, y):
        # check capture diagonal
        checker = self.board[x][y]
        if x + 3 < len(self.board) and y + 3 < len(self.board) and checker == self.board[x + 3][y + 3]:
            if checker != self.board[x + 1][y + 1] and checker != self.board[x + 2][y + 2]:
                if (y + 1, x + 1) in self.dictionary and (y + 2, x + 2) in self.dictionary:
                    self.delete(self.dictionary[(y + 1, x + 1)])
                    self.delete(self.dictionary[(y + 2, x + 2)])
                    del self.dictionary[(y + 1, x + 1)]
                    del self.dictionary[(y + 2, x + 2)]
                    self.board[x + 1][y + 1] = 0
                    self.board[x + 2][y + 2] = 0
                    self.capture_dic[str(checker)] += 1
        if x - 3 >= 0 and y - 3 >= 0 and checker == self.board[x - 3][y - 3]:
            if checker != self.board[x - 1][y - 1] and checker != self.board[x - 2][y - 2]:
                if (y - 1, x - 1) in self.dictionary and (y - 2, x - 2) in self.dictionary:
                    self.delete(self.dictionary[(y - 1, x - 1)])
                    self.delete(self.dictionary[(y - 2, x - 2)])
                    del self.dictionary[(y - 1, x - 1)]
                    del self.dictionary[(y - 2, x - 2)]
                    self.board[x - 1][y - 1] = 0
                    self.board[x - 2][y - 2] = 0
                    self.capture_dic[str(checker)] += 1
        if x + 3 < len(self.board) and y - 3 >= 0 and checker == self.board[x + 3][y - 3]:
            if checker != self.board[x + 1][y - 1] and checker != self.board[x + 2][y - 2]:
                if (y - 1, x + 1) in self.dictionary and (y - 2, x + 2) in self.dictionary:
                    self.delete(self.dictionary[(y - 1, x + 1)])
                    self.delete(self.dictionary[(y - 2, x + 2)])
                    del self.dictionary[(y - 1, x + 1)]
                    del self.dictionary[(y - 2, x + 2)]
                    self.board[x + 1][y - 1] = 0
                    self.board[x + 2][y - 2] = 0
                    self.capture_dic[str(checker)] += 1
        if x - 3 >= 0 and y + 3 < len(self.board) and checker == self.board[x - 3][y + 3]:
            if checker != self.board[x - 1][y + 1] and checker != self.board[x - 2][y + 2]:
                if (y + 1, x - 1) in self.dictionary and (y + 2, x - 2) in self.dictionary:
                    self.delete(self.dictionary[(y + 1, x - 1)])
                    self.delete(self.dictionary[(y + 2, x - 2)])
                    del self.dictionary[(y + 1, x - 1)]
                    del self.dictionary[(y + 2, x - 2)]
                    self.board[x - 1][y + 1] = 0
                    self.board[x - 2][y + 2] = 0
                    self.capture_dic[str(checker)] += 1
        return self.capture_dic[str(checker)] >= 5

    def check_alignment_horizontal(self, x, y):
        # check alignment horizontal
        init_y = y
        checker = self.board[x][y]
        count = 0
        while y < len(self.board):
            if checker == self.board[x][y]:
                count += 1
                y += 1
            else: break
        y = init_y - 1
        while y >= 0:
            if checker == self.board[x][y]:
                count += 1
                y -= 1
            else: break
        return count >= 5

    def check_alignment_vertical(self, x, y):
        # check alignment vertical
        init_x = x
        checker = self.board[x][y]
        count = 0
        while x < len(self.board):
            if checker == self.board[x][y]:
                count += 1
                x += 1
            else: break
        x = init_x - 1
        while x >= 0:
            if checker == self.board[x][y]:
                count += 1
                x -= 1
            else: break
        return count >= 5

    def check_alignment_diagonal(self, x, y):
        # check alignment diagonal
        init_x, init_y = x, y
        checker = self.board[x][y]
        count = 0
        while x < len(self.board) and y < len(self.board):
            if checker == self.board[x][y]:
                count += 1
                x += 1
                y += 1
            else: break
        x, y = init_x - 1, init_y - 1
        while x >= 0 and y >= 0:
            if checker == self.board[x][y]:
                count += 1
                x -= 1
                y -= 1
            else: break
        if count < 5:
            count = 0
            x, y = init_x, init_y
            while x < len(self.board) and y >= 0:
                if checker == self.board[x][y]:
                    count += 1
                    x += 1
                    y -= 1
                else: break
            x, y = init_x - 1, init_y + 1
            while x >= 0 and y < len(self.board):
                if checker == self.board[x][y]:
                    count += 1
                    x -= 1
                    y += 1
                else: break
        return count >= 5
