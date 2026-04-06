"""Télécharge des sprites / textures CC0 depuis le web, avec repli en placeholders colorés."""

from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path

import pygame

# URLs publiques (OpenGameArt, Wikimedia) — si une requête échoue, on génère un PNG local.
URLS: dict[str, str] = {
    "player_idle": "https://opengameart.org/sites/default/files/styles/thumbnail/public/hero_0.png",
    "enemy_rodeur": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png",
    "enemy_traqueur": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/200px-PNG_transparency_demonstration_1.png",
    "enemy_predateur": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/160px-PNG_transparency_demonstration_1.png",
    "enemy_maudit": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/120px-PNG_transparency_demonstration_1.png",
    "ui_bar": "https://opengameart.org/sites/default/files/Preview.png",
}

_COLORS: dict[str, tuple[int, int, int]] = {
    "player_idle": (90, 180, 120),
    "player_walk_0": (88, 178, 118),
    "player_walk_1": (92, 182, 122),
    "player_walk_2": (86, 176, 116),
    "player_walk_3": (94, 184, 124),
    "player_run_0": (95, 185, 125),
    "player_run_1": (98, 188, 128),
    "player_run_2": (91, 181, 121),
    "player_jump": (110, 200, 140),
    "player_roll": (70, 150, 200),
    "player_hurt": (220, 90, 90),
    "player_sneak": (75, 140, 110),
    "enemy_rodeur": (80, 120, 220),
    "enemy_traqueur": (160, 80, 200),
    "enemy_predateur": (255, 140, 60),
    "enemy_maudit": (160, 30, 40),
    "ui_bar": (32, 36, 48),
    "bush": (50, 120, 70),
    "pillar": (120, 118, 130),
    "spike_trap": (180, 60, 60),
    "vase": (140, 100, 70),
    "chest": (160, 120, 50),
    "bg_cave": (35, 32, 45),
    "bg_platform": (45, 55, 75),
    "tile_grass": (60, 140, 70),
    "projectile": (255, 220, 120),
}


def _download(url: str, dest: Path, timeout: float = 12.0) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FredusJonesAdventures/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        dest.write_bytes(data)
        return dest.stat().st_size > 32
    except (urllib.error.URLError, OSError, ValueError):
        return False


