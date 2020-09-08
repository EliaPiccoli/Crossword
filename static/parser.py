import re

pattern = r"([A-Z]+)\n((?:.+\n)+)"

def _parse_text(text):
    # clean input from enter key
    text = text.replace(chr(13), "")        
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