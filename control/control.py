import mido

# Recibe el imput del midi

with mido.open_input() as inport:
    for msg in inport:
        print(msg)