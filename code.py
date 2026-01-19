import stage
import ugame
import time
import random
import constants
import supervisor


# -----------------------
# Splash Scene
# -----------------------
def splash_scene():
    coin_sound = open("coin.wav", "rb")
    ugame.audio.stop()
    ugame.audio.mute(False)
    ugame.audio.play(coin_sound)

    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y,
    )

    background.tile(2, 2, 0)
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)

    background.tile(2, 3, 0)
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)

    background.tile(2, 4, 0)
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)

    background.tile(2, 5, 0)
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    start_time = time.monotonic()
    while time.monotonic() - start_time < 2:
        game.tick()

    menu_scene()


# -----------------------
# Menu Scene
# -----------------------
def menu_scene():
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y,
    )

    text = []

    title = stage.Text(
        width=29,
        height=12,
        font=None,
        palette=constants.RED_PALETTE,
        buffer=None,
    )
    title.move(20, 10)
    title.text("MT Game Studios")
    text.append(title)

    start = stage.Text(
        width=29,
        height=12,
        font=None,
        palette=constants.RED_PALETTE,
        buffer=None,
    )
    start.move(40, 110)
    start.text("PRESS START")
    text.append(start)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        if ugame.buttons.get_pressed() & ugame.K_START:
            game_scene()
        game.tick()


# -----------------------
# Game Over Scene
# -----------------------
def game_over_scene(final_score):
    ugame.audio.stop()

    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y,
    )

    text = []

    score_text = stage.Text(
        width=29,
        height=14,
        font=None,
        palette=constants.BLUE_PALETTE,
        buffer=None,
    )
    score_text.move(22, 20)
    score_text.text("Final Score: {}".format(final_score))
    text.append(score_text)

    game_over = stage.Text(
        width=29,
        height=14,
        font=None,
        palette=constants.BLUE_PALETTE,
        buffer=None,
    )
    game_over.move(43, 60)
    game_over.text("GAME OVER")
    text.append(game_over)

    restart = stage.Text(
        width=29,
        height=14,
        font=None,
        palette=constants.BLUE_PALETTE,
        buffer=None,
    )
    restart.move(32, 110)
    restart.text("PRESS SELECT")
    text.append(restart)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        if ugame.buttons.get_pressed() & ugame.K_SELECT:
            supervisor.reload()
        game.tick()


# -----------------------
# Game Scene
# -----------------------
def game_scene():
    score = 0

    score_text = stage.Text(
        width=29,
        height=12,
        font=None,
        palette=constants.RED_PALETTE,
        buffer=None,
    )
    score_text.move(1, 1)
    score_text.text("Score: 0")

    bg_bank = stage.Bank.from_bmp16("space_aliens_background.bmp")
    sprite_bank = stage.Bank.from_bmp16("space_aliens.bmp")

    pew = open("pew.wav", "rb")
    boom = open("boom.wav", "rb")
    crash = open("crash.wav", "rb")

    ugame.audio.stop()
    ugame.audio.mute(False)

    background = stage.Grid(
        bg_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y,
    )

    for x in range(constants.SCREEN_GRID_X):
        for y in range(constants.SCREEN_GRID_Y):
            background.tile(x, y, random.randint(1, 3))

    ship = stage.Sprite(
        sprite_bank,
        5,
        75,
        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE),
    )

    aliens = []
    for _ in range(constants.TOTAL_NUMBER_OF_ALIENS):
        aliens.append(
            stage.Sprite(
                sprite_bank,
                9,
                constants.OFF_SCREEN_X,
                constants.OFF_SCREEN_Y,
            )
        )

    lasers = []
    for _ in range(constants.TOTAL_NUMBER_OF_LASERS):
        lasers.append(
            stage.Sprite(
                sprite_bank,
                10,
                constants.OFF_SCREEN_X,
                constants.OFF_SCREEN_Y,
            )
        )

    def show_alien():
        for alien in aliens:
            if alien.x < 0:
                alien.move(
                    random.randint(
                        constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break

    show_alien()

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    game.render_block()

    a_button = constants.button_state["button_up"]

    while True:
        keys = ugame.buttons.get_pressed()

        # -----------------------
        # Handle A button (fire laser)
        # -----------------------
        if keys & ugame.K_O:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        if a_button == constants.button_state["button_just_pressed"]:
            for laser in lasers:
                if laser.x < 0:
                    laser.move(ship.x, ship.y)
                    ugame.audio.play(pew)
                    break

        # -----------------------
        # Move ship (warp both sides)
        # -----------------------
        if keys & ugame.K_LEFT:
            ship.move(ship.x - 1, ship.y)
            if ship.x < -constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X, ship.y)

        if keys & ugame.K_RIGHT:
            ship.move(ship.x + 1, ship.y)
            if ship.x > constants.SCREEN_X:
                ship.move(0 - constants.SPRITE_SIZE, ship.y)

        # -----------------------
        # Move lasers
        # -----------------------
        for laser in lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()

        # -----------------------
        # Move aliens
        # -----------------------
        for alien in aliens:
            if alien.x > 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()
                    score -= 1
                    if score < 0:
                        score = 0
                    score_text.clear()
                    score_text.cursor(0, 0)
                    score_text.text("Score: {}".format(score))

        # -----------------------
        # Collisions (lasers vs aliens)
        # -----------------------
        for laser in lasers:
            if laser.x > 0:
                for alien in aliens:
                    if alien.x > 0 and stage.collide(
                        laser.x + 6,
                        laser.y + 2,
                        laser.x + 11,
                        laser.y + 12,
                        alien.x + 1,
                        alien.y,
                        alien.x + 15,
                        alien.y + 15,
                    ):
                        laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        ugame.audio.stop()
                        ugame.audio.play(boom)
                        show_alien()
                        score += 1
                        score_text.clear()
                        score_text.cursor(0, 0)
                        score_text.text("Score: {}".format(score))

        # -----------------------
        # Collisions (aliens vs ship)
        # -----------------------
        for alien in aliens:
            if alien.x > 0 and stage.collide(
                alien.x + 1,
                alien.y,
                alien.x + 15,
                alien.y + 15,
                ship.x,
                ship.y,
                ship.x + 15,
                ship.y + 15,
            ):
                ugame.audio.stop()
                ugame.audio.play(crash)
                time.sleep(3)
                game_over_scene(score)

        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


# -----------------------
# Run Game
# -----------------------
if __name__ == "__main__":
    splash_scene()
