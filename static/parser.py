import re

pattern = r"([A-Z]+)\n((?:.+\n)+)"

def _parse_text(text):
    words_def = {}
    match = re.findall(pattern, text)
    for element in match:
        words_def[element[0].replace(" ", "")] = element[1]
    else:
        return None
    
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
    _parse_text(text)