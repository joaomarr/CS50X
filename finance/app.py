import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_stocks = db.execute("SELECT name, symbol, SUM(shares) as totalShares FROM transactions WHERE user_id=? AND type='buy' GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    stocks = []
    total = 0

    for user_stock in user_stocks:
        stock = lookup(user_stock["symbol"])
        sum_value = stock["price"] * user_stock["totalShares"]
        stocks.append({"symbol": stock["symbol"], "name": stock["name"], "shares": user_stock["totalShares"], "price": stock["price"], "total": sum_value})
        total += stock["price"] * user_stock["totalShares"]

    user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    total += user_cash

    return render_template("index.html", stocks=stocks, usd_function=usd, total=total, user_cash=user_cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        item = lookup(symbol)
        try:
            quantity_shares = int(request.form.get("shares"))
        except:
            return apology("Shares must be numbers")

        if not symbol:
            return apology("must provide a symbol!", 400)
        elif not quantity_shares:
            return apology("must provide quantity of shares!", 400)
        elif not item:
            return apology("invalid symbol!", 400)
        elif quantity_shares < 0:
            return apology("invalid quantity of shares!", 400)

        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
        cost = quantity_shares * item["price"]
        updt_cash = cash - cost

        if cash < cost:
            return apology("sorry, you do not have enough cash", 400)
        else:
            db.execute("UPDATE users SET cash=? WHERE id=?", updt_cash, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                session["user_id"], item["name"], quantity_shares, item["price"], 'buy', item["symbol"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, time FROM transactions WHERE user_id=?", session["user_id"])
    return render_template("history.html", transactions=transactions, usd_function=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide a symbol", 400)

        stock = lookup(symbol)

        if stock == None:
            return apology("invalid sybol!", 400)

        return render_template("quoted.html", stock=stock, usd_function=usd)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not name:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must repeat your password", 400)
        elif password != confirmation:
            return apology("repeat your password correctly", 400)

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, hash)
        except:
            return apology("username is already registered", 400)

        session["user_id"] = db.execute("SELECT id FROM users WHERE username=?", name)[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stocks = db.execute("SELECT shares, symbol FROM transactions WHERE user_id=? AND type='buy' GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        item = lookup(symbol)

        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        elif shares <= 0:
            return apology("must provide a valid number of shares", 400)

        for stock in stocks:
            if stock["symbol"] == symbol:
                if shares > stock["shares"]:
                    return apology("you don't have this shares", 400)

        transaction = shares * item["price"]
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

        updt_cash = transaction + cash
        db.execute("UPDATE users SET cash=? WHERE id=?", updt_cash, session["user_id"]);
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"], item["name"], -shares, item["price"], "sell", item["symbol"])

        return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)
