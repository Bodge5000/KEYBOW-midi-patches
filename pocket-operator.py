###
# Midi Mapping for Pocket Operator 28 Robot
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

rgb = (255, 0, 0)
rgb_off = (25, 25, 25)
start_note = 45
velocity = 127

note_map = [
    45, 52, 57, 64, 47, 53, 59, 65,
    48, 55, 60, 67, 50, 56, 62, 68,
]

for key in keys:
    key.set_led(*rgb_off)

while True:
    keybow.update()

    for key in keys:
        @keybow.on_press(key)
        def press_handler(key):
            note = note_map[key.number]
            key.set_led(*rgb)
            midi.send(NoteOn(note, velocity))

        @keybow.on_release(key)
        def release_handler(key):
            note = note_map[key.number]
            key.set_led(*rgb_off)
            midi.send(NoteOff(note, 0))
