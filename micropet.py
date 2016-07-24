# """
# A nice little digital pet for you to look after.
# By Zeth
# Press button A to feed your pet.
# Press button B to test your pet's blood glucose level.
# Shake to exercise your pet.
# Press A and B to play ball, press a button to go back
# to normal mode
# """
# pylint: disable=missing-docstring
import random
import microbit  # pylint: disable=import-error
INTERVAL = 5000

HAPPY = microbit.Image(
    "09090:"
    "00000:"
    "00000:"
    "90009:"
    "09990")

RIGHT = microbit.Image(
    "90900:"
    "00000:"
    "00000:"
    "90009:"
    "09990")

LEFT = microbit.Image(
    "00909:"
    "00000:"
    "00000:"
    "90009:"
    "09990")

MOUTH_OPEN = microbit.Image(
    "09090:"
    "00000:"
    "09990:"
    "90009:"
    "09990")

MOUTH_CLOSED = microbit.Image(
    "09090:"
    "00000:"
    "00000:"
    "09990:"
    "00000")

SLEEP = microbit.Image(
    "99099:"
    "00000:"
    "00000:"
    "09990:"
    "00000")


class Game(object):
    # """Play ball with your pet."""
    def __init__(self):
        self.last = None
        self.x_pos = 0
        self.y_pos = 0
        microbit.display.scroll("Catch the ball")
        self.draw()

    def draw(self):
        # """Redraw the screen."""
        image = microbit.Image(
            "00000:"
            "00000:"
            "00500:"
            "00000:"
            "00000")
        image.set_pixel(self.x_pos, self.y_pos, 9)
        microbit.display.show(image)

    def start(self):
        # """Start the game running."""
        while True:
            self.check_win()
            self.check_direction()
            if microbit.button_a.is_pressed():
                break
            if microbit.button_b.is_pressed():
                break

    def make_new_spot(self):
        # """Put the spot in new location."""
        self.x_pos = random.randrange(5)
        self.y_pos = random.randrange(5)
        if self.x_pos == 2 and self.y_pos == 2:
            self.x_pos = 4
            self.y_pos = 4

    def check_win(self):
        if self.x_pos == 2 and self.y_pos == 2:
            microbit.display.show(microbit.Image.HEART)
            microbit.sleep(2000)
            self.make_new_spot()
            self.draw()

    def check_direction(self):
        # """Check direction of the microbit."""
        gesture = microbit.accelerometer.current_gesture()
        if gesture == self.last:
            return
        if gesture == "up":
            if self.y_pos < 4:
                self.y_pos += 1
        elif gesture == "down":
            if self.y_pos > 0:
                self.y_pos -= 1
        elif gesture == "left":
            if self.x_pos > 0:
                self.x_pos -= 1
        elif gesture == "right":
            if self.x_pos < 4:
                self.x_pos += 1
        else:
            return
        self.last = gesture
        self.draw()


class Pet(object):
    # """Digital Pet."""
    def __init__(self):
        self.last_time = 0
        self.happy()
        self.action = False
        self.bgl = 6.5

    def happy(self):
        # """Show happy face."""
        microbit.display.show(HAPPY)
        self.action = False

    def sad(self):
        # """Show Sad face."""
        microbit.display.show(microbit.Image.ANGRY)
        self.action = False

    def asleep(self):
        # """Show sleepy face."""
        microbit.display.show(SLEEP)
        self.action = False

    def surprised(self):
        # """Set surprised face."""
        microbit.display.show(microbit.Image.SURPRISED)
        self.action = True
        if self.bgl > 4:
            self.bgl -= 0.1

    def tick(self):
        # """Perform action."""
        if self.bgl > 0:
            self.bgl -= 0.1
        self.set_face()

    def set_face(self):
        # """Set the face."""
        if self.bgl < 4:
            # Too low blood sugar
            self.sad()
        elif self.bgl > 8:
            # Too high blood sugar
            self.asleep()
        else:
            self.happy()

    def check_gesture(self):
        # """Check the accelerometer for what is going on."""
        gesture = microbit.accelerometer.current_gesture()
        if gesture == "shake":
            self.surprised()
        elif gesture == "face down":
            microbit.display.show(microbit.Image.CONFUSED)
            self.action = True
        elif gesture == "left":
            microbit.display.show(LEFT)
            self.action = True
        elif gesture == "right":
            microbit.display.show(RIGHT)
            self.action = True
        else:
            if self.action:
                self.set_face()

    def check_button(self):
        # """Check the buttons for what is going on."""
        if microbit.button_a.is_pressed() and microbit.button_b.is_pressed():
            # play game
            self.play()
        elif microbit.button_a.is_pressed():
            self.bgl += 1
            microbit.display.show(
                [MOUTH_OPEN, MOUTH_CLOSED, MOUTH_OPEN, MOUTH_CLOSED],
                delay=300)
            self.set_face()
        elif microbit.button_b.is_pressed():
            microbit.display.scroll("{0:0.1f}".format(self.bgl))

    def check_death(self):
        # """Check if BGL is really out of range."""
        if self.bgl < 1:
            # Heart Attack
            microbit.display.show(microbit.Image.SKULL)
            return True
        elif self.bgl > 30:
            # Coma
            microbit.display.show(microbit.Image.GHOST)
            return True
        return False

    def wait(self):
        # """Wait for something to happen."""
        while True:
            if self.check_death():
                break
            self.check_gesture()
            self.check_button()
            current = microbit.running_time()
            delta = current - self.last_time
            if delta > INTERVAL:
                self.last_time = current
                self.tick()

    def play(self):
        # """Play a game with your pet."""
        game = Game()
        game.start()

if __name__ == '__main__':
    PET = Pet()
    PET.wait()
