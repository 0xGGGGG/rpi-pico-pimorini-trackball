import time
from pimoroni_i2c import PimoroniI2C
from breakout_trackball import BreakoutTrackball

PINS_BREAKOUT_GARDEN = {"sda": 0, "scl": 1, "baudrate": 100000}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21, "baudrate": 100000}

sensitivity = 2

print("try loading trackball")

i2c = PimoroniI2C(**PINS_BREAKOUT_GARDEN)

print("should have loaded i2c")

trackball = BreakoutTrackball(i2c)
print("initialized trackball")

trackball.set_rgbw(0, 0, 0, 64)

print("Roll the trackball to change colour!")

while True:
    state = trackball.read()
    
    if state[BreakoutTrackball.SW_PRESSED]:
        trackball.set_rgbw(0, 0, 0, 255)
        print("trackball: PRESSED")
    elif state[BreakoutTrackball.LEFT] > sensitivity:
        trackball.set_rgbw(0, 0, 255, 0)
        print("trackball: LEFT")
    elif state[BreakoutTrackball.RIGHT] > sensitivity:
        trackball.set_rgbw(255, 0, 0, 0)
        print("trackball: RIGHT")
    elif state[BreakoutTrackball.UP] > sensitivity:
        trackball.set_rgbw(255, 255, 0, 0)
        print("trackball: UP")
    elif state[BreakoutTrackball.DOWN] > sensitivity:
        trackball.set_rgbw(0, 255, 0, 0)
        print("trackball: DOWN")
    elif state[BreakoutTrackball.SW_CHANGED]:
        trackball.set_rgbw(0, 0, 0, 64)
        print("trackball: SW CHANGED")

    time.sleep(0.02)