def _placeholder(path: Path, color: tuple[int, int, int], size: tuple[int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = size
    surf = pygame.Surface((max(w, 8), max(h, 8)), pygame.SRCALPHA)
    surf.fill((*color, 255))
    pygame.draw.rect(surf, (255, 255, 255, 80), surf.get_rect(), 2)
    pygame.image.save(surf, path)


def ensure_net_sprites(root: Path) -> None:
    """Crée assets/sprites/net/*.png, assets/sprites/ui/bottom_bar.png et tous les gabarits listés dans PATHS."""
    if not pygame.get_init():
        pygame.init()

    net = root / "assets" / "sprites" / "net"
    ui = root / "assets" / "sprites" / "ui"
    net.mkdir(parents=True, exist_ok=True)
    ui.mkdir(parents=True, exist_ok=True)

    targets: dict[str, tuple[Path, tuple[int, int]]] = {
        "player_idle": (net / "player_idle.png", (48, 64)),
        "player_walk_0": (net / "player_walk_0.png", (48, 64)),
        "player_walk_1": (net / "player_walk_1.png", (48, 64)),
        "player_walk_2": (net / "player_walk_2.png", (48, 64)),
        "player_walk_3": (net / "player_walk_3.png", (48, 64)),
        "player_run_0": (net / "player_run_0.png", (48, 64)),
        "player_run_1": (net / "player_run_1.png", (48, 64)),
        "player_run_2": (net / "player_run_2.png", (48, 64)),
        "player_jump": (net / "player_jump.png", (48, 64)),
        "player_roll": (net / "player_roll.png", (48, 64)),
        "player_hurt": (net / "player_hurt.png", (48, 64)),
        "player_sneak": (net / "player_sneak.png", (48, 64)),
        "enemy_rodeur": (net / "enemy_rodeur.png", (38, 38)),
        "enemy_traqueur": (net / "enemy_traqueur.png", (38, 38)),
        "enemy_predateur": (net / "enemy_predateur.png", (38, 38)),
        "enemy_maudit": (net / "enemy_maudit.png", (38, 38)),
        "ui_bar": (ui / "bottom_bar.png", (1280, 120)),
        "bush": (net / "bush.png", (64, 64)),
        "pillar": (net / "pillar.png", (64, 96)),
        "spike_trap": (net / "spike_trap.png", (48, 48)),
        "vase": (net / "vase.png", (48, 48)),
        "chest": (net / "chest.png", (48, 48)),
        "bg_cave": (net / "bg_cave.png", (256, 256)),
        "bg_platform": (net / "bg_platform.png", (256, 256)),
        "tile_grass": (net / "tile_grass.png", (64, 64)),
        "projectile": (net / "projectile.png", (32, 32)),
    }

    for key, (dest, size) in targets.items():
        if dest.is_file() and dest.stat().st_size > 64:
            continue
        ok = False
        if key in URLS:
            ok = _download(URLS[key], dest)
        if not ok:
            _placeholder(dest, _COLORS.get(key, (100, 100, 100)), size)

    try:
        from pygame import transform

        for p, sz in [
            (net / "player_idle.png", (48, 64)),
            (net / "enemy_rodeur.png", (38, 38)),
            (net / "enemy_traqueur.png", (38, 38)),
            (net / "enemy_predateur.png", (38, 38)),
            (net / "enemy_maudit.png", (38, 38)),
        ]:
            if not p.is_file():
                continue
            img = pygame.image.load(str(p)).convert_alpha()
            if img.get_size() != sz:
                img = transform.smoothscale(img, sz)
                pygame.image.save(img, str(p))
    except pygame.error:
        pass


def apply_sprite_path_overrides(root: Path) -> None:
    """Met à jour game.sprite_registry.PATHS (chemins relatifs à la racine du jeu)."""
    from game import sprite_registry as sr

    base = root.resolve()

    def rp(p: Path) -> str:
        return p.relative_to(base).as_posix()

    net = base / "assets" / "sprites" / "net"
    ui = base / "assets" / "sprites" / "ui"

    ov: dict[str, str | list[str]] = {
        "player_idle": rp(net / "player_idle.png"),
        "player_walk": [
            rp(net / "player_walk_0.png"),
            rp(net / "player_walk_1.png"),
            rp(net / "player_walk_2.png"),
            rp(net / "player_walk_3.png"),
        ],
        "player_run": [
            rp(net / "player_run_0.png"),
            rp(net / "player_run_1.png"),
            rp(net / "player_run_2.png"),
        ],
        "player_jump": rp(net / "player_jump.png"),
        "player_roll": rp(net / "player_roll.png"),
        "player_hurt": rp(net / "player_hurt.png"),
        "player_sneak": rp(net / "player_sneak.png"),
        "enemy_rodeur": rp(net / "enemy_rodeur.png"),
        "enemy_traqueur": rp(net / "enemy_traqueur.png"),
        "enemy_predateur": rp(net / "enemy_predateur.png"),
        "enemy_maudit": rp(net / "enemy_maudit.png"),
        "bush": rp(net / "bush.png"),
        "pillar": rp(net / "pillar.png"),
        "spike_trap": rp(net / "spike_trap.png"),
        "vase": rp(net / "vase.png"),
        "chest": rp(net / "chest.png"),
        "bg_cave": rp(net / "bg_cave.png"),
        "bg_platform": rp(net / "bg_platform.png"),
        "tile_grass": rp(net / "tile_grass.png"),
        "projectile": rp(net / "projectile.png"),
    }
    for k, v in ov.items():
        sr.PATHS[k] = v

    bar = ui / "bottom_bar.png"
    if bar.is_file():
        sr.PATHS["hud_bar"] = rp(bar)


def ensure_ui_and_font_placeholders(root: Path) -> None:
    """Gabarits menu / UI et dossier polices (remplacez par vos fichiers)."""
    if not pygame.get_init():
        pygame.init()

    ui = root / "assets" / "sprites" / "ui"
    ui.mkdir(parents=True, exist_ok=True)

    menu_specs: list[tuple[str, tuple[int, int], tuple[int, int, int]]] = [
        ("menu_background.png", (1280, 720), (36, 40, 54)),
        ("panel.png", (640, 480), (48, 52, 68)),
        ("title_logo.png", (640, 160), (220, 220, 235)),
        ("button_idle.png", (240, 56), (70, 120, 200)),
        ("button_hover.png", (240, 56), (90, 150, 230)),
    ]
    for name, size, col in menu_specs:
        p = ui / name
        if not p.is_file() or p.stat().st_size <= 64:
            _placeholder(p, col, size)

    fonts = root / "assets" / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    readme = fonts / "LISEZMOI.txt"
    if not readme.is_file():
        readme.write_text(
            "Polices (remplacement)\n"
            "=======================\n"
            "Placez ici vos fichiers .ttf ou .otf (ex. menu.ttf, hud.ttf).\n"
            "Le jeu utilise les polices système par défaut tant que vous ne branchez pas vos fichiers dans le code.\n",
            encoding="utf-8",
        )
