colours = {
    "red": (196, 0, 0),
    "yellow": (202, 211, 19),
    "green": (38, 181, 36),
    "white": (255, 255, 255),
    "black": (2, 2, 2),
    "gray": (158, 158, 158),
    "grog": (102, 160, 255),
    "menu_bg": (158, 158, 158, 150),
}

possible_colours = ["red", "yellow", "green"]


def next_color(current):
    index = 0
    for i in range(0, len(possible_colours)):
        if current == colours[possible_colours[i]]:
            index = i
            break

    if index + 1 == len(possible_colours):
        return colours[possible_colours[0]]

    return colours[possible_colours[index + 1]]
