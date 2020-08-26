import crossword as c
import os

def _svg_header(edges, size):
    w = ' width="{}"'.format((edges["right"]-edges["left"]+2)*size)
    h = ' height="{}"'.format((edges["bottom"]-edges["top"]+2)*size)
    return '<svg xmlns="http://www.w3.org/2000/svg"' + w + h + '>'

def _svg_end():
    return "</svg>"

def _empty_rect(rect_x, rect_y, width=100, height=100):
    tag = "<rect></rect>"
    x = ' x="{}"'.format(rect_x)
    y = ' y="{}"'.format(rect_y)
    w = ' width="{}"'.format(width)
    h = ' height="{}"'.format(height)
    color = ' fill="white"'
    border = ' stroke-width="{}" stroke="black"'.format(width/25)

    return tag[:5] + x + y + w + h + color + border + tag[5:]

def _numbered_rect(rect_x, rect_y, text, width=100, height=100):
    group = "<g></g>"
    rect = _empty_rect(rect_x, rect_y, width, height)
    text_tag = "<text></text>"
    text_x = ' x="{}"'.format(rect_x + width*0.05)
    text_y = ' y="{}"'.format(rect_y + width*0.2)
    text_style = ' font-family="Times New Roman" fill="black" font-size="{}"'.format(width*0.2)

    return group[:3] + rect + text_tag[:5] + text_x + text_y + text_style + text_tag[5] + str(text) + text_tag[6:] + group[3:]

def _create_crossword_svg(field, edges, word_placements, size, starting_x=10, starting_y=10):
    path_to_file=os.path.realpath(__file__)[:-6] + "crossword.svg"
    print("che cazzo è",path_to_file)
    with open(path_to_file, "w+") as file:
        print("Creating crossword.svg..")
        new_line = "\n"
        current_x, current_y = starting_x, starting_y
        file.write(_svg_header(edges,size))
        file.write(new_line)
        for i in range(edges["top"], edges["bottom"]+1):
            for j in range(edges["left"], edges["right"]+1):
                if field[i][j] != '':
                    if (i,j) in word_placements:
                        print("hello")
                        file.write(_numbered_rect(current_x, current_y, word_placements[(i,j)], size, size))
                    else:
                        file.write(_empty_rect(current_x, current_y, size, size))
                    file.write(new_line)
                current_x += size
            current_x = starting_x
            current_y += size
        file.write(_svg_end())

if __name__ == "__main__":
    field, edges, wordorder = c.create_crossword(c._get_words_file())
    c._print(field, edges=edges)
    #print(_empty_rect(10, 10))
    #print(_numbered_rect(10, 10, 1))
    _create_crossword_svg(field, edges, wordorder, 25)    