import time

import displayio
import pimoroni_trackball_circuitpy as tb
import terminalio
import usb_hid
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_hid.mouse import Mouse
from adafruit_macropad import MacroPad

old_coord = (0, 0, 0)
old_rotation = 0

m = Mouse(usb_hid.devices)

tb.set_leds_red()

macropad = MacroPad()

main_group = displayio.Group()
macropad.display.root_group = main_group

font = bitmap_font.load_font("firacode-regular.bdf")

font.load_glyphs("↑↓←→")

title = label.Label(
    y=4,
    font=font,
    color=0x0,
    text="   Interactions   ",
    background_color=0xFFFFFF,
)
layout = GridLayout(x=0, y=8, width=128, height=48, grid_size=(4, 4), cell_padding=0)
labels = []

for _ in range(16):
    labels.append(label.Label(font, text=""))

for index in range(16):
    x = index % 4
    y = index // 4
    layout.add_content(labels[index], grid_position=(x, y), cell_size=(1, 1))

main_group.append(title)
main_group.append(layout)

multiplier = 9

tb.set_leds_green()

lastSetTime = time.monotonic()

while True:
    macropad.encoder_switch_debounced.update()
    down, up, left, right, switch = tb.read()

    # Enact movements and clicks
    if switch:
        m.click(Mouse.LEFT_BUTTON)
        labels[11].text = f"BUTN"
        labels[15].text = f"   ↓"
        lastSetTime = time.monotonic()
    else:
        x = right - left
        y = down - up
        xmult = int(-x * multiplier)
        ymult = int(-y * multiplier)
        new_coord = (xmult, ymult, 0)
        if new_coord != old_coord:
            timeNow = time.monotonic()
            if timeNow - lastSetTime > 2:
                labels[11].text = f"MOUS"
                labels[15].text = f"↑↓←→"
                lastSetTime = time.monotonic()
        m.move(xmult, ymult, 0)

    timeNow = time.monotonic()

    # Check how many seconds have elapsed since the last mouse state change
    if timeNow - lastSetTime > 5:
        labels[11].text = f""
        labels[15].text = f""

    new_rotation = macropad.encoder

    if macropad.encoder_switch_debounced.pressed:
        if new_rotation < old_rotation:
            labels[3].text = f"KNOB"
            labels[7].text = f"←  ↓"
        elif new_rotation > old_rotation:
            labels[3].text = f"KNOB"
            labels[7].text = f"→  ↓"
        else:
            labels[3].text = f"KNOB"
            labels[7].text = f"   ↓"
        old_rotation = new_rotation
    if macropad.encoder_switch_debounced.released:
        labels[3].text = ""
        labels[7].text = ""
    key_event = macropad.keys.events.get()
    if key_event:
        knum = key_event.key_number
        if 2 < knum <= 5:
            num = knum + 1
        elif 5 < knum <= 8:
            num = knum + 2
        elif 8 < knum:
            num = knum + 3
        else:
            num = key_event.key_number
        txt = "KY"
        if key_event.key_number < 10:
            pvalue = f"0{key_event.key_number}"
        else:
            pvalue = str(key_event.key_number)
        if key_event.pressed:
            print((key_event.key_number, num))
            labels[num].text = f"{txt}{pvalue}"
        else:
            labels[num].text = ""
