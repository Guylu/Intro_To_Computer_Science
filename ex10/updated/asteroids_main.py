from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo, SpecialTorpedo
import random
import math

DEFAULT_ASTEROIDS_NUM = 5
MAX_SPECIAL = 5
INITIAL_X_SPEED = 0
INITIAL_Y_SPEED = 0
INITIAL_DEG = 0
X_POS = 0
Y_POS = 1
LIFE = 3


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__torpedos = []
        self.__special_shoots = []
        self.__asteroids = []
        self.__ships_smashed = 0
        self.__score = 0

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # our code:
        x_rnd = random.randint(self.__screen_min_x, self.__screen_max_x)
        y_rnd = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__ship = Ship(x_rnd, INITIAL_X_SPEED,
                           y_rnd, INITIAL_Y_SPEED, INITIAL_DEG)

        if asteroids_amount is None:
            asteroids_amount = DEFAULT_ASTEROIDS_NUM
        self.__init_rand_asteroids(asteroids_amount)

    def __init_rand_asteroids(self, amount):
        while len(self.__asteroids) < amount:
            x_rnd = random.randint(self.__screen_min_x, self.__screen_max_x)
            y_rnd = random.randint(self.__screen_min_y, self.__screen_max_y)
            x_speed_rnd = random.randint(1, 4)
            y_speed_rnd = random.randint(1, 4)

            if (x_rnd, y_rnd) == self.__ship.get_location():
                continue

            a = Asteroid(x_rnd, x_speed_rnd, y_rnd, y_speed_rnd, 3)
            self.__asteroids.append(a)
            self.__screen.register_asteroid(a, a.get_size())

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # Your code goes here
        x, y = self.__ship.get_location()
        self.__screen.draw_ship(x, y, self.__ship.get_deg())
        self.move_object(self.__ship)
        self.keys_press()
        self.asteroid_draw(self.__asteroids)
        self.asteroids_move(self.__asteroids)

        self.torpedo_move()
        self.torpedo_draw(self.__torpedos)
        self.torpedo_draw(self.__special_shoots)

        for tor in self.__torpedos:
            smashedroid = self.check_collision(tor)
            if smashedroid:
                # remove tor and create new asteroids
                self.tor_smash(tor, smashedroid, self.__torpedos)

        for tor in self.__special_shoots:
            smashedroid = self.check_collision(tor)
            if smashedroid:
                # remove tor and create new asteroids
                self.tor_smash(tor, smashedroid, self.__special_shoots)

        if self.check_collision(self.__ship):
            self.__screen.remove_life()
            self.__ships_smashed += 1
            self.__screen.show_message("SMASH!", "you hit an asteroid -1 life")

        self.__screen.set_score(self.__score)

        if self.game_over():
            self.__screen.end_game()
            sys.exit()

    def game_over(self):
        if self.__ships_smashed == LIFE:
            self.__screen.show_message("Game Over!", "bye bye")
            return True

        if len(self.__asteroids) == 0:
            self.__screen.show_message("You Win!", "hura!")
            return True

        if self.__screen.should_end():
            self.__screen.show_message("That's it?", "bye bye :(")
            return True

        return False

    def tor_smash(self, tor, smashedroid, shoots_list):
        self.__screen.unregister_torpedo(tor)
        shoots_list.remove(tor)

        smashedroid_size = smashedroid.get_size()
        if smashedroid_size == 3:
            self.__score += 20
        elif smashedroid_size == 2:
            self.__score += 50
        elif smashedroid_size == 1:
            self.__score += 100
            return

        delta = math.sqrt(smashedroid.get_speed()[X_POS] ** 2 +
                          smashedroid.get_speed()[Y_POS] ** 2)
        x_speed = (tor.get_speed()[X_POS] + smashedroid.get_speed()[X_POS]) / \
                  delta
        y_speed = (tor.get_speed()[Y_POS] + smashedroid.get_speed()[Y_POS]) / \
                  delta

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

    def torpedo_draw(self, torpedos):
        remove_us = []
        for tor in torpedos:
            self.__screen.draw_torpedo(tor, tor.get_location()[0],
                                       tor.get_location()[1], tor.get_deg())

            if not tor.reduce():
                remove_us.append(tor)

        for tor in remove_us:
            self.__screen.unregister_torpedo(tor)
            torpedos.remove(tor)

    def torpedo_move(self):
        for tor in self.__torpedos:
            self.move_object(tor)

        asteroid = self.__asteroids[0]
        for tor in self.__special_shoots:
            tor.recalibrate(*asteroid.get_location(), *asteroid.get_speed())
            self.move_object(tor)

    def check_collision(self, target):
        for curr_asteroid in self.__asteroids:
            if curr_asteroid.has_intersection(target):
                self.__screen.unregister_asteroid(curr_asteroid)
                self.__asteroids.remove(curr_asteroid)
                return curr_asteroid
        return None

    def asteroids_move(self, asteroids):
        for asteroid in asteroids:
            self.move_object(asteroid)

    def asteroid_draw(self, asteroids):
        for asteroid in asteroids:
            self.__screen.draw_asteroid(asteroid,
                                        asteroid.get_location()[0],
                                        asteroid.get_location()[1])

    def keys_press(self):
        if self.__screen.is_left_pressed():
            self.rotate_ship(0)

        if self.__screen.is_right_pressed():
            self.rotate_ship(1)

        elif self.__screen.is_up_pressed():
            self.accelerate_ship()

        elif self.__screen.is_space_pressed():
            self.shoot()

        elif self.__screen.is_special_pressed():
            self.shoot(is_special=True)

        elif self.__screen.is_teleport_pressed():
            self.teleportation()

    def teleportation_location_valid(self):
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(self.__ship):
                return False

        return True

    def teleportation(self):
        while True:
            x_rnd = random.randint(self.__screen_min_x, self.__screen_max_x)
            y_rnd = random.randint(self.__screen_min_y, self.__screen_max_y)

            self.__ship.set_location(x_rnd, y_rnd)
            if not self.teleportation_location_valid():
                print("bad location")
                continue

            return

    def shoot(self, is_special=False):
        if ((len(self.__torpedos) == 10 and not is_special) or
                (len(self.__special_shoots) == MAX_SPECIAL and is_special)):
            return

        x = self.__ship.get_location()[0]
        y = self.__ship.get_location()[1]
        old_x_speed = self.__ship.get_speed()[0]
        old_y_speed = self.__ship.get_speed()[1]
        deg = self.__ship.get_deg()
        new_x_speed = old_x_speed + 2 * math.cos(deg * math.pi / 180)
        new_y_speed = old_y_speed + 2 * math.sin(deg * math.pi / 180)

        tor = Torpedo(x, new_x_speed, y, new_y_speed, deg) if not is_special \
            else\
            SpecialTorpedo(x, new_x_speed, y, new_y_speed, deg)
        self.__screen.register_torpedo(tor)

        if is_special:
            self.__special_shoots.append(tor)
        else:
            self.__torpedos.append(tor)

    def accelerate_ship(self):
        new_x_speed = self.__ship.get_speed()[0] + math.cos(
            self.__ship.get_deg() *
            math.pi / 180)
        new_y_speed = self.__ship.get_speed()[1] + math.sin(
            self.__ship.get_deg() *
            math.pi / 180)
        self.__ship.set_speed(new_x_speed, new_y_speed)

    def rotate_ship(self, direction):
        if direction == 1:
            self.__ship.add_deg(-7)
        else:
            self.__ship.add_deg(7)

    def move_object(self, ob):
        new_x = (ob.get_speed()[0] + ob.get_location()[0] -
                 self.__screen_min_x) % \
                (self.__screen_max_x - self.__screen_min_x) + \
                self.__screen_min_x
        new_y = (ob.get_speed()[1] + ob.get_location()[1] -
                 self.__screen_min_y) % \
                (self.__screen_max_y - self.__screen_min_y) + \
                self.__screen_min_y

        ob.set_location(new_x, new_y)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
