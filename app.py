from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method =="POST":
        #TODO call script in crossword.py for crossword generation
        print(request.form["words"])
        return "ciao belin" #render_template("crossword.html")
    else:
        return render_template("main_page.html")

if __name__ == "__main__":
    app.run(debug=True)