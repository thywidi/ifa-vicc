from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def home():
    user = {"bla": "Thierry", "age": 42, "home": "Bordeaux"}
    parkingSpots = {"1": "Free", "2": "Free", "3": "Free", "4": "Free"}
    income = 340
    return render_template(
        "pages/index.html",
        title="Home",
        user=user,
        income=income,
        parkingSpots=parkingSpots,
    )


@app.route("/login")
def login():
    return render_template(
        "pages/login.html",
        title="Login",
    )


@app.route("/api")
def typo3():
    posts = {"brand": "Ford", "model": "Mustang", "year": 1964}
    return posts


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
