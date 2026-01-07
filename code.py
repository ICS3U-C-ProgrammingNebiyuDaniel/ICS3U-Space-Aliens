#!/usr/bin/env python3

# Created by: Nebs
# Created on: January 2026
# This program is the "Space Aliens" program on the PyBadge

import ugame
import stage
import constant


def game_scene():
    # this function is the main game game_scene

    # image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # set the background to image 0 in the image bank
    # and the size (10x8 tiles of size 16x16)

    background = stage.Grid(image_bank_background, constant.SCREEN_GRID_X, constant.SCREEN_GRID_Y)

    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # create a stage for the background to show up on
    # and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constant.FPS)

    # set the layers of all sprites, items show up in order
    game.layers = [ship, background]

    # render all sprites
    # most likely you will only render the background once per game scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_X:
            pass
        if keys & ugame.K_O:
            pass
        if keys & ugame.K_START:
            pass
        if keys & ugame.K_SELECT:
            pass
        if keys & ugame.K_RIGHT:
            ship.move(ship.x + 1, ship.y)
        if keys & ugame.K_LEFT:
            ship.move(ship.x - 1, ship.y)
        if keys & ugame.K_UP:
            pass
        if keys & ugame.K_DOWN:
            pass
        # update game logic

        # redraw Sprites
        game.render_sprites([ship])
        game.tick()


if __name__ == "__main__":
    game_scene()
