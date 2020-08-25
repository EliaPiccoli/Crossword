import crossword as c

def _svg_header():
    return '<svg xmlns="http://www.w3.org/2000/svg"></svg>'

def _empty_rect(rect_x, rect_y, width=100, height=100):
    tag = "<rect></rect>"
    x = ' x="{}"'.format(rect_x)
    y = ' y="{}"'.format(rect_y)
    w = ' width="{}"'.format(width)
    h = ' height="{}"'.format(height)
    color = ' fill="white"'
    border = ' stroke-width="2" stroke="black"'

    return tag[:5] + x + y + w + h + color + border + tag[5:]

def _numbered_rect(rect_x, rect_y, text, width=100, height=100):
    group = "<g></g>"
    rect = _empty_rect(rect_x, rect_y, width, height)
    text_tag = "<text></text>"
    text_x = ' x="{}"'.format(rect_x + 5)
    text_y = ' y="{}"'.format(rect_y + 15)
    text_style = ' font-family="Times New Roman" fill="black" font-size="15"'

    return group[:3] + rect + text_tag[:5] + text_x + text_y + text_style + text_tag[5] + str(text) + text_tag[6:] + group[3:]


if __name__ == "__main__":
    field, edges, wordorder = c.create_crossword(c._get_words_file())
    print(_empty_rect(10, 10))
    print(_numbered_rect(10, 10, 1))