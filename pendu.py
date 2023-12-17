import pygame
import pygame_menu
from pygame_menu import themes
import random

# Utilisation d'une liste pour stocker la difficulté
difficulty = [1]

# Lecture des mots depuis le fichier
with open("mots.txt", "r") as file:
    mots_pendu = file.read().split(', ')

# Fonction pour insérer un mot dans le fichier
def insert_word(nouveau_mot):
    with open("mots.txt", "a") as file:
        file.write(f", {nouveau_mot}")
    mots_pendu.append(nouveau_mot)

# Nouvelle fonction pour la page d'insertion de mot
def insertion_page():
    insert_menu = pygame_menu.Menu('Insert Word', 600, 400, theme=themes.THEME_DARK)
    insert_menu.add.text_input('Insert a word: ', default='', maxchar=20, onreturn=insert_word, font_size=35, font_color=(255, 255, 255))
    insert_menu.add.button('Back to Main Menu', mainmenu)
    insert_menu.mainloop(screen)

# Fonction pour lancer le jeu de pendu
def start_the_game():
    mot_a_deviner = get_random_word()
    run_pendu(mot_a_deviner)

def on_change_difficulty(_, value):
    # Utilisation de la liste pour stocker la difficulté
    difficulty[0] = value

def get_random_word():
    if difficulty[0] == 1:
        mots_candidates = [mot for mot in mots_pendu if 3 <= len(mot) <= 4]
    elif difficulty[0] == 2:
        mots_candidates = [mot for mot in mots_pendu if 4 < len(mot) <= 6]    
    else:
        mots_candidates = [mot for mot in mots_pendu if len(mot) > 6]
    
    print('difficulty',difficulty[0])

    if mots_candidates:
        return random.choice(mots_candidates)
    else:
        print("No words found for the selected difficulty.")
        return "default"

# Fonction principale du jeu de pendu
def run_pendu(mot_a_deviner):
    pygame.init()

    # Initialisation de la fenêtre Pygame
    screen = pygame.display.set_mode((660, 450))
    pygame.display.set_caption("Jeu de Pendu")

    # Initialisation des variables du jeu
    mot_cache = ['_' if lettre.isalpha() else lettre for lettre in mot_a_deviner]
    lettres_utilisees = set()
    tentatives_restantes = 10

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key in range(97, 123):  # Check if a key is a lowercase letter
                    lettre = chr(event.key)
                    if lettre not in lettres_utilisees:
                        lettres_utilisees.add(lettre)
                        if lettre in mot_a_deviner:
                            for i, lettre_mot in enumerate(mot_a_deviner):
                                if lettre_mot == lettre:
                                    mot_cache[i] = lettre
                        else:
                            tentatives_restantes -= 1

        screen.fill((255, 255, 255))

        # Affichage du mot caché
        mot_affichage = ' '.join(mot_cache)
        text = font.render(mot_affichage, True, (0, 0, 0))
        screen.blit(text, (250, 200))

        # Affichage des lettres utilisées et des tentatives restantes
        lettres_text = font.render(f"Lettres utilisées: {' '.join(lettres_utilisees)}", True, (0, 0, 0))
        screen.blit(lettres_text, (10, 10))
        tentatives_text = font.render(f"Tentatives restantes: {tentatives_restantes}", True, (0, 0, 0))
        screen.blit(tentatives_text, (10, 50))

        pygame.display.flip()

        if '_' not in mot_cache or tentatives_restantes <= 0:
            run = False
            mainmenu.mainloop(screen)

    pygame.quit()

# Initialisation de pygame et création de la fenêtre
pygame.init()
screen = pygame.display.set_mode((660, 450))
run = True

# Création du menu principal
mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_DARK)
mainmenu.add.text_input('Username: ', default='', maxchar=20, font_size=35, font_color=(255, 255, 255))
mainmenu.add.selector('Difficulty: ', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=on_change_difficulty)
mainmenu.add.button('Play', start_the_game, font_size=35, font_color=(255, 255, 255))
mainmenu.add.button('Insert a Word', insertion_page, font_size=35, font_color=(255, 255, 255))
mainmenu.add.button('Exit', pygame_menu.events.EXIT, font_size=35, font_color=(255, 255, 255))

# Boucle principale
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    screen.fill((255, 255, 255))
    mainmenu.mainloop(screen)
    pygame.display.update()

pygame.quit()
quit()