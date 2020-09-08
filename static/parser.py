import re

pattern = r"([A-Z]+)\n((?:.+\n)+)"

def _parse_text(text):
    words_def = {}

    text = """HELLO
ciao
come stai

HELLOKEKW
ciao
come stai
"""

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