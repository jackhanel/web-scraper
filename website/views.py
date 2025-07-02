from flask import Blueprint, render_template, request
from .functions import scrapeURL
import html

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        soup = scrapeURL(url)
        if soup:
            result = html.escape(soup.prettify())
    return render_template("scrape.html", result=result)
