from djitellopy import Tello
from time import sleep

tello = Tello()

tello.connect()
print(tello.get_battery())
#tello.takeoff()
#sleep(1)
#tello.land()



