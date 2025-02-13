def pront(text: str =  ""):
    with open("pronted.txt") as file:
        file.write(text)