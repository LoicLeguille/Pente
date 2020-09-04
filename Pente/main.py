# Pente (a board game) by Loïc Leguille
# Buttons- art from Kenney.nl
# Japanese Robot- font from Darrell Flood
# Korean Calligraphy- font from hijoju
# Peace at last- Music by Jan125

from game import *

# main function
def main():
    root = Tk()
    g = Game(root)
    g.pack(fill = BOTH, expand = 'yes')
    g.button_event(str(g.Menu_btn))
    root.mainloop()

# run game
if __name__ == '__main__':
    main()
