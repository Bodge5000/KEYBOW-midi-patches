###
# Generates a grid of random notes, going higher in pitch
# To avoid repetition, a random base note is chosen
# and each subsequent note randomly 1-3 higher than the last
###

import random
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
start_note = 45
velocity = 127

# Create an empty array for notes with a size of 16
note_map = [0] * 16

# Create random array of notes and sort them
# It will try 64 times to get a unique number
values = []
base_note = random.randint(36, 80)
current_note = base_note
for _ in range(16):
    values.append(current_note)
    current_note += random.randint(1, 3)
values.sort(reverse=True)

# Setup 2 mappings
# my_map is how the above will map it (also how it logically should be mapped :/)
# real_map is how its actually mapped
my_map = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16,
]

real_map = [
    16, 12, 8, 4,
    15, 11, 7, 3,
    14, 10, 6, 2,
    13, 9, 5, 1,
]

# Map the correct values to the notes array according to the real_map
for i in my_map:
    correct_index = real_map.index(i)
    note_map[correct_index] = values[my_map.index(i)]


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
