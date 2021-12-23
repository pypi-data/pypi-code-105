import irccodes.constants


def colored(text, color, background_color=None):
    text_color_code = str(getattr(constants, color.replace(' ', '').upper()))
    if background_color is not None:
        background_color_code = ',' + str(getattr(constants, background_color.replace(' ', '').upper()))
    else:
        background_color_code = ''
    color_code = chr(constants.COLOR) + text_color_code + background_color_code
    return color_code + text + chr(constants.COLOR)


def bold(text):
    return chr(constants.BOLD) + text + chr(constants.BOLD)


def italic(text):
    return chr(constants.ITALIC) + text + chr(constants.ITALIC)


def strikethrough(text):
    return chr(constants.STRIKETHROUGH) + text + chr(constants.STRIKETHROUGH)


def underline(text):
    return chr(constants.UNDERLINE) + text + chr(constants.UNDERLINE)


def underline2(text):
    return chr(constants.UNDERLINE2) + text + chr(constants.UNDERLINE2)


def reverse(text):
    return chr(constants.REVERSE) + text + chr(constants.REVERSE)


def reset():
    return chr(constants.RESET)
