import pygame
import soragl as SORA
import struct

from pygame import draw as pgdraw
from pygame import math as pgmath

from soragl import (
    animation,
    scene,
    physics,
    base_objects,
    mgl,
    smath,
    signal,
    statesystem,
)

# -------------------------------------------------------------- #
# setup

WW = 1280
WINDOW_SIZE = [WW, int(WW / 16 * 9)]
WW = 1280 // 3
FB_SIZE = [WW, int(WW / 16 * 9)]

# mac version -- since no opengl

# ------------------------------ #
# setup
SORA.initialize(
    {
        "fps": 30,
        "window_size": [1280, 720],
        "window_flags": pygame.RESIZABLE
        | pygame.OPENGL
        | pygame.DOUBLEBUF
        | pygame.HWSURFACE
        | pygame.OPENGL
        if SORA.get_os() == SORA.OS_WINDOWS
        else 0,
        "window_bits": 32,
        "framebuffer_flags": pygame.SRCALPHA,
        "framebuffer_size": [1280 // 3, 720 // 3],
        "framebuffer_bits": 32,
        "debug": True,
    }
)


SORA.create_context()

# if moderngl stuff setup
if SORA.is_flag_active(pygame.OPENGL):
    mgl.ModernGL.create_context(
        options={
            "standalone": False,
            "gc_mode": "context_gc",
            "clear_color": [0.0, 0.0, 0.0, 1.0],
        }
    )

# -------------------------------------------------------------- #
# imports

from scripts import grass

# -------------------------------------------------------------- #

sc = scene.Scene(config=scene.load_config(scene.Scene.DEFAULT_CONFIG))
sc._config["chunkpixw"] = 300
sc._config["chunkpixh"] = 300
sc._config["render_distance"] = 5
scw = sc.make_layer(sc.get_config(), 1)
# scw.get_chunk(0, 0)
BG_COL = (153, 220, 80)

# -- add entities
# particle handler test



# aspects
scw.add_aspect(base_objects.TileMapDebug())
scw.add_aspect(base_objects.SpriteRendererAspect())
scw.add_aspect(base_objects.Collision2DAspect())
# scw.add_aspect(base_objects.Collision2DRendererAspectDebug())
scw.add_aspect(base_objects.Area2DAspect())
scw.add_aspect(base_objects.ScriptAspect())
scw.add_aspect(statesystem.StateHandlerAspect())

# push scene
scene.SceneHandler.push_scene(sc)

# -------------------------------------------------------------- #
# game loop
SORA.start_engine_time()
while SORA.RUNNING:
    # SORA.FRAMEBUFFER.fill((255, 255, 255, 255))
    # SORA.FRAMEBUFFER.fill((0, 0, 0, 255))
    SORA.FRAMEBUFFER.fill(BG_COL)
    SORA.DEBUGBUFFER.fill((0, 0, 0, 0))
    # pygame update + render
    scene.SceneHandler.update()

    if SORA.is_key_clicked(pygame.K_d) and SORA.is_key_pressed(pygame.K_LSHIFT):
        SORA.DEBUG = not SORA.DEBUG

    # update signals
    signal.handle_signals()
    # push frame
    SORA.push_framebuffer()
    # pygame.display.flip()
    # update events
    SORA.update_hardware()
    SORA.handle_pygame_events()
    # clock tick
    SORA.CLOCK.tick(SORA.FPS)
    SORA.update_time()

# ------------------------------- #

pygame.quit()
