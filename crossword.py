import string

def _get_words():
	#return [line.strip() for line in open("words.txt")]
    return ["emergente", "ciao", "ramo", "sole", "luce"]

def _print_crossword(field, size):
	for i in range(size):
		for j in range(size):
			print(field[i][j] if field[i][j] != "" else "-", end="")
		print()

#dictionary with all the words
w = _get_words()
w.sort(reverse=True, key=len)
print(w)

size = 2*len(w[0])
field = [["" for _ in range(size)] for _ in range(size)]

#list with the info of the words placement
# (row, col, vertical(True)-horizontal(False))
placements = {}

#insert first word top-left corner
for i in range(len(w[0])):
	field[i][0] = w[0][i]
placements[w[0]] = (0, 0, True)

#try to add all the words
stats = {}
stats[w[0]] = 0
for i in range(1, len(w)): #new words
	add_word = False
	for j in range(i): #words already placed
		for c in w[i]:
			if c in w[j]:
				#possible link
				print(w[j], w[i], c)

				if placements[w[j]][2]: #vertical word
					col = placements[w[j]][1]
					row = w[j].find(c)
					pos = w[i].find(c)
					print(col, row, pos)

					#check word fit
					if col-pos < 0:
							#word out of field need to shift all
							print("shift")
							#exit(1)
					else:
						fit = all(field[row][col+k-pos] == "" for k in range(len(w[i])) if k != pos)
					
					if fit:
						for k in range(1, len(w[i])):
							field[row][col+k-pos] = w[i][k]
						placements[w[i]] = (row, col-pos, False)
						add_word = True
					break
				else: #horizontal word
					print("Horizontal")
					exit(1)
		_print_crossword(field, size)
		if add_word:
			break
