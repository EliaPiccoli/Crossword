from flask import Flask, redirect, url_for, render_template, request
from crossword import create_crossword, _print

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        while True:
            crossword_matrix_1, edges_1, word_placement_1 = create_crossword(request.form["words"])
            crossword_matrix_2, edges_2, _ = create_crossword(request.form["words"])
            if crossword_matrix_1 != -1 and crossword_matrix_2 != -1: #if is equal to -1 means crossword was not created succesfully
                break
            else:
                print("Trying generating crossword again..")
        return render_template("crossword_page.html", crossword_1 = crossword_matrix_1, crossword_2 = crossword_matrix_2, edges_1 = edges_1, edges_2 = edges_2, wordplacements_1 = word_placement_1)
    else:
        return render_template("main_page.html")

if __name__ == "__main__":
    app.run(debug=True)