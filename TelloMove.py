# Importing arcade module
import logging

import arcade
from djitellopy import Tello
import cv2

from threading import Thread



# Creating MainGame class
class TelloDrone(arcade.Window):
    HANDLER = logging.StreamHandler()
    FORMATTER = logging.Formatter('[%(levelname)s] %(filename)s - %(lineno)d - %(message)s')
    HANDLER.setFormatter(FORMATTER)

    LOGGER = logging.getLogger('tello')
    LOGGER.addHandler(HANDLER)
    LOGGER.setLevel(logging.INFO)

    def __init__(self):

        super().__init__(600, 600, title="Drone Movement")

        arcade.set_background_color(arcade.color.BLACK)

        # status of the cam
        self.isCamOn = False
        # status of the drone
        self.isDroneOn = False

        # x / y coordinates of the UI
        self.x = 250
        self.y = 250

        # x / y coordinates of the drone
        self.vel_x = 0
        self.vel_y = 0

        # previous x / y coordinates of the drone
        self.vel_prev_x = 0
        self.vel_prev_y = 0

    # -------------------------------------------------------------------------------------------------------------------
    # controls drone
    # -------------------------------------------------------------------------------------------------------------------

    def startDrone(self):
        # connects to drone
        self.tello = Tello()
        t1 = Thread(target=self.connect)
        t1.start()

    def connect(self):
        try:
            self.tello.connect()
            self.LOGGER.info('Battery % {}'.format(self.tello.get_battery()))
            self.stabilize()
            self.isDroneOn = True;

            # starts cam stream
            try:
                self.tello.streamon()
                self.img = self.get_image()
                self.isCamOn = True
            except Exception as c:
                self.LOGGER.error(c)
                self.isCamOn = False

        except Exception as d:
            self.LOGGER.error(d)
            self.isDroneOn = False
            self.isCamOn = False

    def take_off(self):
        if self.isDroneOn:
            self.LOGGER.info("Drone taking off...")
            try:
                self.tello.takeoff()
                self.LOGGER.info("Drone took off")
                self.stabilize()

            except Exception as d:
                self.LOGGER.error(d)
                self.LOGGER.warning("Drone failed to take off")
                self.isDroneOn = False
                self.isCamOn = False
        else:
            self.LOGGER.warning("Drone not available for take off")

    def stabilize(self):
        self.tello.send_rc_control(0, 0, 0, 0)

    def land(self):
        if self.isDroneOn:
            self.LOGGER.info("Drone landing...")
            try:
                self.tello.land()
                self.LOGGER.info("Drone landed")
            except Exception as d:
                self.LOGGER.error(d)
                self.LOGGER.warning("Drone failed to land")
                self.isDroneOn = False
                self.isCamOn = False
        else:
            self.LOGGER.warning("Drone not available for landing")

    # gets a drone cam frame
    def get_image(self):
        return cv2.resize(self.tello.get_frame_read().frame, (360, 240)) if self.isCamOn else None

    # -------------------------------------------------------------------------------------------------------------------
    # overrides UI commands
    # -------------------------------------------------------------------------------------------------------------------

    # Overrides on_draw() function to draw on the screen
    def on_draw(self):

        arcade.start_render()

        # Drawing the rectangle using draw_rectangle_filled function
        arcade.draw_circle_filled(self.x, self.y, 5, arcade.color.GRAY)

        # update img
        if self.isCamOn:
            cv2.imshow("Image", self.img)

    # overrides on_update
    def on_update(self, delta_time):

        uiCenter = 300

        if self.isDroneOn:

            # display
            self.x = uiCenter + self.vel_x
            self.y = uiCenter + self.vel_y

            # drone
            if (self.vel_x != self.vel_prev_x) or (self.vel_y != self.vel_prev_y):

                # drone
                self.LOGGER.info('x : {}, y : {}'.format(self.vel_x, self.vel_y))

                try:

                    # sends command
                    self.tello.send_rc_control(self.vel_x, self.vel_y, 0, 0)

                    # updates drone last values to current values
                    self.vel_prev_x = self.vel_x
                    self.vel_prev_y = self.vel_y

                except Exception as d:

                    # resets display
                    self.x = uiCenter + self.vel_prev_x
                    self.y = uiCenter + self.vel_prev_y

                    # resets the drone coordinates
                    self.vel_x = self.vel_prev_x
                    self.vel_y = self.vel_prev_y

                    # logs
                    self.LOGGER.error(d)
                    self.LOGGER.warning("Drone not able to get direction command")

                    self.land()

            # images
            self.img = self.get_image()

    #  handles keyboard events
    def on_key_press(self, symbol, modifier):

        maxValue = 99
        increments = 3;

        # Checking the button pressed
        # and changing the value of velocity

        if symbol == arcade.key.UP and self.vel_y < maxValue:
            self.vel_y += int(maxValue/increments)
            self.LOGGER.info("Up arrow key is pressed")
        elif symbol == arcade.key.DOWN and self.vel_y > -maxValue:
            self.vel_y -= int(maxValue/increments)
            self.LOGGER.info("Down arrow key is pressed")

        elif symbol == arcade.key.RIGHT and self.vel_x < maxValue:
            self.vel_x += int(maxValue/increments)
            self.LOGGER.info("Right arrow key is pressed")
        elif symbol == arcade.key.LEFT and self.vel_x > -maxValue:
            self.vel_x -= int(maxValue/increments)
            self.LOGGER.info("Left arrow key is pressed")

        elif symbol == arcade.key.SPACE:
            self.take_off()
        elif symbol == arcade.key.RETURN:
            self.land()
            self.tello.streamoff();
            self.tello.end()


# -------------------------------------------------------------------------------------------------------------------
# main
# -------------------------------------------------------------------------------------------------------------------


# Calling MainGame class
tello = TelloDrone()
tello.startDrone()
arcade.run()

