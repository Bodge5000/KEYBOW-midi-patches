###
# Not an actual patch!
# Used for mapping logic note layout (starting at bottom left) to actual
###

def logic_to_actual(mymap):
    logic = [
        0, 1, 2, 3, 4, 5, 6, 7,
        8, 9, 10, 11, 12, 13, 14, 15,
    ]

    actual = [
        0, 4, 8, 12,
        1, 5, 9, 13,
        2, 6, 10, 14,
        3, 7, 11, 15
    ]
    
    output = [0] * 16

    for i in logic:
        correct_index = actual.index(i)
        output[correct_index] = mymap[i]
    
    return output

# -------------------------------------------------

# Change this to whatever you want to map

map = [
    "B2", "C3", "D3", "E3", 
    "F3", "G3", "A3", "B3",
    "C4", "D4", "E4", "F4",
    "G4", "A4", "B4", "C5"
]

print(logic_to_actual(map))
