from flask import Flask, redirect, url_for, render_template, request
from crossword import create_crossword

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        #TODO call script in crossword.py for crossword generation
        crossword_matrix_1 = create_crossword(request.form["words"])
        crossword_matrix_2 = create_crossword(request.form["words"])
        return render_template("crossword_page.html", crossword_1 = crossword_matrix_1, crossword_2 = crossword_matrix_2)
    else:
        return render_template("main_page.html")

if __name__ == "__main__":
    app.run(debug=True)