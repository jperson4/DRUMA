import mido    
    
def main():
    inputs = mido.get_input_names()
    for i, input_name in enumerate(inputs):
        print(f"{i}: {input_name}")
    selected = int(input("Selecciona un dispositivo: "))
    with mido.open_input(inputs[selected]) as inport:
        for msg in inport:
            print(msg)
    
if __name__ == "__main__":
    main()