"""Réglages gameplay / HUD / sprites après chargement du bytecode principal."""

from __future__ import annotations

import math
from pathlib import Path

import pygame

def _root() -> Path:
    import _pyc_hook

    return _pyc_hook.ROOT


def _mutate_config() -> None:
    import config

    cfg = config
    if "crouch" not in cfg.CONTROLS:
        cfg.CONTROLS["crouch"] = pygame.K_LCTRL

    cfg.ROOM_TRANSITION_DURATION = 1.0
    cfg.ROLL_DURATION = cfg.ROLL_DURATION / 3.0
    cfg.ROLL_COOLDOWN = cfg.ROLL_COOLDOWN / 3.0

    cfg.JUMP_HEIGHT = int(cfg.JUMP_HEIGHT * 1.55)
    cfg.JUMP_LENGTH = int(cfg.JUMP_LENGTH * 1.5)
    cfg.JUMP_VELOCITY = -math.sqrt(2.0 * cfg.GRAVITY * float(cfg.JUMP_HEIGHT))


def _sync_player_module() -> None:
    import config
    import entities.player as ep

    names = (
        "ROLL_DURATION",
        "ROLL_COOLDOWN",
        "JUMP_VELOCITY",
        "JUMP_HEIGHT",
        "PLAYER_SPEED",
        "NOISE_WALK",
        "NOISE_ROLL",
        "NOISE_DECAY",
        "LONGER_ROLL_MULT",
        "SPEED_BOOST_MULT",
        "LAMP_RANGE",
        "LAMP_COOLDOWN",
        "LAMP_BLIND_DURATION",
        "TILE_SIZE",
        "PLAYER_SIZE",
        "PLAYER_SPRITE_DISPLAY",
    )
    for n in names:
        if hasattr(ep, n) and hasattr(config, n):
            setattr(ep, n, getattr(config, n))


def _patch_player() -> None:
    from entities.player import Player

    _orig_update = Player.update
    _orig_top = Player._update_topdown
    _orig_speed = Player.effective_speed

    def update(self, dt, keys, obstacles, hide_rects, particles=None):
        from config import CONTROLS

        c = CONTROLS.get("crouch", pygame.K_LCTRL)
        self.crouching = bool(keys[c])
        r = _orig_update(self, dt, keys, obstacles, hide_rects, particles)
        if getattr(self, "crouching", False):
            an = getattr(self, "_anim_name", None)
            if an in ("idle", "walk"):
                self._anim_name = "sneak"
        return r

    def _update_topdown(self, dt, keys, direction, obstacles, particles):
        import entities.player as ep

        if getattr(self, "crouching", False):
            old = ep.NOISE_WALK
            ep.NOISE_WALK = 0
            try:
                return _orig_top(self, dt, keys, direction, obstacles, particles)
            finally:
                ep.NOISE_WALK = old
        return _orig_top(self, dt, keys, direction, obstacles, particles)

    def effective_speed(self):
        sp = _orig_speed(self)
        if getattr(self, "crouching", False):
            sp *= 0.38
        return sp

    Player.update = update  # type: ignore[assignment]
    Player._update_topdown = _update_topdown  # type: ignore[assignment]
    Player.effective_speed = effective_speed  # type: ignore[assignment]


def _patch_transition() -> None:
    import config
    import rooms.transition as rt

    rt.ROOM_TRANSITION_DURATION = config.ROOM_TRANSITION_DURATION


def _patch_room_entry_grace() -> None:
    """Évite la mort au spawn (pièges / poison calés sur l'entrée en salle stealth)."""
    from rooms.room import Room

    _orig = Room.update
    _GRACE_SEC = 0.65

    def update(self, dt, player):  # type: ignore[no-untyped-def]
        if not hasattr(self, "_entry_grace_left"):
            self._entry_grace_left = _GRACE_SEC
        events = _orig(self, dt, player)
        self._entry_grace_left = max(0.0, float(self._entry_grace_left) - float(dt))
        if self._entry_grace_left > 0:
            events = dict(events)
            if events.get("hit_player"):
                events["hit_player"] = False
            if events.get("platform_timeout"):
                events["platform_timeout"] = False
        return events

    Room.update = update  # type: ignore[assignment]


def _patch_get_player_frame() -> None:
    from game import sprite_registry as sr

    _orig = sr.get_player_frame

    def get_player_frame(anim, frame_i, display_size):  # type: ignore[no-untyped-def]
        if anim == "sneak":
            p = sr.PATHS.get("player_sneak")
            if p:
                return sr.get_scaled(p, display_size)
        return _orig(anim, frame_i, display_size)

    sr.get_player_frame = get_player_frame  # type: ignore[assignment]


def apply() -> None:
    """À appeler avant `import game.game_manager`."""
    _mutate_config()
    _sync_player_module()
    _patch_player()
    _patch_transition()
    _patch_room_entry_grace()

    root = _root()
    try:
        import net_assets

        net_assets.ensure_net_sprites(root)
        net_assets.apply_sprite_path_overrides(root)
        net_assets.ensure_ui_and_font_placeholders(root)
    except (OSError, pygame.error) as e:
        import sys

        print("net_assets:", e, file=sys.stderr)

    _patch_get_player_frame()
    _sync_player_module()
