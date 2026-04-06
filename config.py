"""Constantes et configuration — Fredus Jones Adventures."""

from __future__ import annotations

import math

import pygame

# --- Affichage ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 30
TITLE = "Fredus Jones Adventures"

ROOM_SIZE_SMALL = (SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
ROOM_SIZE_LARGE = (SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3)
PLATFORM_ROOM_LENGTH = SCREEN_WIDTH * 8
TILE_SIZE = 64

# --- Joueur ---
PLAYER_SPEED = 200
PLAYER_SIZE = 32
ROLL_DISTANCE = PLAYER_SIZE * 2
ROLL_DURATION = 0.5
ROLL_COOLDOWN = 3.0
ROLL_INVINCIBILITY = True

JUMP_HEIGHT = TILE_SIZE * 2
JUMP_LENGTH = TILE_SIZE * 3
JUMP_TIME = 0.6
GRAVITY = (2 * JUMP_HEIGHT) / max(JUMP_TIME**2 / 4, 0.001)
JUMP_VELOCITY = -math.sqrt(2 * GRAVITY * JUMP_HEIGHT)

PLAYER_HEALTH = 1

# Utilisé par runtime_patches / sprites (échelle d’affichage)
PLAYER_SPRITE_DISPLAY = 1

# Taille d’affichage des sprites ennemis (côté en pixels, alignée sur la hitbox logique)
ENEMY_SPRITE_SIZE = PLAYER_SIZE

LONGER_ROLL_MULT = 1.25
SPEED_BOOST_MULT = 1.2

# --- Ennemis ---
ENEMY_SPEEDS = {
    "rodeur": 1.2,
    "traqueur": 1.4,
    "predateur": 1.5,
    "maudit": 0.3,
}

ENEMY_DETECTION = {
    "rodeur": {"angle": 90, "vision": 384, "hearing": 192},
    "traqueur": {"angle": 120, "vision": 448, "hearing": 320},
    "predateur": {"angle": 60, "vision": 128, "hearing": 448},
    "maudit": {"angle": 160, "vision": 960, "hearing": 0},
}

PATROL_SHAPE = "square"
PATHFINDING_UPDATE = 5.0
ALERT_DURATION = 3.0
MAUDIT_IMMOBILIZE_TIME = 3.0

ENEMY_COLORS = {
    "rodeur": (80, 120, 220),
    "traqueur": (160, 80, 200),
    "predateur": (255, 140, 60),
    "maudit": (160, 30, 40),
}

# --- Lampe ---
LAMP_RANGE = 192
LAMP_ANGLE = 360
LAMP_BLIND_DURATION = 2.0
LAMP_COOLDOWN = 5.0

# --- Objets ---
ITEMS_ACTIVE = {
    "totem_reanimation": {"uses_per_room": 1, "auto_on_death": True},
    "chapeau_invisibilite": {"uses_per_room": 1, "duration": 15.0, "can_interact": True},
    "boite_carton": {"uses_per_room": 1, "duration": float("inf"), "noise_level": "high"},
    "anneau_spectral": {"uses_per_room": 1, "range": 1280},
}

ITEMS_PASSIVE = {
    "bottes_vitesse": {"speed_bonus": 0.2},
    "amulette_lumineuse": {"lamp_charges": 2, "no_cooldown_between": True},
}

# --- Salles ---
TOTAL_ROOMS = 10
ROOM_TYPES_WEIGHTS = {
    "puzzle": 35,
    "stealth": 30,
    "platform": 20,
    "treasure": 10,
    "rest": 5,
}
PLATFORM_FREQUENCY = 5
TREASURE_CHANCE = 0.5
TREASURE_FREQUENCY = 10

MAX_LEVERS = 4
LEVER_TIMEOUT = 60.0
LEVER_LIGHT_COLOR = (255, 255, 0)

MAX_VASES = 3
MAX_PLATES = 3
VASE_SIZE = PLAYER_SIZE
PUSH_DISTANCE = TILE_SIZE

DOOR_COLORS = {"correct": (0, 255, 0), "wrong": (255, 0, 0)}
MAX_DOORS = 2
WRONG_DOOR_PENALTY = 4

TRAPS = {
    "spikes": {"retractable": True, "damage": "instant_death"},
    "arrows": {"fire_rate": 4.0, "speed": 400, "warning": False},
    "collapsing_floor": {"delay": 1.0, "regenerate": True, "fall_death": True},
    "poison": {"duration": 15.0, "damage": "instant_death_on_contact"},
    "alert_zone": {"alerts": "on_screen_enemies"},
}

SCORE_PER_ROOM = 5
SCORE_PER_ENEMY_KILL = 1
SCORE_PACIFIST_BONUS = 10

UPGRADE_COSTS = {
    "speed_boost": 100,
    "new_item": 100,
    "longer_roll": 100,
}

MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.5
MUSIC_TRACKS = {
    "exploration": "assets/sounds/music/exploration.ogg",
    "combat": "assets/sounds/music/combat.ogg",
}

NOISE_WALK = 25
NOISE_RUN_BONUS = 0
NOISE_ROLL = 60
NOISE_PUSH = 45
NOISE_DECAY = 80.0
NOISE_HEARING_THRESHOLD = 15

CAMERA_SMOOTHNESS = 0.12
ROOM_TRANSITION_DURATION = 2.0

HUB_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

COLOR_BG = (17, 20, 24)
COLOR_WALL = (62, 73, 87)
COLOR_PLAYER = (80, 220, 120)
COLOR_TEXT = (240, 240, 240)
COLOR_GRID = (28, 33, 40)
COLOR_EXIT = (60, 180, 90)
COLOR_CHEST = (220, 200, 80)

CONTROLS = {
    "move_up": pygame.K_z,
    "move_down": pygame.K_s,
    "move_left": pygame.K_q,
    "move_right": pygame.K_d,
    "interact": pygame.K_e,
    "active_item_2": pygame.K_a,
    "roll": pygame.K_SPACE,
    "pause": pygame.K_m,
    "quit": pygame.K_ESCAPE,
    "hub_menu": pygame.K_TAB,
    "debug": pygame.K_F3,
}


def get_difficulty_modifiers(room_number: int) -> dict:
    n = max(0, room_number)
    extra_enemies = n // 2
    speed_mult = 1.0 + (0.1 * (n // 2))
    extra_levers = n // 5
    return {"enemies": extra_enemies, "speed": speed_mult, "levers": extra_levers}


def calculate_currency(rooms_completed: int, enemies_killed: int) -> int:
    return rooms_completed + (10 * enemies_killed)
