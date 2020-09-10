import string
import numpy as np #my love
import time

def _get_words_file():
	return "".join(line for line in open("words.txt"))

def _get_words(text):
	return [line.strip() for line in text.split("\n")]

def _print(field, empty = " ", edges=None):
	_print_crossword(field, len(field[0]), empty, edges)

def _update_edges(field, size, edges, shift=False, axis=False, offset=0):
	if shift:
		if axis: # horizontal-shift
			edges["right"] = edges["right"] + offset
			edges["left"] = edges["left"] + offset
		else: # vertical shift
			edges["top"] = edges["top"] + offset
			edges["bottom"] = edges["bottom"] + offset			
	else:	
		for i in range(size):
			for j in range(size):
				if field[i][j] != '':
					edges["top"] = edges["top"] if i >= edges["top"] else i
					edges["bottom"] = edges["bottom"] if i <= edges["bottom"] else i
					edges["right"] = edges["right"] if j <= edges["right"] else j
					edges["left"] = edges["left"] if j >= edges["left"] else j
	return edges

def _print_crossword(field, size, empty="-", edges=None):
	if edges:
		for i in range(edges["top"], edges["bottom"]+1):
			for j in range(edges["left"], edges["right"]+1):
				print("{}".format(field[i][j]) if field[i][j] != "" else "{}".format(empty), end="")
			print()				
	else:
		for i in range(size):
			for j in range(size):
				print("{}".format(field[i][j]) if field[i][j] != "" else "{}".format(empty), end="")
			print()

# BUG we accept same letter only if is the position of the match not others -> overlap
def _check_fit(field, row, col, pos, old_word, new_word, is_new_word_horizontal, size):

	#check if we are writing 2 words consecutevely
	if is_new_word_horizontal:
		if col-pos>0:
			if field[row][col-pos-1] != '':
				return False
		if col-pos+len(new_word)<size:
			if field[row][col-pos+len(new_word)] != '':
				return False
	elif (not is_new_word_horizontal):
		if row-pos>0:
			if field[row-pos-1][col] != '':
				return False
		if row-pos+len(new_word)<size:
			if field[row-pos+len(new_word)][col] != '':
				return False

	#check if cells needed are free or fille with compatible chars
	for k in range(len(new_word)):
		if is_new_word_horizontal:
			r,c = row, col+k-pos
		else:
			r,c = row+k-pos, col
		x = field[r][c]
		if x not in ('', new_word[k]):
			return False
		
		
		#check if words are being written side by side 
		if x == '': 
			if is_new_word_horizontal: #check previous row and next row (if within matrix borders) 
				if r-1 >= 0:
					#print(f"HORIZONTAL: inserting {new_word} --- especially letter '{new_word[k]}' ---  field[r-1] = {field[r-1][c]}")
					if field[r-1][c]!='':
						return False
				if r+1 < size:
					#print(f"HORIZONTAL: inserting {new_word} --- especially letter '{new_word[k]}' ---  field[r+1] = {field[r+1][c]}")
					if field[r+1][c]!='':
						return False
			else: #check previous column and next column (if within matrix borders) 
				if c-1 >= 0:
					#print(f"VERTICAL: inserting {new_word} --- especially letter '{new_word[k]}' ---  field[c-1] = {field[r][c-1]}")
					if field[r][c-1]!='':
						return False
				if c+1 < size:
					#print(f"VERTICAL: inserting {new_word} --- especially letter '{new_word[k]}' ---  field[c+1] = {field[r][c+1]}")
					if field[r][c+1]!='':
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

def _create_definitions_file(words_with_def,placements,used,word_order):
	v = [x for x in used if placements[x][2]]                               #create list of used vertical words
	h = list(set(words_with_def.keys())-set(v))                             #create list of used horizontal words
	v.sort(key=lambda x : word_order[(placements[x][0], placements[x][1])]) #ordering words on word_order values
	h.sort(key=lambda x : word_order[(placements[x][0], placements[x][1])]) #same as above

	with open("definitions.txt", "w") as f:
		f.write("-"*50+"VERTICAL"+"-"*50+"\n")
		for word in v: f.write("{}.\n{}\n".format(word_order[(placements[word][0], placements[word][1])], words_with_def[word]))
		f.write("-"*50+"HORIZONTAL"+"-"*50+"\n")
		for word in h: f.write("{}.\n{}\n".format(word_order[(placements[word][0], placements[word][1])], words_with_def[word]))

def create_crossword(words_with_def):
	start = time.time()

	#dictionary with all the words
	w = [word for word in words_with_def.keys()]

	w.sort(reverse=True, key=len)
	print(w)

	size = 10*len(w[0])
	field = [["" for _ in range(size)] for _ in range(size)]

	# dictionary with the info of the words placement
	# (row, col, vertical(True)-horizontal(False))
	placements = {}
	# dictionary with edges index
	edges = {}
	# dictionary with info about the word
	stats = {word:0 for word in w}
	# dictionary for word order
	word_order = {}

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
		#_print_sets(used, remaining)

		inserted_new_word = False
		
		# TODO - EP - see main not true we get the same crossword
		#recreate set to obtain different crosswords on different executions
		remaining=list(remaining)
		np.random.shuffle(remaining)
		remaining=set(remaining)

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
								shift = pos-col
								field = _shift(field, shift, 1)
								_update_placements(placements, shift, True)
								_update_edges(field, size, edges, True, True, shift)
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
								shift = pos-row
								field = _shift(field, shift, 0)
								_update_placements(placements, shift, False)
								_update_edges(field, size, edges, True, False, shift)
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
					edges = _update_edges(field, size, edges)
					break
			if inserted_new_word:
					break
		else:
			print("Could not create a full crossword")
			print("These words could not be introduced: ", remaining)
			field = -1
			break

	#print("FINAL CROSSWORD")
	#_print_crossword(field, size, " ")
	if field != -1:
		i = 1
		for word in used:
			if (placements[word][0], placements[word][1]) in word_order:
				pass
			else:
				word_order[(placements[word][0], placements[word][1])], i = i, i+1

		_create_definitions_file(words_with_def,placements,used,word_order)

	print("Execution time: {:.3f}".format(time.time() - start))
	#return field, edges["bottom"]+1, edges["left"]+1
	return field, edges, word_order

# TODO
# 1. shift field then check for word, if it doesnt fit it wont unshift the field
# 2. numpy.roll() if the crossword extends too much vertically or horizontally warps -> bigger field/check (?)

if __name__ == "__main__":
	f,e,o = create_crossword(_get_words_file())
	_print(f)
	print(e, o)
	#f1 = create_crossword(_get_words_file())
	#print("-----------------------------------------------------------")
	#f2 = create_crossword(_get_words_file())
	#_print(f1)
	#_print(f2)