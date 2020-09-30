import re

pattern = r"([A-Z]+)\n((?:.+\n)+)"

# TODO special chars errors
# TODO è, ... <- brake everything LOL
def _parse_text(text):
    # clean input from enter key
    if type(text) is bytes:
        text = str(text)[2:-1]
        text = text.replace("\\r","\r")
        text = text.replace("\\n","\n")
    text = text.replace(chr(13), "")
    if text[-1] != "\n":
        text += "\n"
    #for c in text:
    #    print("{} : {}".format(ord(c), c))
    #print(type(text), text)
    words_def = {}
    match = re.findall(pattern, text)
    for element in match:
        print(element[0], element[1])
        words_def[element[0]] = element[1]
    
    return words_def

if __name__ == "__main__":
    text = """A
aaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaa

B
bbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbbb

C
ccccccccccccccccc
ccccccccccccccccc
ccccccccccccccccc
ccccccccccccccccc
ccccccccccccccccc
"""
    print(_parse_text(text))