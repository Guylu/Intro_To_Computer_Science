import math
import random
import sys

from asteroid import Asteroid
from screen import Screen
from ship import Ship

DEFAULT_ASTEROIDS_NUM = 5
MAX_SPECIAL = 5
MAX_TORPEDO = 10
INITIAL_X_SPEED = 0
INITIAL_Y_SPEED = 0
MIN_INITIAL_SPEED = 1
MAX_INITIAL_SPEED = 4
INITIAL_DEG = 0
X_POS = 0
Y_POS = 1
MIN_SIZE = 1
START_SIZE = 3
POINTS = {
    MIN_SIZE: 100,
    2: 50,
    3: 20,
}


class GameRunner:
    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__torpedos = []
        self.__special_shots = []
        self.__asteroids = []
        self.__score = 0

        x_rnd = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        y_rnd = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        self.__ship = Ship(x_rnd, INITIAL_X_SPEED,
                           y_rnd, INITIAL_Y_SPEED, INITIAL_DEG)

        if asteroids_amount is None:
            asteroids_amount = DEFAULT_ASTEROIDS_NUM
        self.__init_random_asteroids(asteroids_amount)

    def __init_random_asteroids(self, amount):
        """
        generate random asteroids
        :param amount: the amount of asteroids to generate
        :return: None
        """
        while len(self.__asteroids) < amount:
            x_rnd = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
            y_rnd = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
            x_speed_rnd = random.randint(MIN_INITIAL_SPEED, MAX_INITIAL_SPEED)
            y_speed_rnd = random.randint(MIN_INITIAL_SPEED, MAX_INITIAL_SPEED)

            if (x_rnd, y_rnd) == self.__ship.get_location():
                continue

            a = Asteroid(x_rnd, x_speed_rnd, y_rnd, y_speed_rnd, START_SIZE)
            self.__asteroids.append(a)
            self.__screen.register_asteroid(a, a.get_size())

    def run(self):
        """
        not my code here :P
        :return:
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        not my code here :P
        :return:
        """
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def __move_asteroids(self):
        """
        update asteroids location
        :return: None
        """
        for asteroid in self.__asteroids:
            asteroid.move((Screen.SCREEN_MAX_X, Screen.SCREEN_MAX_Y),
                          (Screen.SCREEN_MIN_X, Screen.SCREEN_MIN_Y))
            self.__screen.draw_asteroid(asteroid, *asteroid.get_location())

    def __move_shots(self, torpedo, asteroid=None):
        """
        update the relevant torpedo list locations regulars/special
        :param torpedo: list of torpedo
        :param asteroid: given for homing torpedoes to lock on
        :return: None
        """
        dead_torpedo = []
        args = {"world_min": (Screen.SCREEN_MIN_X, Screen.SCREEN_MIN_Y),
                "world_max": (Screen.SCREEN_MAX_X, Screen.SCREEN_MAX_Y)}

        if asteroid is not None and len(torpedo) != 0:
            args[torpedo[0].ASTEROID_VAR] = asteroid.get_location()

        for shot in torpedo:
            shot.move(**args)

            shot_x, shot_y = shot.get_location()
            self.__screen.draw_torpedo(shot, shot_x, shot_y, shot.get_deg())

            if not shot.reduce():
                dead_torpedo.append(shot)

        for shot in dead_torpedo:
            self.__screen.unregister_torpedo(shot)
            torpedo.remove(shot)

    def __move_all(self):
        """
        move all objects within screen
        :return:
        """
        self.__ship.move((Screen.SCREEN_MAX_X, Screen.SCREEN_MAX_Y),
                         (Screen.SCREEN_MIN_X, Screen.SCREEN_MIN_Y))
        self.__screen.draw_ship(*self.__ship.get_location(),
                                self.__ship.get_deg())

        self.__move_asteroids()

        self.__move_shots(self.__torpedos)
        # pass last asteroid to be followed
        self.__move_shots(self.__special_shots, self.__asteroids[-1])

    def __check_collision(self, target):
        """
        check if target collides with any of the asteroids
        :param target: an object within screen derived from BasicObject
        :return: the collided asteroid if exists else None
        """
        for curr_asteroid in self.__asteroids:
            if curr_asteroid.has_intersection(target):
                self.__screen.unregister_asteroid(curr_asteroid)
                self.__asteroids.remove(curr_asteroid)
                return curr_asteroid
        return None

    def __tor_smash(self, tor, smashedroid, shoots_list):
        """
        once an asteroid collides with a torpedo we smash the asteroid
        and delete the torpedo
        :param tor: the hitting torpedo
        :param smashedroid: the smashed asteroid
        :param shoots_list: the relevant list to remove the torpedo from
        :return: None
        """
        self.__screen.unregister_torpedo(tor)
        shoots_list.remove(tor)

        self.__score += POINTS[smashedroid.get_size()]

        if smashedroid.get_size() == MIN_SIZE:
            return

        smashedroid_speed_x, smashedroid_speed_y = smashedroid.get_speed()
        delta = math.sqrt(smashedroid_speed_x ** 2 + smashedroid_speed_y ** 2)
        x_speed = (tor.get_speed()[X_POS] + smashedroid_speed_x) / delta
        y_speed = (tor.get_speed()[Y_POS] + smashedroid_speed_y) / delta

        newdroid1 = Asteroid(smashedroid.get_location()[X_POS],
                             x_speed,
                             smashedroid.get_location()[Y_POS],
                             y_speed, smashedroid.get_size() - 1)
        newdroid2 = Asteroid(smashedroid.get_location()[X_POS],
                             -1 * x_speed,
                             smashedroid.get_location()[Y_POS],
                             -1 * y_speed, smashedroid.get_size() - 1)

        self.__asteroids.extend([newdroid1, newdroid2])
        self.__screen.register_asteroid(newdroid1, newdroid1.get_size())
        self.__screen.register_asteroid(newdroid2, newdroid2.get_size())

    def __collisions(self):
        """
        check for collisions with asteroids
        :return: None
        """
        for tor in self.__torpedos:
            smashedroid = self.__check_collision(tor)
            if smashedroid:
                # remove tor and create new asteroids
                self.__tor_smash(tor, smashedroid, self.__torpedos)

        for tor in self.__special_shots:
            smashedroid = self.__check_collision(tor)
            if smashedroid:
                # remove tor and create new asteroids
                self.__tor_smash(tor, smashedroid, self.__special_shots)

        if self.__check_collision(self.__ship):
            if self.__ship.man_count() > 0:
                self.__screen.remove_life()
            self.__ship.man_down()
            self.__screen.show_message("SMASH!", "you hit an asteroid -1 life")

    def __game_over(self):
        """
        check if the game reached an end for one of the given reasons
        :return: True if game ended, False otherwise
        """
        if self.__ship.man_count() <= 0:
            self.__screen.show_message("Game Over!", "bye bye")
            return True

        if len(self.__asteroids) == 0:
            self.__screen.show_message("You Win!", "hura!")
            return True

        if self.__screen.should_end():
            self.__screen.show_message("That's it?", "bye bye :(")
            return True

        return False

    def __teleportation_location_valid(self):
        """
        validate the location by checking collisions
        :return: False for a non-valid location, true otherwise
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                return False

        return True

    def __teleportation(self):
        """
        teleport the ship to a new collision-les location
        :return: None
        """
        while True:
            x_rnd = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
            y_rnd = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)

            self.__ship.set_location(x_rnd, y_rnd)
            if not self.__teleportation_location_valid():
                continue

            return

    def __shoot(self, is_special=False):
        """
        generate a new sho through ship
        :param is_special: the type of shot to create
        :return: None
        """
        if ((len(self.__torpedos) == MAX_TORPEDO and not is_special) or
                (len(self.__special_shots) == MAX_SPECIAL and is_special)):
            return

        tor = self.__ship.shoot(is_special)
        self.__screen.register_torpedo(tor)

        if is_special:
            self.__special_shots.append(tor)
        else:
            self.__torpedos.append(tor)

    def __keys_press(self):
        """
        apply key presses, they are coupled to movement and shooting groups
        :return: None
        """
        if self.__screen.is_left_pressed():
            self.__ship.rotate_left()
        elif self.__screen.is_right_pressed():
            self.__ship.rotate_right()
        elif self.__screen.is_up_pressed():
            self.__ship.accelerate()
        elif self.__screen.is_teleport_pressed():
            self.__teleportation()

        if self.__screen.is_space_pressed():
            self.__shoot()
        elif self.__screen.is_special_pressed():
            self.__shoot(is_special=True)

    def _game_loop(self):
        """
        main game body, this functions calls all other functions by order
        :return: None
        """
        self.__keys_press()

        self.__move_all()

        self.__collisions()

        self.__screen.set_score(self.__score)

        if self.__game_over():
            self.__screen.end_game()
            sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
