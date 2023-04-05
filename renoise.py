###
# Midi Mapping like Renoise, basic style piano roll
# (Added a lower note so that C4 root sits in an easy place)
###

import usb_midi
import adafruit_midi
from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

keybow = PMK(Hardware())
keys = keybow.keys
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

rgb = (255, 0, 0)
rgb_off = (25, 25, 25)
velocity = 127

note_map = [
    'B2', 'F3', 'C4', 'G4',
    'C3', 'G3', 'D4', 'A4',
    'D3', 'A3', 'E4', 'B4',
    'E3', 'B3', 'F4', 'C5',
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
