from flask import Flask, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
from crossword import create_crossword, _print
from static.svg import _create_crossword_svg
from static.parser import _parse_text

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("main_page.html")

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            while True:
                crossword_matrix, edges, word_placement = create_crossword(_parse_text(image.read()))
                if crossword_matrix != -1: #if is equal to -1 means crossword was not created succesfully
                    _create_crossword_svg(crossword_matrix, edges, word_placement, 50)
                    break
                else:
                    render_template("error.html")
            return render_template("crossword_page.html", crossword = crossword_matrix, edges = edges, wordplacements = word_placement, svg_path = 'crossword.svg')

@app.route("/upload-text", methods=["GET", "POST"])
def upload_text():
    if request.method == "POST":
        while True:
            crossword_matrix, edges, word_placement = create_crossword(_parse_text(request.form["words"]))
            if crossword_matrix != -1: #if is equal to -1 means crossword was not created succesfully
                _create_crossword_svg(crossword_matrix, edges, word_placement, 50)
                break
            else:
                render_template("error.html")
        return render_template("crossword_page.html", crossword = crossword_matrix, edges = edges, wordplacements = word_placement, svg_path = 'crossword.svg')

if __name__ == "__main__":
    app.run(debug=True)