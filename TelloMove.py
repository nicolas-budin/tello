# Importing arcade module
import arcade
from djitellopy import Tello
import cv2

# Creating MainGame class
class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(600, 600, title="Drone Movement")

        # Initializing the initial x and y coordinated
        self.x = 250
        self.y = 250

        # Initializing a variable to store the velocity of the player
        self.vel_x = 0
        self.vel_y = 0

        # connects to drone
        self.tello = Tello()
        self.tello.connect()
        print(self.tello.get_battery())

        # starts cam stream
        self.tello.streamon();
        self.img = self.get_image()

    # Creating on_draw() function to draw on the screen
    def on_draw(self):
        arcade.start_render()

        # Drawing the rectangle using draw_rectangle_filled function
        arcade.draw_circle_filled(self.x, self.y, 25, arcade.color.GREEN)

        # update img
        cv2.imshow("Image", self.img)

    # Creating on_update function to
    # update the x coordinate
    def on_update(self, delta_time):
        self.x += self.vel_x * delta_time
        self.y += self.vel_y * delta_time

        self.img = self.get_image()

    def get_image(self):
        return cv2.resize(self.tello.get_frame_read().frame, (360, 240))

    # Creating function to change the velocity
    # when button is pressed
    def on_key_press(self, symbol, modifier):

        # Checking the button pressed
        # and changing the value of velocity
        if symbol == arcade.key.UP:
            self.vel_y = 300
            print("Up arrow key is pressed")
        elif symbol == arcade.key.DOWN:
            self.vel_y = -300
            print("Down arrow key is pressed")
        elif symbol == arcade.key.LEFT:
            self.vel_x = -300
            print("Left arrow key is pressed")
        elif symbol == arcade.key.RIGHT:
            self.vel_x = 300
            print("Right arrow key is pressed")
        elif symbol == arcade.key.SPACE:
            print("Drone taking off...")
            self.tello.takeoff()
            print("Drone took off")
        elif symbol == arcade.key.RETURN:
            print("Drone landing...")
            self.tello.land()
            self.tello.land()
            print("Drone landed")



    def on_key_release(self, symbol, modifier):

        # Checking the button released
        # and changing the value of velocity
        if symbol == arcade.key.UP:
            self.vel_y = 0
        elif symbol == arcade.key.DOWN:
            self.vel_y = 0
        elif symbol == arcade.key.LEFT:
            self.vel_x = 0
        elif symbol == arcade.key.RIGHT:
            self.vel_x = 0


# Calling MainGame class
MainGame()
arcade.run()
