# Importing arcade module
import logging

import arcade
from djitellopy import Tello
import cv2


# Creating MainGame class
class MainGame(arcade.Window):


    HANDLER = logging.StreamHandler()
    FORMATTER = logging.Formatter('[%(levelname)s] %(filename)s - %(lineno)d - %(message)s')
    HANDLER.setFormatter(FORMATTER)

    LOGGER = logging.getLogger('tello')
    LOGGER.addHandler(HANDLER)
    LOGGER.setLevel(logging.INFO)

    def __init__(self):
        super().__init__(600, 600, title="Drone Movement")

        self.isCamOn = False;
        self.isDroneOn = False;

        # Initializing the initial x and y coordinated
        self.x = 250
        self.y = 250

        # Initializing a variable to store the velocity of the player
        self.vel_x = 0
        self.vel_y = 0

        self.vel_prev_x = 0
        self.vel_prev_y = 0

        # connects to drone
        self.tello = Tello()

        try:
            self.tello.connect()

            self.LOGGER.info('Battery % {}'.format(self.tello.get_battery()))

            # starts cam stream
            try:
                self.tello.streamon();
                self.img = self.get_image()
            except Exception as c:
                self.LOGGER.error(c)
                self.isCamOn = False

        except Exception as d:
            self.LOGGER.error(d)
            self.isDroneOn = False;
            self.isCamOn = False

    # Creating on_draw() function to draw on the screen
    def on_draw(self):

        arcade.start_render()

        # Drawing the rectangle using draw_rectangle_filled function
        arcade.draw_circle_filled(self.x, self.y, 5, arcade.color.GRAY)

        # update img
        if self.isCamOn:
            cv2.imshow("Image", self.img)

    # Creating on_update function to
    # update the x coordinate
    def on_update(self, delta_time):

        # display
        self.x = 300 + self.vel_x * 10
        self.y = 300 + self.vel_y * 10

        # drone
        if (self.vel_x != self.vel_prev_x) or (self.vel_y != self.vel_prev_y):

            self.vel_prev_x = self.vel_x
            self.vel_prev_y = self.vel_y

            # drone
            self.LOGGER.info('x : {}, y : {}'.format(self.vel_x, self.vel_y))
            if self.isDroneOn:
                try:
                    self.tello.send_rc_control(self.vel_x, self.vel_y)
                except Exception as d:
                    self.LOGGER.error(d)
                    self.LOGGER.warning("Drone not able to get direction command")
                    self.isDroneOn = False;
                    self.isCamOn = False
            else:
                self.LOGGER.warning("Drone not available for direction command")

        # images
        self.img = self.get_image()

    def get_image(self):
        return cv2.resize(self.tello.get_frame_read().frame, (360, 240)) if self.isCamOn else None

    def takeOff(self):
        if self.isDroneOn:
            self.LOGGER.info("Drone taking off...")
            try:
                self.tello.takeoff()
                self.LOGGER.info("Drone took off")
            except Exception as d:
                self.LOGGER.error(d)
                self.LOGGER.warning("Drone failed to take off")
                self.isDroneOn = False;
                self.isCamOn = False
        else:
            self.LOGGER.warning("Drone not available for take off")

    def land(self):
        if self.isDroneOn:
            self.LOGGER.info("Drone landing...")
            try:
                self.tello.land()
                self.LOGGER.info("Drone landed")
            except Exception as d:
                self.LOGGER.error(d)
                self.LOGGER.warning("Drone failed to land")
                self.isDroneOn = False;
                self.isCamOn = False
        else:
            self.LOGGER.warning("Drone not available for landing")

    # Creating function to change the velocity
    # when button is pressed
    def on_key_press(self, symbol, modifier):

        # Checking the button pressed
        # and changing the value of velocity
        if symbol == arcade.key.UP:
            self.vel_y += 10
            self.LOGGER.info("Up arrow key is pressed")
        elif symbol == arcade.key.DOWN:
            self.vel_y -= 10
            self.LOGGER.info("Down arrow key is pressed")
        elif symbol == arcade.key.LEFT:
            self.vel_x -= 10
            self.LOGGER.info("Left arrow key is pressed")
        elif symbol == arcade.key.RIGHT:
            self.vel_x += 10
            self.LOGGER.info("Right arrow key is pressed")
        elif symbol == arcade.key.SPACE:
            self.takeOff()
        elif symbol == arcade.key.RETURN:
            self.land()


# Calling MainGame class
MainGame()
arcade.run()
