# Fredus Jones Adventures

MVP du jeu roguelite top-down en Pygame (puzzle + infiltration + plateforme).

## Etat actuel

Cette version implémente la **Phase 1**:
- structure modulaire initiale;
- joueur déplaçable en ZQSD;
- caméra avec suivi fluide et limites de salle;
- salle de test plus grande que l'écran avec murs/obstacles;
- collisions de base (AABB avec `pygame.Rect`).

## Lancer le jeu

**Le plus simple sous Windows :** double-cliquer sur `Lancer le jeu.bat` (utilise `venv311` si présent).

Sinon, depuis le dossier du projet :

1. Utiliser Python **3.11** avec pygame (évite les erreurs `No module named 'pygame'` avec Python 3.14) :

```powershell
.\venv311\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

2. Si tu vois `No module named 'config'`, lance toujours `main.py` **depuis la racine du projet**, ou utilise le `.bat` ci-dessus (le script force le bon dossier de travail).

## Contrôles

- `ZQSD`: déplacement
- `ESC`: quitter

## Sources de visuels

- Super Package Retro Pixel Effects 32x32 pack 2 Free
- Pixel Art Lantern Pack
- mp_character_animation_asset_pack_v1.0
- stringstar fields
- PixelFantasy_Caves_1.0
- RF_Catacombs_v1.0
- mystic_woods_free_2.2
- Pixel Art Top Down - Basic v1.2.3
- Tiny Swords