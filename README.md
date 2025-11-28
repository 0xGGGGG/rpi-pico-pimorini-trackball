# Joaquina's Trackball

This project uses circuitpython with raspberry pi pico wh to control a trackball (pimo).

- raspberry pi pico wh (rp2040): https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico-1-family
- pimorini trackball breakout: https://shop.pimoroni.com/products/trackball-breakout?variant=27672765038675
- circuitpython: https://circuitpython.org/

You should be able to access the file system of pico as an external drive on macOS or Windows. The drive will appear as "CIRCUITPY" in File Explorer after connecting the Pico via USB to your computer.

### Device connection

- Connect the Raspberry Pi Pico WH to your computer via USB.
- If a drive named "CIRCUITPY" appears, CircuitPython is already installed. If "RPI-RP2" appears (or nothing appears), hold the BOOTSEL button while plugging in to enter bootloader mode.
- When CircuitPython is running, a serial device shows up as `/dev/tty.usbmodem*` on macOS (useful for REPL/logs).
- Pin reference (Pico W pinout), helpful for locating `GP0` (SDA), `GP1` (SCL), `3V3(OUT)`, and `GND`:

![Pimorini Trackball](https://shop.pimoroni.com/cdn/shop/products/Trackball_2_of_4_1500x1500_crop_center.JPG?v=1560173220)

![Raspberry Pi Pico W Pinout](https://www.raspberrypi.com/documentation/microcontrollers/images/picow-pinout.svg)

### Bootstrap

**1. Install CircuitPython on the Pico WH**

- Unplug USB. Hold BOOTSEL, plug USB in, then release. A drive named "RPI-RP2" appears.
- Download the UF2 for Pico W from the CircuitPython site: [CircuitPython for Pico W](https://circuitpython.org/board/raspberry_pi_pico_w/).
- Drag the `.uf2` onto "RPI-RP2". The board will reboot as "CIRCUITPY".
- Optional: open `CIRCUITPY/boot_out.txt` and note the CircuitPython version (for matching libraries).

**2. Add the minimal library**

- Download the matching "mpy" library bundle: [CircuitPython Library Bundle](https://circuitpython.org/libraries).
- On "CIRCUITPY", create a `lib` folder (if missing).
- Copy only `adafruit_hid/` into `CIRCUITPY/lib/`. Do not copy the whole bundle, as it causes raspberry pi pico to go out of memory.

**3. Copy project files**

- Copy `trackball/code.py` to `CIRCUITPY/code.py`.
- Copy `trackball/settings.toml` to the root of "CIRCUITPY".

**4. Wire the Pimoroni Trackball (I2C)**

- VCC → Pico 3V3(OUT)
- GND → Pico GND
- SDA → Pico `GP0`
- SCL → Pico `GP1`
- The code expects I2C address `0x0A`.

**5. Test & Confirm**

- The trackball LED should set to `DEFAULT_COLOR`.
- Moving the ball should move your computer cursor (HID mouse).
- Adjust `TRACKBALL_SENSITIVITY` in `settings.toml` as needed. Save to auto‑reload.

### Changing settings

There are a few settings that can be changed in the settings.toml file without needing to change the code file. This is useful for changing the color of the trackball and the sensitivity of the trackball.

Here are the settings that can be changed:

- DEFAULT_COLOR_R: The red component of the default color of the trackball.
- DEFAULT_COLOR_G: The green component of the default color of the trackball.
- DEFAULT_COLOR_B: The blue component of the default color of the trackball.
- TRACKBALL_SENSITIVITY: The sensitivity of the trackball.

You can change the settings.toml file directly in the drive. If you see a flashing led on the raspberry pi pico board that means settings have changed, being restarted and you should be able to see the changes in the trackball.

If you don't see the changes or not sure if they are affected, you can always try unplugging the pico and plugging it back in.

### Changing the code

You can change the code in the code.py file directly in the drive. If you see a flashing led on the raspberry pi pico board that means code has changed and being restarted.

If you don't see the changes or not sure if they are affected, you can always try unplugging the pico and plugging it back in.

There is also a backup copy of the `code.py` file in the drive called `code_backup.py`. You can use this to restore the code to the original state. **PLEASE DON'T CHANGE OR DELETE THIS FILE.**
