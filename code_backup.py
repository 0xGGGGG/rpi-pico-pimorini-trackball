import os
import time
import board
import busio
from adafruit_hid.mouse import Mouse
import usb_hid

# USB HID mouse
mouse = Mouse(usb_hid.devices)

# Set up I2C (SDA = GP0, SCL = GP1)
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

# Trackball I2C address (default 0x0A)
TRACKBALL_ADDR = 0x0a

# Trackball register map
REG_LEFT = 0x04
REG_RIGHT = 0x05
REG_UP = 0x06
REG_DOWN = 0x07
REG_SWITCH = 0x08

# Register LED Base
REG_LED_BASE = 0x00

# Mouse State
SENSITIVITY = int(os.getenv("TRACKBALL_SENSITIVITY") or 5)
button_pressed = False      # Current press state
button_was_pressed = False  # Last cycle state

# LED State
DEFAULT_COLOR = tuple(
    int(v) if (v := os.getenv(k)) not in (None, "") else 255
    for k in ("DEFAULT_COLOR_R", "DEFAULT_COLOR_G", "DEFAULT_COLOR_B")
)
COLOR_LIST = [
    DEFAULT_COLOR
]

def read_trackball():
    """Read all directions and button state from the trackball."""
    while not i2c.try_lock():
        pass
    try:
        data = bytearray(5)
        i2c.writeto_then_readfrom(TRACKBALL_ADDR, bytes([REG_LEFT]), data)
        left, right, up, down, switch = data
        return left, right, up, down, switch
    except Exception as e:
        print("I2C read error:", e)
        return 0, 0, 0, 0, 0
    finally:
        i2c.unlock()


def set_rgbw(red, green, blue, white=0):
    """Set RGB color of the trackball LED."""
    while not i2c.try_lock():
        pass
    try:
        data = bytes([REG_LED_BASE, red, green, blue, white])
        i2c.writeto(TRACKBALL_ADDR, data, start=0)
    finally:
        i2c.unlock()


def fade_rgbw(current, target, step=10):
    """Slowly transitions rgb color tuple from current to target by the given step"""
    new_color = []

    for c, t in zip(current, target):
        if c < t:
            c = min(c + step, t)
        elif c > t:
            c = max(c - step, t)

        new_color.append(c)

    return tuple(new_color)


# Set the default color
set_rgbw(*DEFAULT_COLOR)


# Main loop
while True:
    left, right, up, down, switch = read_trackball()

    # Mouse movement
    dx = (right - left) * SENSITIVITY
    dy = (down - up) * SENSITIVITY

    if dx != 0 or dy != 0:
        mouse.move(x=dx, y=dy)

    if switch & 0x01:
        mouse.press(Mouse.LEFT_BUTTON)
    else:
        mouse.release(Mouse.LEFT_BUTTON)


    # Button press
    button_pressed = bool(switch & 0x01)

    # Uncomment if you want to cycle through colors
    # if button_pressed and not button_was_pressed:
    #     color_index = (color_index + 1) % len(COLOR_LIST)
    #     set_rgbw(*COLOR_LIST[color_index])


    button_was_pressed = button_pressed

    time.sleep(0.01)
