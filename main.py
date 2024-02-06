import datetime
from classes.search import Query, Searchbar
from classes.holiday import Holiday
import flask
from flask import redirect, render_template, request, session

app = flask.Flask(__name__)
app.secret_key = "secretkey"

offers = {}
searchbar = Searchbar()

@app.route('/', methods=['GET', 'POST']) # Index
def index():
    if request.method == "GET":
        session["query"] = None
        session["results"] = None
        return render_template('search.html')
    else:
        # Logic for calling query function
        query = Query("05062024", 7, "LGW", "GRZA") #test data
        res = query.query()
        offers[str(query)] = res
        # session["results"] = [h.to_json() for h in res]
        return redirect(f"/results/{str(query)}")

@app.route('/results/<queryid>')
def results(queryid: str):
    try:
        res = offers[queryid]
    except:
        return redirect("/")
    # delete results from storage after access
    del offers[queryid]
    return render_template("results.html", results = res)

@app.route('/searchbar/<query>')
def searchbar(query: str):
    searchbar.

app.run("0.0.0.0")