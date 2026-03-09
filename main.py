import pygame
import sys

# Initialisation
pygame.init()
pygame.mixer.init()

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Mon Jeu - Livrable 2"

# Couleurs de base
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


def main():
    running = True

    while running:
        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Mise à jour de la logique ---
        # TODO : mettre à jour les entités du jeu

        # --- Rendu ---
        screen.fill(BLACK)

        # TODO : dessiner le terrain, les sprites, l'UI

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()