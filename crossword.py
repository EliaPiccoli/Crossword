import string
import numpy as np #my love
import time

def _get_words_file():
	return "".join(line for line in open("words.txt"))

def _get_words(text):
	return [line.strip() for line in text.split("\n")]

def _print(field):
	_print_crossword(field, len(field[0]), " ")

def _print_crossword(field, size, empty="-"):
	for i in range(size):
		for j in range(size):
			print(" {} ".format(field[i][j]) if field[i][j] != "" else " {} ".format(empty), end="")
		print()

# BUG we accept same letter only if is the position of the match not others -> overlap
def _check_fit(field, row, col, pos, old_word, new_word, is_new_word_horizontal, size):
	#print(f"Checking if {new_word} fits in current crossword..")
	#print(is_new_word_horizontal)

	#check if we are writing 2 words consecutevely
	if is_new_word_horizontal and col-pos> 0:
		if field[row][col-pos-1] != '':
			return False
	elif (not is_new_word_horizontal) and row-pos>0:
		if field[row-pos-1][col] != '':
			return False

	for k in range(len(new_word)):
		if is_new_word_horizontal:
			r,c = row, col+k-pos
		else:
			r,c = row+k-pos, col
		x = field[r][c]
		#print(x if x != "" else "-", r, c)
		if x not in ('', new_word[k]):
			return False

		#enormous and horrible check for avoiding 2 vertical/horizontal words side by side
		if x == '' and ((is_new_word_horizontal and ((r-1>0 and field[r-1][c]!='') or (r+1<size and field[r+1][c]!=''))) or ((not is_new_word_horizontal) and ((c-1>0 and field[r][c-1]!='') or (c+1<size and field[r][c+1]!='')))):
			return False
	return True

# TODO: check roll() -> warp error
# is_horizontal -> 1 = horizontal shift, 0 = vertical shift
def _shift(field, offset, is_horizontal):
	#if offset negative then left shift, else right shift.
	return np.roll(field, offset, is_horizontal)

def _print_sets(used, remaining):
	print("used {}".format(used))
	print("remaining {}".format(remaining))

# is_horizontal -> 1 = horizontal shift, 0 = vertical shift
def _update_placements(placements, shift, is_horizontal):
	for element, value in placements.items():
		placements[element] = (value[0], value[1]+shift, value[2]) if is_horizontal else (value[0]+shift, value[1], value[2])

def _debug(field, size, placements, stats):
	#debug
	_print_crossword(field, size)
	print(placements)
	print(stats)
	x = input()

def create_crossword(text):
	start = time.time()

	#dictionary with all the words
	w = _get_words(text)
	w.sort(reverse=True, key=len)
	print(w)

	size = 4*len(w[0])
	field = [["" for _ in range(size)] for _ in range(size)]

	# dictionary with the info of the words placement
	# (row, col, vertical(True)-horizontal(False))
	placements = {}
	# dictionary with edges index
	edges = {}
	# dictionary with info about the word
	stats = {word:0 for word in w}

	#insert first word top-left corner
	for i in range(len(w[0])):
		field[i][0] = w[0][i]
	placements[w[0]] = (0, 0, True)

	#initialize current crossword edges, useful for later shifting
	# TODO: add edge control
	edges["top"] = 0
	edges["bottom"] = len(w[0]) - 1
	edges["left"] = 0
	edges["right"] = 0

	#initialize two sets that will be updated and represents the status of the words
	used = set(w[0:1])
	remaining = set(w[1:])
	#_print_sets(used, remaining)

	while len(remaining) > 0:
		print("words left: {}".format(len(remaining)))
		_print_sets(used, remaining)

		inserted_new_word = False
		
		# TODO - EP - see main not true we get the same crossword
		#recreate set to obtain different crosswords on different executions
		#i know it looks like shit, but it works!
		#remaining=list(remaining)
		#np.random.shuffle(remaining)
		#remaining=set(remaining)

		for word in remaining:
			#print(word)
			#create a list of the placed words sorted by the value of stats -> first we check words with no link to others
			words_placed = list(used)
			words_placed.sort(key=lambda x:stats[x])
			#print(words_placed)
			for word_placed in words_placed:
				for c in word:
					#print(c, word, word_placed)
					if c in word_placed:
						#possible link
						#print(f"Found a possible link between {word} and {word_placed} due to common character '{c}'")
						if placements[word_placed][2]: #vertical word
							row = word_placed.find(c) + placements[word_placed][0]
							col = placements[word_placed][1]
							pos = word.find(c)

							#print("row {} col {} pos {}".format(row, col, pos))

							#check if word fits in current crossword boundaries 
							if col-pos < 0 or col+(len(word)-pos) > size:
								#print("We gotta shift brother")
								field = _shift(field, pos-col, 1)
								_update_placements(placements, pos-col, True)
								col = pos

							#check if fits in needed cells
							fit = _check_fit(field, row, col, pos, word_placed, word, placements[word_placed][2], size)

							if fit:
								for k in range(0, len(word)):
									field[row][col+k-pos] = word[k]
								placements[word] = (row, col-pos, False)

								#add placed word to correct set and remove from remaining
								used.add(word)
								remaining.remove(word)

								#pretty printing cause we fenoch
								#print(f"Updated sets after inserting word {word}")
								#_print_sets(used,remaining)
								
								stats[word_placed] = stats[word_placed] + 1 
								inserted_new_word = True
								break
						else: #horizontal word
							row = placements[word_placed][0]
							col = word_placed.find(c) + placements[word_placed][1]
							pos = word.find(c)

							#print("row {} col {} pos {}".format(row, col, pos))

							#check if word fits in current crossword boundaries 
							if row-pos < 0 or row+(len(word)-pos) > size:
								#print("We gotta shift brother")
								field = _shift(field, pos-row, 0)
								_update_placements(placements, pos-row, False)
								row=pos

							#check if fits in needed cells
							fit = _check_fit(field, row, col, pos, word_placed, word, placements[word_placed][2], size)

							if fit:
								for k in range(0, len(word)):
									field[row+k-pos][col] = word[k]
								placements[word] = (row-pos, col, True)

								#add placed word to correct set and remove from remaining
								used.add(word)
								remaining.remove(word)

								#pretty printing cause we fenoch
								#print(f"Updated sets after inserting word {word}")
								#_print_sets(used,remaining)

								stats[word_placed] = stats[word_placed] + 1
								inserted_new_word = True
								break
				# TODO: change this trash
				if inserted_new_word:
					break
			if inserted_new_word:
					break
		else:
			print("Could not create a full crossword")
			print("These words could not be introduced: ", remaining)
			exit(1)

	#print("FINAL CROSSOWORD")
	#_print_crossword(field, size, " ")

	print("Execution time: {:.3f}".format(time.time() - start))
	return field

# TODO
# 1. shift field then check for word, if it doesnt fit it wont unshift the field
# 2. numpy.roll() if the crossword extends too much vertically or horizontally warps -> bigger field/check (?)

if __name__ == "__main__":
	f1 = create_crossword(_get_words_file())
	print("-----------------------------------------------------------")
	f2 = create_crossword(_get_words_file())
	_print(f1)
	_print(f2)