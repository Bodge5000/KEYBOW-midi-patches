###
# 4 faders which control velocity of a constant note
# All 4 notes together play, in this case, a C 7th chord
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

rgb = (255, 255, 255)
rgb_off = (25, 25, 25)

# Set the off lighting
lighting_map_off = [
    (128, 0, 0), (128, 0, 0), (128, 0, 0), (128, 0, 0), #ch1 - red
    (0, 128, 0), (0, 128, 0), (0, 128, 0), (0, 128, 0), # ch2 - green
    (0, 0, 128), (0, 0, 128), (0, 0, 128), (0, 0, 128), # ch3 - blue
    (128, 0, 128), (128, 0, 128), (128, 0, 128), (128, 0, 128), # ch4 - yellow
]

# Set the initial velocities and notes
ch1_vel, ch1_note = 0, 60
ch2_vel, ch2_note = 0, 64
ch3_vel, ch3_note = 0, 67
ch4_vel, ch4_note = 0, 70

# Set the velocity and channel map
key_map = [
    (0, ch1_note), (35, ch1_note), (80, ch1_note), (127, ch1_note), 
    (0, ch2_note), (35, ch2_note), (80, ch2_note), (127, ch2_note),
    (0, ch3_note), (35, ch3_note), (80, ch3_note), (127, ch3_note),
    (0, ch4_note), (35, ch4_note), (80, ch4_note), (127, ch4_note),
]

for key in keys:
    key.set_led(*lighting_map_off[key.number])

while True:
    keybow.update()
    for key in keys:
        @keybow.on_press(key)
        def press_handler(key):
            vel, note = key_map[key.number]
            key.set_led(*rgb)
            midi.send(NoteOff(note))
            midi.send(NoteOn(note, vel))
        
        @keybow.on_release(key)
        def release_handler(key):
            key.set_led(*lighting_map_off[key.number])
