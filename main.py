"""Point d'entrée du jeu Fredus Jones Adventures."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# --- Racine du projet ---
if getattr(sys, "frozen", False):
    _ROOT = Path(sys.executable).resolve().parent
else:
    _ROOT = Path(__file__).resolve().parent

_root_str = str(_ROOT.resolve())
if _root_str in sys.path:
    sys.path.remove(_root_str)
sys.path.insert(0, _root_str)

_CONFIG = _ROOT / "config.py"
if not _CONFIG.is_file():
    print(
        f"Erreur : fichier introuvable : {_CONFIG}\n"
        "Lance le jeu depuis la racine du projet (avec config.py).",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import pygame
except ModuleNotFoundError:
    venv_py = _ROOT / "venv311" / "Scripts" / "python.exe"
    print(
        "Erreur : pygame n'est pas installé pour cet interpréteur Python.\n\n"
        f'  "{venv_py}" -m pip install -r requirements.txt\n'
        f'  "{venv_py}" main.py\n',
        file=sys.stderr,
    )
    sys.exit(1)

# Charger le bytecode (.pyc) quand les .py sont absents ou vides (voir _pyc_hook.py)
import _pyc_hook

_pyc_hook.install()

import runtime_patches

runtime_patches.apply()

from config import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from game.game_manager import GameManager


def main() -> None:
    os.chdir(_ROOT)

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    game = GameManager(screen)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
