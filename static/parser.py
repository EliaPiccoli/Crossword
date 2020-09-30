def _parse_text(text):
    if text[-1] != "\n":
        text += "\n"
    wd = text.split("\n")
    definition_rows = []
    words_def = {}
    word = definition = ""
    for line in wd:
        if line == '':
            #print("DEF")
            #print("\n".join(definition))
            if len(definition_rows) == 0:
                continue
            else:
                definition = "\n".join(definition_rows) + "\n"
                print(word, definition)
                words_def[word] = definition
                definition_rows = []
        elif all(str.isupper(c) or c==" " for c in line):
            #print("WORD: ", line)
            word = line.replace(" ", "")
        else:
            definition_rows.append(line)

    print(words_def)
    print("---------------------")

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