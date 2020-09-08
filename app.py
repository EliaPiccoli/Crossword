from flask import Flask, redirect, url_for, render_template, request
from crossword import create_crossword, _print
from static.svg import _create_crossword_svg
from static.parser import _parse_text

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        while True:
            crossword_matrix, edges, word_placement = create_crossword(_parse_text(request.form["words"]))
            _create_crossword_svg(crossword_matrix, edges, word_placement, 50)
            if crossword_matrix != -1: #if is equal to -1 means crossword was not created succesfully
                break
            else:
                print("Trying generating crossword again..")
        return render_template("crossword_page.html", crossword = crossword_matrix, edges = edges, wordplacements = word_placement, svg_path = 'crossword.svg')
    else:
        return render_template("main_page.html")

if __name__ == "__main__":
    app.run(debug=True)