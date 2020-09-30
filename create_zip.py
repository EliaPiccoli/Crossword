from zipfile import ZipFile
from static.svg import _create_crossword_svg
from crossword import _create_definitions_file
import os



def _create_zip(words_with_def,placements,used, crossword_matrix, edges, word_placement):
    #create svg file
    _create_crossword_svg(crossword_matrix, edges, word_placement, 50)

    #create definitions file
    _create_definitions_file(words_with_def,placements,used,word_placement)

    # create a ZipFile object
    path_to_file = os.path.realpath(__file__)[:-13] + 'static\crossword.zip' #on whichever machine the path will end with Crossword\create_zip.py, cut final part to save file where needed
    zipObj = ZipFile(path_to_file, 'w')
    # Add multiple files to the zip
    zipObj.write('crossword.svg')
    zipObj.write('definitions.txt')
    # close the Zip File
    zipObj.close()