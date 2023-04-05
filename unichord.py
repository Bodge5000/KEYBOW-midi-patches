###
# Inspired by Omnichord
# 4 banks of chords, major, minor, 7th and sus4
###

from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

keybow = PMK(Hardware())
keys = keybow.keys
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

rgb = (255, 255, 255)
start_note = 45
velocity = 127

# Notes
# Uses F, C, G, D
note_map = [
    [62, 67, 69, 72, 76], [62, 66, 69, 72], [62, 65, 69], [62, 66, 69],
    [67, 72, 74, 77, 81], [67, 71, 74, 77], [67, 70, 74], [67, 71, 74],
    [60, 65, 67, 70, 74], [60, 64, 67, 70], [60, 63, 67], [60, 64, 67],
    [65, 70, 72, 75, 79], [65, 69, 72, 75], [65, 68, 72], [65, 69, 72],
]

lighting_map = [
    (255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255),
]

for key in keys:
    key.set_led(*lighting_map[key.number])

while True:
    keybow.update()
    for key in keys:
        @keybow.on_press(key)
        def press_handler(key):
            key.set_led(*rgb)
            midi.send([NoteOn(a, velocity) for a in note_map[key.number]])

        @keybow.on_release(key)
        def release_handler(key):
            key.set_led(*lighting_map[key.number])
            midi.send([NoteOff(a, velocity) for a in note_map[key.number]])
