import string
import numpy as np #my love

def _get_words():
	return [line.strip() for line in open("words.txt")]
    #return ["emergente", "ciao", "ramo", "sole", "luce"]

def _print_crossword(field, size):
	for i in range(size):
		for j in range(size):
			print(field[i][j] if field[i][j] != "" else "-", end="")
		print()

def _check_fit(field, row, col, pos, old_word, new_word, is_new_word_horizontal):
	print(f"Checking if {new_word} fits in current crossword..")
	if is_new_word_horizontal:
		for k in range(len(new_word)):
			if field[row][col+k-pos] not in ("", new_word[k]):
				return False
	else:
		for k in range(len(new_word)):
			if field[row+k-pos][col] not in ("", new_word[k]):
				return False
	return True

def _shift(field, offset, is_horizontal):
	#if offset negative then left shift, else right shift.
	return np.roll(field, offset, is_horizontal)


def _print_sets(used, remaining):
	print("used {}".format(used))
	print("remaining {}".format(remaining))

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

#initialize current crossword edges, useful for later shifting
top = 0
bottom = len(w[0]) - 1
left = 0
right = 0

#initialize two sets that will be updated and represents the status of the words
used = set(w[0:1])
remaining = set(w[1:])
_print_sets(used, remaining)

inserted_new_word = True

while len(remaining) > 0:
	if not inserted_new_word:
		print("Restart the script, crossword cannot be completed with current word structure")
		exit(1)

	#print current crossword
	_print_crossword(field, size)

	inserted_new_word = False

	for word in remaining:
		for c in word:
			for word_placed in used:
				if c in word_placed:
					#possible link
					print(f"Found a possible link between {word} and {word_placed} due to common character '{c}'")
					if placements[word_placed][2]: #vertical word
						col = placements[word_placed][1]
						row = word_placed.find(c)
						pos = word.find(c)

						#check if word fits in current crossword boundaries 
						if col-pos < 0 or col+(len(word)-pos) > size:
							print("We gotta shift brother")
							field = _shift(field, col-pos, 1) #1 = horizontal shift, 0 = vertical shift

						#check if fits in needed cells
						fit = _check_fit(field, row, col, pos, word_placed, word, placements[word_placed][2])

						if fit:
							for k in range(0, len(word)):
								field[row][col+k-pos] = word[k]
							placements[word] = (row, col-pos, False)

							#add placed word to correct set and remove from remaining
							used.add(word)
							remaining.remove(word)

							#pretty printing cause we fenoch
							print(f"Updated sets after inserting word {word}")
							_print_sets(used,remaining)

							inserted_new_word = True
							break
					else: #horizontal word
						row = placements[word_placed][0]
						col = word_placed.find(c)
						pos = word.find(c)

						#check if word fits in current crossword boundaries 
						if row-pos < 0 or row+(len(word)-pos) > size:
							print("We gotta shift brother")
							field = _shift(field, row-pos, 0) #1 = horizontal shift, 0 = vertical shift

						#check if fits in needed cells
						fit = _check_fit(field, row, col, pos, word_placed, word, placements[word_placed][2])

						if fit:
							for k in range(0, len(word)):
								field[row+k-pos][col] = word[k]
							placements[word] = (row-pos, col, True)

							#add placed word to correct set and remove from remaining
							used.add(word)
							remaining.remove(word)

							#pretty printing cause we fenoch
							print(f"Updated sets after inserting word {word}")
							_print_sets(used,remaining)

							inserted_new_word = True
							break


	else:
		print("Could not create a full crossword")
		exit(1)

# --------------------------------------------------------
# --------------------------------------------------------

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
						fit = _check_fit(field, row, col, pos, w[j], w[i], placements[w[j]][2])

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
