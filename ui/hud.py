"""HUD en jeu — source prioritaire sur le .pyc (signature alignée sur game_manager)."""

from __future__ import annotations

import pygame

from config import COLOR_TEXT, SCREEN_HEIGHT, SCREEN_WIDTH, TOTAL_ROOMS


def _blit_text(
    surface: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    font: pygame.font.Font,
    color: tuple[int, int, int],
) -> None:
    surface.blit(font.render(str(text), True, color), pos)


class HUD:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def draw(
        self,
        screen: pygame.Surface,
        player,
        room_index: int,
        noise_label: str = "",
        lamp_cd: float = 0.0,
        platform_timer: float | None = None,
        debug_noise: float = 0.0,
        debug: bool = False,
        *extra,
    ) -> None:
        """8 args après self (+ optionnel *extra) pour compatibilité avec l’appel du GameManager."""
        _ = extra

        try:
            rn = int(room_index) + 1
        except (TypeError, ValueError):
            rn = 1
        _blit_text(
            screen,
            f"Salle {rn}/{TOTAL_ROOMS}",
            (max(8, SCREEN_WIDTH // 2 - 80), 10),
            self.font,
            COLOR_TEXT,
        )

        items = getattr(player, "active_items", None) or [None, None]
        a0, a1 = (items[0] if len(items) > 0 else None), (items[1] if len(items) > 1 else None)
        _blit_text(
            screen,
            f"Objets: [{a0 or '-'}] | [{a1 or '-'}]",
            (16, 42),
            self.font,
            (200, 200, 200),
        )

        noise = float(getattr(player, "noise_level", debug_noise) or 0)
        col = (210, 70, 70) if noise > 40 else (90, 110, 200)
        pygame.draw.circle(screen, col, (36, 102), 15)
        _blit_text(screen, "Bruit", (58, 94), self.font, COLOR_TEXT)

        try:
            lcd = float(lamp_cd)
        except (TypeError, ValueError):
            lcd = 0.0
        if lcd > 0:
            _blit_text(screen, f"Lampe: {lcd:.1f}s", (16, 128), self.font, (170, 170, 170))
        else:
            _blit_text(screen, "Lampe: pret", (16, 128), self.font, (110, 200, 130))

        if platform_timer is not None:
            try:
                t = max(0.0, float(platform_timer))
                _blit_text(screen, f"Timer: {t:.1f}s", (SCREEN_WIDTH - 230, 10), self.font, (255, 200, 100))
            except (TypeError, ValueError):
                pass

        if noise_label:
            _blit_text(screen, str(noise_label), (16, 156), self.font, (180, 180, 200))

        if debug:
            _blit_text(screen, f"DBG bruit={noise:.0f}", (16, 182), self.font, (255, 230, 120))

        _blit_text(
            screen,
            "ZQSD  Espace  E  Souris  |  M pause  |  ESC quitter  |  F3 debug",
            (16, SCREEN_HEIGHT - 34),
            self.font,
            (120, 120, 130),
        )
